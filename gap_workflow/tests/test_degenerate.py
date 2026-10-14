import itertools
import random
import unittest
from fractions import Fraction as F

from gapflow.degenerate import (temporal_defects,
    ising_cycle_pair_polynomial, ising_cycle_uniform_certificate)


class DegenerateTests(unittest.TestCase):
    def test_excited_multiplicity_not_divisible_by_g(self):
        result = temporal_defects(2, [F(1,10)])
        u, v = result['defect'], result['doubled_defect']
        self.assertEqual(u, F(13,147))
        self.assertEqual(v, F(133,13467))
        old = u*u/(2*(1-u)**2)
        self.assertGreater(v, old)
        self.assertGreater(v, 2*old)
        self.assertLessEqual(v, result['quadratic_upper'])

    def test_exact_random_spectra(self):
        rng = random.Random(10830)
        for g in range(1,9):
            for count in range(15):
                xs = [F(rng.randrange(1,100),100) for _ in range(count)]
                result = temporal_defects(g, xs)
                u, v = result['defect'], result['doubled_defect']
                self.assertLessEqual(0, v)
                self.assertLessEqual(v, u)
                self.assertLessEqual(v, result['quadratic_upper'])
                self.assertLessEqual(sum(xs), result['excited_weight_sum_upper'])

    def test_identical_sector_recovers_unique_defect_bound(self):
        for g in (2,3,5):
            xs = [F(1,10),F(1,7),F(2,5)]
            a = temporal_defects(g, xs*g)
            b = temporal_defects(1, xs)
            self.assertEqual(a['defect'], b['defect'])
            self.assertEqual(a['doubled_defect'], b['doubled_defect'])
            u = a['defect']
            self.assertLessEqual(a['doubled_defect'],u*u/(2*(1-u)**2))

    def test_cycle_coefficients_by_enumeration(self):
        for length in range(2,11):
            histogram = [0]*(length+1)
            for spins in itertools.product((-1,1), repeat=length):
                walls = sum(spins[i] != spins[(i+1)%length] for i in range(length))
                histogram[walls] += 1
            coefficients = ising_cycle_pair_polynomial(length)
            self.assertEqual(tuple(histogram), tuple(2*c for c in coefficients))
            self.assertEqual(sum(coefficients), 2**(length-1))
            self.assertEqual(coefficients[0], 1)
            self.assertEqual(coefficients[1], 0)
            self.assertGreater(coefficients[2], 0)
            for t in (F(1,10), F(1,2), F(9,10)):
                a = sum(c*t**k for k,c in enumerate(coefficients))
                self.assertEqual(a, ((1+t)**length+(1-t)**length)/2)

    def test_rescaled_spatial_ratio_exceeds_one(self):
        t, length = F(1,2), 4
        z = lambda n: (1+t)**n+(1-t)**n
        spatial = z(2*length)/z(length)**2
        self.assertLessEqual(spatial, 1)
        self.assertGreater(2*spatial, 1)

    def test_longitudinal_field_preserves_u1_removes_degeneracy(self):
        # Exact diagonal energies; all longitudinal terms commute with Mz.
        j = F(3,2)
        for length in range(2,9):
            for h in (F(1,10), F(1), F(3)):
                energies = []
                for spins in itertools.product((-1,1), repeat=length):
                    e = -j*sum(spins[i]*spins[(i+1)%length]
                               for i in range(length))/4-h*sum(spins)/2
                    energies.append(e)
                energies.sort()
                self.assertEqual(energies.count(energies[0]), 1)
                self.assertEqual(energies[0], -length*(j/4+h/2))
                self.assertEqual(energies[1]-energies[0], min(h*length,j+h))

    def test_graph_state_lacks_physical_u1(self):
        # Sparse exact real matrices: [H,Mz]_(a,b)=H_(a,b)*(m_b-m_a).
        # Each stabilizer flips exactly its own bit, so no off-diagonal
        # term can cancel another generator's term at the same entry.
        for n,edges in ((1,[]),(2,[(0,1)]),(3,[(0,1),(1,2),(2,0)])):
            neighbors = [set() for _ in range(n)]
            for a,b in edges:
                neighbors[a].add(b)
                neighbors[b].add(a)
            commutator_entries = []
            for b in range(2**n):
                mb = F(n-2*b.bit_count(),2)
                for i in range(n):
                    a = b^(1<<i)
                    ma = F(n-2*a.bit_count(),2)
                    phase = (-1)**sum((b>>k)&1 for k in neighbors[i])
                    hab = -F(phase,2)
                    commutator_entries.append(hab*(mb-ma))
            self.assertTrue(all(x != 0 for x in commutator_entries))

    def test_uniform_certificate_and_validation(self):
        self.assertEqual(ising_cycle_uniform_certificate('3/2')['gap_above_ground_space'], '3/2')
        for g,xs in [(0,[]),(True,[]),(2,[0]),(2,[1]),(2,[.5]),(2,[-1])]:
            with self.assertRaises(ValueError): temporal_defects(g,xs)
        for length in (1,True,2.0):
            with self.assertRaises(ValueError): ising_cycle_pair_polynomial(length)
        for j in (0,-1,.5,True,'bad'):
            with self.assertRaises(ValueError): ising_cycle_uniform_certificate(j)


if __name__ == '__main__':
    unittest.main()
