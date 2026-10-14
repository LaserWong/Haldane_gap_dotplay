"""Independent adversarial endpoint and multiplicity regressions."""
import unittest
from fractions import Fraction as F
from gapflow.low_band import certify_low_band,certify_sector_low_band,kramers_symmetry_certificate
from gapflow.model import Model

class IndependentLowBandTests(unittest.TestCase):
    def test_lower_endpoint_closed_upper_endpoint_excluded_threshold_inclusive(self):
        H=[[0,0,0],[0,0,0],[0,0,2]]
        c=certify_low_band(H,0,F(1,2),2,infer_multiplicity=True)
        self.assertTrue(c['certified']);self.assertEqual(c['true_ground_multiplicity'],2)
        self.assertEqual(c['true_ground_gap_lower'],F(3,2))
        self.assertFalse(certify_low_band(H,-1,0,2,infer_multiplicity=True)['certified'])
        self.assertFalse(certify_low_band(H,F(1,100),1,2,infer_multiplicity=True)['certified'])
    def test_unresolvably_small_rational_splitting_stays_distinct(self):
        H=[[0,0,0],[0,F(1,10**100),0],[0,0,2]]
        c=certify_low_band(H,0,F(1,100),1,infer_multiplicity=True)
        self.assertTrue(c['certified']);self.assertEqual(c['distinct_ground_cluster_roots'],2)
        self.assertIsNone(c['ground_multiplicity']);self.assertIsNone(c['true_ground_gap_lower'])
    def test_weighted_nondiagonal_irrational_root_equality(self):
        # D H D with D=diag(2,3,4,5), two +/-sqrt(2) blocks.
        d=[2,3,4,5];H=[[-1,1,0,0],[1,1,0,0],[0,0,-1,1],[0,0,1,1]]
        A=[[d[i]*H[i][j]*d[j] for j in range(4)] for i in range(4)]
        c=certify_low_band(A,-2,-1,1,Wdiag=[x*x for x in d],infer_multiplicity=True)
        self.assertEqual(c['true_ground_multiplicity'],2);self.assertEqual(c['distinct_ground_cluster_roots'],1)
    def test_kramers_termwise_invariance_and_parity(self):
        def model(spins,terms):return Model.from_dict({'spins':spins,'geometry':{'type':'graph','n_sites':len(spins),'edges':[]},'terms':terms})
        self.assertTrue(kramers_symmetry_certificate(model([.5,1],[]))['certified'])
        self.assertFalse(kramers_symmetry_certificate(model([.5,.5],[]))['certified'])
        self.assertFalse(kramers_symmetry_certificate(model([.5],[{'type':'field_z','h':'1/1000000'}]))['certified'])
        odd={'type':'spin_product','coefficient':1,'factors':[{'site':0,'operator':'x'}]}
        self.assertFalse(kramers_symmetry_certificate(model([.5],[odd]))['certified'])
        even={'type':'spin_product','coefficient':1,'factors':[{'site':0,'operator':'x'},{'site':1,'operator':'z'}]}
        self.assertTrue(kramers_symmetry_certificate(model([.5,1],[even]))['certified'])
        with self.assertRaises(ValueError):certify_sector_low_band(model([.5,1],[even]),-10,1,10,infer_multiplicity=True)
    def test_rank_four_does_not_become_exact_g_four_from_kramers(self):
        m=Model.from_dict({'spin':.5,'geometry':{'type':'graph','n_sites':3,'edges':[[0,1],[1,2]]},'terms':[{'type':'heisenberg','J':1}]})
        c=certify_sector_low_band(m,-2,F(1,4),F(1,2),infer_multiplicity=True,distinct_root_max_dimension=1)
        self.assertTrue(c['certified']);self.assertEqual(c['low_band_rank'],4)
        self.assertIsNone(c['true_ground_multiplicity']);self.assertIsNone(c['true_ground_gap_lower'])
    def test_all_space_cluster_no_gap_despite_root_multiplicity(self):
        c=certify_low_band([[1,0],[0,1]],0,2,3,infer_multiplicity=True)
        self.assertEqual(c['true_ground_multiplicity'],2);self.assertFalse(c['certified'])
        self.assertEqual(c['status'],'NO_EXCITED_SPACE');self.assertIsNone(c['true_ground_gap_lower'])

if __name__=='__main__':unittest.main()
