import itertools
import unittest
from fractions import Fraction as F
from gapflow.classical_seed import analytic_thermal_seed,certify_target,find_thermal_seed


def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transfer_and_enumeration(width,length):
    states=list(itertools.product((0,1),repeat=width))
    def onsite(a):
        return 2*sum(a)+(sum(2*(a[k]!=a[(k+1)%width]) for k in range(width)) if width>1 else 0)
    def cross(a,b):return sum(2*(x!=y) for x,y in zip(a,b))
    t=[[F(1,2)**(onsite(a)//2+cross(a,b)+onsite(b)//2) for b in states] for a in states]
    power=[[F(int(i==j)) for j in range(len(states))] for i in range(len(states))]
    for _ in range(length):power=mm(power,t)
    tr=sum(power[i][i] for i in range(len(states)))
    explicit=F(0)
    for columns in itertools.product(states,repeat=length):
        energy=sum(onsite(a) for a in columns)+sum(cross(columns[i],columns[(i+1)%length]) for i in range(length))
        explicit+=F(1,2)**energy
    return t,tr,explicit


class ClassicalSeedTests(unittest.TestCase):
    def test_exact_transfer_identity(self):
        for width in (1,2):
            for length in (2,3,4,5):
                t,tr,z=transfer_and_enumeration(width,length)
                self.assertEqual(t,[list(x) for x in zip(*t)])
                self.assertEqual(tr,z)

    def test_counted_bound_and_gap_not_exact(self):
        q=F(1,3)
        for n in (2,3,4,6):
            z=F(0);energies=[]
            for bits in itertools.product((0,1),repeat=n):
                energy=sum(bits)+sum(2*(bits[i]!=bits[(i+1)%n]) for i in range(n))
                self.assertGreaterEqual(energy,sum(bits))
                energies.append(energy);z+=q**energy
            self.assertGreaterEqual(z,1)
            self.assertLessEqual(z,(1+q)**n)
            self.assertGreater(min(x for x in energies if x>0),1)

    def test_purity_lower_bound(self):
        for d in (1,2,3):
            seed=analytic_thermal_seed([2]*d,F(1,10000))
            v=seed['temporal_seed_volume'];q=F(seed['q'])
            self.assertLessEqual(F(seed['purities'][0]),(1+q)**(-2*v))

    def test_all_dimensions_and_strong_coupling(self):
        for d in range(1,7):
            result=find_thermal_seed([2]*d,J=10**20)
            self.assertTrue(result['certificate']['target_verified'])
            self.assertEqual(result['seed']['numerically_computed_eigenpairs'],0)
            self.assertFalse(result['certificate']['physical_gap_is_claimed_exact'])

    def test_tamper_and_invalid(self):
        seed=analytic_thermal_seed([2]);seed['defect']='1/100000000000000'
        with self.assertRaises(ValueError):certify_target(seed,F(1,2))
        for shape,q,j,h in [([3],F(1,10),1,1),([2],0,1,1),([2],1,1,1),([2],F(1,10),-1,1),([2],F(1,10),1,0)]:
            with self.assertRaises(ValueError):analytic_thermal_seed(shape,q,j,h)
        self.assertFalse(certify_target(analytic_thermal_seed([2],F(1,10)),F(1,2))['target_verified'])
        self.assertFalse(certify_target(analytic_thermal_seed([2],F(1,10**20)),1)['target_verified'])

if __name__=='__main__':unittest.main()
