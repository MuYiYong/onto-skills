"""Development-only reference calculations for original projections, not standards runtimes."""
import copy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def instant(value):
    stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if stamp.tzinfo is None:
        raise ValueError('timezone required')
    return stamp.astimezone(timezone.utc)


def number(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError('finite numeric value required')
    try:
        result = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError('finite numeric value required') from error
    if not result.is_finite():
        raise ValueError('finite numeric value required')
    return result


def canonical(record, omit=()):
    return json.dumps({k: v for k, v in record.items() if k not in omit},
                      sort_keys=True, ensure_ascii=False)


def grouped(rows, fields):
    groups = {}
    for row in rows:
        # Preserve identifier value types in grouping (e.g. string "1" vs integer 1).
        key = tuple((type(row[f]).__name__, row[f]) for f in fields)
        groups.setdefault(key, {})[canonical(row)] = row
    return {key: list(values.values()) for key, values in groups.items()}


def typed_key(*values):
    return tuple((type(v).__name__, v) for v in values)


def evaluate_bim(data):
    before, after = data['before'], data['after']
    result = dict(changes=[], unchanged=[], unresolved=[], decision='candidate_only')
    if before['lineage'] != after['lineage']:
        result['unresolved'].append(dict(global_id=None, reason='different_lineage'))
        return result
    indexes = [grouped(s['objects'], ['global_id']) for s in (before, after)]
    types = [grouped(s['types'], ['global_id']) for s in (before, after)]

    def value(obj, snapshot, type_index):
        def selected(properties):
            return [p for p in properties if p['pset'] == data['property']['pset']
                    and p['name'] == data['property']['name']]
        properties = selected(obj['properties'])
        if not properties:
            matches = type_index.get(typed_key(obj['type_id']), [])
            if len(matches) != 1:
                return None
            properties = selected(matches[0]['properties'])
        if len(properties) != 1:
            return None
        p = properties[0]
        if p['measure_type'] != 'IfcLengthMeasure':
            return None
        unit = p['unit'] if p['unit'] is not None else snapshot['project_length_unit']
        factor = {'m': Decimal('1'), 'cm': Decimal('.01'), 'mm': Decimal('.001')}.get(unit)
        if factor is None:
            return None
        try:
            return number(p['value']) * factor
        except ValueError:
            return None

    for key in sorted(set(indexes[0]) | set(indexes[1])):
        left, right = (index.get(key, []) for index in indexes)
        gid, reason = key[0][1], None
        if len(left) > 1 or len(right) > 1:
            reason = 'conflicting_identity'
        elif not left or not right:
            reason = 'missing_snapshot_object'
        elif any(len(set(o['primary_spaces'])) != 1 for o in (left[0], right[0])):
            reason = 'invalid_containment'
        if reason:
            result['unresolved'].append(dict(global_id=gid, reason=reason))
            continue
        values = [value(obj, snap, idx) for obj, snap, idx in
                  zip((left[0], right[0]), (before, after), types)]
        if any(v is None for v in values):
            result['unresolved'].append(dict(global_id=gid, reason='unknown_property'))
        elif values[0] == values[1]:
            result['unchanged'].append(gid)
        else:
            spaces = sorted({s for o in (left[0], right[0])
                             for s in o['primary_spaces'] + o['referenced_spaces']})
            result['changes'].append(dict(global_id=gid, before_m=format(values[0].normalize(), 'f'),
                                          after_m=format(values[1].normalize(), 'f'), spaces=spaces))
    return result


def evaluate_environment(data):
    policy, known = data['policy'], instant(data['known_as_of'])
    start, end = instant(policy['window_start']), instant(policy['window_end'])
    if start >= end:
        raise ValueError('ordered window required')
    upper = number(policy['upper'])
    streams = grouped([s for s in data['datastreams'] if instant(s['observed_at']) <= known],
                      ['service', 'id'])
    groups = grouped(data['observations'], ['service', 'id'])
    assessments = []
    for key, receipts in sorted(groups.items()):
        # Visibility precedes content conflict checks; future evidence cannot alter the past.
        visible = [o for o in receipts if instant(o['observed_at']) <= known]
        contents = {canonical(o, ('observed_at',)): o for o in visible}
        state, reason = 'unknown', 'not_known_at_cutoff'
        if len(contents) > 1:
            reason = 'conflicting_identity'
        elif contents:
            o = next(iter(contents.values()))
            candidates = streams.get(typed_key(o['service'], o['stream_id']), [])
            if o['service'] != policy['service'] or o['foi_id'] != policy['foi_id']:
                state, reason = 'out_of_scope', 'feature_or_service'
            elif len(candidates) != 1:
                reason = 'missing_datastream' if not candidates else 'conflicting_datastream'
            else:
                stream = candidates[0]
                if (stream['observed_property'] != policy['observed_property']
                        or stream['unit_definition'] != policy['unit_definition']
                        or stream['observation_type'] !=
                        'http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement'):
                    reason = 'incompatible_measurement'
                elif '/' in o['phenomenonTime']:
                    reason = 'interval_requires_policy'
                elif not start <= instant(o['phenomenonTime']) < end:
                    state, reason = 'out_of_scope', 'time_window'
                elif instant(o['phenomenonTime']) > known:
                    reason = 'future_phenomenon'
                elif o.get('validTime') is not None:
                    reason = 'valid_time_requires_policy'
                elif o['resultTime'] is not None and instant(o['resultTime']) > known:
                    reason = 'future_result'
                elif o['quality_decision'] != 'accepted':
                    reason = 'quality_not_accepted'
                else:
                    try:
                        value = number(o['result'])
                        state = 'exceedance_candidate' if value > upper else 'within_local_threshold'
                        reason = 'local_policy'
                    except ValueError:
                        reason = 'invalid_result'
        assessments.append(dict(observation=[key[0][1], key[1][1]], status=state, reason=reason))
    return dict(assessments=assessments, regulatory_conclusion=None)


def evaluate_education(data):
    policy = data['policy']
    at, known = instant(data['as_of']), instant(data['known_as_of'])
    max_age = policy['status_max_age_seconds']
    if type(max_age) is not int or max_age < 0:
        raise ValueError('nonnegative integer freshness required')
    assessments = []
    for key, receipts in sorted(grouped(data['credentials'], ['issuer_id', 'id']).items()):
        visible = [c for c in receipts if instant(c['observed_at']) <= known]
        contents = {canonical(c, ('observed_at',)): c for c in visible}
        state, reason = 'unknown', 'credential_not_known'
        if len(contents) > 1:
            reason = 'conflicting_identity'
        elif contents:
            content, credential = next(iter(contents.items()))
            valid_from = instant(credential['validFrom'])
            valid_until = instant(credential['validUntil']) if credential['validUntil'] else None
            if valid_until is not None and valid_from > valid_until:
                raise ValueError('ordered validity required')
            if at < valid_from or (valid_until is not None and at >= valid_until):
                state, reason = 'not_eligible', 'outside_validity'
            elif credential['subject_id'] != policy['subject_id']:
                state, reason = 'not_eligible', 'subject_mismatch'
            elif credential['issuer_id'] not in policy['trusted_issuers']:
                reason = 'issuer_not_trusted'
            else:
                reports = [r for r in data['reports']
                           if r['credential_id'] == credential['id']
                           and r['issuer_id'] == credential['issuer_id']
                           and r['subject_id'] == credential['subject_id']
                           and credential['credential_status_id'] is not None
                           and r['status_reference'] == credential['credential_status_id']
                           and canonical(r['credential_content']) == content
                           and instant(r['observed_at']) <= known]
                unique = {canonical(r, ('observed_at',)): r for r in reports}
                reason = 'missing_bound_report'
                if len(unique) > 1:
                    reason = 'conflicting_reports'
                elif unique:
                    report = next(iter(unique.values()))
                    if report['simulated'] is not True:
                        raise ValueError('oracle handles simulated reports only')
                    checked = instant(report['checked_at'])
                    if checked > min(at, known) or (at - checked).total_seconds() > max_age:
                        reason = 'stale_or_future_report'
                    elif report['schema'] == 'fail' or report['proof'] == 'fail':
                        state, reason = 'not_eligible', 'reported_check_failure'
                    elif report['schema'] != 'pass' or report['proof'] != 'pass':
                        reason = 'checks_unresolved'
                    elif report['status'] == 'revoked':
                        state, reason = 'not_eligible', 'reported_revoked'
                    elif report['status'] != 'active':
                        reason = 'status_unresolved'
                    else:
                        state, reason = 'candidate_for_review', 'simulated_checks_only'
        assessments.append(dict(credential=[key[0][1], key[1][1]], status=state, reason=reason))
    return dict(assessments=assessments, credential_verified=False, competence_confirmed=None)


EVALUATORS = {'built-environment': evaluate_bim, 'environmental-monitoring': evaluate_environment,
              'education': evaluate_education}


class StandardsExpansionExamplesTests(unittest.TestCase):
    def data(self, sector):
        return json.loads((ROOT / 'examples' / sector / 'input.json').read_text())

    def test_all_manual_positive_and_adverse_cases(self):
        for sector, evaluate in EVALUATORS.items():
            cases = json.loads((ROOT / 'examples' / sector / 'acceptance.json').read_text())['cases']
            for case in cases:
                with self.subTest(sector=sector, case=case['id']):
                    self.assertEqual(evaluate(case['input']), case['expected'])
            self.assertEqual(evaluate(self.data(sector)), cases[0]['expected'])

    def test_bim_type_changes_do_not_overwrite_occurrence_and_wrong_measure_is_unknown(self):
        data = self.data('built-environment')
        data['after']['types'][0]['properties'][0]['measure_type'] = 'IfcAreaMeasure'
        result = evaluate_bim(data)
        self.assertEqual(len(result['unchanged']), 1)
        self.assertEqual(result['unresolved'][0]['reason'], 'unknown_property')
        self.assertEqual(result['changes'], [])

    def test_bim_spatial_candidates_include_before_and_after_not_only_current(self):
        data = self.data('built-environment')
        data['after']['objects'][0]['primary_spaces'] = ['new-space']
        spaces = evaluate_bim(data)['changes'][0]['spaces']
        self.assertIn('new-space', spaces)
        self.assertIn(data['before']['objects'][0]['primary_spaces'][0], spaces)

    def test_invalid_numeric_values_never_become_valid_measurements(self):
        for value in (True, False, 'NaN', 'Infinity', '-Infinity', {}, [], ''):
            with self.subTest(value=value):
                data = self.data('environmental-monitoring')
                data['observations'][0]['result'] = value
                self.assertEqual(evaluate_environment(data)['assessments'][0]['reason'], 'invalid_result')

    def test_visibility_precedes_conflicts_and_replay_is_order_independent(self):
        for sector, evaluate, field in [('environmental-monitoring', evaluate_environment, 'observations'),
                                        ('education', evaluate_education, 'credentials')]:
            data = self.data(sector)
            extra = copy.deepcopy(data[field][0])
            extra['observed_at'] = '2026-11-08T00:00:00Z'
            extra['untrusted_future_change'] = True
            data[field].insert(0, extra)
            self.assertEqual(evaluate(data), evaluate(self.data(sector)))

    def test_environment_valid_time_needs_separate_use_policy(self):
        data = self.data('environmental-monitoring')
        data['observations'][0]['validTime'] = '2026-11-06T09:00:00Z/2026-11-06T10:00:00Z'
        self.assertEqual(evaluate_environment(data)['assessments'][0]['reason'], 'valid_time_requires_policy')

    def test_environment_id_type_and_conflicting_stream_are_not_silently_merged(self):
        data = self.data('environmental-monitoring')
        data['datastreams'][0]['id'] = 1
        self.assertEqual(evaluate_environment(data)['assessments'][0]['reason'], 'missing_datastream')
        data = self.data('environmental-monitoring')
        data['datastreams'].append(dict(data['datastreams'][0], unit_definition='another-unit'))
        self.assertEqual(evaluate_environment(data)['assessments'][0]['reason'], 'conflicting_datastream')

    def test_later_stream_metadata_cannot_answer_an_earlier_question(self):
        data = self.data('environmental-monitoring')
        data['datastreams'][0]['observed_at'] = '2026-11-07T00:00:00Z'
        self.assertEqual(evaluate_environment(data)['assessments'][0]['reason'], 'missing_datastream')

    def test_education_conflicting_reports_and_unknown_proof_stay_unknown(self):
        data = self.data('education')
        data['reports'].append(dict(data['reports'][0], status='revoked', report_id='report-2'))
        self.assertEqual(evaluate_education(data)['assessments'][0]['reason'], 'conflicting_reports')
        data = self.data('education')
        data['reports'][0]['proof'] = 'unknown'
        self.assertEqual(evaluate_education(data)['assessments'][0]['reason'], 'checks_unresolved')

    def test_synthetic_report_cannot_be_laundered_into_real_verification(self):
        data = self.data('education')
        data['reports'][0]['simulated'] = False
        with self.assertRaisesRegex(ValueError, 'simulated'):
            evaluate_education(data)

    def test_unzoned_times_and_reversed_windows_fail_explicitly(self):
        for sector, evaluate in [('education', evaluate_education),
                                 ('environmental-monitoring', evaluate_environment)]:
            data = self.data(sector)
            data['known_as_of'] = '2026-11-06T12:00:00'
            with self.assertRaisesRegex(ValueError, 'timezone'):
                evaluate(data)
        data = self.data('environmental-monitoring')
        data['policy']['window_end'] = data['policy']['window_start']
        with self.assertRaisesRegex(ValueError, 'ordered window'):
            evaluate_environment(data)


if __name__ == '__main__':
    unittest.main()
