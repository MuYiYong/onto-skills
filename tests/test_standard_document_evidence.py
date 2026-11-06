"""Integrity of actual standards-tool receipts; this never reruns external tools."""
import hashlib
import json
import copy
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'tests/standards/cybersecurity'


class StandardDocumentEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads((EVIDENCE / 'receipt.json').read_text())

    def test_receipt_binds_every_original_native_document_and_raw_report(self):
        for relative, expected in self.receipt['source_sha256'].items():
            with self.subTest(source=relative):
                self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), expected)
        for relative, expected in self.receipt['artifact_sha256'].items():
            self.assertEqual(hashlib.sha256((EVIDENCE / relative).read_bytes()).hexdigest(), expected)

    def test_actual_spdx_parser_rejects_duplicate_identity(self):
        results = self.receipt['spdx']['results']
        self.assertEqual(len(results), 3)
        self.assertTrue(all(row['passed'] for row in results))
        self.assertEqual(sum(row['exit_code'] == 0 for row in results), 2)
        rejected, = [r for r in results if not r['expected_valid']]
        self.assertEqual(rejected['exit_code'], 1)

    def test_complete_csaf_test_dispatch_rejects_semantic_counterexamples(self):
        results = self.receipt['csaf']['results']
        self.assertEqual(len(results), 4)
        for row in results:
            with self.subTest(source=row['filename']):
                report = json.loads((EVIDENCE / row['report']).read_text())
                self.assertEqual(len(report['tests']), 75)
                names = {t['name'] for t in report['tests']}
                self.assertIn('mandatoryTest_6_1_8', names)
                self.assertIn('mandatoryTest_6_1_27_9', names)
                self.assertIn('mandatoryTest_6_1_27_10', names)
                self.assertTrue(any(n.startswith('optionalTest_') for n in names))
                self.assertTrue(any(n.startswith('informativeTest_') for n in names))
                self.assertEqual(report['isValid'], not row['filename'].startswith('negative-'))
                if row['filename'] == 'negative-contradictory-status.csaf.json':
                    self.assertTrue(next(t for t in report['tests']
                                         if t['name'] == 'mandatoryTest_6_1_6')['errors'])
                if row['filename'] == 'negative-missing-impact.csaf.json':
                    self.assertTrue(next(t for t in report['tests']
                                         if t['name'] == 'mandatoryTest_6_1_27_9')['errors'])

    def test_cvss_requires_complete_vector_and_computed_score_not_schema_only(self):
        positive = json.loads((ROOT / 'examples/cybersecurity/standards-native/cvss-4.0.json').read_text())
        result = self.receipt['cvss']
        self.assertEqual(positive['vectorString'], result['vector'])
        self.assertEqual(positive['baseScore'], result['score'])
        self.assertEqual(result['score'], result['independent_implementation']['score'])
        self.assertEqual(result['commit'], 'c5b0d409ae9f57c44264c6ce5f27d89298e1d32a')
        negative = json.loads((ROOT / 'examples/cybersecurity/standards-native/negative/negative-inconsistent-cvss.json').read_text())
        self.assertEqual(positive['vectorString'], negative['vectorString'])
        self.assertNotEqual(negative['baseScore'], result['score'])


class EpcisCorrectionEvidenceTests(unittest.TestCase):
    def test_standard_correction_replay_preserves_original_content(self):
        directory = ROOT / 'tests/standards/epcis'
        receipt = json.loads((directory / 'receipt.json').read_text())
        for name, digest in receipt['source_sha256'].items():
            self.assertEqual(hashlib.sha256((directory / name).read_bytes()).hexdigest(), digest)
        def events(name):
            return json.loads((directory / name).read_text())['epcisBody']['eventList']
        original, = events('original.jsonld')
        declaration, corrective = events('declaration-and-corrective.jsonld')
        negative = events('negative-changed-original.jsonld')[0]
        def original_content(event):
            result = copy.deepcopy(event)
            result.pop('recordTime', None)
            result.pop('errorDeclaration', None)
            return result
        self.assertEqual(original_content(original), original_content(declaration))
        self.assertNotEqual(original_content(original), original_content(negative))
        self.assertEqual(declaration['eventID'], original['eventID'])
        self.assertNotEqual(corrective['eventID'], original['eventID'])
        self.assertEqual(declaration['errorDeclaration']['correctiveEventIDs'], [corrective['eventID']])
        self.assertTrue(all(r['publisher_schema_valid'] for r in receipt['schema_results']))


if __name__ == '__main__':
    unittest.main()
