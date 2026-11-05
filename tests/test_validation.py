"""Negative cases for asset isolation and semantic model handoff."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.validate import (validate_skill, validate_model, validate_repository,
                              validate_knowledge, knowledge_catalog)

ROOT = Path(__file__).resolve().parents[1]


class SkillIsolationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.skill = Path(self.tmp.name) / 'sample-skill'
        self.skill.mkdir()
        self.write('name: sample-skill\ndescription: Model equipment ownership when given asset records.')

    def write(self, frontmatter, body='## 输入\n资产\n## 工作流程\n核对身份\n## 输出\n模型\n'):
        (self.skill / 'SKILL.md').write_text('---\n' + frontmatter + '\n---\n' + body)

    def test_minimal_standard_metadata_is_valid(self):
        self.assertEqual(validate_skill(self.skill), [])

    def test_malformed_yaml_is_reported(self):
        self.write('name: [')
        self.assertTrue(any('YAML' in x for x in validate_skill(self.skill)))

    def test_duplicate_yaml_keys_are_rejected(self):
        self.write('name: sample-skill\nname: other\ndescription: test')
        self.assertTrue(validate_skill(self.skill))

    def test_empty_or_numeric_description_is_rejected(self):
        for value in ('""', '123', 'null'):
            with self.subTest(value=value):
                self.write('name: sample-skill\ndescription: ' + value)
                self.assertTrue(validate_skill(self.skill))

    def test_mismatched_name_is_rejected(self):
        self.write('name: other-skill\ndescription: Useful task description.')
        self.assertTrue(validate_skill(self.skill))

    def test_missing_reference_is_rejected(self):
        (self.skill / 'SKILL.md').write_text((self.skill / 'SKILL.md').read_text() + '[Guide](references/missing.md)')
        self.assertTrue(validate_skill(self.skill))

    def test_parent_absolute_and_windows_paths_are_rejected(self):
        for dest in ('../private.md', '/tmp/private.md', 'C:/private.md', '%2e%2e/private.md'):
            with self.subTest(dest=dest):
                self.write('name: sample-skill\ndescription: Test isolation.', '[source](' + dest + ')')
                self.assertTrue(validate_skill(self.skill))

    def test_external_symlink_is_rejected(self):
        (self.skill / 'references').symlink_to(Path(self.tmp.name), target_is_directory=True)
        self.assertTrue(validate_skill(self.skill))

    def test_source_package_root_symlink_is_rejected(self):
        alias = Path(self.tmp.name) / 'alias' / 'sample-skill'
        alias.parent.mkdir()
        alias.symlink_to(self.skill, target_is_directory=True)
        self.assertTrue(validate_skill(alias))

    def test_nested_reference_closure_is_checked(self):
        (self.skill / 'references').mkdir()
        (self.skill / 'references' / 'guide.md').write_text('[Leak](../../outside.md)')
        self.write('name: sample-skill\ndescription: Test isolation.', '[Guide](references/guide.md)')
        self.assertTrue(validate_skill(self.skill))

    def test_reference_definitions_and_html_paths_are_checked(self):
        for body in ('Read [guide][g].\n\n[g]: ../outside.md',
                     'Read [guide][g].\n\n[g]: /tmp/outside.md',
                     '<a href="/tmp/outside.md">guide</a>',
                     '<img src="../outside.png">'):
            with self.subTest(body=body):
                self.write('name: sample-skill\ndescription: Test isolation.', body)
                self.assertTrue(validate_skill(self.skill))

    def test_commonmark_angle_spaces_and_unquoted_html_are_checked(self):
        for body in ('[guide](<../outside file.md>)',
                     '[guide](</tmp/outside file.md>)',
                     '[guide][g]\n\n[g]: <../outside file.md>',
                     '<a href=/tmp/outside.md>guide</a>'):
            with self.subTest(body=body):
                self.write('name: sample-skill\ndescription: Test isolation.', body)
                self.assertTrue(validate_skill(self.skill))


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.model = json.loads((ROOT / 'examples/finance/graph-model.json').read_text())

    def test_complete_handoff_is_valid(self):
        self.assertEqual(validate_model(self.model), [])

    def test_missing_target_version_is_rejected(self):
        del self.model['target']['version']
        self.assertTrue(validate_model(self.model))

    def test_unknown_endpoint_is_rejected(self):
        self.model['edge_types'][0]['to'] = 'Missing'
        self.assertTrue(validate_model(self.model))

    def test_nullable_or_multivalued_identity_is_rejected(self):
        for field in ('nullable', 'multivalued'):
            m = copy.deepcopy(self.model)
            m['node_types'][0]['properties'][0][field] = True
            self.assertTrue(validate_model(m))

    def test_duplicate_names_are_rejected(self):
        self.model['node_types'].append(copy.deepcopy(self.model['node_types'][0]))
        self.assertTrue(validate_model(self.model))

    def test_unknown_primary_key_is_rejected(self):
        self.model['node_types'][0]['primary_key'] = ['missing']
        self.assertTrue(validate_model(self.model))

    def test_unknown_provenance_is_rejected(self):
        self.model['node_types'][0]['source_ids'] = ['invented-standard']
        self.assertTrue(validate_model(self.model))

    def test_unresolved_constraint_blocks_handoff(self):
        self.model['constraints'][0]['enforcement'] = 'unresolved'
        self.assertTrue(validate_model(self.model, ready=True))

    def test_invented_mapping_target_is_rejected(self):
        self.model['mappings'][0]['target'] = 'node:Missing'
        self.assertTrue(validate_model(self.model))

    def test_mapping_constraint_reference_must_exist(self):
        self.model['mappings'][0]['constraint_ids'] = ['nonexistent']
        self.assertTrue(validate_model(self.model))

    def test_temporal_fields_must_exist(self):
        edge = next(e for e in self.model['edge_types'] if e['temporal']['kind'] != 'none')
        edge['temporal']['start'] = 'missing'
        self.assertTrue(validate_model(self.model))

    def test_optional_temporal_reference_is_not_ignored(self):
        edge = next(e for e in self.model['edge_types'] if e['temporal']['kind'] == 'valid_time')
        edge['temporal']['observed_at'] = 'invented'
        self.assertTrue(validate_model(self.model))

    def test_temporal_start_cannot_be_nullable_or_multivalued(self):
        for field in ('nullable', 'multivalued'):
            model = copy.deepcopy(self.model)
            edge = next(e for e in model['edge_types'] if e['temporal']['kind'] != 'none')
            start = next(p for p in edge['properties'] if p['name'] == edge['temporal']['start'])
            start[field] = True
            self.assertTrue(validate_model(model))

    def test_same_start_and_end_field_is_rejected(self):
        edge = next(e for e in self.model['edge_types'] if e['temporal']['kind'] == 'valid_time')
        edge['temporal']['end'] = edge['temporal']['start']
        self.assertTrue(validate_model(self.model))

    def test_ready_gate_requires_explicit_target_version(self):
        self.model['target'] = {'database': 'NebulaGraph', 'version': 'unspecified'}
        self.assertEqual(validate_model(self.model), [])
        self.assertTrue(validate_model(self.model, ready=True))

    def test_entire_repository(self):
        self.assertEqual(validate_repository(ROOT), [])


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / 'knowledge/finance/standards/sources.json').read_text())
        self.asset = json.loads((ROOT / 'knowledge/finance/terminology/glossary.json').read_text())

    def test_curated_asset_is_traceable(self):
        self.assertEqual(validate_knowledge(self.asset, self.catalog), [])

    def test_nested_unknown_source_is_rejected(self):
        self.asset['terms'][0]['source_ids'] = ['untraceable']
        self.assertTrue(validate_knowledge(self.asset, self.catalog))

    def test_invalid_evidence_classification_is_rejected(self):
        self.asset['terms'][0]['classification'] = 'official-because-ai-said-so'
        self.assertTrue(validate_knowledge(self.asset, self.catalog))

    def test_source_license_and_version_are_required(self):
        for field in ('license', 'version'):
            catalog = copy.deepcopy(self.catalog)
            del catalog['sources'][0][field]
            self.assertTrue(validate_knowledge(self.asset, catalog))

    def test_bad_date_and_scalar_source_ids_are_rejected(self):
        self.asset['updated_at'] = 'not-a-date'
        self.asset['source_ids'] = 'fibo'
        self.assertTrue(validate_knowledge(self.asset, self.catalog))


class IndustryCatalogueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def create(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value))
        return target

    def test_each_industry_uses_its_own_nearest_catalogue(self):
        finance = self.create('knowledge/finance/standards/sources.json', {'sources': []})
        power = self.create('knowledge/electric-power/standards/sources.json', {'sources': []})
        nested = self.create('knowledge/finance/regulatory/standards/sources.json', {'sources': []})
        for asset, expected in [
            ('knowledge/finance/concepts/bank.json', finance),
            ('knowledge/electric-power/concepts/grid.json', power),
            ('knowledge/finance/regulatory/concepts/report.json', nested),
            ('knowledge/finance/regulatory/standards/sources.json', nested),
        ]:
            with self.subTest(asset=asset):
                path = self.create(asset, {}) if not (self.root / asset).exists() else self.root / asset
                self.assertEqual(knowledge_catalog(path, self.root), expected)

    def test_absent_industry_catalogue_does_not_fall_back_to_finance(self):
        self.create('knowledge/finance/standards/sources.json', {'sources': []})
        asset = self.create('knowledge/retail/concepts/stock.json', {})
        with self.assertRaisesRegex(ValueError, 'missing.*source catalog'):
            knowledge_catalog(asset, self.root)

    def test_escaping_catalogue_symlink_is_rejected(self):
        outside = self.create('outside.json', {'sources': []})
        asset = self.create('knowledge/retail/concepts/stock.json', {})
        link = self.root / 'knowledge/retail/standards/sources.json'
        link.parent.mkdir(parents=True)
        link.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symlink|escapes'):
            knowledge_catalog(asset, self.root)

    def test_malformed_nearest_catalogue_is_reported_instead_of_ignored(self):
        self.create('knowledge/finance/standards/sources.json', {'sources': []})
        self.create('knowledge/finance/regulatory/standards/sources.json', {'wrong': []})
        asset = self.create('knowledge/finance/regulatory/concepts/report.json', {})
        failures = validate_repository(self.root)
        self.assertTrue(any(str(asset) in e and 'source catalog' in e for e in failures), failures)


if __name__ == '__main__':
    unittest.main()
