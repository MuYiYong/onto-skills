"""Offline integrity of dated CLI/desktop evidence, never new native acceptance."""
import hashlib
import json
from pathlib import Path
import unittest

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'tests/compatibility/codex-execution'
DESKTOP = ROOT / 'tests/compatibility/cc-switch-native'


def read(path):
    return json.loads(path.read_text())


def package_files(name):
    directory, = ROOT.glob('skills/*/' + name)
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in directory.rglob('*') if p.is_file()}


class CompatibilityEvidenceTests(unittest.TestCase):
    def test_cli_cases_bind_actual_outputs_and_current_independent_packages(self):
        receipt = read(CLI / 'receipt.json')
        for relative, expected in receipt['artifact_sha256'].items():
            path = CLI / relative
            self.assertTrue(path.resolve().is_relative_to(CLI))
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
        self.assertEqual(len(receipt['results']), 4)
        for result in receipt['results']:
            name = result['skill']
            with self.subTest(skill=name):
                self.assertEqual(result['exit_code'], 0)
                self.assertTrue(result['turn_completed'])
                self.assertEqual(result['files_sha256'], package_files(name))
                directory = CLI / name
                output = directory / 'result.json'
                self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(),
                                 result['output_sha256'])
                jsonschema.validate(read(output), read(directory / 'schema.json'))
                self.assertEqual(read(output)['skill_used'], name)
                commands = read(directory / 'commands.json')
                self.assertTrue(all(c['exit_code'] == 0 for c in commands))
                self.assertTrue(any('/SKILL.md' in c['command'] for c in commands))
                self.assertTrue(any('/references/' in c['command'] for c in commands))

    def test_cli_scenario_retains_distinct_institution_counterexamples(self):
        output = read(CLI / 'multi-lending-detection/result.json')
        self.assertEqual(output['candidates'], ['Alpha'])
        self.assertEqual({r['borrower_id']: r['distinct_lenders']
                          for r in output['lender_counts']},
                         {'Alpha': 2, 'Beta': 1, 'Gamma': 0})
        review = read(CLI / 'review.json')['results']
        self.assertEqual({r['skill'] for r in review},
                         {r['skill'] for r in read(CLI / 'receipt.json')['results']})
        self.assertTrue(all(r['passed'] and r['observed'] for r in review))

    def test_desktop_artifacts_and_all_synchronized_resources_match_sources(self):
        receipt = read(DESKTOP / 'receipt.json')
        self.assertTrue(all(c['passed'] for c in receipt['checks']))
        for relative, expected in receipt['artifact_sha256'].items():
            with self.subTest(artifact=relative):
                path = DESKTOP / relative
                self.assertTrue(path.resolve().is_relative_to(DESKTOP))
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
        expected_packages = receipt['source_packages_sha256']
        self.assertEqual(len(expected_packages), 13)
        self.assertEqual(sum(len(v) for v in expected_packages.values()), 84)
        for name, expected in expected_packages.items():
            self.assertEqual(package_files(name), expected)
        for stage in ('02-all-installed', '07-restored-all'):
            for location, packages in read(DESKTOP / (stage + '.json')).items():
                self.assertEqual(set(packages), set(expected_packages))
                for name, package in packages.items():
                    with self.subTest(stage=stage, location=location, skill=name):
                        self.assertEqual(package['files'], expected_packages[name])

    def test_selective_disable_uninstall_and_selected_install_preserve_other_packages(self):
        expected = read(DESKTOP / 'receipt.json')['source_packages_sha256']
        removed = 'entity-relationship-modeling'
        disabled = read(DESKTOP / '03-codex-one-disabled.json')
        for location, packages in disabled.items():
            self.assertEqual(set(packages), set(expected) - {removed}
                             if location == 'codex' else set(expected))
        uninstalled = read(DESKTOP / '05-one-uninstalled.json')
        for packages in uninstalled.values():
            self.assertEqual(set(packages), set(expected) - {removed})
            for name, package in packages.items():
                self.assertEqual(package['files'], expected[name])
        for packages in read(DESKTOP / '10-selected-installed.json').values():
            self.assertEqual(set(packages), {'fibo-ontology', 'credit-risk-knowledge'})
            for name, package in packages.items():
                self.assertEqual(package['files'], expected[name])
        for stage in ('09-all-uninstalled', '11-final-clean'):
            self.assertTrue(all(not p for p in read(DESKTOP / (stage + '.json')).values()))

    def test_native_codex_discovered_actual_desktop_sync_entries(self):
        discovered = read(DESKTOP / '06-codex-discovery.json')['data'][0]
        self.assertEqual(discovered['errors'], [])
        packages = read(DESKTOP / '07-restored-all.json')['ssot']
        self.assertEqual({s['name'] for s in discovered['skills']}, set(packages))
        for skill in discovered['skills']:
            self.assertTrue(skill['enabled'])
            self.assertEqual(skill['path'], packages[skill['name']]['target'] + '/SKILL.md')


if __name__ == '__main__':
    unittest.main()
