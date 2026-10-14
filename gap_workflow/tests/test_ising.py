import itertools
import math
import random
import unittest
from fractions import Fraction as F
from gapflow.ising import weighted_min_cut, diagnose_ising_obstruction
from gapflow.model import Model


def direct_energies(n, edges):
    return [sum((-F(w)*s[i]*s[j]/4 for i,j,w in edges), F(0))
            for s in itertools.product((-1, 1), repeat=n)]


class IsingTests(unittest.TestCase):
    def check_graph(self, n, edges):
        energies = sorted(direct_energies(n, edges))
        result = diagnose_ising_obstruction(n, edges)
        self.assertEqual(energies.count(energies[0]), 2)
        self.assertEqual(F(result['ground_energy']), energies[0])
        self.assertEqual(F(result['gap_above_ground_space']),
                         next(e for e in energies if e > energies[0])-energies[0])
        cut, side = weighted_min_cut(n, edges)
        self.assertEqual(cut, sum((F(w) for i,j,w in edges if (i in side) != (j in side)), F(0)))
        self.assertTrue(result['entry_impossible'])
        for beta in (0, .1, 1, 10, 1000):
            weights = [math.exp(-beta*float(e-energies[0])) for e in energies]
            purity = sum(w*w for w in weights)/sum(weights)**2
            self.assertLessEqual(purity, .5 + 1e-14)
        return result

    def test_dimer_parallel_and_fraction_weights(self):
        r = self.check_graph(2, [(0,1,'1/3'),(1,0,'2/7')])
        self.assertEqual(r['gap_above_ground_space'], '13/42')

    def test_random_connected_graphs_against_full_diagonal(self):
        rng = random.Random(914)
        for n in range(2, 9):
            for _ in range(12):
                edges = [(i-1,i,F(rng.randint(1,9),rng.randint(1,7))) for i in range(1,n)]
                edges += [(i,j,F(rng.randint(1,9),rng.randint(1,7)))
                          for i in range(n) for j in range(i+1,n) if rng.random()<.35]
                self.check_graph(n, edges)

    def test_model_exact_matrix_crosscheck(self):
        edges = [(0,1,F(1,3)),(1,2,F(2)),(2,0,F(5,7)),(1,0,F(1,5))]
        model = Model.from_dict({'spin':.5, 'geometry':{'type':'graph','n_sites':3,'edges':[]},
            'terms':[{'type':'xxz','sites':[i,j],'Jxy':0,'Jz':str(-w)} for i,j,w in edges]})
        matrix = model.exact_hamiltonian()
        self.assertEqual(sorted(matrix[i][i] for i in range(8)), sorted(direct_energies(3,edges)))
        self.assertTrue(all(matrix[i][j] == 0 for i in range(8) for j in range(8) if i != j))

    def test_cycles_and_finite_tori(self):
        for n in range(2,9):
            result=self.check_graph(n, [(i,(i+1)%n,F(3,2)) for i in range(n)])
            self.assertEqual(result['gap_above_ground_space'], '3/2')
        for shape in ([2,2],[2,3],[2,2,2]):
            model=Model.from_dict({'spin':.5,'geometry':{'type':'lattice','shape':shape,'periodic':True},
                                   'terms':[{'type':'xxz','Jxy':0,'Jz':-1}]})
            self.check_graph(model.n_sites,[(i,j,1) for i,j in model.edges])

    def test_invalid_inputs(self):
        for n,edges in [(1,[]),(True,[]),(3,[(0,1,1)]),(2,[]),(2,[(0,0,1)]),
                        (2,[(0,2,1)]),(2,[(0,1,0)]),(2,[(0,1,-1)]),
                        (2,[(0,1,.5)]),(2,[(0,1,True)]),(2,[(0,1,'nan')]),
                        (2,[(0,1,'1/0')]),(2,[(0,1)]),(2,[(False,1,1)])]:
            with self.subTest(n=n,edges=edges), self.assertRaises(ValueError):
                diagnose_ising_obstruction(n,edges)
        for threshold in (0,2,True,.9):
            with self.assertRaises(ValueError):
                diagnose_ising_obstruction(2,[(0,1,1)],threshold)
        self.assertFalse(diagnose_ising_obstruction(2,[(0,1,1)],'1/2')['entry_impossible'])


if __name__ == '__main__':
    unittest.main()
