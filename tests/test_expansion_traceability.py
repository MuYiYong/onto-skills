"""Cross-artifact coverage: current knowledge, standards review and competency cases."""
import hashlib
import json
from pathlib import Path
import unittest

from scripts.validate import validate_model

ROOT = Path(__file__).resolve().parents[1]
SECTORS = ('built-environment', 'environmental-monitoring', 'education')


def identified(value, pointer='/'):
    if isinstance(value, dict):
        if 'id' in value:
            yield pointer, value
        for key, child in value.items():
            token = key.replace('~', '~0').replace('/', '~1')
            yield from identified(child, pointer.rstrip('/') + '/' + token)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from identified(child, pointer.rstrip('/') + '/' + str(index))


class ExpansionTraceabilityTests(unittest.TestCase):
    def test_all_current_knowledge_objects_are_reviewed_exactly_once(self):
        actual = {}
        for path in (ROOT / 'knowledge').rglob('*.json'):
            asset = json.loads(path.read_text())
            if 'sources' in asset:
                continue
            for pointer, record in identified(asset):
                actual[str(path.relative_to(ROOT)), pointer] = (record, path)
        found = set()
        for name in ('ledger.json', 'expansion-ledger.json'):
            ledger = json.loads((ROOT / 'tests/standards/knowledge-review' / name).read_text())
            self.assertEqual(ledger['identified_objects'], len(ledger['records']))
            for record in ledger['records']:
                key = record['asset'], record['json_pointer']
                with self.subTest(key=key):
                    self.assertNotIn(key, found)
                    found.add(key)
                    value, path = actual[key]
                    self.assertEqual(record['asset_sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
                    self.assertEqual(record['id'], value['id'])
                    self.assertEqual(record['standard_status'], value['standard_status'])
                    self.assertEqual(record['standard_basis'], value.get('standard_basis', []))
                    self.assertEqual(record['standard_gap'], value.get('standard_gap'))
            for catalog in ledger['catalogues']:
                self.assertEqual(catalog['sha256'], hashlib.sha256((ROOT / catalog['path']).read_bytes()).hexdigest())
        self.assertEqual(found, set(actual))

    def test_questions_link_real_model_elements_and_cover_all_adverse_cases(self):
        for sector in SECTORS:
            directory = ROOT / 'examples' / sector
            with self.subTest(sector=sector):
                model = json.loads((directory / 'graph-model.json').read_text())
                trace = json.loads((directory / 'cq-trace.json').read_text())['questions']
                cases = json.loads((directory / 'acceptance.json').read_text())['cases']
                self.assertEqual(validate_model(model), [])
                self.assertTrue(validate_model(model, ready=True))
                self.assertEqual({q['question'] for q in trace}, set(model['competency_questions']))
                elements = {e['name'] for kind in ('node_types', 'edge_types') for e in model[kind]}
                covered = set()
                for row in trace:
                    self.assertTrue(row['model_elements'])
                    self.assertLessEqual(set(row['model_elements']), elements)
                    self.assertTrue(row['case_ids'])
                    covered.update(row['case_ids'])
                self.assertEqual(covered, {case['id'] for case in cases})

    def test_models_can_represent_payload_conflicts_without_overwriting(self):
        expected = {'built-environment': ('ModelRevision', 'ObjectSnapshot'),
                    'environmental-monitoring': ('DatastreamSnapshot', 'ObservationRecord'),
                    'education': ('CredentialRecord',)}
        for sector, names in expected.items():
            model = json.loads((ROOT / 'examples' / sector / 'graph-model.json').read_text())
            nodes = {node['name']: node for node in model['node_types']}
            for name in names:
                self.assertIn('payload_hash', nodes[name]['primary_key'])
            source_properties = {p['name'] for p in nodes['SourceRecord']['properties']}
            self.assertLessEqual({'supersedes_record_id', 'derived_from_record_id',
                                  'payload_hash', 'source_locator', 'observed_at'}, source_properties)
            self.assertTrue(any(m['status'] == 'unmapped' for m in model['mappings']))


if __name__ == '__main__':
    unittest.main()
