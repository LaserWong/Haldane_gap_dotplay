import unittest
from fractions import Fraction
from math import comb
import numpy as np
from gapflow.stabilizer import exact_thermal_seed, certify_target, find_thermal_seed


def graph_state_twice_h(n, edges):
    D=2**n;H=n*np.eye(D,dtype=np.int64);H0=H.copy();phase=np.ones(D,dtype=np.int64)
    neighbors=[set() for _ in range(n)]
    for a,b in edges:neighbors[a].add(b);neighbors[b].add(a)
    for x in range(D):
        phase[x]=(-1)**sum(((x>>a)&1)*((x>>b)&1) for a,b in edges)
        for a in range(n):
            y=x^(1<<a);H0[y,x]-=1
            H[y,x]-=(-1)**sum((x>>b)&1 for b in neighbors[a])
    return H,H0,phase

class StabilizerTests(unittest.TestCase):
    def test_exact_unitary_and_float_spectrum(self):
        for n,edges in [(4,[(0,1),(1,2),(2,3),(3,0)]),
                        (4,[(0,1),(0,2),(1,3),(2,3)]),
                        (8,[(i,i^(1<<a)) for i in range(8) for a in range(3) if i<(i^(1<<a))])]:
            H,H0,phase=graph_state_twice_h(n,edges)
            self.assertTrue(np.array_equal(H,phase[:,None]*H0*phase[None,:]))
            self.assertTrue(np.array_equal(H@phase,np.zeros(2**n,dtype=np.int64)))
            expected=np.repeat(np.arange(n+1),[comb(n,k) for k in range(n+1)])
            np.testing.assert_allclose(np.linalg.eigvalsh(H/2),expected,atol=1e-12)
    def test_bernoulli_lower_purity(self):
        for d in range(1,4):
            s=exact_thermal_seed([2]*d,Fraction(1,10000))
            q=Fraction(s['q']);v=s['temporal_seed_volume']
            exact=((1+q*q)/(1+q)**2)**v
            self.assertLessEqual(Fraction(s['purities'][-1]),exact)
    def test_exact_targets_d1_through_d6(self):
        for d in range(1,7):
            r=find_thermal_seed([2]*d)
            self.assertTrue(r['certificate']['target_verified'])
            self.assertEqual(r['seed']['trial_rank'],1)
    def test_tampered_seed_rejected(self):
        s=exact_thermal_seed([2]);s['defect']='1/'+str(10**100)
        with self.assertRaises(ValueError):certify_target(s,2)
        s=exact_thermal_seed([2]);s['dimension']=3
        with self.assertRaises(ValueError):certify_target(s,Fraction(1,2))

    def test_bad_seeds_fail(self):
        s=exact_thermal_seed([2,2],Fraction(1,10))
        self.assertFalse(certify_target(s,Fraction(1,2))['target_verified'])
        with self.assertRaises(ValueError):exact_thermal_seed([3])
        with self.assertRaises(ValueError):exact_thermal_seed([2],Fraction(0))

if __name__=='__main__':unittest.main()
