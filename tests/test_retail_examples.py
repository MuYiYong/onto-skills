"""Bounded offline stock-policy checks; not certification, audit or native DB proof."""
import copy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / 'examples/retail'
GRAIN = ('merchant_id', 'sku', 'location_id', 'lot_issuer', 'lot_id', 'unit')


def instant(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('timezone required')
    return result.astimezone(timezone.utc)


def decimal(value):
    result = Decimal(value)
    if not result.is_finite():
        raise ValueError('finite quantity required')
    return result


def amount(value):
    if value is None:
        return None
    return format(value, 'f').rstrip('0').rstrip('.') if '.' in format(value, 'f') else str(value)


def evaluate_retail(data):
    """Test-only reference calculation, using only the fixture's declared policy."""
    as_of, known = instant(data['as_of']), instant(data['known_as_of'])
    scope = data['stock_scope']

    def matches(row):
        return all(row.get(k) == scope[k] for k in GRAIN)

    anchors, balances = {}, {}
    for condition in ('sellable', 'damaged'):
        candidates = [s for s in data['snapshots'] if matches(s) and s['condition'] == condition
                      and instant(s['event_time']) <= as_of and instant(s['observed_at']) <= known]
        if not candidates:
            balances[condition] = None
            continue
        latest = max(instant(s['event_time']) for s in candidates)
        values = {decimal(s['quantity']) for s in candidates if instant(s['event_time']) == latest}
        if len(values) != 1 or min(values) < 0:
            balances[condition] = None
            continue
        anchors[condition], balances[condition] = latest, values.pop()
    groups, rejected, pre_anchor = {}, set(), set()
    for event in data['movements']:
        key = event['source_system'] + ':' + event['event_id']
        try:
            if instant(event['observed_at']) <= known and instant(event['event_time']) <= as_of:
                groups.setdefault(key, []).append(event)
        except (ValueError, TypeError):
            rejected.add(key)
    events, duplicates = [], 0
    for key, receipts in groups.items():
        payloads = {json.dumps({k: v for k, v in e.items() if k != 'observed_at'}, sort_keys=True)
                    for e in receipts}
        if len(payloads) != 1:
            rejected.add(key)
        else:
            events.append((key, receipts[0]))
            duplicates += len(receipts) - 1
    valid, reversed_keys = {}, set()

    def normalized(postings, inverse=False):
        return sorted(tuple(p[k] for k in GRAIN) + (p['condition'],
                      -decimal(p['quantity_delta']) if inverse else decimal(p['quantity_delta']))
                      for p in postings)

    for key, event in sorted(events, key=lambda pair: (instant(pair[1]['event_time']), pair[0])):
        try:
            postings = event['postings']
            if not postings or any(p['unit'] != scope['unit'] for p in postings):
                raise ValueError('no conversion supplied')
            deltas = [decimal(p['quantity_delta']) for p in postings]
            if any(p['condition'] not in ('sellable', 'damaged') for p in postings):
                raise ValueError('condition outside bounded example')
            if event['kind'] in ('receipt', 'return') and any(q <= 0 for q in deltas):
                raise ValueError('positive movement required')
            if event['kind'] in ('sale', 'disposal') and any(q >= 0 for q in deltas):
                raise ValueError('negative movement required')
            if event['kind'] == 'damage':
                if len({tuple(p[k] for k in GRAIN) for p in postings}) != 1 or sum(deltas) != 0:
                    raise ValueError('unbalanced damage transfer')
                if not any(p['condition'] == 'sellable' and q < 0 for p, q in zip(postings, deltas)):
                    raise ValueError('sellable decrement required')
                if any((p['condition'] == 'sellable' and q >= 0)
                       or (p['condition'] == 'damaged' and q <= 0) for p, q in zip(postings, deltas)):
                    raise ValueError('damage direction')
            if event['kind'] == 'reversal':
                original_key = event['reverses_event_key']
                original = valid.get(original_key)
                if original is None or original['kind'] == 'reversal' or original_key in reversed_keys:
                    raise ValueError('invalid or duplicate reversal')
                if normalized(postings) != normalized(original['postings'], inverse=True):
                    raise ValueError('full inverse required')
                reversed_keys.add(original_key)
            elif event['kind'] not in ('receipt', 'return', 'sale', 'disposal', 'damage'):
                raise ValueError('unsupported event')
            valid[key] = event
        except (ValueError, KeyError, TypeError, InvalidOperation):
            rejected.add(key)
            continue
        for posting, delta in zip(postings, deltas):
            if not matches(posting):
                continue
            condition = posting['condition']
            if condition not in anchors:
                continue
            if instant(event['event_time']) <= anchors[condition]:
                pre_anchor.add(key)
            else:
                balances[condition] += delta
    reserved, reservation_groups, ambiguous = Decimal(0), {}, False
    for row in data['reservations']:
        if (instant(row['observed_at']) <= known and instant(row['valid_from']) <= as_of
                and matches(row) and row['condition'] == 'sellable'):
            key = row['source_system'] + ':' + row['reservation_id']
            reservation_groups.setdefault(key, []).append(row)
    for rows in reservation_groups.values():
        revision = max(row['revision'] for row in rows)
        current = [row for row in rows if row['revision'] == revision]
        payloads = {json.dumps({k: v for k, v in row.items() if k != 'observed_at'}, sort_keys=True)
                    for row in current}
        if len(payloads) != 1:
            ambiguous = True
            continue
        row = current[0]
        if row['status'] == 'active' and (row['valid_to'] is None or as_of < instant(row['valid_to'])):
            quantity = decimal(row['quantity'])
            if quantity < 0:
                ambiguous = True
            else:
                reserved += quantity
    transit = sum((decimal(row['outstanding_quantity']) for row in data['in_transit']
                   if instant(row['observed_at']) <= known
                   and matches(row)), Decimal(0))
    policy = data['policy']
    available, signal, suggested = None, None, None
    if balances.get('sellable') is None:
        status = 'insufficient_snapshot'
    elif ambiguous:
        status = 'ambiguous_reservation'
    elif (not policy or policy['available_rule'] != 'sellable_on_hand_minus_active_reserved'
          or policy['unit'] != scope['unit']):
        status = 'policy_required'
    else:
        available = balances['sellable'] - reserved
        point, target = decimal(policy['reorder_point']), decimal(policy['target_available'])
        if not target >= point >= 0:
            raise ValueError('invalid policy thresholds')
        signal = available < point
        suggested = target - available if signal else Decimal(0)
        status = 'signal' if signal else 'no_signal'
    warnings = []
    if balances.get('sellable') is not None and balances['sellable'] < 0:
        warnings.append('negative_sellable_on_hand')
    if available is not None and available < 0:
        warnings.append('negative_available')
    return dict(status=status, on_hand_by_condition={k: amount(v) for k, v in balances.items()},
                reserved=amount(reserved), available=amount(available), in_transit=amount(transit),
                restock_signal=signal, suggested_quantity=amount(suggested), order_created=False,
                duplicate_receipts=duplicates, rejected_event_keys=sorted(rejected),
                pre_anchor_event_keys=sorted(pre_anchor), warnings=warnings)


class RetailExamplesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.acceptance = json.loads((EXAMPLES / 'acceptance.json').read_text())
        cls.input = json.loads((EXAMPLES / 'input.json').read_text())

    def test_hand_calculated_cases(self):
        for case in self.acceptance['cases']:
            with self.subTest(case=case['id']):
                self.assertEqual(evaluate_retail(case['input']), case['expected'])

    def test_realistic_input_matches_case(self):
        self.assertEqual(evaluate_retail(self.input), self.acceptance['cases'][0]['expected'])

    def test_order_amount_and_transit_cannot_change_on_hand(self):
        data = copy.deepcopy(self.input)
        data['commercial_lines'][0]['amount'] = '10000000.13'
        data['commercial_lines'][1]['quantity'] = '90000'
        data['in_transit'][0]['outstanding_quantity'] = '200000'
        output = evaluate_retail(data)
        self.assertEqual(output['available'], '11')
        self.assertEqual(output['suggested_quantity'], '19')
        self.assertEqual(output['in_transit'], '200000')

    def test_conflicting_identity_is_not_last_write_wins(self):
        data = copy.deepcopy(self.input)
        changed = copy.deepcopy(data['movements'][0])
        changed['postings'][0]['quantity_delta'] = '-9'
        data['movements'].append(changed)
        output = evaluate_retail(data)
        self.assertEqual(output['rejected_event_keys'], ['pos:sale-1'])
        self.assertEqual(output['on_hand_by_condition']['sellable'], '22')

    def test_partial_reversal_applies_no_postings(self):
        case = next(c for c in self.acceptance['cases'] if c['id'] == 'ret-reversal')
        data = copy.deepcopy(case['input'])
        data['movements'][1]['postings'][0]['quantity_delta'] = '6'
        output = evaluate_retail(data)
        self.assertEqual(output['on_hand_by_condition']['sellable'], '13')
        self.assertEqual(output['rejected_event_keys'], ['pos:reverse-1'])

    def test_future_reservation_state_does_not_release_current_reservation(self):
        data = copy.deepcopy(self.input)
        future = copy.deepcopy(data['reservations'][0])
        future.update(revision=2, status='released', valid_from='2026-11-05T13:00:00Z',
                      observed_at='2026-11-05T11:00:00Z')
        data['reservations'].append(future)
        self.assertEqual(evaluate_retail(data)['reserved'], '4')

    def test_conflicting_reservation_revision_suppresses_signal(self):
        data = copy.deepcopy(self.input)
        conflict = copy.deepcopy(data['reservations'][0])
        conflict['quantity'] = '6'
        data['reservations'].append(conflict)
        output = evaluate_retail(data)
        self.assertEqual(output['status'], 'ambiguous_reservation')
        self.assertIsNone(output['available'])
        self.assertIsNone(output['restock_signal'])

    def test_missing_snapshot_is_unknown_not_zero(self):
        data = copy.deepcopy(self.input)
        data['snapshots'] = [s for s in data['snapshots'] if s['condition'] != 'sellable']
        output = evaluate_retail(data)
        self.assertEqual(output['status'], 'insufficient_snapshot')
        self.assertIsNone(output['on_hand_by_condition']['sellable'])
        self.assertIsNone(output['available'])

    def test_decimal_precision_and_receipt_order(self):
        data = copy.deepcopy(self.input)
        data['movements'].reverse()
        data['movements'].append(dict(source_system='wms', event_id='fractional-receipt', kind='receipt',
                                     event_time='2026-11-05T11:45:00Z', observed_at='2026-11-05T11:46:00Z',
                                     postings=[dict(data['movements'][0]['postings'][0], condition='sellable',
                                                    quantity_delta='0.1')]))
        output = evaluate_retail(data)
        self.assertEqual(output['available'], '11.1')
        self.assertEqual(output['suggested_quantity'], '18.9')


if __name__ == '__main__':
    unittest.main()
