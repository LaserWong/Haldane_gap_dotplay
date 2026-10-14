import unittest
from fractions import Fraction as F
import numpy as np
from scipy.sparse import csr_matrix
from gapflow.certify import (inertia, schur_certificate, ritz_candidates,
    partial_ritz_candidates, thermal_tail_certificate, search_trial_dimension,
    spectral_gap_certificate, exact_matrix)

class CertificationTests(unittest.TestCase):
    def test_zero_diagonal_two_by_two_pivot(self):
        c=inertia([[0,2],[2,0]])
        self.assertEqual((c.negative,c.zero,c.positive),(1,0,1))
        c=inertia([[0,0],[0,0]])
        self.assertEqual((c.negative,c.zero,c.positive),(0,2,0))

    def test_exact_inertia_against_independent_float(self):
        rng=np.random.default_rng(91)
        for n in range(1,10):
            for _ in range(10):
                A=rng.integers(-5,6,(n,n)); H=A+A.T
                c=inertia(H, F(1,3))
                vals=np.linalg.eigvalsh(H.astype(float))-1/3
                self.assertEqual(c.negative,int(sum(vals < -1e-9)))
                self.assertEqual(c.positive,int(sum(vals > 1e-9)))
                self.assertEqual(c.zero,int(sum(abs(vals) <= 1e-9)))

    def test_schur_agrees_with_full_inertia(self):
        H=[[0,1,0],[1,4,1],[0,1,5]]
        cert=schur_certificate(H,[0],1)
        self.assertEqual(cert['inertia'],inertia(H,1))
        self.assertEqual(cert['schur_matrix'],[[-F(15,11)]])
        with self.assertRaises(ValueError):
            schur_certificate(H,[0],6)

    def test_omitted_low_state_defeats_zero_residual(self):
        H=np.diag([-5.,0.,2.,3.])
        Q=np.eye(4)[:,[1,2]]
        r=ritz_candidates(H,Q)
        np.testing.assert_equal(r['residual_norms'],[0,0])
        self.assertEqual(r['ritz_values'][0],0)
        self.assertFalse(r['certifies_omitted_spectrum'])
        c=thermal_tail_certificate(np.diag([-5,0,2,3]),[1,2],1,target=F(1,10))
        self.assertEqual(c['complement_lower'],-5)
        self.assertFalse(c['target_met'])
        self.assertEqual(inertia(np.diag([-5,0,2,3]),-1).negative,1)

    def test_floats_never_become_exact_proof(self):
        with self.assertRaises(TypeError): inertia(np.eye(2))
        with self.assertRaises(TypeError): inertia(csr_matrix(np.eye(2)))
        with self.assertRaises(ValueError): exact_matrix(np.eye(65))

    def test_exact_tail_target_and_dimension_budget(self):
        H=np.diag([0,1,4,8])
        result=search_trial_dimension(H,2,F(1,100),max_trial_dimension=3)
        self.assertEqual(result['sufficient_dimension'],2)
        cert=result['records'][-1]
        actual=sum(np.exp(-2*np.linalg.eigvalsh(H)[2:]))
        self.assertLessEqual(actual,float(cert['tail_upper_rational']))
        self.assertLessEqual(cert['tail_upper_rational'],F(1,100))
        fail=search_trial_dimension(H,2,F(1,100),max_trial_dimension=1)
        self.assertEqual(fail['status'],'no_certificate_within_dimension_budget')
        fail=search_trial_dimension(H,2,F(1,100),max_seconds=0)
        self.assertEqual(fail['status'],'time_budget_exhausted')

    def test_residual_coupling_young_bound(self):
        H=[[0,1,0],[1,4,1],[0,1,5]]
        c=thermal_tail_certificate(H,[0],2,young_parameter=F(1,2))
        self.assertEqual(c['residual_frobenius_squared'],1)
        self.assertEqual(c['ground_energy_lower'],-F(1,2))
        d=np.diag([float(c['block_energy_lowers'][0])]+[float(c['block_energy_lowers'][1])]*2)
        self.assertGreaterEqual(np.linalg.eigvalsh(np.array(H)-d)[0],-1e-12)
        vals=np.linalg.eigvalsh(np.array(H))
        actual=sum(np.exp(-2*(vals[1:]-vals[0])))
        self.assertLessEqual(actual,float(c['tail_upper_rational']))

    def test_iterative_candidates_sparse_and_gap(self):
        H=csr_matrix(np.diag([0.,1.,4.,8.]))
        r=partial_ritz_candidates(H,2)
        np.testing.assert_allclose(r['ritz_values'],[0,1],atol=1e-12)
        self.assertFalse(r['certifies_omitted_spectrum'])
        c=spectral_gap_certificate(np.diag([0,1,4,8]),F(9,10))
        self.assertTrue(c['certified'])
        self.assertEqual(c['gap_lower'],F(9,10))
        self.assertFalse(spectral_gap_certificate(np.diag([0,0,4]),1)['certified'])


class ExactGapTests(unittest.TestCase):
    def test_exact_degenerate_ground_and_boundary(self):
        from gapflow.certify import certify_gap,verify_gap_certificate
        H=np.diag([0,0,2,4])
        c=certify_gap(H,0,2)
        self.assertTrue(c['certified'])
        self.assertEqual(c['ground_multiplicity'],2)
        self.assertTrue(verify_gap_certificate(H,c))
        self.assertFalse(certify_gap(H,0,3)['certified'])
        self.assertFalse(certify_gap(H,-1,1)['certified'])
        self.assertFalse(certify_gap([[0,0],[0,0]],0,1)['certified'])
        self.assertFalse(verify_gap_certificate(np.diag([0,0,1,4]),c))


class RayleighGapTests(unittest.TestCase):
    def test_heisenberg_dimer_singlet(self):
        from gapflow.certify import certify_gap_from_vector
        H=[[F(1,4),0,0,0],[0,-F(1,4),F(1,2),0],
           [0,F(1,2),-F(1,4),0],[0,0,0,F(1,4)]]
        c=certify_gap_from_vector(H,[0,1,-1,0],F(1,4))
        self.assertTrue(c['certified'])
        self.assertEqual(c['ground_energy_upper'],-F(3,4))
        self.assertEqual(c['gap_lower_bound'],1)
        self.assertEqual(c['residual_squared'],0)
        c=certify_gap_from_vector(H,[0,100,-99,0],0)
        self.assertTrue(c['certified'])
        self.assertGreater(c['residual_squared'],0)
        self.assertLess(c['gap_lower_bound'],F(3,4))
        with self.assertRaises(TypeError):
            certify_gap_from_vector(H,[0.,1.,-1.,0.],0)
        with self.assertRaises(ValueError):
            certify_gap_from_vector(H,[0,0,0,0],0)


class NoExcitedSpaceTests(unittest.TestCase):
    def test_all_public_gap_paths(self):
        from gapflow.certify import certify_gap, certify_gap_from_vector
        for H,v in [([[0]],[1]), ([[3]],[2]), ([[0,0],[0,0]],[1,0]), ([[3,0],[0,3]],[1,1])]:
            e=H[0][0]
            reports=[certify_gap(H,e,100), spectral_gap_certificate(H,e+100),
                     certify_gap_from_vector(H,v,e+100)]
            for report in reports:
                self.assertFalse(report['certified'])
                self.assertEqual(report['status'],'NO_EXCITED_SPACE')
        self.assertIsNone(spectral_gap_certificate([[0]],1)['gap_lower'])
        self.assertIsNone(certify_gap_from_vector([[0]],[1],1)['gap_lower_bound'])


class PencilTests(unittest.TestCase):
    def test_rescaled_pencil_inertia_and_rayleigh(self):
        from gapflow.certify import pencil_inertia,certify_pencil_gap,certify_pencil_gap_from_vector
        H=[[0,1],[1,2]]
        A=[[0,6],[6,18]]
        w=[4,9]
        for t in [-2,-1,0,1,2,3]:
            self.assertEqual(pencil_inertia(A,w,t),inertia(H,t))
        c=certify_pencil_gap_from_vector(A,w,[3,-1],1)
        d=__import__('gapflow.certify',fromlist=['certify_gap_from_vector']).certify_gap_from_vector(H,[6,-3],1)
        self.assertEqual(c['ground_energy_upper'],d['ground_energy_upper'])
        self.assertEqual(c['residual_squared'],d['residual_squared'])
        self.assertTrue(c['certified'])
        self.assertEqual(certify_pencil_gap([[0,0],[0,18]],[4,9],0,2)['gap_lower_bound'],2)
        for bad in ([0,1],[-1,1],[1],[1.,2]):
            with self.assertRaises((ValueError,TypeError)):
                pencil_inertia(A,bad)
        with self.assertRaises(TypeError):
            pencil_inertia([[0.,6.],[6.,18.]],w)
        for A,w,v in [([[3]],[2],[1]), ([[6,0],[0,12]],[2,4],[1,1])]:
            c=certify_pencil_gap_from_vector(A,w,v,100)
            self.assertFalse(c['certified'])
            self.assertEqual(c['status'],'NO_EXCITED_SPACE')

    def test_mixed_spin_exact_pencil(self):
        from gapflow.model import Model
        from gapflow.certify import pencil_inertia,certify_pencil_gap,verify_pencil_gap_certificate
        model=Model.from_dict({'spins':[0.5,1],
            'geometry':{'type':'graph','n_sites':2,'edges':[[0,1]]},
            'terms':[{'type':'heisenberg','J':'1'}]})
        A,w=model.exact_pencil()
        c=certify_pencil_gap(A,w,-1,F(3,2))
        self.assertTrue(c['certified'])
        self.assertEqual(c['ground_multiplicity'],2)
        self.assertEqual(pencil_inertia(A,w,F(1,2)).zero,4)
        self.assertTrue(verify_pencil_gap_certificate(A,w,c))
        self.assertFalse(certify_pencil_gap(A,w,-1,2)['certified'])

if __name__=='__main__': unittest.main()
