import unittest
from fractions import Fraction as F
import numpy as np
from gapflow.model import Model
from gapflow.sectors import certify_sectors_gap,certify_sectors_gap_from_vector
from gapflow.certify import certify_pencil_gap,partial_ritz_candidates


def dimer(spins=(.5,.5),J='1'):
    return Model.from_dict({'spins':list(spins),'geometry':{'type':'graph','n_sites':2,'edges':[[0,1]]},
                           'terms':[{'type':'heisenberg','J':J}]})


class SectorTests(unittest.TestCase):
    def test_exact_degenerate_mixed_spin_full_coverage(self):
        m=dimer((.5,1))
        c=certify_sectors_gap(m,-1,F(3,2),max_sector_dimension=2)
        self.assertTrue(c['certified'])
        self.assertTrue(c['coverage_complete'])
        self.assertEqual(c['covered_dimension'],6)
        self.assertEqual(c['ground_multiplicity'],2)
        self.assertEqual(len(c['sector_evidence']),4)
        A,w=m.exact_pencil()
        direct=certify_pencil_gap(A,w,-1,F(3,2))
        self.assertEqual(c['ground_inertia'],direct['ground_inertia'])
        self.assertEqual(c['gap_threshold_inertia'],direct['gap_threshold_inertia'])

    def test_trial_vector_and_omitted_sector(self):
        m=dimer()
        c=certify_sectors_gap_from_vector(m,0,[1,-1],F(1,4),max_sector_dimension=2)
        self.assertTrue(c['certified'])
        self.assertEqual(c['gap_lower_bound'],1)
        # Polarized sector has zero residual but is not the global ground.
        c=certify_sectors_gap_from_vector(m,2,[1],F(1,2),max_sector_dimension=2)
        self.assertFalse(c['certified'])
        self.assertEqual(c['residual_squared'],0)
        self.assertEqual(c['threshold_inertia'].negative,4)

    def test_budgets_and_symmetry_rejection(self):
        m=dimer()
        c=certify_sectors_gap(m,-F(3,4),1,max_sector_dimension=1)
        self.assertEqual(c['status'],'SECTOR_DIMENSION_BUDGET_EXCEEDED')
        self.assertFalse(c['coverage_complete'])
        self.assertEqual(c['covered_dimension'],0)
        c=certify_sectors_gap(m,-F(3,4),1,max_seconds=0)
        self.assertEqual(c['status'],'TIME_BUDGET_EXHAUSTED')
        self.assertFalse(c['coverage_complete'])
        m=Model.from_dict({'spin':.5,'geometry':{'type':'graph','n_sites':1,'edges':[]},
            'terms':[{'type':'spin_product','coefficient':'1','factors':[{'site':0,'operator':'x'}]}]})
        with self.assertRaises(ValueError):
            certify_sectors_gap(m,-F(1,2),1)

    def test_zero_model_not_positive_gap(self):
        m=Model.from_dict({'spin':.5,'geometry':{'type':'graph','n_sites':2,'edges':[]},'terms':[]})
        for c in [certify_sectors_gap(m,0,100),certify_sectors_gap_from_vector(m,2,[1],100)]:
            self.assertFalse(c['certified'])
            self.assertEqual(c['status'],'NO_EXCITED_SPACE')

    def test_three_dimensional_cube_without_full_matrix(self):
        m=Model.from_dict({'spin':.5,'geometry':{'type':'lattice','shape':[2,2,2],'periodic':False},
                          'terms':[{'type':'heisenberg','J':'1'}]})
        H=m.hamiltonian(total_m2=0,matrix_free=False,max_dimension=70)
        q=partial_ritz_candidates(H,1)['vectors'][:,0]
        # Spin-half pencil weights are all one. Rounding is candidate preparation.
        v=[F(str(round(float(x),8))) for x in q]
        c=certify_sectors_gap_from_vector(m,0,v,-4,max_sector_dimension=70)
        self.assertTrue(c['certified'])
        self.assertEqual(c['full_hilbert_dimension'],256)
        self.assertEqual(c['largest_sector_dimension'],70)
        self.assertEqual(c['covered_dimension'],256)
        self.assertEqual(len(c['sector_evidence']),9)
        self.assertGreater(c['gap_lower_bound'],F(4,5))
        self.assertEqual(c['threshold_inertia'].negative,1)

if __name__=='__main__': unittest.main()
