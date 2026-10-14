import unittest
from fractions import Fraction as F
from gapflow.invariant_witness import verify_invariant_witness


def irrational_example():
    A=[[-1,1,0,0,0,0],[1,1,0,0,0,0],
       [0,0,-1,1,0,0],[0,0,1,1,0,0],
       [0,0,0,0,3,0],[0,0,0,0,0,4]]
    V=[[int(i==j) for j in range(4)] for i in range(6)]
    T=[row[:4] for row in A[:4]]
    return A,[1]*6,V,T


def verify_example(**kwargs):
    return verify_invariant_witness(*irrational_example(),[1,0,-2],-2,-1,1,**kwargs)


class InvariantWitnessTests(unittest.TestCase):
    def test_proper_subspace_irrational_ground(self):
        c=verify_example()
        self.assertTrue(c['certified'])
        self.assertTrue(c['coverage_complete'])
        self.assertEqual(c['witness_dimension'],4)
        self.assertEqual(c['full_dimension'],6)
        self.assertEqual(c['ground_multiplicity'],2)
        self.assertEqual(c['gap_lower_bound'],2)
        self.assertEqual([i.negative for i in c['full_inertias']],[0,2,2])
        self.assertTrue(all(c['checks'].values()))

    def test_small_split_is_not_degeneracy(self):
        epsilon=F(1,100000000)
        A=[[0,0,0],[0,epsilon,0],[0,0,2]]
        V=[[1,0],[0,1],[0,0]]
        T=[[0,0],[0,epsilon]]
        c=verify_invariant_witness(A,[1]*3,V,T,[1,-epsilon,0],-1,F(1,10),1)
        self.assertFalse(c['certified'])
        self.assertEqual(c['status'],'NOT_ONE_DISTINCT_ROOT')
        self.assertEqual(c['distinct_polynomial_roots_in_bracket'],2)
        self.assertIsNone(c['ground_multiplicity'])

    def test_rounded_noninvariant_witness(self):
        A,W,V,T=irrational_example()
        V[4][0]=F(1,10**12)
        c=verify_invariant_witness(A,W,V,T,[1,0,-2],-2,-1,1)
        self.assertFalse(c['certified'])
        self.assertEqual(c['status'],'NONINVARIANT_WITNESS')

    def test_omitted_lower_state(self):
        A,W,V,T=irrational_example()
        A[-1][-1]=-10
        c=verify_invariant_witness(A,W,V,T,[1,0,-2],-2,-1,1)
        self.assertFalse(c['certified'])
        self.assertEqual(c['status'],'FULL_COMPLETENESS_FAILED')
        self.assertEqual(c['full_inertias'][0].negative,1)
        self.assertIsNone(c['ground_multiplicity'])

    def test_wrong_and_nonsquarefree_polynomials(self):
        for polynomial,status in [([1,0,-3],'WRONG_ANNIHILATOR'),
                                  ([1,0,-4,0,4],'POLYNOMIAL_NOT_SQUAREFREE')]:
            c=verify_invariant_witness(*irrational_example(),polynomial,-2,-1,1)
            self.assertFalse(c['certified'])
            self.assertEqual(c['status'],status)

    def test_nonpositive_metric_and_rank_deficiency(self):
        A,W,V,T=irrational_example()
        W[0]=-1
        c=verify_invariant_witness(A,W,V,T,[1,0,-2],-2,-1,1)
        self.assertEqual(c['status'],'NONPOSITIVE_METRIC')
        A,W,V,T=irrational_example()
        for row in V: row[1]=row[0]
        c=verify_invariant_witness(A,W,V,T,[1,0,-2],-2,-1,1)
        self.assertEqual(c['status'],'RANK_DEFICIENT_WITNESS')

    def test_dense_positive_metric(self):
        A=[[0,0,0],[0,0,0],[0,0,2]]
        W=[[1,1,0],[1,2,0],[0,0,1]]
        V=[[1,0],[0,1],[0,0]]
        c=verify_invariant_witness(A,W,V,[[0,0],[0,0]],[1,0],-1,F(1,10),1)
        self.assertTrue(c['certified'])
        self.assertEqual(c['ground_multiplicity'],2)
        self.assertEqual(c['gap_lower_bound'],F(9,10))

    def test_budgets_and_float_rejection(self):
        c=verify_example(max_seconds=0)
        self.assertEqual(c['status'],'TIME_BUDGET_EXHAUSTED')
        self.assertFalse(c['coverage_complete'])
        for kw in ({'max_dimension':5},{'max_witness_dimension':3},
                   {'max_polynomial_degree':1},{'max_input_bits':1}):
            with self.assertRaises(ValueError): verify_example(**kw)
        A,W,V,T=irrational_example()
        V[0][0]=1.0
        with self.assertRaises(TypeError):
            verify_invariant_witness(A,W,V,T,[1,0,-2],-2,-1,1)

    def test_all_space_one_energy_is_not_excitation_gap(self):
        c=verify_invariant_witness([[0]],[1],[[1]],[[0]],[1,0],-1,1,2)
        self.assertFalse(c['certified'])
        self.assertIsNone(c['gap_lower_bound'])
        self.assertIsNone(c['ground_multiplicity'])
        self.assertEqual(c['status'],'NO_SPECTRUM_ABOVE_CLUSTER')


class NoCharacteristicPolynomialTests(unittest.TestCase):
    def test_nonminimal_annihilator_without_matrix_charpoly(self):
        from unittest.mock import patch
        import sympy as sp
        with patch.object(sp.MatrixBase,'charpoly',side_effect=AssertionError('Full charpoly forbidden')):
            c=verify_invariant_witness(*irrational_example(),[1,-10,-2,20],-2,-1,1)
        self.assertTrue(c['certified'])
        self.assertEqual(c['ground_multiplicity'],2)

if __name__=='__main__': unittest.main()
