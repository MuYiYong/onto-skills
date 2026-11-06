"""Offline integrity of dated native observations; never invokes a host/model."""
import hashlib
import json
from pathlib import Path
import unittest

import jsonschema
from evidence_sources import packages, package_digest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'tests/compatibility/standards-first-native'


def read(relative):
    return json.loads((EVIDENCE / relative).read_text())


class StandardsFirstNativeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packages = packages(EVIDENCE)
        cls.files = {name: {p: hashlib.sha256(data).hexdigest() for p, data in files.items()}
                     for name, files in cls.packages.items()}

    def test_frozen_sources_and_published_evidence_are_intact(self):
        self.assertEqual(self.files, read('source-files.json'))
        self.assertEqual(len(self.files), 27)
        self.assertEqual(sum(map(len, self.files.values())), 227)
        for relative, digest in read('receipt.json')['artifacts_sha256'].items():
            with self.subTest(artifact=relative):
                self.assertEqual(hashlib.sha256((EVIDENCE / relative).read_bytes()).hexdigest(), digest)

    def test_actual_discovery_binds_both_layouts_to_frozen_sources(self):
        evidence = read('discovery.json')
        self.assertEqual(evidence['codex_version'], 'codex-cli 0.166.0')
        rows = [r for r in evidence['results'] if r['phase'] == 'multiple']
        self.assertEqual({r['scope'] for r in rows}, {'project', 'legacy-codex-home'})
        for row in rows:
            self.assertEqual(row['resource_files_read'], 227)
            self.assertEqual(set(row['skill_names']), set(self.files))
            self.assertEqual(row['model_invocation'], 'not-run')
            self.assertEqual(row['package_sha256'], {n: package_digest(v) for n, v in self.packages.items()})

    def test_desktop_install_toggle_restore_and_terminal_uninstall(self):
        for relative in ('desktop/release-installed.json', 'desktop/release-restored.json'):
            snapshot = read(relative)
            for scope in ('ssot', 'codex'):
                self.assertEqual(set(snapshot[scope]), set(self.files))
                for name, files in self.files.items():
                    self.assertEqual(snapshot[scope][name]['files'], files)
        disabled = read('desktop/release-disabled.json')
        self.assertEqual(set(disabled['ssot']), set(self.files))
        self.assertEqual(set(disabled['codex']), set(self.files) - {'software-vulnerability-impact'})
        self.assertEqual(read('desktop/release-synced-discovery.json')['source_packages_sha256'], self.files)
        self.assertEqual(read('desktop/release-clean.json'), {'ssot': {}, 'codex': {}})

    def test_agent_results_and_actual_reads_are_source_bound(self):
        review = read('agent-application/review.json')
        self.assertEqual(review['final_skill_count'], 21)
        self.assertEqual(len({r['skill'] for r in review['cases']}), 21)
        for case in review['cases']:
            name = case['skill']
            with self.subTest(skill=name):
                self.assertEqual(case['source_sha256'], self.files[name])
                result = read(f'agent-application/{name}/result.json')
                schema = read(f'agent-application/{name}/schema.json')
                jsonschema.validate(result, schema)
                self.assertEqual(result['skill_used'], name)
                self.assertIn('SKILL.md', case['consumed_package_files_sha256'])
                for relative, digest in case['consumed_package_files_sha256'].items():
                    self.assertFalse(relative.startswith(('examples/', 'tests/')))
                    self.assertEqual(digest, self.files[name][relative])
                if case['expected_answer'] is not None:
                    self.assertEqual(result['answer'], case['expected_answer'])
                else:
                    self.assertTrue(result['answer']['concepts'])
                    self.assertTrue(result['answer']['decisions'])
                self.assertTrue(case['semantic_review'])

    def test_failed_cli_is_retained_as_failed_not_counted_as_application(self):
        rows = read('cli-failures/receipt.json')['attempts']
        self.assertEqual(len(rows), 5)
        for row in rows:
            self.assertEqual(row['exit_code'], 1)
            self.assertEqual(row['http_status'], 429)
            self.assertEqual(row['terminal_event'], 'turn.failed')
            self.assertFalse(row['model_output_generated'])
            directory = EVIDENCE / 'cli-failures' / row['attempt']
            events = [json.loads(line) for line in (directory / 'events.jsonl').read_text().splitlines()]
            self.assertEqual(events[-1]['type'], 'turn.failed')


if __name__ == '__main__':
    unittest.main()
