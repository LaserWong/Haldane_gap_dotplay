"""Forecast admission, exact scalar boundaries, and evidence separation."""
from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
import json
import unittest
from unittest.mock import patch

from gapflow.forecast import forecast_seed_size


def provenance(threshold='1/1000'):
    return {
        'model_family': {
            'id': 'spin_one_heisenberg_v1',
            'settings': {'spin': '1', 'J': '1', 'normalization': 'S_dot_S'},
        },
        'geometry_family': {
            'id': 'cycle_v1',
            'settings': {'boundary': 'periodic', 'shape_rule': ['n'],
                         'size_unit': 'sites', 'bonds': 'positive_direction_multigraph'},
        },
        'temperature_protocol': {
            'id': 'grid_minimum_v1',
            'settings': {'beta_grid': ['2', '4', '8'], 'stop': 'exhaust_grid'},
        },
        'trial_rank_protocol': {
            'id': 'partial_ritz_v1',
            'settings': {'rank_rule': 'min(6,dimension-1)', 'tolerance': '1/1000000000'},
        },
        'certificate_criterion': {
            'id': 'synthetic_scalar_test_v1',
            'settings': {'defect': 'u', 'comparison': '<=', 'target': 'unique_ground'},
            'threshold': str(threshold),
        },
    }


class ForecastTests(unittest.TestCase):
    def rows(self, us=(.1, .05, .025), threshold='1/1000'):
        return [{'linear_size': 2*(i+1), 'defect_upper': u,
                 'evidence': 'floating_estimate', 'provenance': provenance(threshold)}
                for i, u in enumerate(us)]

    def assert_no_proof(self, result):
        for field in ('minimality_proved', 'uniform_gap_proved', 'prediction_is_certified',
                      'input_bound_certification_reverified'):
            self.assertFalse(result[field], field)
        self.assertIsNone(result['true_minimum_size'])
        self.assertEqual(result['model_gapless'], 'not established')
        self.assertFalse(result['sample_compatibility']['source_artifacts_reverified'])

    def assert_blocked(self, rows, status, threshold='1/1000'):
        with patch('gapflow.forecast.np.polyfit', side_effect=AssertionError('fit reached')):
            result = forecast_seed_size(rows, threshold)
        self.assertEqual(result['status'], status)
        self.assertIsNone(result['prediction'])
        self.assertIsNone(result['smallest_tested_sufficient_size'])
        self.assert_no_proof(result)
        return result

    def test_no_minimum_claim(self):
        result = forecast_seed_size(self.rows(), .001)
        self.assertEqual(result['status'], 'HEURISTIC_NEXT_SEED')
        self.assertEqual(result['sample_compatibility']['status'], 'verified')
        self.assertEqual(result['sample_compatibility']['scope'], 'declared_metadata_only')
        self.assertEqual(result['prediction']['candidate_even_linear_size'], 16)
        self.assert_no_proof(result)

    def test_failures_are_not_no_go(self):
        result = forecast_seed_size(self.rows([.01, .02, .03]), .001)
        self.assertEqual(result['status'], 'NO_IMPROVING_TREND')
        self.assert_no_proof(result)

    def test_certified_scalar_still_needs_theorem(self):
        rows = self.rows([.1, .01], '.02')
        rows[-1]['evidence'] = 'certified_bound'
        result = forecast_seed_size(rows, .02)
        self.assertEqual(result['status'], 'TESTED_SUFFICIENT_SCALAR_SEED')
        self.assertEqual(result['smallest_tested_sufficient_size'], 4)
        self.assertIsNone(result['prediction'])
        self.assert_no_proof(result)

    def test_decimal_threshold_no_rounding(self):
        rows = self.rows([Decimal('0.100000000000000000000001')], '.1')
        rows[0]['evidence'] = 'certified_bound'
        result = forecast_seed_size(rows, Decimal('0.1'))
        self.assertIsNone(result['smallest_tested_sufficient_size'])
        self.assertFalse(result['samples'][0]['defect_at_or_below_threshold'])
        self.assertEqual(result['status'], 'INSUFFICIENT_PILOT_DATA')

    def test_exact_equality_and_just_below_threshold(self):
        for bound in (Fraction(1, 10), Decimal('0.099999999999999999999999')):
            with self.subTest(bound=bound):
                rows = self.rows([bound], '.1')
                rows[0]['evidence'] = 'certified_bound'
                result = forecast_seed_size(rows, Decimal('.1'))
                self.assertEqual(result['smallest_tested_sufficient_size'], 2)
                self.assertTrue(result['samples'][0]['defect_at_or_below_threshold'])
                self.assert_no_proof(result)

    def test_low_data(self):
        result = forecast_seed_size(self.rows([.1, .05]), .001)
        self.assertEqual(result['status'], 'INSUFFICIENT_PILOT_DATA')

    def test_budget(self):
        result = forecast_seed_size(self.rows(), .001, max_size=8)
        self.assertEqual(result['status'], 'FORECAST_OUTSIDE_SIZE_BUDGET')
        self.assert_no_proof(result)

    def test_each_definition_mismatch_blocks(self):
        for field in provenance():
            with self.subTest(field=field):
                rows = self.rows()
                rows[1]['provenance'][field]['id'] += '_different'
                result = self.assert_blocked(rows, 'INCOMPATIBLE_SAMPLES')
                self.assertEqual(result['sample_compatibility']['status'], 'incompatible')
                self.assertIn(field+'.id', [x['field'] for x in
                                           result['sample_compatibility']['conflicts']])

    def test_fixed_parameters_and_protocol_settings_must_match(self):
        changes = [
            ('model_family', 'J', '2'),
            ('model_family', 'normalization', 'Pauli'),
            ('geometry_family', 'boundary', 'open'),
            ('geometry_family', 'shape_rule', ['n', '2*n']),
            ('geometry_family', 'size_unit', 'cells'),
            ('geometry_family', 'bonds', 'simple_graph'),
            ('temperature_protocol', 'beta_grid', ['2', '4', '16']),
            ('temperature_protocol', 'stop', 'first_passing'),
            ('trial_rank_protocol', 'rank_rule', 'min(12,dimension-1)'),
            ('trial_rank_protocol', 'tolerance', '1/1000'),
            ('certificate_criterion', 'defect', 'different_defect'),
            ('certificate_criterion', 'target', 'low_band'),
        ]
        for field, key, value in changes:
            with self.subTest(field=field, key=key):
                rows = self.rows()
                rows[-1]['provenance'][field]['settings'][key] = value
                self.assert_blocked(rows, 'INCOMPATIBLE_SAMPLES')

    def test_added_settings_and_bool_integer_distinction(self):
        rows = self.rows()
        rows[1]['provenance']['model_family']['settings']['field_z'] = '1/10'
        self.assert_blocked(rows, 'INCOMPATIBLE_SAMPLES')
        rows = self.rows()
        for row in rows:
            row['provenance']['geometry_family']['settings']['periodic'] = True
        rows[1]['provenance']['geometry_family']['settings']['periodic'] = 1
        self.assert_blocked(rows, 'INCOMPATIBLE_SAMPLES')

    def test_threshold_bound_to_criterion_even_for_one_record(self):
        rows = self.rows([.0001])
        rows[0]['evidence'] = 'certified_bound'
        self.assert_blocked(rows, 'INCOMPATIBLE_SAMPLES', threshold='.01')

    def test_threshold_metadata_uses_exact_arithmetic(self):
        rows = self.rows(threshold='.1')
        rows[-1]['provenance']['certificate_criterion']['threshold'] = '0.100000000000000000000001'
        self.assert_blocked(rows, 'INCOMPATIBLE_SAMPLES', threshold='.1')

    def test_equivalent_threshold_lexemes_are_compatible(self):
        rows = self.rows()
        for row, threshold in zip(rows, ('0.001', Fraction(1, 1000), Decimal('.001'))):
            row['provenance']['certificate_criterion']['threshold'] = threshold
        result = forecast_seed_size(rows, Fraction(1, 1000))
        self.assertEqual(result['status'], 'HEURISTIC_NEXT_SEED')

    def test_old_records_are_unverified(self):
        rows = self.rows()
        for row in rows:
            del row['provenance']
        result = self.assert_blocked(rows, 'UNVERIFIED_SAMPLE_COMPATIBILITY')
        self.assertEqual(result['sample_compatibility']['status'], 'unverified')
        self.assertEqual(len(result['sample_compatibility']['missing_metadata']), 3)

    def test_each_missing_descriptor_and_member_blocks(self):
        for field in provenance():
            for member in (None, *provenance()[field]):
                with self.subTest(field=field, member=member):
                    rows = self.rows()
                    if member is None:
                        del rows[1]['provenance'][field]
                    else:
                        del rows[1]['provenance'][field][member]
                    result = self.assert_blocked(rows, 'UNVERIFIED_SAMPLE_COMPATIBILITY')
                    self.assertTrue(result['sample_compatibility']['missing_metadata'])

    def test_empty_or_null_provenance_is_unverified(self):
        for value in ({}, None):
            with self.subTest(value=value):
                rows = self.rows()
                rows[0]['provenance'] = value
                self.assert_blocked(rows, 'UNVERIFIED_SAMPLE_COMPATIBILITY')

    def test_incomplete_samples_are_not_silently_dropped(self):
        rows = self.rows([.1, .05, .025, .0125])
        del rows[-1]['provenance']
        result = self.assert_blocked(rows, 'UNVERIFIED_SAMPLE_COMPATIBILITY')
        self.assertEqual(len(result['samples']), 4)

    def test_known_conflict_takes_precedence_over_missing_information(self):
        rows = self.rows()
        del rows[0]['provenance']
        rows[1]['provenance']['model_family']['id'] = 'different_model'
        del rows[1]['provenance']['model_family']['settings']
        result = self.assert_blocked(rows, 'INCOMPATIBLE_SAMPLES')
        self.assertTrue(result['sample_compatibility']['missing_metadata'])

    def test_scalar_success_cannot_bypass_compatibility(self):
        for missing in (False, True):
            with self.subTest(missing=missing):
                rows = self.rows([.0001, .0002, .0003])
                rows[0]['evidence'] = 'certified_bound'
                if missing:
                    del rows[-1]['provenance']
                    status = 'UNVERIFIED_SAMPLE_COMPATIBILITY'
                else:
                    rows[-1]['provenance']['geometry_family']['id'] = 'other_geometry'
                    status = 'INCOMPATIBLE_SAMPLES'
                result = self.assert_blocked(rows, status)
                self.assertTrue(result['samples'][0]['defect_at_or_below_threshold'])

    def test_single_old_success_is_still_unverified(self):
        rows = self.rows([.0001])
        rows[0]['evidence'] = 'certified_bound'
        del rows[0]['provenance']
        self.assert_blocked(rows, 'UNVERIFIED_SAMPLE_COMPATIBILITY')

    def test_mixed_evidence_levels_do_not_upgrade_prediction(self):
        rows = self.rows()
        rows[0]['evidence'] = 'certified_bound'
        result = forecast_seed_size(rows, .001)
        self.assertEqual(result['status'], 'HEURISTIC_NEXT_SEED')
        self.assertEqual([r['evidence'] for r in result['samples']],
                         ['certified_bound', 'floating_estimate', 'floating_estimate'])
        self.assert_no_proof(result)

    def test_floating_success_is_not_a_certified_seed(self):
        result = forecast_seed_size(self.rows([.0003, .0002, .0001]), .001)
        self.assertEqual(result['status'], 'HEURISTIC_NEXT_SEED')
        self.assertEqual(result['prediction']['candidate_even_linear_size'], 8)
        self.assertIsNone(result['smallest_tested_sufficient_size'])
        self.assert_no_proof(result)

    def test_smallest_success_uses_only_certified_records(self):
        rows = self.rows([.0001, .0002, .0003])
        rows[1]['evidence'] = rows[2]['evidence'] = 'certified_bound'
        result = forecast_seed_size(rows[::-1], .001)
        self.assertEqual(result['smallest_tested_sufficient_size'], 4)

    def test_metadata_is_copied_order_independent_and_serializable(self):
        rows = self.rows()
        rows[1]['provenance'] = dict(reversed(list(rows[1]['provenance'].items())))
        settings = rows[1]['provenance']['geometry_family']['settings']
        rows[1]['provenance']['geometry_family']['settings'] = dict(reversed(list(settings.items())))
        before = deepcopy(rows)
        result = forecast_seed_size(rows[::-1], .001)
        self.assertEqual(result['status'], 'HEURISTIC_NEXT_SEED')
        self.assertEqual(rows, before)
        self.assertEqual(json.loads(json.dumps(result)), result)
        rows[0]['provenance']['model_family']['settings']['J'] = '2'
        self.assertEqual(result['samples'][0]['provenance']['model_family']['settings']['J'], '1')

    def test_search_order_is_part_of_the_protocol(self):
        rows = self.rows()
        rows[0]['provenance']['temperature_protocol']['settings']['beta_grid'].reverse()
        self.assert_blocked(rows, 'INCOMPATIBLE_SAMPLES')

    def test_missing_and_invalid_evidence_rejected(self):
        for value in (None, '', 'verified', [], True):
            with self.subTest(value=value):
                rows = self.rows()
                rows[1]['evidence'] = value
                with self.assertRaises(ValueError):
                    forecast_seed_size(rows, .001)

    def test_duplicate_sizes_rejected_before_compatibility(self):
        rows = self.rows()
        rows[-1]['linear_size'] = rows[0]['linear_size']
        del rows[-1]['provenance']
        with self.assertRaisesRegex(ValueError, 'Duplicate linear sizes'):
            forecast_seed_size(rows, .001)

    def test_malformed_provenance_rejected(self):
        invalid = [[], 'shared_name', {'typo': {}}, {'model_family': 'name'},
                   {'model_family': {'id': ''}}, {'model_family': {'id': True}},
                   {'model_family': {'settings': []}}, {'model_family': {'setting': {}}},
                   {'model_family': {'settings': {'J': float('nan')}}},
                   {'model_family': {'settings': {1: 'one'}}},
                   {'model_family': {'settings': {'values': {1, 2}}}},
                   {'certificate_criterion': {'threshold': 'not_a_rational'}},
                   {'certificate_criterion': {'threshold': '1/0'}},
                   {'certificate_criterion': {'threshold': '1'}}]
        for value in invalid:
            with self.subTest(value=value):
                rows = self.rows()
                rows[0]['provenance'] = value
                with self.assertRaises(ValueError):
                    forecast_seed_size(rows, .001)

    def test_budget_is_validated_on_early_returns(self):
        for values in ([.1], [.0001], [.01, .02, .03]):
            for budget in (True, 0, 2.5):
                with self.subTest(values=values, budget=budget):
                    rows = self.rows(values)
                    rows[0]['evidence'] = 'certified_bound'
                    with self.assertRaises(ValueError):
                        forecast_seed_size(rows, .001, max_size=budget)


if __name__ == '__main__':
    unittest.main()
