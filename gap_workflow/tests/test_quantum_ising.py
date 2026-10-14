import math
from fractions import Fraction
import unittest
import numpy as np
from gapflow.quantum_ising import log_partition, log_partition_mp, canonical_seed, replay_candidate, shifted_partition_mp


def ed_levels(L,J,h):
    """Independent bit-basis Hamiltonian, validation only, never seed generation."""
    H=np.zeros((2**L,2**L))
    for s in range(2**L):
        H[s,s]=-J*sum((1-2*((s>>i)&1))*(1-2*((s>>((i+1)%L))&1)) for i in range(L))
        for i in range(L): H[s,s^(1<<i)]-=h
    return np.linalg.eigvalsh(H)


class QuantumIsingTests(unittest.TestCase):
    def test_ed_all_lengths_and_phases(self):
        for L in range(2,9):
            for J,h in [(1,.5),(1,1),(1,1.5),(1,2),(1,-1.5),(0,.7),(1,0),(0,0)]:
                E=ed_levels(L,J,h)
                for beta in (0,.1,1,8):
                    expected=-beta*E[0]+math.log(float(np.exp(-beta*(E-E[0])).sum()))
                    self.assertAlmostEqual(log_partition(L,beta,J,h),expected,places=10)

    def test_paramagnetic_analytic_bridge(self):
        for L in range(2,9):
            for J,h in ((0,1),(1,1.01),(1,1.5),(1,2)):
                E=ed_levels(L,J,h)
                self.assertGreaterEqual(E[1]-E[0]+1e-11,2*(h-J))
                sums=[]
                for shift in (.5,0):
                    sums.append(sum(math.sqrt((J-h)**2+4*J*h*math.sin(math.pi*(m+shift)/L)**2) for m in range(L)))
                self.assertGreaterEqual(sums[0]+1e-12,sums[1])

    def test_four_product_parity_sign(self):
        for L in range(2,9):
            for h in (0,.5,1,1.5,2):
                beta=.7
                products=[]
                for shift in (.5,0):
                    es=[2*math.sqrt((1-h)**2+4*h*math.sin(math.pi*(m+shift)/L)**2) for m in range(L)]
                    products.append((math.prod(2*math.cosh(beta*e/2) for e in es), math.prod(2*math.sinh(beta*e/2) for e in es)))
                (cn,sn),(cr,sr)=products
                sign=(h>1)-(h<1)
                self.assertAlmostEqual(math.log((cn+sn+cr-sign*sr)/2),log_partition(L,beta,1,h),places=12)

    def test_candidate_replay(self):
        result=replay_candidate(canonical_seed(8,4,h=2))
        self.assertEqual(result['status'],'NUMERICAL_ENTRY_CANDIDATE')
        self.assertFalse(result['uniform_family_claim'])
        self.assertGreater(result['rounds'],0)
        self.assertEqual(replay_candidate(canonical_seed(16,8,h=.5))['status'],'NUMERICAL_RECURRENCE_INCONCLUSIVE')

    def test_shifted_positive_factors(self):
        for L in (2,3,8,16):
            for h in (0,.5,1,1.5,2,-1.5):
                beta=3
                shifted=shifted_partition_mp(L,beta,1,h)
                self.assertAlmostEqual(math.log(float(shifted)),log_partition(L,beta,1,h)-beta*(1+abs(h))*L,places=11)

    def test_zero_limits(self):
        for L in range(2,20):
            for beta in (0,.3,2):
                self.assertAlmostEqual(log_partition(L,beta,0,1), L*math.log(2*math.cosh(beta)),places=11)
                expected=math.log((2*math.cosh(beta))**L+(2*math.sinh(beta))**L)
                self.assertAlmostEqual(log_partition(L,beta,1,0),expected,places=11)

    def test_low_temperature_no_cancellation(self):
        for L in (2,3,8,32):
            for h in (.5,1,1.5,2):
                self.assertAlmostEqual(log_partition(L,1000,1,h),float(log_partition_mp(L,1000,1,h)),places=8)

    def test_seeds_and_precision(self):
        for n in (2,4,8,16):
            for h in (.5,1,1.5,2):
                a=canonical_seed(n,8,h=h,dps=50); b=canonical_seed(n,8,h=h,dps=90)
                self.assertEqual(a['edges'][1]['base_lengths'],[2*n])
                self.assertFalse(a['uniform_family_claim'])
                for p,q in zip(a['edges'],b['edges']):
                    self.assertAlmostEqual(float(p['candidate']),float(q['candidate']),places=14)
                    self.assertTrue(0<float(p['candidate'])<=1+1e-14)
        self.assertTrue(canonical_seed(16,8,h=1.5)['dedicated_entry_candidate'])
        self.assertFalse(canonical_seed(16,8,h=.5)['dedicated_entry_candidate'])

    def test_rational_parameter_strings(self):
        for params in (("1/2","3/2","7/4"),(Fraction(1,2),Fraction(3,2),Fraction(7,4))):
            beta,J,h=params
            self.assertEqual(log_partition(4,beta,J,h),log_partition(4,.5,1.5,1.75))
            self.assertEqual(log_partition_mp(4,beta,J,h),log_partition_mp(4,.5,1.5,1.75))
            self.assertEqual(shifted_partition_mp(4,beta,J,h),shifted_partition_mp(4,.5,1.5,1.75))
        seed=canonical_seed(16,"8/1",J="1/1",h="3/2")
        decimal=canonical_seed(16,8,J=1,h=1.5)
        self.assertEqual(seed['edges'][0]['candidate'],decimal['edges'][0]['candidate'])
        self.assertEqual(seed['h'],"3/2")
        self.assertEqual(replay_candidate(seed)['status'],'NUMERICAL_ENTRY_CANDIDATE')
        for bad in ('1/0','NaN','Infinity','abc',True):
            with self.assertRaises(ValueError): log_partition_mp(4,1,J=bad)

    def test_reject_bad_inputs(self):
        for args in [(1,1),(True,1),(2,-1),(2,math.inf),(2,1,-1),(2,1,1,math.nan)]:
            with self.assertRaises(ValueError): log_partition(*args)
        with self.assertRaises(ValueError): canonical_seed(3,1)
        with self.assertRaises(ValueError): canonical_seed(2,0)
        with self.assertRaises(ValueError): log_partition_mp(2,1,dps=10)

if __name__=='__main__': unittest.main()
