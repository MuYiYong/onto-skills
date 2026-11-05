"""Bounded offline genealogy arithmetic; not EPCIS/ISA-95 or factory compliance."""
import copy
import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / 'examples/manufacturing'
KEYS = ('event_id', 'lot_id', 'inspection_id', 'specification_id')


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


def lot_key(row):
    return '|'.join(row[key] for key in ('source_system', 'site_id', 'lot_id'))


def canonical(value):
    return format(value.normalize(), 'f')


def descendants(starts, adjacency):
    seen, pending = set(starts), list(starts)
    while pending:
        for neighbor in adjacency.get(pending.pop(), ()):
            if neighbor not in seen:
                seen.add(neighbor)
                pending.append(neighbor)
    return seen - set(starts)


def inspection_results(data, when, cutoff):
    results = {}
    for row in data['inspections']:
        if instant(row['event_time']) > when or instant(row['observed_at']) > cutoff:
            continue
        specs = [s for s in data['quality_specifications']
                 if s['specification_id'] == row['specification_id']
                 and s['version'] == row['specification_version']
                 and s['metric'] == row['metric'] and s['unit'] == row['unit']
                 and instant(s['valid_from']) <= instant(row['event_time'])
                 and (s['valid_to'] is None or instant(row['event_time']) < instant(s['valid_to']))]
        result = 'unknown'
        if len(specs) == 1 and specs[0]['operator'] == '<=':
            result = 'pass' if Decimal(row['value']) <= Decimal(specs[0]['limit_value']) else 'fail'
        results[row['inspection_id']] = result
    return results


def evaluate(data):
    """Mass-conserving fixture events; never traverse resource-use as material flow."""
    query = data['query']
    when, cutoff = instant(query['event_as_of']), instant(query['knowledge_cutoff'])
    events = {}
    for event in data['events']:
        if instant(event['event_time']) > when or instant(event['observed_at']) > cutoff:
            continue
        key = (event['source_system'], event['event_id'])
        if key in events and events[key] != event:
            return {'status': 'rejected', 'reason': 'conflicting_event_id', 'event_id': event['event_id']}
        events[key] = event
    lots = {lot_key(row): row for row in data['lots']}
    if len(lots) != len(data['lots']):
        return {'status': 'rejected', 'reason': 'conflicting_lot_id'}
    adjacency, output_quantities, reconciliation, produced_by, equipment_outputs = {}, {}, {}, {}, {}
    consumed_quantities = {}
    incomplete = False
    conversions = {(row['from'], row['to']): Decimal(row['factor'])
                   for row in data['unit_conversions'] if row['dimension'] == 'mass'}
    for event in events.values():
        eid = event['event_id']
        if event['event_kind'] not in ('production', 'consumption', 'transformation', 'split', 'merge', 'rework'):
            return {'status': 'rejected', 'reason': 'invalid_event_kind', 'event_id': eid}
        sides = []
        for side in ('inputs', 'outputs'):
            total = Decimal(0)
            seen_participation = set()
            for participation in event[side]:
                key = lot_key(participation)
                if key in seen_participation:
                    return {'status': 'rejected', 'reason': 'duplicate_participation', 'event_id': eid}
                seen_participation.add(key)
                if key not in lots:
                    return {'status': 'rejected', 'reason': 'unknown_lot', 'event_id': eid}
                unit = participation['unit']
                factor = Decimal(1) if unit == 'kg' else conversions.get((unit, 'kg'))
                if factor is None or factor <= 0:
                    return {'status': 'rejected', 'reason': 'unapproved_unit_conversion', 'event_id': eid, 'unit': unit}
                value = participation['quantity']
                if value is None:
                    total = None
                    amount = None
                    incomplete = True
                else:
                    try:
                        amount = Decimal(value) * factor
                        if not amount.is_finite() or amount < 0:
                            raise InvalidOperation
                    except (InvalidOperation, ValueError):
                        return {'status': 'rejected', 'reason': 'invalid_quantity', 'event_id': eid}
                    if total is not None:
                        total += amount
                if side == 'inputs':
                    previous = consumed_quantities.get(key, Decimal(0))
                    consumed_quantities[key] = None if amount is None or previous is None else previous + amount
                if side == 'outputs':
                    if key in {lot_key(row) for row in event['inputs']}:
                        return {'status': 'rejected', 'reason': 'genealogy_cycle'}
                    if key in produced_by and produced_by[key] != (event['source_system'], eid):
                        return {'status': 'rejected', 'reason': 'reused_output_lot', 'lot': key}
                    produced_by[key] = (event['source_system'], eid)
                    output_quantities[key] = amount
                    equipment_outputs.setdefault(event['equipment_id'], set()).add(key)
            sides.append(total)
        if event['loss_unit'] != 'kg':
            return {'status': 'rejected', 'reason': 'unapproved_unit_conversion', 'event_id': eid, 'unit': event['loss_unit']}
        loss = Decimal(event['declared_loss'])
        if not loss.is_finite() or loss < 0:
            return {'status': 'rejected', 'reason': 'invalid_quantity', 'event_id': eid}
        if event['conservation_basis'] == 'mass':
            if None in sides:
                reconciliation[eid] = 'incomplete'
            elif sides[0] != sides[1] + loss:
                return {'status': 'rejected', 'reason': 'mass_imbalance', 'event_id': eid,
                        'input': canonical(sides[0]), 'output_plus_loss': canonical(sides[1] + loss), 'unit': 'kg'}
            else:
                reconciliation[eid] = 'balanced'
        else:
            reconciliation[eid] = 'not_applicable'
        for before in event['inputs']:
            for after in event['outputs']:
                adjacency.setdefault(lot_key(before), set()).add(lot_key(after))
    # Known supply cannot be allocated twice; missing producer observations are not invented.
    for key, consumed in consumed_quantities.items():
        opening = Decimal(lots[key]['opening_quantity'])
        produced = output_quantities.get(key)
        if consumed is not None and (opening > 0 or key in output_quantities):
            if produced is not None or key not in output_quantities:
                available = opening + (produced or Decimal(0))
                if consumed > available:
                    return {'status': 'rejected', 'reason': 'overallocated_input_lot', 'lot': key,
                            'available': canonical(available), 'consumed': canonical(consumed), 'unit': 'kg'}
    # New output identities prevent split/rework cycles, including a direct self-loop.

    for key in lots:
        if key in adjacency.get(key, set()) or any(key in adjacency.get(child, set())
                                                  for child in descendants([key], adjacency)):
            return {'status': 'rejected', 'reason': 'genealogy_cycle'}
    seed = lot_key(query['seed_lot'])
    if seed not in lots:
        return {'status': 'rejected', 'reason': 'unknown_seed_lot'}
    traced = descendants([seed], adjacency)
    terminals = {key for key in traced | {seed} if not adjacency.get(key)}
    candidates = sorted(key for key in terminals if lots[key]['status'] in query['candidate_statuses'])
    quantities = [output_quantities[key] if key in output_quantities
                  else Decimal(lots[key]['opening_quantity']) for key in candidates]
    total = None if None in quantities else sum(quantities, Decimal(0))
    # This contrast is diagnostic only; shared resources never create ancestry.
    used = {event['equipment_id'] for event in events.values()
            if any(lot_key(row) in traced | {seed} for row in event['inputs'])}
    unrelated_roots = {key for equipment in used for key in equipment_outputs.get(equipment, ())
                       if key not in traced}
    unrelated = unrelated_roots | descendants(unrelated_roots, adjacency)
    excluded = sorted(key for key in unrelated if not adjacency.get(key)
                      and lots[key]['status'] in query['candidate_statuses'])
    return {'status': 'incomplete' if incomplete else 'ok', 'candidate_lots': candidates,
            'candidate_quantity': {'value': None if total is None else canonical(total), 'unit': 'kg'},
            'intermediate_lots': sorted(key for key in traced if adjacency.get(key)),
            'excluded_same_equipment_lots': excluded,
            'inspection_results': inspection_results(data, when, cutoff),
            'event_count': len(events), 'reconciliation': reconciliation}


class ManufacturingExamples(unittest.TestCase):
    def test_acceptance_inputs_to_expected(self):
        cases = json.loads((EXAMPLES / 'acceptance.json').read_text())['cases']
        for case in cases:
            with self.subTest(case=case['id']):
                self.assertEqual(evaluate(materialize(case['input'])), case['expected'])

    def test_rework_reusing_input_identity_rejects_cycle(self):
        data = materialize({'fixture': 'input.json'})
        data['events'][2]['outputs'][0]['lot_id'] = 'RW-50'
        self.assertEqual(evaluate(data), {'status': 'rejected', 'reason': 'genealogy_cycle'})

    def test_explicit_approved_conversion_reconciles(self):
        data = materialize({'fixture': 'input.json'})
        row = data['events'][0]['inputs'][0]
        row['quantity'], row['unit'] = '100000', 'g'
        self.assertEqual(evaluate(data)['reason'], 'unapproved_unit_conversion')
        data['unit_conversions'] = [{'from': 'g', 'to': 'kg', 'factor': '0.001', 'dimension': 'mass'}]
        result = evaluate(data)
        self.assertEqual(result['reconciliation']['E1'], 'balanced')
        self.assertEqual(result['candidate_quantity'], {'value': '108', 'unit': 'kg'})

    def test_event_time_cutoff_and_observed_time_are_independent(self):
        data = materialize({'fixture': 'input.json'})
        data['query']['event_as_of'] = '2026-11-01T09:30:00Z'
        result = evaluate(data)
        self.assertEqual(result['event_count'], 2)
        self.assertEqual(result['candidate_lots'], ['M1|P1|FG-60'])
        self.assertEqual(result['candidate_quantity'], {'value': '60', 'unit': 'kg'})

    def test_wrong_local_specification_is_unknown_and_pass_does_not_clear_recall(self):
        data = materialize({'fixture': 'input.json'})
        self.assertIn('M1|P1|FG-48', evaluate(data)['candidate_lots'])
        data['inspections'][1]['specification_version'] = 'unapproved-v2'
        result = evaluate(data)
        self.assertEqual(result['inspection_results']['I2'], 'unknown')
        self.assertIn('M1|P1|FG-48', result['candidate_lots'])

    def test_negative_quantity_and_unknown_lot_reject(self):
        data = materialize({'fixture': 'input.json'})
        data['events'][0]['inputs'][0]['quantity'] = '-100'
        self.assertEqual(evaluate(data)['reason'], 'invalid_quantity')
        data = materialize({'fixture': 'input.json'})
        data['events'][1]['outputs'][0]['lot_id'] = 'NO-SUCH-LOT'
        self.assertEqual(evaluate(data)['reason'], 'unknown_lot')


if __name__ == '__main__':
    unittest.main()
