"""Reference calculations on synthetic projections, not a CSAF/SPDX validator."""
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import unittest

from scripts.validate import validate_model

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / 'examples/cybersecurity'


def instant(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('timezone required')
    return result.astimezone(timezone.utc)


def evaluate_cybersecurity(data):
    """Bounded oracle: exact pre-reviewed mappings, integer advisory revisions only."""
    as_of, known = instant(data['as_of']), instant(data['known_as_of'])
    packages = {}
    for package in data['packages']:
        key = (package['namespace'], package['spdx_id'])
        if key in packages and packages[key] != package:
            raise ValueError('conflicting package identity')
        packages[key] = package

    groups = {}
    for advisory in data['advisories']:
        if (advisory['document_status'] != 'final'
                or instant(advisory['released_at']) > as_of
                or instant(advisory['observed_at']) > known):
            continue
        if type(advisory['revision']) is not int or advisory['revision'] < 1:
            raise ValueError('fixture requires positive integer revisions')
        groups.setdefault((advisory['publisher'], advisory['tracking_id']), []).append(advisory)
    selected = []
    for key, revisions in groups.items():
        newest = max(a['revision'] for a in revisions)
        revisions = [a for a in revisions if a['revision'] == newest]
        # Repeated receipts may change observed_at, never the signed/source payload.
        payloads = {json.dumps({k: v for k, v in a.items() if k != 'observed_at'}, sort_keys=True)
                    for a in revisions}
        selected.append((key, newest, revisions, len(payloads) > 1))

    allowed = {'known_affected', 'known_not_affected', 'fixed', 'under_investigation'}
    assessments, affected, unknown = [], set(), []
    for key, package in sorted(packages.items()):
        mappings = [m for m in data['mappings']
                    if (m['namespace'], m['spdx_id']) == key
                    and m['version'] == package['version'] and m['evidence_id'].strip()
                    and instant(m['observed_at']) <= known]
        evidence, statuses, conflict, invalid = set(), set(), False, False
        for (publisher, tracking), revision, receipts, bad_revision in selected:
            products = {m['product_id'] for m in mappings
                        if m['publisher'] == publisher and m['tracking_id'] == tracking
                        and m['advisory_revision'] == revision}
            matches = [s for a in receipts for s in a['product_status']
                       if s['product_id'] in products and s['vulnerability_id'] == data['vulnerability_id']]
            if not matches:
                continue
            evidence.add(f'{publisher}/{tracking}@{revision}')
            conflict |= bad_revision
            invalid |= any(s['status'] not in allowed for s in matches)
            for assertion in matches:
                required = {'known_not_affected': 'impact_statement',
                            'known_affected': 'action_statement'}.get(assertion['status'])
                if required:
                    statement = assertion.get(required)
                    if not isinstance(statement, str) or not statement.strip():
                        invalid = True
            statuses.update(s['status'] for s in matches)
        status = ('conflicting_evidence' if conflict or len(statuses) > 1 else
                  'invalid_evidence' if invalid else next(iter(statuses), 'unknown'))
        assets = sorted({d['asset_id'] for d in data['deployments']
                         if (d['namespace'], d['spdx_id']) == key
                         and instant(d['observed_at']) <= known
                         and instant(d['valid_from']) <= as_of
                         and (d['valid_to'] is None or as_of < instant(d['valid_to']))})
        component = '#'.join(key)  # Presentation only; actual keys remain scoped pairs.
        if status == 'known_affected':
            affected.update(assets)
        if status in {'unknown', 'under_investigation', 'conflicting_evidence', 'invalid_evidence'}:
            unknown.append(component)
        assessments.append(dict(component=component, version=package['version'], status=status,
                                active_assets=assets, evidence=sorted(evidence)))
    return dict(assessments=assessments, affected_asset_ids=sorted(affected),
                unresolved_component_keys=sorted(unknown), exploited=None,
                remediation_installed=None)


class CybersecurityExamplesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input = json.loads((EXAMPLES / 'input.json').read_text())
        cls.cases = json.loads((EXAMPLES / 'acceptance.json').read_text())['cases']

    def test_hand_reviewed_cases(self):
        for case in self.cases:
            with self.subTest(case=case['id']):
                self.assertEqual(evaluate_cybersecurity(case['input']), case['expected'])

    def test_source_input_matches_first_manual_case(self):
        self.assertEqual(evaluate_cybersecurity(self.input), self.cases[0]['expected'])

    def test_order_duplicate_receipts_and_cvss_do_not_change_applicability(self):
        data = copy.deepcopy(self.input)
        data['advisories'].reverse()
        data['advisories'].append(copy.deepcopy(data['advisories'][-1]))
        data['cvss']['base_score'] = '0.0'
        data['patch_available'] = False
        data['dependencies'].reverse()
        self.assertEqual(evaluate_cybersecurity(data), evaluate_cybersecurity(self.input))

    def test_same_name_or_dependency_does_not_prove_status_or_deployment(self):
        result = evaluate_cybersecurity(self.input)
        by_key = {r['component']: r for r in result['assessments']}
        self.assertEqual(by_key['urn:sbom:B#SPDXRef-lib']['status'], 'unknown')
        self.assertEqual(by_key['urn:sbom:A#SPDXRef-util']['active_assets'], [])
        self.assertIsNone(result['exploited'])
        self.assertIsNone(result['remediation_installed'])

    def test_expired_inventory_is_not_a_current_affected_asset(self):
        data = copy.deepcopy(self.input)
        data['deployments'][0]['valid_to'] = data['as_of']
        self.assertEqual(evaluate_cybersecurity(data)['affected_asset_ids'], [])

    def test_mapping_is_bound_to_the_assessed_document_revision(self):
        data = copy.deepcopy(self.input)
        data.update(as_of='2026-11-09T12:00:00Z', known_as_of='2026-11-09T12:00:00Z')
        for mapping in data['mappings']:
            mapping['advisory_revision'] = 1
        result = evaluate_cybersecurity(data)
        self.assertEqual(result['assessments'][0]['status'], 'unknown')
        self.assertEqual(result['assessments'][0]['evidence'], [])

    def test_malformed_source_statements_do_not_support_reassuring_status(self):
        for status, field in (('known_not_affected', 'impact_statement'),
                              ('known_affected', 'action_statement')):
            for value in (None, {}, 0, False, ' '):
                with self.subTest(status=status, value=value):
                    data = copy.deepcopy(self.input)
                    data['advisories'][0]['product_status'][0].update(status=status, **{field: value})
                    self.assertEqual(evaluate_cybersecurity(data)['assessments'][0]['status'],
                                     'invalid_evidence')

    def test_conflicting_identity_and_unordered_revision_fail_explicitly(self):
        data = copy.deepcopy(self.input)
        package = copy.deepcopy(data['packages'][0])
        package['version'] = '9.9'
        data['packages'].append(package)
        with self.assertRaisesRegex(ValueError, 'identity'):
            evaluate_cybersecurity(data)
        data = copy.deepcopy(self.input)
        data['advisories'][0]['revision'] = '1.0.0'
        with self.assertRaisesRegex(ValueError, 'integer revisions'):
            evaluate_cybersecurity(data)

    def test_unzoned_time_is_rejected(self):
        data = copy.deepcopy(self.input)
        data['known_as_of'] = '2026-11-06T12:00:00'
        with self.assertRaisesRegex(ValueError, 'timezone'):
            evaluate_cybersecurity(data)

    def test_model_can_preserve_conflicting_payloads_without_merging_ownership(self):
        model = json.loads((EXAMPLES / 'graph-model.json').read_text())
        self.assertEqual(validate_model(model), [])
        nodes = {n['name']: n for n in model['node_types']}
        for name in ('AdvisoryRevision', 'ProductAssessment'):
            self.assertIn('payload_hash', nodes[name]['primary_key'])
        edges = {e['name']: e for e in model['edge_types']}
        self.assertEqual(edges['HAS_ASSESSMENT']['cardinality']['per_target'], '1')
        self.assertEqual(edges['ASSESSES']['cardinality']['per_source'], '1')
        self.assertTrue(validate_model(model, ready=True))


if __name__ == '__main__':
    unittest.main()
