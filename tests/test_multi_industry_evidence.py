"""Offline integrity of dated multi-industry use; never starts a native client."""
import hashlib
import json
from pathlib import Path
import unittest

import jsonschema
from evidence_sources import packages, package_files, package_digest

ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / 'tests/compatibility/multi-industry-native'
FINANCE = ROOT / 'tests/content-validation/multi-industry-finance'


def read(path):
    return json.loads(path.read_text())


class MultiIndustryEvidenceTests(unittest.TestCase):
    def assert_artifacts(self, directory, receipt):
        for relative, expected in receipt['artifact_sha256'].items():
            with self.subTest(artifact=relative):
                path = directory / relative
                self.assertTrue(path.resolve().is_relative_to(directory))
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)

    def test_native_discovery_binds_dated_packages_in_both_locations(self):
        receipt = read(NATIVE / 'receipt.json')
        self.assert_artifacts(NATIVE, receipt)
        sources = packages()
        discovery = read(NATIVE / 'discovery.json')
        self.assertEqual(len(sources), 25)
        self.assertEqual({(r['scope'], r['phase']) for r in discovery['results']},
                         {(scope, phase) for scope in ('project', 'legacy-codex-home')
                          for phase in ('single', 'multiple')})
        for result in discovery['results']:
            first = 'entity-relationship-modeling'
            names = set(sources) if result['phase'] == 'multiple' else {first}
            self.assertEqual(set(result['skill_names']), names)
            self.assertEqual(result['native_metadata_discovery'], 'passed')
            total_files = 0
            for name in names:
                total_files += len(sources[name])
                self.assertEqual(result['package_sha256'][name], package_digest(sources[name]))
            self.assertEqual(result['resource_files_read'], total_files)

    def test_explicit_native_use_binds_twelve_final_independent_packages(self):
        receipt = read(NATIVE / 'receipt.json')
        review = {r['skill']: r for r in read(NATIVE / 'review.json')['results']}
        self.assertEqual(len(receipt['results']), 12)
        expected = set(read(ROOT / 'tests/compatibility/cc-switch-native/receipt.json')
                       ['source_packages_sha256'])
        dated = set(packages())
        self.assertEqual({r['skill'] for r in receipt['results']}, dated - expected)
        self.assertEqual(set(review), dated - expected)
        for result in receipt['results']:
            name = result['skill']
            with self.subTest(skill=name):
                self.assertEqual(result['exit_code'], 0)
                self.assertTrue(result['turn_completed'])
                self.assertEqual(result['files_sha256'], package_files(name))
                directory = NATIVE / name
                output = read(directory / 'result.json')
                jsonschema.validate(output, read(directory / 'schema.json'))
                self.assertEqual(output['skill_used'], name)
                for key in ('identity_rules', 'time_and_units', 'source_limits', 'unresolved'):
                    self.assertTrue(output[key], key)
                commands = read(directory / 'commands.json')
                self.assertTrue(any(c['exit_code'] == 0 and '/SKILL.md' in c['command']
                                    for c in commands))
                self.assertTrue(any(c['exit_code'] == 0 and '/references/' in c['command']
                                    for c in commands))
                self.assertTrue(all(c.get('explanation') for c in commands if c['exit_code']))
                self.assertTrue(review[name]['passed'])
                self.assertTrue(review[name]['observed'])
                if 'expected_answer' in review[name]:
                    self.assertEqual(output['answer'], review[name]['expected_answer'])

    def test_finance_independent_review_retains_original_findings_and_final_recheck(self):
        receipt = read(FINANCE / 'receipt.json')
        self.assert_artifacts(FINANCE, receipt)
        original = read(FINANCE / 'verification.json')
        recheck = read(FINANCE / 'recheck.json')
        self.assertEqual(original['count'], 17)
        self.assertTrue(all(c['result'] == 'passed' for c in original['checks']))
        self.assertEqual(recheck['passed_check_count'], 21)
        self.assertTrue(all(c['result'] == 'passed' for c in recheck['checks']))
        self.assertEqual({f['id']: f['status'] for f in recheck['findings_status']},
                         {key: 'addressed' for key in ('F1', 'F2', 'F3', 'F4')})
        self.assertEqual(recheck['remaining_substantive_gaps_in_requested_scope'], [])
        for relative, expected in recheck['original_artifact_sha256'].items():
            self.assertEqual(hashlib.sha256((FINANCE / relative).read_bytes()).hexdigest(), expected)
        for name, files in receipt['source_packages_sha256'].items():
            self.assertEqual(package_files(name), files)
        for relative, hashes in recheck['reviewed_current_vs_frozen_hashes'].items():
            name, path = relative.split('/', 1)
            self.assertEqual(hashlib.sha256(packages()[name][path]).hexdigest(),
                             hashes['current_recheck_sha256'])
        schema = read(ROOT / 'schemas/graph-model.schema.json')
        for name in ('task-a-graph-model.json', 'task-b-graph-model.json'):
            jsonschema.validate(read(FINANCE / name), schema)
        for record in recheck['schema_validations']:
            self.assertEqual(record['result'], 'passed')
            self.assertEqual(record['errors'], [])


if __name__ == '__main__':
    unittest.main()
