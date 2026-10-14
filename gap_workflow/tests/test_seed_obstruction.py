import copy
from fractions import Fraction as F
import unittest
from gapflow.seed_obstruction import (diagnose_hoeffding_seed, exp_negative_bounds,
                                     split_bound,verify_obstruction,THRESHOLD)


class SeedObstructionTests(unittest.TestCase):
    def test_threshold_without_irrational_arithmetic(self):
        self.assertLess((1+THRESHOLD)**2,2)

    def test_coarse_cutoffs(self):
        for model,g in [('bilayer_s_half','1/160'),('square_spin_one_large_D','1/240')]:
            c=split_bound(model,g,'4')
            self.assertTrue(c['obstructed'])
            self.assertLessEqual(F(c['all_beta_joint_seed_upper']),THRESHOLD)

    def test_improved_exact_split_examples(self):
        for model,g in [('bilayer_s_half','1/190'),('square_spin_one_large_D','1/250')]:
            out=diagnose_hoeffding_seed(model,g)
            self.assertEqual(out['status'],'CERTIFIED_CRITERION_OBSTRUCTION')
            self.assertTrue(verify_obstruction(out))
            self.assertFalse(out['physical_gaplessness'])
            self.assertFalse(out['physical_seed_exclusion'])

    def test_known_positive_baselines_not_rejected(self):
        for model,g in [('bilayer_s_half','1/4000'),('square_spin_one_large_D','1/6000')]:
            out=diagnose_hoeffding_seed(model,g)
            self.assertEqual(out['status'],'INCONCLUSIVE')

    def test_larger_cells_and_couplings(self):
        a=split_bound('bilayer_s_half','1/160','4',4)
        b=split_bound('bilayer_s_half','1/100','4',16)
        self.assertLessEqual(F(b['low_beta_upper']),F(a['low_beta_upper']))
        self.assertLessEqual(F(b['high_beta_upper']),F(a['high_beta_upper']))
        self.assertTrue(b['obstructed'])

    def test_zero_coupling_not_obstructed(self):
        self.assertEqual(diagnose_hoeffding_seed('bilayer_s_half','0')['status'],'INCONCLUSIVE')

    def test_exp_enclosures(self):
        self.assertEqual(exp_negative_bounds(0),(F(1),F(1)))
        lo,hi=exp_negative_bounds(1)
        # Independent elementary series bound 2.71828 < e < 2.71829.
        self.assertGreater(lo,F(100000,271829))
        self.assertLess(hi,F(100000,271828))

    def test_tampered_certificate_rejected(self):
        out=diagnose_hoeffding_seed('bilayer_s_half','1/100')
        out['certificate']['all_beta_joint_seed_upper']='0'
        self.assertFalse(verify_obstruction(out))

    def test_bad_input(self):
        self.assertEqual(diagnose_hoeffding_seed('other','1/100')['status'],'INVALID_INPUT')
        self.assertEqual(diagnose_hoeffding_seed('bilayer_s_half',0.01)['status'],'INVALID_INPUT')
        self.assertEqual(diagnose_hoeffding_seed('bilayer_s_half','-1')['status'],'INVALID_INPUT')

if __name__=='__main__':unittest.main()
