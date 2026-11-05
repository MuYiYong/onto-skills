"""Bounded synthetic reporting/control evidence checks, not filing/legal compliance."""
import copy
from datetime import datetime
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def moment(value):
    result = datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError('timezone_required')
    return result


def unique_records(records, fields, reason):
    seen = {}
    for record in records:
        key = tuple(record[f] for f in fields)
        if key in seen and seen[key] != record:
            raise ValueError(reason)
        seen[key] = record
    return list(seen.values())


def reporting_example(data):
    """Reference calculation for DEMO-LINEAGE-01 only; no XBRL/regulator engine."""
    try:
        operation = data['operation']
        if operation == 'submission_state':
            receipts = sorted(data['receipts'], key=lambda r: moment(r['received_at']))
            business = [r for r in receipts if r['kind'] == 'business']
            state = business[-1]['status'] if business else 'received'
            return {'submission': data['submission'], 'state': state, 'accepted': state == 'accepted'}
        if operation == 'current_accepted':
            submissions = data['submissions']
            accepted = [s for s in submissions if s['state'] == 'accepted']
            return {'current_accepted': max(accepted, key=lambda s: s['revision'])['id'] if accepted else None,
                    'history': [s['id'] for s in sorted(submissions, key=lambda s: s['revision'])]}
        if data['period_kind'] != data['definition_period_kind']:
            raise ValueError('context_definition_mismatch')
        if data['template_version'] != data['fact_template_version']:
            raise ValueError('template_version_mismatch')
        records = unique_records(data['records'], ('source_system', 'record_id', 'source_version'),
                                 'source_identity_conflict')
        latest = {}
        for record in records:
            if record['entity_id'] != data['entity_id']:
                continue
            if moment(record['observed_at']) > moment(data['known_at']):
                continue
            key = (record['source_system'], record['record_id'])
            if key not in latest or moment(record['observed_at']) > moment(latest[key]['observed_at']):
                latest[key] = record
            elif (moment(record['observed_at']) == moment(latest[key]['observed_at'])
                  and record['source_version'] != latest[key]['source_version']):
                raise ValueError('ambiguous_source_revision')
        included = [r for r in latest.values()
                    if moment(r['event_time']) <= moment(data['as_of']) and r['status'] == 'active']
        total = Decimal('0')
        keys = []
        for record in included:
            if (record['currency'], record['unit']) != (data['currency'], data['unit']):
                raise ValueError('unit_or_currency_mismatch')
            if record['amount'] is None:
                raise ValueError('unknown_amount')
            value = Decimal(record['amount'])
            if not value.is_finite():
                raise ValueError('invalid_amount')
            total += value
            keys.append('/'.join(record[f] for f in ('source_system', 'record_id', 'source_version')))
        return {'status': 'candidate', 'value': format(total, '.2f'), 'source_versions': sorted(keys)}
    except (ValueError, InvalidOperation) as exc:
        return {'status': 'blocked', 'reason': str(exc)}


def related_example(data):
    """Confirmed-control-only demonstration, never complete legal classification."""
    try:
        if data['regime'] != 'demonstration-confirmed-control-only':
            raise ValueError('unsupported_demonstration_regime')
        transactions = unique_records(data['transactions'], ('source_system', 'tx_id', 'tx_version'),
                                      'transaction_identity_conflict')
        candidates, included, not_demonstrated, excluded, totals = set(), set(), set(), set(), {}
        units = {}
        known = moment(data['known_at'])
        latest = {}
        versions = {(t['source_system'], t['tx_id'], t['tx_version']): t for t in transactions}
        for tx in transactions:
            if moment(tx['observed_at']) > known:
                continue
            if tx.get('change_kind') in ('correction', 'status_update'):
                reference = tx.get('revises_ref')
                if not reference:
                    raise ValueError('missing_revision_reference')
                key = tuple(reference[f] for f in ('source_system', 'tx_id', 'tx_version'))
                if (key not in versions or key[:2] != (tx['source_system'], tx['tx_id'])
                    or key[2] == tx['tx_version']):
                    raise ValueError('invalid_revision_reference')
            if tx.get('change_kind') == 'compensation' or tx.get('reverses_ref'):
                raise ValueError('separate_reversal_policy_required')
            key = (tx['source_system'], tx['tx_id'])
            if key not in latest or moment(tx['observed_at']) > moment(latest[key]['observed_at']):
                latest[key] = tx
            elif (moment(tx['observed_at']) == moment(latest[key]['observed_at'])
                  and tx['tx_version'] != latest[key]['tx_version']):
                raise ValueError('ambiguous_transaction_revision')
        for tx in latest.values():
            if tx['status'] != 'executed':
                not_demonstrated.add(tx['tx_id'])
                continue
            at = moment(tx['event_time'])
            parents = {}
            for control in data['controls']:
                if (control['status'] != 'confirmed' or not control.get('evidence_id')
                    or moment(control['observed_at']) > known
                    or moment(control['valid_from']) > at
                    or (control['valid_to'] is not None and at >= moment(control['valid_to']))
                    or (control['basis'] == 'state_only'
                        and data['only_state_holding_does_not_qualify'])):
                    continue
                parents.setdefault(control['controlled'], set()).add(control['controller'])
            def ancestors(party):
                visited = {party}
                pending = [party]
                while pending:
                    current = pending.pop()
                    for parent in parents.get(current, ()):
                        if parent not in visited:
                            visited.add(parent)
                            pending.append(parent)
                return visited
            if tx['from_party'] == tx['to_party']:
                not_demonstrated.add(tx['tx_id'])
                continue
            if not (ancestors(tx['from_party']) & ancestors(tx['to_party'])):
                not_demonstrated.add(tx['tx_id'])
                continue
            candidates.add(tx['tx_id'])
            if (data['basis'] == 'financial_statement'
                and {tx['from_party'], tx['to_party']} <= set(data['consolidated_members'])):
                excluded.add(tx['tx_id'])
                continue
            included.add(tx['tx_id'])
            if not tx.get('unit'):
                raise ValueError('unknown_transaction_unit')
            if tx['currency'] in units and units[tx['currency']] != tx['unit']:
                raise ValueError('transaction_unit_mismatch')
            units[tx['currency']] = tx['unit']
            amount = Decimal(tx['amount'])
            if not amount.is_finite():
                raise ValueError('invalid_amount')
            totals[tx['currency']] = totals.get(tx['currency'], Decimal('0')) + amount
        return {'candidate_tx_ids': sorted(candidates), 'included_tx_ids': sorted(included),
                'not_demonstrated': sorted(not_demonstrated), 'excluded_internal': sorted(excluded),
                'totals_by_currency': {k: format(v, '.2f') for k, v in sorted(totals.items())},
                'legal_conclusion': 'not_determined'}
    except (ValueError, InvalidOperation) as exc:
        return {'status': 'blocked', 'reason': str(exc)}


class FinanceExtensionExampleTests(unittest.TestCase):
    def fixture(self, domain, name='input.json'):
        return json.loads((ROOT / 'examples/finance' / domain / name).read_text())

    def test_all_reporting_acceptance_cases_compute_expected_outputs(self):
        for case in self.fixture('regulatory-reporting', 'acceptance.json')['cases']:
            with self.subTest(case=case['id']):
                self.assertEqual(reporting_example(case['input']), case['expected'])

    def test_all_related_party_cases_compute_expected_outputs(self):
        for case in self.fixture('related-party', 'acceptance.json')['cases']:
            with self.subTest(case=case['id']):
                self.assertEqual(related_example(case['input']), case['expected'])

    def test_report_unknown_timezone_and_nonfinite_money_are_blocked(self):
        for mutation, expected in [('timezone', 'timezone_required'), ('nan', 'invalid_amount')]:
            data = self.fixture('regulatory-reporting')
            if mutation == 'timezone':
                data['known_at'] = '2026-09-30T23:59:59'
            else:
                data['records'][1]['amount'] = 'NaN'
            self.assertEqual(reporting_example(data), {'status': 'blocked', 'reason': expected})

    def test_report_same_time_distinct_revisions_are_ambiguous(self):
        data = self.fixture('regulatory-reporting')
        record = copy.deepcopy(data['records'][0])
        record['source_version'] = 'other-version'
        data['records'].append(record)
        self.assertEqual(reporting_example(data), {'status': 'blocked', 'reason': 'ambiguous_source_revision'})

    def test_shareholding_or_phone_without_control_does_not_qualify(self):
        data = self.fixture('related-party')
        data['controls'] = []
        result = related_example(data)
        self.assertEqual(result['candidate_tx_ids'], [])
        self.assertEqual(result['legal_conclusion'], 'not_determined')

    def test_invented_legal_regime_is_not_silently_applied(self):
        data = self.fixture('related-party')
        data['regime'] = 'complete-nfra-compliance'
        self.assertEqual(related_example(data), {'status': 'blocked', 'reason': 'unsupported_demonstration_regime'})

    def test_withdrawn_control_evidence_does_not_remain_usable(self):
        data = self.fixture('related-party')
        data['controls'][1]['status'] = 'retracted'
        self.assertNotIn('T1', related_example(data)['candidate_tx_ids'])

    def test_related_revision_requires_explicit_reference_and_tie_is_not_guessed(self):
        cases = self.fixture('related-party', 'acceptance.json')['cases']
        data = copy.deepcopy(next(c['input'] for c in cases if c['id'] == 'corrected-version-counted-once'))
        data['transactions'][-1]['revises_ref'] = None
        self.assertEqual(related_example(data), {'status': 'blocked', 'reason': 'missing_revision_reference'})
        data = copy.deepcopy(next(c['input'] for c in cases if c['id'] == 'corrected-version-counted-once'))
        data['transactions'][-1]['observed_at'] = data['transactions'][0]['observed_at']
        self.assertEqual(related_example(data), {'status': 'blocked', 'reason': 'ambiguous_transaction_revision'})

    def test_independent_compensation_does_not_silently_net_regulatory_amounts(self):
        data = self.fixture('related-party')
        data['transactions'][0]['change_kind'] = 'compensation'
        data['transactions'][0]['reverses_ref'] = {'source_system': 'payments', 'tx_id': 'OTHER', 'tx_version': 'v1'}
        data['transactions'][1] = copy.deepcopy(data['transactions'][0])
        self.assertEqual(related_example(data), {'status': 'blocked', 'reason': 'separate_reversal_policy_required'})


if __name__ == '__main__':
    unittest.main()
