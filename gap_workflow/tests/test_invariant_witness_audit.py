"""Independent adversarial tests for supplied exact invariant witnesses."""
from fractions import Fraction as F
import unittest
from unittest.mock import patch
import sympy as sp
from gapflow.invariant_witness import verify_invariant_witness


def rational_rows(M):return [[F(x) for x in row] for row in M.tolist()]

class IndependentInvariantWitnessTests(unittest.TestCase):
    def test_dense_metric_nonorthogonal_coordinates_and_nonsymmetric_T(self):
        # Independent congruence of physical diag(0,0,2,5), with a trial
        # basis containing both the ground space and an outside eigenstate.
        H=sp.diag(0,0,2,5)
        S=sp.Matrix([[1,2,-1,3],[0,1,3,-2],[0,0,1,4],[0,0,0,1]])
        U=sp.eye(4)[:,:3];R=sp.Matrix([[1,2,3],[0,1,4],[0,0,1]])
        A=S.T*H*S;W=S.T*S;V=S.inv()*U*R;T=R.inv()*sp.diag(0,0,2)*R
        self.assertNotEqual(T,T.T)
        args=[rational_rows(x) for x in (A,W,V,T)]
        c=verify_invariant_witness(*args,[1,-2,0],0,F(1,10),2)
        self.assertTrue(c['certified']);self.assertEqual(c['ground_multiplicity'],2)
        self.assertEqual(c['gap_lower_bound'],F(19,10));self.assertEqual(c['restricted_cluster_rank'],2)
    def test_missing_equal_energy_ground_state_fails_completeness(self):
        c=verify_invariant_witness([[0,0,0],[0,0,0],[0,0,2]],[1]*3,[[1],[0],[0]],[[0]],[1,0],0,F(1,10),1)
        self.assertFalse(c['certified']);self.assertEqual(c['status'],'FULL_COMPLETENESS_FAILED')
    def test_missing_unequal_low_state_fails_completeness(self):
        eps=F(1,10**100)
        c=verify_invariant_witness([[0,0,0],[0,eps,0],[0,0,2]],[1]*3,[[1],[0],[0]],[[0]],[1,0],0,F(1,10),1)
        self.assertFalse(c['certified']);self.assertEqual(c['status'],'FULL_COMPLETENESS_FAILED')
    def test_orthogonality_is_not_assumed_and_gram_detects_dependence(self):
        A=sp.diag(0,0,2);W=sp.eye(3);V=sp.Matrix([[1,2],[2,4],[0,0]])
        c=verify_invariant_witness(*[rational_rows(x) for x in (A,W,V,sp.zeros(2))],[1,0],0,F(1,10),1)
        self.assertEqual(c['status'],'RANK_DEFICIENT_WITNESS')
    def test_root_endpoint_and_extra_polynomial_roots(self):
        A=[[0,0],[0,2]];args=(A,[1,1],[[1],[0]],[[0]])
        self.assertTrue(verify_invariant_witness(*args,[1,-7,0],0,F(1,10),2)['certified'])
        # An extraneous annihilator root in the bracket makes the sufficient
        # criterion inconclusive, even though the invariant state is exact.
        c=verify_invariant_witness(*args,[1,F(-1,20),0],0,F(1,10),2)
        self.assertEqual(c['status'],'NOT_ONE_DISTINCT_ROOT')
        c=verify_invariant_witness(*args,[1,0],-1,0,2)
        self.assertFalse(c['certified'])
    def test_zero_wrong_and_complex_polynomials_cannot_certify(self):
        args=([[0,0],[0,2]],[1,1],[[1],[0]],[[0]])
        with self.assertRaises(ValueError):verify_invariant_witness(*args,[0,0],-1,1,2)
        self.assertEqual(verify_invariant_witness(*args,[1,0,1],-1,1,2)['status'],'WRONG_ANNIHILATOR')
        with self.assertRaises(TypeError):verify_invariant_witness(*args,[1,1j],-1,1,2)
    def test_dense_indefinite_metric_and_nonsymmetric_energy_form_rejected(self):
        c=verify_invariant_witness([[0,0],[0,2]],[[1,2],[2,1]],[[1],[0]],[[0]],[1,0],-1,1,2)
        self.assertEqual(c['status'],'NONPOSITIVE_METRIC')
        with self.assertRaises(ValueError):verify_invariant_witness([[0,1],[0,2]],[1,1],[[1],[0]],[[0]],[1,0],-1,1,2)
    def test_no_characteristic_polynomial_called(self):
        with patch.object(sp.matrices.matrixbase.MatrixBase,'charpoly',side_effect=AssertionError('charpoly forbidden')):
            c=verify_invariant_witness([[0,0],[0,2]],[1,1],[[1],[0]],[[0]],[1,0],-1,F(1,10),1)
        self.assertTrue(c['certified'])

if __name__=='__main__':unittest.main()
