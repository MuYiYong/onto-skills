"""Reject missing or overstated standards evidence; no online/conformance claim."""
import copy
import hashlib
import json
from pathlib import Path
import unittest

from scripts.validate import validate_knowledge, knowledge_catalog

ROOT = Path(__file__).resolve().parents[1]


class StandardsGroundingTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / 'knowledge/finance/standards/sources.json').read_text())
        self.asset = dict(id='sample', name='Original bounded guidance', version='1.0.0',
                          license='MIT', updated_at='2026-11-06', scope='Synthetic test',
                          authority='Original project interpretation', classification='project-curated',
                          source_ids=['onto-project', 'owl2'], standards_policy='standards-first-v1',
                          standard_status='standard-backed',
                          standard_basis=[dict(source_id='owl2', locator='OWL 2 Primer, section 4',
                                               relation='supports', scope='Classes and properties only')])

    def test_bounded_standard_basis_and_explicit_local_gap_are_valid(self):
        self.assertEqual(validate_knowledge(self.asset, self.catalog), [])
        self.asset['standard_basis'] = []
        self.asset['standard_status'] = 'nonstandard-modeling'
        self.asset['standard_gap'] = 'No universal domain rule; a task-specific policy is required.'
        self.assertEqual(validate_knowledge(self.asset, self.catalog), [])

    def test_policy_and_record_evidence_cannot_be_omitted(self):
        for field in ('standards_policy', 'standard_basis'):
            asset = copy.deepcopy(self.asset)
            del asset[field]
            self.assertTrue(validate_knowledge(asset, self.catalog), field)
        self.asset['records'] = [dict(id='uncovered', classification='project-curated',
                                      source_ids=['onto-project'])]
        self.assertTrue(validate_knowledge(self.asset, self.catalog))

    def test_project_source_cannot_be_declared_standard_support(self):
        self.asset['standard_basis'][0]['source_id'] = 'onto-project'
        self.assertTrue(validate_knowledge(self.asset, self.catalog))

    def test_unknown_unattached_and_incomplete_citations_are_rejected(self):
        for changes in ({'source_id': 'unknown'}, {'source_id': 'fibo'}, {'locator': ' '},
                        {'scope': ''}, {'relation': 'equivalent-to'}):
            asset = copy.deepcopy(self.asset)
            asset['standard_basis'][0].update(changes)
            self.assertTrue(validate_knowledge(asset, self.catalog), changes)

    def test_malformed_citations_and_gaps_are_rejected_without_crashing(self):
        for value in ('owl2', {}, [None], [{'source_id': []}]):
            asset = copy.deepcopy(self.asset)
            asset['standard_basis'] = value
            self.assertTrue(validate_knowledge(asset, self.catalog), value)
        for value in (' ', [], False):
            asset = copy.deepcopy(self.asset)
            asset['standard_basis'] = []
            asset['standard_gap'] = value
            self.assertTrue(validate_knowledge(asset, self.catalog), value)

    def test_official_definition_requires_direct_support(self):
        self.asset.update(classification='official-standard', standard_basis=[],
                          standard_gap='Local interpretation only')
        self.assertTrue(validate_knowledge(self.asset, self.catalog))

    def test_sources_field_cannot_bypass_record_evidence(self):
        self.asset['sources'] = []
        del self.asset['standard_basis']
        self.assertTrue(validate_knowledge(self.asset, self.catalog))

    def test_kind_field_cannot_bypass_knowledge_record_checks(self):
        for record in (self.asset, dict(id='nested', classification='project-curated',
                                        source_ids=['onto-project'])):
            asset = copy.deepcopy(self.asset)
            invalid = copy.deepcopy(record)
            invalid['kind'] = 'project-curated'
            for field in ('standard_status', 'standard_basis', 'standard_gap'):
                invalid.pop(field, None)
            asset['records'] = [invalid]
            with self.subTest(record=record['id']):
                self.assertTrue(validate_knowledge(asset, self.catalog))

    def test_missing_or_invented_standard_status_is_rejected(self):
        for value in (None, '', 'certified-because-official-link'):
            self.asset['standard_status'] = value
            self.assertTrue(validate_knowledge(self.asset, self.catalog), value)

    def test_background_does_not_become_standard_backed(self):
        self.asset['standard_basis'][0]['relation'] = 'background'
        self.asset['standard_gap'] = 'Only public orientation material was verified.'
        self.assertTrue(validate_knowledge(self.asset, self.catalog))
        self.asset['standard_status'] = 'nonstandard-modeling'
        self.assertEqual(validate_knowledge(self.asset, self.catalog), [])

    def test_nonstandard_modeling_requires_an_explicit_reason(self):
        self.asset['standard_status'] = 'nonstandard-modeling'
        self.assertTrue(validate_knowledge(self.asset, self.catalog))

    def test_all_central_knowledge_has_standards_first_coverage(self):
        for path in (ROOT / 'knowledge').rglob('*.json'):
            asset = json.loads(path.read_text())
            if 'sources' in asset:
                continue
            with self.subTest(asset=str(path.relative_to(ROOT))):
                self.assertEqual(asset.get('standards_policy'), 'standards-first-v1')
                catalog = json.loads(knowledge_catalog(path, ROOT).read_text())
                self.assertEqual(validate_knowledge(asset, catalog), [])

    def test_review_ledger_binds_all_identified_objects_to_current_knowledge(self):
        ledger = json.loads((ROOT / 'tests/standards/knowledge-review/ledger.json').read_text())
        self.assertEqual(len(ledger['records']), ledger['identified_objects'])
        self.assertEqual(ledger['identified_objects'], 149)
        found = set()
        for record in ledger['records']:
            path = ROOT / record['asset']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), record['asset_sha256'])
            value = json.loads(path.read_text())
            pointer = record['json_pointer']
            if pointer != '/':
                for token in pointer.lstrip('/').split('/'):
                    token = token.replace('~1', '/').replace('~0', '~')
                    value = value[int(token)] if isinstance(value, list) else value[token]
            self.assertEqual(value['id'], record['id'])
            self.assertEqual(value['standard_status'], record['standard_status'])
            self.assertEqual(value.get('standard_basis', []), record['standard_basis'])
            self.assertEqual(value.get('standard_gap'), record['standard_gap'])
            key = record['asset'], pointer
            self.assertNotIn(key, found)
            found.add(key)


if __name__ == '__main__':
    unittest.main()
