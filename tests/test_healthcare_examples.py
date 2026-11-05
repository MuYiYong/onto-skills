"""Offline reference computations for synthetic healthcare examples only.

These checks do not validate full FHIR, clinical correctness, compliance, patient
systems or native database execution. Helpers are test-only, not a runtime API.
"""
from copy import deepcopy
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / 'examples/healthcare'
SERVER_A = 'https://clinic-a.example.invalid/fhir'
QUANTITATIVE_STATUSES = {'final', 'amended', 'corrected'}


def logical_key(row):
    resource = row['resource']
    return '/'.join((row['source_server'], resource['resourceType'], resource['id']))


def version_key(row):
    return logical_key(row) + '/_history/' + row['resource']['meta']['versionId']


def canonical(resource):
    return json.dumps(resource, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def set_path(value, path, replacement):
    parts = path.split('.')
    for part in parts[:-1]:
        value = value[int(part)] if isinstance(value, list) else value[part]
    last = parts[-1]
    value[int(last) if isinstance(value, list) else last] = deepcopy(replacement)


def prepare(fixture, params):
    """Each acceptance case starts from fresh input, including deliberate faults."""
    fixture = deepcopy(fixture)
    for mutation in params.get('mutations', []):
        matches = [row for row in fixture['resources']
                   if row['source_server'] == mutation.get('source_server', SERVER_A)
                   and row['is_current']
                   and row['resource']['resourceType'] == mutation['resource_type']
                   and row['resource']['id'] == mutation['resource_id']]
        if len(matches) != 1:
            raise ValueError('mutation must select one current resource')
        for path, value in mutation['set'].items():
            set_path(matches[0]['resource'], path, value)
    replay = params.get('replay_version_key')
    conflict = params.get('conflicting_replay')
    if replay or conflict:
        target = replay or conflict['version_key']
        matches = [row for row in fixture['resources'] if version_key(row) == target]
        if len(matches) != 1:
            raise ValueError('replay must select one source snapshot')
        row = deepcopy(matches[0])
        if conflict:
            for path, value in conflict['set'].items():
                set_path(row['resource'], path, value)
        fixture['resources'].append(row)
    return fixture


def intake(fixture):
    """Selected source invariants; explicitly not a full FHIR validator."""
    unique = {}
    errors = set()
    for row in fixture['resources']:
        resource = row['resource']
        if not resource.get('meta', {}).get('versionId'):
            errors.add('missing-version-id')
            continue
        key = version_key(row)
        if key in unique:
            if canonical(unique[key]['resource']) != canonical(resource):
                errors.add('conflicting-version-payload')
            elif unique[key]['is_current'] != row['is_current']:
                errors.add('conflicting-current-claim')
        else:
            unique[key] = row
        if (resource['resourceType'] == 'Observation'
                and 'dataAbsentReason' in resource
                and any(name.startswith('value') for name in resource)):
            errors.add('obs-6-value-and-absent-reason')
    current = {}
    for row in unique.values():
        if row['is_current']:
            logical = logical_key(row)
            if logical in current:
                errors.add('multiple-current-versions')
            current[logical] = row
    return list(unique.values()), sorted(errors)


def current_rows(rows, resource_type):
    return [row for row in rows
            if row['is_current'] and row['resource']['resourceType'] == resource_type]


def current_resource(rows, resource_type, resource_id, server=SERVER_A):
    found = [row for row in current_rows(rows, resource_type)
             if row['source_server'] == server and row['resource']['id'] == resource_id]
    if len(found) != 1:
        raise ValueError('resource current version unresolved')
    return found[0]


def reference_logical(row, reference):
    """Bounded fixture resolution, not a general FHIR reference resolver."""
    if reference.startswith('https://'):
        return reference.split('/_history/')[0]
    return row['source_server'] + '/' + reference


def based_on(row, order_id):
    wanted = SERVER_A + '/ServiceRequest/' + order_id
    return any(reference_logical(row, ref['reference']) == wanted
               for ref in row['resource'].get('basedOn', []))


def coding_tuple(resource):
    codings = resource.get('code', {}).get('coding', [])
    if len(codings) != 1:
        return None  # No arbitrary choice among multiple clinical codings.
    coding = codings[0]
    values = tuple(coding.get(name) for name in ('system', 'version', 'code'))
    return values if all(values) else None


def unit_tuple(resource):
    quantity = resource.get('valueQuantity', {})
    values = tuple(quantity.get(name) for name in ('system', 'code'))
    return values if all(values) else None


def quantitative_eligible(row):
    resource = row['resource']
    value = resource.get('valueQuantity', {}).get('value')
    return (row['is_current'] and resource['status'] in QUANTITATIVE_STATUSES
            and isinstance(value, (int, float)) and not isinstance(value, bool)
            and 'comparator' not in resource.get('valueQuantity', {})
            and 'dataAbsentReason' not in resource
            and coding_tuple(resource) is not None and unit_tuple(resource) is not None)


def observation_state(row):
    resource = row['resource']
    if resource['status'] == 'entered-in-error':
        state = 'entered-in-error'
    elif resource['status'] == 'unknown':
        state = 'unknown-status'
    elif resource['status'] == 'preliminary':
        state = 'provisional'
    elif 'valueQuantity' not in resource:
        absent = resource.get('dataAbsentReason', {}).get('coding', [])
        state = 'unknown-value' if any(x.get('code') == 'unknown' for x in absent) else 'missing-value'
    elif quantitative_eligible(row):
        state = 'quantitative-eligible'
    else:
        state = 'not-eligible'
    return {'version_key': version_key(row), 'state': state,
            'quantitative_eligible': quantitative_eligible(row), 'normality': 'not-assessed'}


def evaluate(fixture, params):
    """Reference calculations for operations-v1 in the bundled method."""
    fixture = prepare(fixture, params)
    rows, errors = intake(fixture)
    operation = params['operation']
    if operation == 'validate_intake':
        return {'accepted': not errors, 'error_codes': errors}
    if errors:
        raise ValueError(errors)
    if operation == 'completed_procedures':
        procedures = [row for row in current_rows(rows, 'Procedure') if based_on(row, params['order_id'])]
        completed = sorted(version_key(row) for row in procedures if row['resource']['status'] == 'completed')
        result = {'procedure_version_keys': completed, 'count': len(completed)}
        not_done = sorted(version_key(row) for row in procedures if row['resource']['status'] == 'not-done')
        if not_done:
            result['documented_not_done_keys'] = not_done
        return result
    if operation == 'observation_state':
        return observation_state(current_resource(rows, 'Observation', params['observation_id']))
    if operation == 'order_result_state':
        observations = sorted(version_key(row) for row in current_rows(rows, 'Observation')
                              if based_on(row, params['order_id']))
        return {'order_id': params['order_id'], 'observation_version_keys': observations,
                'state': 'missing-result' if not observations else 'documented-result',
                'negative_result': None}
    if operation == 'identity_inventory':
        observations = [row for row in rows if row['resource']['resourceType'] == 'Observation']
        selected = current_resource(rows, 'Observation', 'obs-1')
        return {'resource_version_count': len(rows),
                'logical_resource_count': len({logical_key(row) for row in rows}),
                'patient_count': len(fixture['patients']),
                'encounter_logical_ids': sorted({row['resource']['id'] for row in current_rows(rows, 'Encounter')}),
                'observation_version_count': len(observations),
                'current_observation_count': len(current_rows(rows, 'Observation')),
                'obs_1_version_keys': sorted(version_key(row) for row in observations
                                             if logical_key(row) == logical_key(selected)),
                'obs_1_current_key': version_key(selected)}
    if operation == 'identity_decision':
        attempt = next(row for row in fixture['identity_match_attempts'] if row['attempt_id'] == params['attempt_id'])
        # This example supports only evidence-absent shared-contact candidates.
        authorized = bool(attempt.get('approved_crosswalk_evidence')) and attempt.get('evidence_kind') == 'approved-crosswalk'
        return {'attempt_id': attempt['attempt_id'], 'merge_authorized': authorized,
                'patient_count': len(fixture['patients']),
                'patient_keys': sorted(p['patient_key'] for p in fixture['patients'])}
    if operation == 'compare_observations':
        selected = [current_resource(rows, 'Observation', rid) for rid in params['observation_ids']]
        selected.sort(key=version_key)
        comparable = False
        if not all(quantitative_eligible(row) for row in selected):
            reason = 'ineligible-observation'
        elif len({coding_tuple(row['resource']) for row in selected}) != 1:
            reason = 'coding-mismatch'
        elif len({unit_tuple(row['resource']) for row in selected}) != 1:
            reason = 'unit-mismatch'
        else:
            comparable, reason = True, 'same-code-version-and-unit'
        result = {'version_keys': [version_key(row) for row in selected], 'comparable': comparable,
                  'reason_code': reason, 'aggregate_value': sum(row['resource']['valueQuantity']['value'] for row in selected) if comparable else None}
        if comparable:
            result['clinical_interpretation'] = 'not-assessed'
        return result
    if operation == 'retraction_decision':
        instruction = params['instruction']
        target = instruction['target_version_key']
        keys = {version_key(row) for row in rows}
        applied = (instruction.get('authorized') is True and bool(instruction.get('evidence_id'))
                   and '/_history/' in target and target in keys)
        logical = target.split('/_history/')[0]
        return {'applied': applied, 'excluded_version_keys': [target] if applied else [],
                'retained_history_version_keys': sorted(version_key(row) for row in rows if logical_key(row) == logical),
                'fallback_to_prior_version': False}
    if operation == 'disclosure_decision':
        authorization = fixture['authorization']
        allowed = authorization['purpose_approved'] is True and authorization['disclosure_approved'] is True
        return {'disclosure_allowed': allowed, 'released_record_count': len(rows) if allowed else 0}
    raise ValueError('unknown example operation: ' + operation)


class HealthcareExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((EXAMPLES / 'input.json').read_text())
        cls.acceptance = json.loads((EXAMPLES / 'acceptance.json').read_text())

    def test_all_documented_acceptance_cases(self):
        for case in self.acceptance['cases']:
            with self.subTest(case=case['id']):
                self.assertEqual(evaluate(self.fixture, case['input']), case['expected'])

    def test_procedure_status_controls_completion_independently_of_order(self):
        params = {'operation': 'completed_procedures', 'order_id': 'ord-1',
                  'mutations': [{'resource_type': 'Procedure', 'resource_id': 'proc-1', 'set': {'status': 'not-done'}}]}
        result = evaluate(self.fixture, params)
        self.assertEqual(result['count'], 0)
        self.assertEqual(len(result['documented_not_done_keys']), 1)
        # A completed request without a completed event still has no completed act.
        params['mutations'].append({'resource_type': 'ServiceRequest', 'resource_id': 'ord-1', 'set': {'status': 'completed'}})
        self.assertEqual(evaluate(self.fixture, params)['count'], 0)

    def test_missing_unknown_and_error_are_distinct(self):
        state = evaluate(self.fixture, {'operation': 'observation_state', 'observation_id': 'obs-error'})
        self.assertEqual(state['state'], 'entered-in-error')
        self.assertFalse(state['quantitative_eligible'])
        unknown = evaluate(self.fixture, {'operation': 'observation_state', 'observation_id': 'obs-unknown'})
        self.assertEqual(unknown['state'], 'unknown-value')
        missing = evaluate(self.fixture, {'operation': 'order_result_state', 'order_id': 'ord-3'})
        self.assertEqual(missing['state'], 'missing-result')
        self.assertIsNone(missing['negative_result'])
        for status, expected in [('unknown', 'unknown-status'), ('preliminary', 'provisional')]:
            result = evaluate(self.fixture, {'operation': 'observation_state', 'observation_id': 'obs-repeat',
                              'mutations': [{'resource_type': 'Observation', 'resource_id': 'obs-repeat', 'set': {'status': status}}]})
            self.assertEqual(result['state'], expected)
            self.assertFalse(result['quantitative_eligible'])
            self.assertEqual(result['normality'], 'not-assessed')

    def test_opaque_versions_do_not_control_current_selection(self):
        fixture = deepcopy(self.fixture)
        for row in fixture['resources']:
            if row['resource']['resourceType'] == 'Observation' and row['resource']['id'] == 'obs-1':
                row['resource']['meta']['versionId'] = 'a' if row['is_current'] else 'zz99'
        result = evaluate(fixture, {'operation': 'identity_inventory'})
        self.assertTrue(result['obs_1_current_key'].endswith('/_history/a'))
        self.assertEqual(result['observation_version_count'], 6)
        self.assertEqual(result['encounter_logical_ids'], ['enc-1', 'enc-2'])

    def test_identity_includes_server_type_id_and_version(self):
        original = self.fixture['resources'][0]
        keys = set()
        for field, value in [('server', 'https://other.example.invalid/fhir'), ('type', 'Encounter'), ('id', 'other'), ('version', 'other')]:
            row = deepcopy(original)
            if field == 'server':
                row['source_server'] = value
            elif field == 'version':
                row['resource']['meta']['versionId'] = value
            else:
                row['resource']['resourceType' if field == 'type' else 'id'] = value
            keys.add(version_key(row))
        self.assertEqual(len(keys | {version_key(original)}), 5)
        row = deepcopy(original)
        row['ingested_at'] = '2026-11-01T00:00:00Z'
        self.assertEqual(version_key(row), version_key(original))

    def test_missing_code_version_comparator_or_unit_blocks_arithmetic(self):
        for path, value in [('code.coding.0.version', None), ('valueQuantity.code', None), ('valueQuantity.comparator', '<')]:
            with self.subTest(path=path):
                fixture = deepcopy(self.fixture)
                target = next(row for row in fixture['resources'] if row['resource']['id'] == 'obs-repeat')
                if path == 'valueQuantity.comparator':
                    target['resource']['valueQuantity']['comparator'] = value
                else:
                    set_path(target['resource'], path, value)
                result = evaluate(fixture, {'operation': 'compare_observations', 'observation_ids': ['obs-1', 'obs-repeat']})
                self.assertFalse(result['comparable'])
                self.assertIsNone(result['aggregate_value'])

    def test_conflicting_current_claims_and_missing_version_are_rejected(self):
        fixture = deepcopy(self.fixture)
        next(row for row in fixture['resources'] if row['resource']['id'] == 'obs-1' and not row['is_current'])['is_current'] = True
        result = evaluate(fixture, {'operation': 'validate_intake'})
        self.assertIn('multiple-current-versions', result['error_codes'])
        fixture = deepcopy(self.fixture)
        fixture['resources'][0]['resource']['meta'].pop('versionId')
        self.assertIn('missing-version-id', evaluate(fixture, {'operation': 'validate_intake'})['error_codes'])

    def test_retraction_needs_exact_version_and_evidence(self):
        target = SERVER_A + '/Observation/obs-1/_history/v2'
        for instruction in [{'target_version_key': target, 'authorized': True, 'evidence_id': None},
                            {'target_version_key': target.split('/_history/')[0], 'authorized': True, 'evidence_id': 'synthetic-authority'}]:
            result = evaluate(self.fixture, {'operation': 'retraction_decision', 'instruction': instruction})
            self.assertFalse(result['applied'])
            self.assertFalse(result['fallback_to_prior_version'])
            self.assertEqual(len(result['retained_history_version_keys']), 2)

    def test_clock_precision_and_condition_assertion_remain_separate(self):
        rows, errors = intake(self.fixture)
        self.assertEqual(errors, [])
        observation = current_resource(rows, 'Observation', 'obs-1')
        self.assertEqual(observation['resource']['effectiveDateTime'], '2026-10-01T09:00:00Z')
        self.assertEqual(observation['resource']['issued'], '2026-10-02T10:00:00Z')
        self.assertEqual(observation['ingested_at'], '2026-10-04T12:00:00Z')
        condition = current_resource(rows, 'Condition', 'concern-1')['resource']
        self.assertEqual(condition['onsetDateTime'], '2026-10-01')
        self.assertEqual(condition['verificationStatus']['coding'][0]['code'], 'unconfirmed')


if __name__ == '__main__':
    unittest.main()
