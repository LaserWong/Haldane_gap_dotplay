import unittest
from fractions import Fraction
from gapflow.gapless import (FAMILY, diagnose_gapless_family,
                             ferromagnetic_cycle, numerical_control_check)


class GaplessControlTests(unittest.TestCase):
    def test_analytic_diagnostic(self):
        result = diagnose_gapless_family(J='2/3')
        self.assertEqual(result['status'], 'CERTIFIED_GAPLESS_FAMILY')
        self.assertTrue(result['physical_gaplessness'])
        self.assertTrue(result['finite_size_gap_positive'])
        self.assertFalse(result['general_gaplessness_algorithm'])
        self.assertEqual(result['J'], '2/3')

    def test_no_general_or_bad_input_claim(self):
        for family, coupling in [('unknown', '1'), (FAMILY, 0),
                                  (FAMILY, '-1'), (FAMILY, True),
                                  (FAMILY, 0.5), (FAMILY, '1/0')]:
            result = diagnose_gapless_family(family, coupling)
            self.assertEqual(result['status'], 'INVALID_INPUT')
            self.assertFalse(result['physical_gaplessness'])

    def test_all_sectors_and_magnon_L3_through_L10(self):
        for length in range(3, 11):
            with self.subTest(L=length):
                check = numerical_control_check(length)
                self.assertEqual(check['evidence'], 'floating_point_check_only')
                self.assertEqual(check['covered_dimension'], 2**length)
                self.assertEqual(check['ground_multiplicity'], length+1)
                self.assertGreater(check['minimum_energy_over_J'], -1e-10)
                self.assertGreater(check['gap_over_J'], 0)
                self.assertAlmostEqual(check['gap_over_J'], check['magnon_energy_over_J'], places=10)
                self.assertLess(check['magnon_residual_over_J'], 1e-10)
                self.assertAlmostEqual(check['magnon_norm'], 1)
                self.assertLess(check['symmetric_ground_overlap'], 1e-10)
                self.assertLessEqual(check['magnon_energy_over_J'],
                                     check['quadratic_upper_bound_over_J'])

    def test_L2_double_bond_normalization(self):
        model = ferromagnetic_cycle(2, '2/3')
        self.assertEqual(len(model.edges), 2)
        self.assertTrue(all(term[3] == Fraction(-2, 3) for term in model.terms))
        check = numerical_control_check(2, '2/3')
        self.assertEqual(check['ground_multiplicity'], 3)
        self.assertAlmostEqual(check['gap_over_J'], 2)

    def test_bounded_numerical_check(self):
        for length in [True, 1, 3.0, 11]:
            with self.assertRaises(ValueError):
                numerical_control_check(length)


if __name__ == '__main__':
    unittest.main()
