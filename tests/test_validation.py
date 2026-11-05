"""Negative cases for asset isolation and semantic model handoff."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.validate import validate_skill, validate_model, validate_repository, validate_knowledge

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


if __name__ == '__main__':
    unittest.main()
