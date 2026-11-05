"""Bounded offline semantic checks; no standards conformance or database proof."""
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / 'examples/logistics'


def instant(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('timezone required')
    return result.astimezone(timezone.utc)


def evaluate_logistics(data):
    """Reference calculation for the deliberately bounded fixture projection."""
    as_of, known = instant(data['as_of']), instant(data['known_as_of'])
    rejected, groups = set(), {}
    for event in data['events']:
        key = event['source_system'] + ':' + event['event_id']
        try:
            if instant(event['observed_at']) > known or instant(event['issued_at']) > known:
                continue
        except (ValueError, TypeError):
            rejected.add(key)
            continue
        groups.setdefault(key, []).append(event)
    accepted, duplicates = [], 0
    for key, receipts in groups.items():
        payloads = {json.dumps({k: v for k, v in row.items() if k != 'observed_at'}, sort_keys=True)
                    for row in receipts}
        if len(payloads) != 1:
            rejected.add(key)
            continue
        event = min(receipts, key=lambda row: instant(row['observed_at']))
        duplicates += len(receipts) - 1
        try:
            effective = instant(event['event_time'])
            if event['classifier'] not in ('planned', 'estimated', 'actual'):
                raise ValueError('unsupported classifier')
            if event['classifier'] == 'actual' and effective > as_of:
                raise ValueError('future actual')
        except (ValueError, TypeError):
            rejected.add(key)
            continue
        if event['valid'] and event['shipment_id'] == data['shipment_id']:
            accepted.append(event)
    actual = [e for e in accepted if e['classifier'] == 'actual']
    latest = max((instant(e['event_time']) for e in actual), default=None)
    delivered = sorted({e['unit_id'] for e in actual
                        if e['location_id'] == data['delivery_location_id']
                        and e['milestone'] == data['delivery_milestone']
                        and e['unit_id'] in data['required_unit_ids']})
    complete = bool(data['required_unit_ids']) and set(delivered) == set(data['required_unit_ids'])
    estimates = [e for e in accepted if e['classifier'] == 'estimated'
                 and e['location_id'] == data['delivery_location_id']
                 and e['milestone'] == data['delivery_milestone']]
    selected, eta, delay, status = None, None, None, 'insufficient_evidence'
    if estimates:
        issued = max(instant(e['issued_at']) for e in estimates)
        estimates = [e for e in estimates if instant(e['issued_at']) == issued]
        rank = {source: index for index, source in enumerate(data['source_priority'])}
        priority = min(rank[e['source_system']] for e in estimates)
        estimates = [e for e in estimates if rank[e['source_system']] == priority]
        times = {instant(e['event_time']) for e in estimates}
        if len(times) > 1:
            status = 'ambiguous_eta'
        else:
            # Equivalent-time evidence is tied deterministically only for presentation.
            selected = min(estimates, key=lambda e: e['event_id'])['event_id']
            value = times.pop()
            eta = value.isoformat().replace('+00:00', 'Z')
            delay = (value - instant(data['planned_arrival'])).total_seconds() / 60
            status = 'eta_delay' if delay > data['delay_threshold_minutes'] else 'on_schedule'
    if complete:
        status = 'delivered'
    return dict(status=status, selected_eta_event_id=selected, latest_eta=eta,
                delay_minutes=delay, delivery_confirmed=complete, delivered_unit_ids=delivered,
                latest_actual_event_ids=sorted(e['event_id'] for e in actual
                                               if instant(e['event_time']) == latest),
                actual_event_count=len(actual), duplicate_receipts=duplicates,
                rejected_event_keys=sorted(rejected))


class LogisticsExamplesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.acceptance = json.loads((EXAMPLES / 'acceptance.json').read_text())
        cls.input = json.loads((EXAMPLES / 'input.json').read_text())

    def test_hand_calculated_cases(self):
        for case in self.acceptance['cases']:
            with self.subTest(case=case['id']):
                self.assertEqual(evaluate_logistics(case['input']), case['expected'])

    def test_realistic_input_matches_case(self):
        self.assertEqual(evaluate_logistics(self.input), self.acceptance['cases'][0]['expected'])

    def test_message_order_and_record_time_do_not_change_effective_evidence(self):
        data = copy.deepcopy(self.input)
        data['events'].reverse()
        for event in data['events']:
            event['record_time'] = '2026-11-05T11:59:00Z'
        self.assertEqual(evaluate_logistics(data), evaluate_logistics(self.input))

    def test_transshipment_arrival_cannot_complete_destination_delivery(self):
        data = copy.deepcopy(self.input)
        # Even an actual SG arrival for one unit cannot complete a two-unit NL delivery.
        event = copy.deepcopy(data['events'][-1])
        event.update(event_id='sg-arrival', milestone='arrival')
        data['events'].append(event)
        output = evaluate_logistics(data)
        self.assertFalse(output['delivery_confirmed'])
        self.assertEqual(output['delivered_unit_ids'], [])

    def test_reclassifying_actual_as_plan_removes_delivery(self):
        case = next(c for c in self.acceptance['cases'] if c['id'] == 'log-complete-delivery')
        data = copy.deepcopy(case['input'])
        data['events'][1]['classifier'] = 'planned'
        result = evaluate_logistics(data)
        self.assertFalse(result['delivery_confirmed'])
        self.assertEqual(result['delivered_unit_ids'], ['LU-1'])

    def test_strict_delay_threshold(self):
        data = copy.deepcopy(self.input)
        data['delay_threshold_minutes'] = 180
        self.assertEqual(evaluate_logistics(data)['status'], 'on_schedule')


if __name__ == '__main__':
    unittest.main()
