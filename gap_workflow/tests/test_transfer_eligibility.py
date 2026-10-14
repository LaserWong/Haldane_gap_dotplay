import unittest
from fractions import Fraction as F
from gapflow.transfer_eligibility import bond_realignment_certificate


def kron(a,b):
    return [[x*y for x in ar for y in br] for ar in a for br in b]


def scaled(a,c):return [[c*x for x in row] for row in a]


class TransferEligibilityTests(unittest.TestCase):
    def test_ferromagnetic_and_transverse_onsite(self):
        z=[[1,0],[0,-1]];x=[[0,1],[1,0]]
        out=bond_realignment_certificate(scaled(kron(z,z),-3),onsite=scaled(x,-2))
        self.assertEqual(out['status'],'LOCAL_IDENTICAL_FACTOR_WITNESS_VERIFIED')
        self.assertEqual(out['realignment_inertia'],{'negative':0,'zero':3,'positive':1})
        self.assertTrue(out['onsite_real_metric_selfadjoint_verified'])
        self.assertFalse(out['spatial_transfer_family_certified'])
        self.assertEqual(len(out['identical_factor_witness']),1)

    def test_antiferromagnetic_classical_other_route(self):
        z=[[1,0],[0,-1]]
        out=bond_realignment_certificate(kron(z,z))
        self.assertEqual(out['realignment_inertia']['negative'],1)
        self.assertEqual(out['status'],'IDENTICAL_FACTOR_ROUTE_INCONCLUSIVE')
        self.assertTrue(out['classical_diagonal_symmetric_bond'])

    def test_metric_coefficient_matrix(self):
        # S+ + S- for spin one in the rational non-normalized basis.
        a=[[0,2,0],[1,0,1],[0,2,0]]
        out=bond_realignment_certificate(scaled(kron(a,a),-1),metric_weights=[1,2,1],onsite=a)
        self.assertTrue(out['witness_reconstruction_verified'])
        self.assertEqual(out['realignment_inertia']['positive'],1)
        with self.assertRaises(ValueError):bond_realignment_certificate(scaled(kron(a,a),-1))

    def test_multiple_factors_and_zero_bond(self):
        z=[[1,0],[0,-1]];x=[[0,1],[1,0]]
        zz=kron(z,z);xx=kron(x,x)
        h=[[-zz[i][j]-2*xx[i][j] for j in range(4)] for i in range(4)]
        out=bond_realignment_certificate(h)
        self.assertEqual(out['realignment_inertia']['positive'],2)
        self.assertEqual(len(out['identical_factor_witness']),2)
        zero=bond_realignment_certificate([[0]*4 for _ in range(4)])
        self.assertTrue(zero['witness_reconstruction_verified'])
        self.assertEqual(zero['identical_factor_witness'],[])

    def test_asymmetric_realignment_and_input_rejection(self):
        z=[[1,0],[0,-1]];x=[[0,1],[1,0]]
        out=bond_realignment_certificate(kron(z,x))
        self.assertFalse(out['realignment_symmetric'])
        self.assertFalse(out['witness_reconstruction_verified'])
        with self.assertRaises(TypeError):bond_realignment_certificate([[0.0]*4 for _ in range(4)])
        with self.assertRaises(ValueError):bond_realignment_certificate(kron(z,z),metric_weights=[1,0])
        with self.assertRaises(ValueError):bond_realignment_certificate(kron(z,z),onsite=[[0,1],[0,0]])
        with self.assertRaises(ValueError):bond_realignment_certificate(kron(z,z),max_dimension=3)

if __name__=='__main__':unittest.main()
