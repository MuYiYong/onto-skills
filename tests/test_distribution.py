"""Offline package closure and selective/multiple copy-layout checks."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from scripts.validate import metadata, validate_skill, validate_model

ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def test_each_skill_is_self_contained_in_an_unrelated_directory(self):
        for entry in (ROOT / 'skills').glob('*/*/SKILL.md'):
            with self.subTest(skill=entry.parent.name), tempfile.TemporaryDirectory() as td:
                installed = Path(td) / entry.parent.name
                shutil.copytree(entry.parent, installed)
                self.assertEqual(validate_skill(installed), [])
                self.assertTrue((installed / 'LICENSE').is_file())
                self.assertTrue(list((installed / 'references').glob('*')))
                self.assertTrue(list((installed / 'examples').glob('*')))
                for model in installed.rglob('*graph-model.json'):
                    self.assertEqual(validate_model(json.loads(model.read_text())), [])

    def test_selective_and_multiple_install_layout_names_do_not_collide(self):
        entries = sorted((ROOT / 'skills').glob('*/*/SKILL.md'))
        with tempfile.TemporaryDirectory() as td:
            dest = Path(td) / '.agents/skills'
            dest.mkdir(parents=True)
            selected = [e for e in entries if e.parent.name in {'fibo-ontology', 'property-graph-mapping'}]
            for entry in selected:
                shutil.copytree(entry.parent, dest / entry.parent.name)
            self.assertEqual(len(list(dest.glob('*/SKILL.md'))), 2)
            for entry in entries:
                if not (dest / entry.parent.name).exists():
                    shutil.copytree(entry.parent, dest / entry.parent.name)
            names = [metadata(p)[0]['name'] for p in dest.glob('*/SKILL.md')]
            self.assertEqual(len(names), len(entries))
            self.assertEqual(len(names), len(set(names)))

    def test_standard_draft_does_not_pass_ready_gate(self):
        model = json.loads((ROOT / 'examples/finance/top-down-graph-model.json').read_text())
        self.assertEqual(validate_model(model), [])
        self.assertTrue(validate_model(model, ready=True))

    def test_fraud_example_is_a_distinct_evidence_network(self):
        model = json.loads((ROOT / 'examples/finance/fraud-graph-model.json').read_text())
        names = {n['name'] for n in model['node_types']}
        self.assertIn('EvidenceRecord', names)
        self.assertIn('InvestigationHypothesis', names)
        self.assertIn('Transaction', names)
        self.assertEqual(validate_model(model, ready=True), [])


if __name__ == '__main__':
    unittest.main()
