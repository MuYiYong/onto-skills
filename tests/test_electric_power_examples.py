"""Bounded offline candidate semantics; not electrical simulation or IEC compliance."""
import copy
import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / 'examples/electric-power'
KEYS = ('version_id', 'state_id', 'outage_id', 'segment_id', 'equipment_id',
        'terminal_id', 'service_point_id', 'lot_id', 'event_id')


def materialize(case_input):
    data = json.loads((EXAMPLES / case_input['fixture']).read_text())
    data['query'].update(copy.deepcopy(case_input.get('query', {})))
    for patch in case_input.get('patches', []):
        parts = patch['path'].split('/')
        target = data
        for part in parts[:-1]:
            if isinstance(target, list):
                if part.isdecimal():
                    target = target[int(part)]
                else:
                    matches = [row for row in target if part in [row.get(k) for k in KEYS]]
                    if len(matches) != 1:
                        raise ValueError('patch selector must match one record')
                    target = matches[0]
            else:
                target = target[part]
        target[parts[-1]] = copy.deepcopy(patch['value'])
    for field, records in case_input.get('append', {}).items():
        data[field].extend(copy.deepcopy(records))
    return data


def instant(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def active(row, event_time, cutoff):
    return (instant(row['valid_from']) <= event_time
            and (row['valid_to'] is None or event_time < instant(row['valid_to']))
            and instant(row['observed_at']) <= cutoff)


def reachable(starts, adjacency):
    seen, pending = set(starts), list(starts)
    while pending:
        for neighbor in adjacency.get(pending.pop(), ()):
            if neighbor not in seen:
                seen.add(neighbor)
                pending.append(neighbor)
    return seen


def restoration(data):
    query = data['query']
    when, cutoff = instant(query['event_as_of']), instant(query['knowledge_cutoff'])
    intervals, open_points, count = {}, set(), 0
    for segment in data['restoration_segments']:
        if (segment['outage_id'] != query['outage_id']
                or segment['event_kind'] != 'actual'
                or instant(segment['observed_at']) > cutoff
                or instant(segment['interrupted_from']) > when):
            continue
        service = segment['service_point_id']
        if segment['restored_at'] is None:
            open_points.add(service)
            continue
        end = instant(segment['restored_at'])
        if end > when:
            continue
        start = instant(segment['interrupted_from'])
        if end <= start:
            return {'status': 'rejected', 'reason': 'invalid_restoration_interval'}
        count += 1
        intervals.setdefault(service, []).append((start, end))
    totals = {}
    for service, rows in intervals.items():
        merged = []
        for start, end in sorted(rows):
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
            else:
                merged.append((start, end))
        seconds = sum(int((end - start).total_seconds()) for start, end in merged)
        totals[service] = format(Decimal(seconds) / Decimal(60), 'f')
    return {'status': 'ok', 'minutes_by_service_point': totals,
            'closed_segment_count': count, 'open_service_points': sorted(open_points)}


def evaluate(data):
    """Two reachability bounds on a declared aggregate, two-terminal topology."""
    query = data['query']
    if query['operation'] == 'restoration':
        return restoration(data)
    when, cutoff = instant(query['event_as_of']), instant(query['knowledge_cutoff'])
    versions = [row for row in data['topology_versions'] if active(row, when, cutoff)]
    if len(versions) != 1:
        return {'status': 'rejected', 'reason': 'no_unique_known_topology'}
    version = versions[0]['version_id']
    outages = [row for row in data['outages'] if row['outage_id'] == query['outage_id']
               and instant(row['event_time']) <= when
               and instant(row['observed_at']) <= cutoff
               and (row['end_time'] is None or when < instant(row['end_time']))]
    if not outages:
        return {'status': 'not_known', 'outage_id': query['outage_id']}
    if len(outages) != 1:
        return {'status': 'rejected', 'reason': 'conflicting_outage'}
    outage = outages[0]
    terminals = {}
    for row in data['terminals']:
        if row['version_id'] == version and active(row, when, cutoff):
            if row['terminal_id'] in terminals:
                return {'status': 'rejected', 'reason': 'conflicting_terminal'}
            terminals[row['terminal_id']] = row['connectivity_id']
    states = {}
    for row in data['states']:
        if row['version_id'] == version and active(row, when, cutoff):
            equipment = row['equipment_id']
            if equipment in states:
                return {'status': 'rejected', 'reason': 'conflicting_state'}
            states[equipment] = row['state']
    definite, possible, known_sources, possible_sources = {}, {}, set(), set()
    uncertain_assets = []
    for equipment in data['equipment']:
        eid, kind = equipment['equipment_id'], equipment['kind']
        if eid == outage['equipment_id']:
            continue
        if any(tid not in terminals for tid in equipment['terminal_ids']):
            return {'status': 'rejected', 'reason': 'incomplete_terminal_topology'}
        points = [terminals[tid] for tid in equipment['terminal_ids']]
        state = states.get(eid, 'unknown')
        if kind in ('source', 'DER'):
            if len(points) != 1:
                return {'status': 'rejected', 'reason': 'unsupported_terminal_count'}
            if state not in ('available', 'unavailable', 'unknown'):
                return {'status': 'rejected', 'reason': 'invalid_source_state'}
            if state == 'available':
                known_sources.add(points[0])
                possible_sources.add(points[0])
            elif state == 'unknown':
                possible_sources.add(points[0])
                reason = 'unknown_source' if eid in states else 'missing_state'
                uncertain_assets.append((eid + ':' + reason, set(points)))
            continue
        if kind not in ('line', 'switch') or len(points) != 2:
            return {'status': 'rejected', 'reason': 'unsupported_terminal_count'}
        left, right = points
        if kind == 'switch' and state not in ('closed', 'open', 'unknown'):
            return {'status': 'rejected', 'reason': 'invalid_switch_state'}
        if kind == 'line' or state == 'closed':
            definite.setdefault(left, set()).add(right)
            definite.setdefault(right, set()).add(left)
        if kind == 'line' or state != 'open':
            possible.setdefault(left, set()).add(right)
            possible.setdefault(right, set()).add(left)
        if kind == 'switch' and state == 'unknown':
            reason = 'unknown_switch' if eid in states else 'missing_state'
            uncertain_assets.append((eid + ':' + reason, set(points)))
    known = reachable(known_sources, definite)
    maybe = reachable(possible_sources, possible)
    disconnected, uncertain, unaffected, outside, customers, uncertain_nodes = [], [], [], [], set(), set()
    for row in data['service_points']:
        if row['version_id'] != version or not active(row, when, cutoff):
            continue
        sid, point = row['service_point_id'], row['connectivity_id']
        if row['circuit_id'] != query['circuit_id']:
            outside.append(sid)
        elif point in known:
            unaffected.append(sid)
        else:
            customers.add(row['customer_id'])
            if point in maybe:
                uncertain.append(sid)
                uncertain_nodes.add(point)
            else:
                disconnected.append(sid)
    reasons = []
    for reason, nodes in uncertain_assets:
        if reachable(nodes, possible) & uncertain_nodes:
            reasons.append(reason)
    return {'status': 'ok', 'mode': outage['event_kind'], 'topology_version': version,
            'actual_outage_count': int(outage['event_kind'] == 'actual'),
            'disconnected_candidates': sorted(disconnected),
            'uncertain_service_points': sorted(uncertain),
            'unaffected_service_points': sorted(unaffected),
            'outside_scope_service_points': sorted(outside),
            'customer_candidates': sorted(customers), 'uncertainty_reasons': sorted(reasons)}


class ElectricPowerExamples(unittest.TestCase):
    def test_acceptance_inputs_to_expected(self):
        cases = json.loads((EXAMPLES / 'acceptance.json').read_text())['cases']
        for case in cases:
            with self.subTest(case=case['id']):
                self.assertEqual(evaluate(materialize(case['input'])), case['expected'])

    def test_unknown_open_and_closed_have_different_bounds(self):
        base = materialize({'fixture': 'input.json'})
        unknown = evaluate(base)
        for row in base['states']:
            if row['equipment_id'] == 'DER-1':
                row['state'] = 'unavailable'
            if row['equipment_id'] == 'SW-TIE':
                row['state'] = 'open'
        self.assertEqual(evaluate(base)['disconnected_candidates'], ['SP2'])
        self.assertEqual(unknown['uncertain_service_points'], ['SP2'])
        next(row for row in base['states'] if row['equipment_id'] == 'SW-TIE')['state'] = 'closed'
        self.assertEqual(evaluate(base)['unaffected_service_points'], ['SP1', 'SP2'])

    def test_conflicting_state_and_incomplete_topology_reject(self):
        data = materialize({'fixture': 'input.json'})
        data['states'].append(copy.deepcopy(data['states'][1]))
        self.assertEqual(evaluate(data)['reason'], 'conflicting_state')
        data = materialize({'fixture': 'input.json'})
        data['terminals'] = [row for row in data['terminals'] if row['terminal_id'] != 'T-ST3']
        self.assertEqual(evaluate(data)['reason'], 'incomplete_terminal_topology')

    def test_shared_customer_counts_once_and_boundary_source_survives_scope(self):
        data = materialize({'fixture': 'input.json'})
        service = copy.deepcopy(data['service_points'][1])
        service['service_point_id'] = 'SP2-B'
        data['service_points'].append(service)
        self.assertEqual(evaluate(data)['customer_candidates'], ['CUS2'])
        self.assertEqual(evaluate(data)['uncertain_service_points'], ['SP2', 'SP2-B'])

    def test_open_restoration_is_not_closed_at_receipt_time(self):
        data = materialize({'fixture': 'input.json', 'query': {
            'operation': 'restoration', 'event_as_of': '2026-11-01T12:00:00Z',
            'knowledge_cutoff': '2026-11-01T12:00:00Z'}})
        data['restoration_segments'][1]['restored_at'] = None
        result = evaluate(data)
        self.assertEqual(result['minutes_by_service_point'], {'SP2': '20'})
        self.assertEqual(result['open_service_points'], ['SP2'])


if __name__ == '__main__':
    unittest.main()
