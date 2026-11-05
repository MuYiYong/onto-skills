"""Coverage of the requested additive scope and public independent distribution paths."""
import json
from pathlib import Path
import re
import unittest

from scripts.validate import knowledge_catalog, validate_knowledge, validate_model, validate_skill

ROOT = Path(__file__).resolve().parents[1]
INDUSTRIES = {
    'electric-power': ('electric-power-domain-knowledge', 'power-outage-impact-analysis'),
    'manufacturing': ('manufacturing-domain-knowledge', 'manufacturing-quality-traceability'),
    'logistics': ('logistics-domain-knowledge', 'shipment-exception-analysis'),
    'healthcare': ('healthcare-domain-knowledge', 'healthcare-care-pathway-modeling'),
    'retail': ('retail-domain-knowledge', 'retail-inventory-replenishment'),
}
FINANCE = {
    'regulatory': ('financial-regulatory-reporting', 'regulatory-reporting'),
    'related-parties': ('related-party-transaction-modeling', 'related-party'),
}


class MultiIndustryAssetTests(unittest.TestCase):
    def test_every_requested_industry_has_both_real_knowledge_and_scenario(self):
        for sector, (knowledge_name, scenario) in INDUSTRIES.items():
            with self.subTest(industry=sector):
                catalogue = ROOT / 'knowledge' / sector / 'standards/sources.json'
                domain = ROOT / 'knowledge' / sector / 'concepts/domain.json'
                self.assertEqual(knowledge_catalog(domain, ROOT), catalogue)
                self.assertEqual(validate_knowledge(json.loads(domain.read_text()),
                                                    json.loads(catalogue.read_text())), [])
                for category, name in [('industries', knowledge_name), ('scenarios', scenario)]:
                    package = ROOT / 'skills' / category / name
                    self.assertEqual(validate_skill(package), [])
                    self.assertEqual((package / 'references/domain.json').read_bytes(), domain.read_bytes())
                    self.assertEqual((package / 'references/sources.json').read_bytes(), catalogue.read_bytes())
                self.assertTrue((ROOT / 'packs' / (sector + '-ontology/README.md')).is_file())

    def test_new_financial_scenarios_use_specialist_chinese_source_scopes(self):
        for branch, (name, example) in FINANCE.items():
            with self.subTest(scenario=name):
                directory = ROOT / 'knowledge/finance' / branch
                catalogue = directory / 'standards/sources.json'
                domain = directory / 'concepts/domain.json'
                self.assertEqual(knowledge_catalog(domain, ROOT), catalogue)
                sources = json.loads(catalogue.read_text())
                self.assertTrue(any(s['publisher'].find('金融监督') >= 0 for s in sources['sources']))
                self.assertEqual(validate_knowledge(json.loads(domain.read_text()), sources), [])
                package = ROOT / 'skills/scenarios' / name
                self.assertEqual(validate_skill(package), [])
                self.assertEqual((package / 'references/domain.json').read_bytes(), domain.read_bytes())

    def test_all_new_scenario_models_and_raw_cases_are_independent_exact_copies(self):
        paths = [(ROOT / 'examples' / sector, ROOT / 'skills/scenarios' / names[1])
                 for sector, names in INDUSTRIES.items()]
        paths += [(ROOT / 'examples/finance' / example, ROOT / 'skills/scenarios' / name)
                  for name, example in FINANCE.values()]
        for central, package in paths:
            with self.subTest(scenario=package.name):
                model = json.loads((central / 'graph-model.json').read_text())
                self.assertEqual(validate_model(model), [])
                self.assertEqual(model['target']['database'], 'unspecified')
                self.assertTrue(model['competency_questions'])
                for filename in ('graph-model.json', 'input.json', 'acceptance.json'):
                    self.assertEqual((central / filename).read_bytes(),
                                     (package / 'examples' / filename).read_bytes())
                cases = json.loads((central / 'acceptance.json').read_text())['cases']
                self.assertTrue(cases)
                self.assertEqual(len({c['id'] for c in cases}), len(cases))
                self.assertTrue(all(isinstance(c['expected'], dict) and c['expected'] for c in cases))

    def test_current_inventory_and_install_guide_cover_every_package(self):
        entries = list((ROOT / 'skills').glob('*/*/SKILL.md'))
        readme = (ROOT / 'README.md').read_text()
        guide = (ROOT / 'docs/installation-guide.md').read_text()
        links = re.findall(r'\]\((skills/[^)]+/SKILL\.md)\)', readme)
        paths = {str(e.relative_to(ROOT)) for e in entries}
        self.assertEqual(set(links), paths)
        for entry in entries:
            self.assertIn(str(entry.parent.relative_to(ROOT)), guide)
        self.assertEqual(len(entries), len({e.parent.name for e in entries}))

    def test_each_new_asset_copy_is_guarded_by_snapshot_mapping(self):
        snapshots = json.loads((ROOT / 'tests/content-validation/snapshots.json').read_text())
        copies = {c for s in snapshots for c in s['copies']}
        new_names = {n for names in INDUSTRIES.values() for n in names}
        new_names.update(n for n, _ in FINANCE.values())
        for entry in (ROOT / 'skills').glob('*/*/SKILL.md'):
            if entry.parent.name not in new_names:
                continue
            for filename in ('references/sources.json', 'references/domain.json', 'LICENSE'):
                self.assertIn(str((entry.parent / filename).relative_to(ROOT)), copies)
            if entry.parent.parent.name == 'scenarios':
                for filename in ('examples/graph-model.json', 'examples/input.json', 'examples/acceptance.json'):
                    self.assertIn(str((entry.parent / filename).relative_to(ROOT)), copies)


if __name__ == '__main__':
    unittest.main()
