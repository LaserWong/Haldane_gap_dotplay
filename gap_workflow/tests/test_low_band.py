import unittest
from fractions import Fraction as F
from gapflow.low_band import certify_low_band,certify_sector_low_band
from gapflow.model import Model

class LowBandTests(unittest.TestCase):
    def test_nearly_degenerate_is_cluster_not_ground_degeneracy(self):
        H=[[0,0,0],[0,F(1,1000),0],[0,0,2]]
        c=certify_low_band(H,-1,F(1,100),1,infer_multiplicity=True)
        self.assertTrue(c['certified'])
        self.assertEqual(c['low_band_rank'],2)
        self.assertEqual(c['distinct_ground_cluster_roots'],2)
        self.assertIsNone(c['true_ground_multiplicity'])
        self.assertIsNone(c['true_ground_gap_lower'])
        self.assertEqual(c['gap_above_cluster_lower'],F(99,100))
        self.assertEqual(c['status'],'CERTIFIED_LOW_BAND')

    def test_double_rational_ground_inferred_without_input(self):
        H=[[0,0,0],[0,0,0],[0,0,2]]
        c=certify_low_band(H,-1,F(1,10),1)
        self.assertIsNone(c['true_ground_multiplicity'])
        c=certify_low_band(H,-1,F(1,10),1,infer_multiplicity=True)
        self.assertEqual(c['true_ground_multiplicity'],2)
        self.assertEqual(c['true_ground_gap_lower'],F(9,10))
        # Ground may lie exactly at the lower bracket.
        self.assertEqual(certify_low_band(H,0,F(1,10),1,infer_multiplicity=True)['true_ground_multiplicity'],2)

    def test_double_irrational_ground_inferred(self):
        # Two copies with roots +/-sqrt(2), not rational exact ground energies.
        H=[[-1,1,0,0],[1,1,0,0],[0,0,-1,1],[0,0,1,1]]
        c=certify_low_band(H,-2,-1,0,infer_multiplicity=True)
        self.assertTrue(c['certified'])
        self.assertEqual(c['low_band_rank'],2)
        self.assertEqual(c['distinct_ground_cluster_roots'],1)
        self.assertEqual(c['true_ground_multiplicity'],2)
        self.assertEqual(c['true_ground_gap_lower'],1)
        self.assertEqual(c['multiplicity_evidence']['squarefree_union_coefficients'],['1','0','-2'])

    def test_omitted_states_and_boundaries_fail(self):
        c=certify_low_band([[-5,0,0],[0,0,0],[0,0,2]],-1,1,F(3,2),infer_multiplicity=True)
        self.assertFalse(c['certified'])
        self.assertIsNone(c['low_band_rank'])
        self.assertFalse(certify_low_band([[0,0],[0,1]],-1,1,2)['certified'])
        with self.assertRaises(ValueError):
            certify_low_band([[0]],1,0,2)
        c=certify_low_band([[0]],-1,1,2,infer_multiplicity=True)
        self.assertFalse(c['certified'])
        self.assertEqual(c['status'],'NO_EXCITED_SPACE')
        self.assertIsNone(c['true_ground_gap_lower'])

    def test_pencil_and_root_budget(self):
        A=[[0,0,0],[0,0,0],[0,0,18]]
        c=certify_low_band(A,-1,F(1,10),1,Wdiag=[2,3,9],infer_multiplicity=True)
        self.assertEqual(c['true_ground_multiplicity'],2)
        c=certify_low_band(A,-1,F(1,10),1,Wdiag=[2,3,9],infer_multiplicity=True,distinct_root_max_dimension=2)
        self.assertTrue(c['certified'])
        self.assertIsNone(c['true_ground_multiplicity'])
        self.assertEqual(c['multiplicity_evidence'],'distinct_root_dimension_budget_exceeded')

    def test_all_sector_root_union_multiplicity(self):
        m=Model.from_dict({'spins':[.5,1],'geometry':{'type':'graph','n_sites':2,'edges':[[0,1]]},
                          'terms':[{'type':'heisenberg','J':'1'}]})
        c=certify_sector_low_band(m,-2,F(-1,2),0,max_sector_dimension=2,infer_multiplicity=True)
        self.assertTrue(c['coverage_complete'])
        self.assertTrue(c['certified'])
        self.assertEqual(c['low_band_rank'],2)
        self.assertEqual(c['true_ground_multiplicity'],2)
        self.assertEqual(c['distinct_ground_cluster_roots'],1)
        self.assertEqual(c['ground_multiplicity_status'],'certified_by_Kramers_and_exhaustive_rank_two_cluster')
        c=certify_sector_low_band(m,-2,F(-1,2),0,max_sector_dimension=1,infer_multiplicity=True)
        self.assertFalse(c['coverage_complete'])
        self.assertFalse(c['certified'])
        self.assertIsNone(c['true_ground_multiplicity'])


class KramersTests(unittest.TestCase):
    def test_odd_half_spin_chain_and_symmetry_breaking_field(self):
        from gapflow.low_band import kramers_symmetry_certificate
        spec={'spin':.5,'geometry':{'type':'graph','n_sites':3,'edges':[[0,1],[1,2]]},
              'terms':[{'type':'heisenberg','J':'1'}]}
        m=Model.from_dict(spec)
        self.assertTrue(kramers_symmetry_certificate(m)['certified'])
        c=certify_sector_low_band(m,-2,F(-1,2),F(-1,10),infer_multiplicity=True,distinct_root_max_dimension=1)
        self.assertTrue(c['certified'])
        self.assertEqual(c['true_ground_multiplicity'],2)
        self.assertEqual(c['ground_multiplicity_status'],'certified_by_Kramers_and_exhaustive_rank_two_cluster')
        spec['terms'].append({'type':'field_z','h':'1/100'})
        m=Model.from_dict(spec)
        self.assertFalse(kramers_symmetry_certificate(m)['certified'])
        c=certify_sector_low_band(m,-2,F(-1,2),F(-1,10),infer_multiplicity=True,distinct_root_max_dimension=1)
        self.assertTrue(c['certified'])
        self.assertEqual(c['low_band_rank'],2)
        self.assertIsNone(c['true_ground_multiplicity'])
        self.assertEqual(c['status'],'CERTIFIED_LOW_BAND')


class UnionRootTests(unittest.TestCase):
    def test_even_integer_spins_union_counts_one_root_across_five_sectors(self):
        m=Model.from_dict({'spin':1,'geometry':{'type':'graph','n_sites':2,'edges':[[0,1]]},
                          'terms':[{'type':'heisenberg','J':'-1'}]})
        c=certify_sector_low_band(m,-2,F(-1,2),0,max_sector_dimension=3,infer_multiplicity=True)
        self.assertTrue(c['certified'])
        self.assertEqual(c['true_ground_multiplicity'],5)
        self.assertEqual(c['distinct_ground_cluster_roots'],1)
        self.assertEqual(c['multiplicity_evidence']['squarefree_union_degree'],3)
        self.assertEqual(c['ground_multiplicity_status'],'certified_by_single_distinct_root')

if __name__=='__main__': unittest.main()
