"""Offline integrity checks for the dated native receipt, not a new database run."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'tests/compatibility/native-yueshu'


class NativeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads((EVIDENCE / 'receipt.json').read_text())
        cls.records = json.loads((EVIDENCE / 'native-records.json').read_text())
        cls.by_label = {r['label']: r for r in cls.records}

    def test_native_receipt_is_bound_to_current_sources_and_artifacts(self):
        self.assertEqual(self.receipt['status'], 'passed')
        self.assertEqual(self.receipt['check_count'], len(self.receipt['checks']))
        self.assertTrue(all(c['passed'] for c in self.receipt['checks']))
        for relative, expected in self.receipt['file_sha256'].items():
            with self.subTest(path=relative):
                path = ROOT / relative
                self.assertTrue(path.resolve().is_relative_to(ROOT))
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
        query = (ROOT / 'examples/finance/generated/multi-lending.gql').read_text()
        for key in self.by_label:
            if key.startswith('final_lending_'):
                self.assertEqual(self.by_label[key]['query'], query)

    def test_native_rows_match_positive_and_negative_business_cases(self):
        expected = {
            'final_lending_asof_feb01': [{'borrower_id': 'B1', 'lender_count': 2}],
            'final_lending_distinct_lenders': [{'borrower_id': 'B1', 'lender_count': 2},
                                               {'borrower_id': 'B2', 'lender_count': 1}],
            'final_lending_before_overlap': [],
            'final_lending_inclusive_start': [{'borrower_id': 'B1', 'lender_count': 2}],
            'final_lending_exclusive_end': [],
            'historical_shared_phone': [{'first_borrower': 'B1', 'second_borrower': 'B2',
                                         'phone_token': 'phone-token-shared'}],
            'expired_shared_phone': [],
            'multiple_disbursements_same_loan': [{'loan_id': 'C', 'disbursements': 2}],
            'fraud_temporal_chain': [{'first_tx': 'T1', 'next_tx': 'T2', 'via_account': 'FA2'}],
        }
        for label, rows in expected.items():
            with self.subTest(case=label):
                actual = self.by_label[label]
                self.assertEqual(actual['server_status_code'], '00000')
                key = lambda r: json.dumps(r, sort_keys=True)
                self.assertEqual(sorted(actual['rows'], key=key), sorted(rows, key=key))
        self.assertEqual(self.by_label['lending_count_after_rejections']['rows'], [{'nodes': 19}])

    def test_expected_server_errors_and_owned_cleanup_are_explicit(self):
        expected_errors = {'original_query_failure': '42001',
                           'diagnostic_statement_terminator': '42001',
                           'reject_duplicate_primary_key': 'NR205',
                           'reject_null_primary_key': 'ND008'}
        for row in self.records:
            if row['label'] in expected_errors:
                self.assertEqual(row['status'], 'error')
                self.assertEqual(row['server_status_code'], expected_errors[row['label']])
            else:
                self.assertEqual(row['status'], 'success')
                self.assertEqual(row['server_status_code'], '00000')
        owned = json.loads((EVIDENCE / 'resources.json').read_text())
        drops = [r for r in self.records if r['label'].startswith('drop_owned_')]
        self.assertEqual(len(drops), 4)
        expected_drops = set()
        for model in owned['resources'].values():
            for kind, target in model.items():
                command = 'DROP GRAPH TYPE' if kind == 'type' else 'DROP GRAPH'
                expected_drops.add(command + ' ' + target.replace('/default_schema/', '/default_schema/`') + '`')
        self.assertEqual({row['query'] for row in drops}, expected_drops)
        for label in ('after_graph_catalog', 'after_type_catalog'):
            self.assertEqual(self.by_label[label]['rows'], [])
            self.assertEqual(self.by_label[label]['server_status_code'], '00000')
        self.assertEqual(self.receipt['cleanup']['remaining_owned_graphs'], 0)
        self.assertEqual(self.receipt['cleanup']['remaining_owned_graph_types'], 0)

    def test_native_schema_readback_preserves_model_properties_keys_and_endpoints(self):
        physical = {'identifier': 'STRING', 'string': 'STRING', 'decimal': 'DECIMAL(18,2)',
                    'datetime': 'ZONEDDATETIME'}
        for kind, filename in [('lending', 'graph-model.json'), ('fraud', 'fraud-graph-model.json')]:
            model = json.loads((ROOT / 'examples/finance' / filename).read_text())
            ddl = self.by_label['readback_' + kind + '_type']['rows'][0]['create_graph_type_statement']
            nodes = {n: (label, fields) for n, label, fields in re.findall(
                r'NODE TYPE `([^`]+)` \(LABEL `([^`]+)`\{(.*?)\}\)', ddl, re.S)}
            edges = {n: (src, label, fields, dst) for n, src, label, fields, dst in re.findall(
                r'EDGE TYPE `([^`]+)` \(`([^`]+)`\)-\[LABEL `([^`]+)`\{(.*?)\}\]->\(`([^`]+)`\)', ddl, re.S)}
            self.assertEqual(set(nodes), {n['name'] for n in model['node_types']})
            self.assertEqual(set(edges), {e['name'] for e in model['edge_types']})
            for group, definitions, marker in [('node_types', nodes, 'PRIMARY KEY'),
                                                ('edge_types', edges, 'MULTIEDGE KEY')]:
                for item in model[group]:
                    with self.subTest(model=kind, type=item['name']):
                        parts = definitions[item['name']]
                        if group == 'node_types':
                            label, fields = parts
                        else:
                            src, label, fields, dst = parts
                            self.assertEqual((src, dst), (item['from'], item['to']))
                        self.assertEqual(label, item['name'])
                        key = re.search(marker + r'\s*\((.*?)\)', fields).group(1)
                        self.assertEqual(re.findall(r'`([^`]+)`', key), item['primary_key'])
                        for prop in item['properties']:
                            declaration = re.search(r'`' + re.escape(prop['name']) +
                                r'`\s+(.+?)(?=,\s*`|,\s*(?:PRIMARY KEY|MULTIEDGE KEY)|$)', fields, re.S).group(1)
                            self.assertTrue(re.sub(r'\s+', '', declaration).startswith(physical[prop['logical_type']]))
                            self.assertEqual('NOT NULL' in declaration, not prop['nullable'])


if __name__ == '__main__':
    unittest.main()
