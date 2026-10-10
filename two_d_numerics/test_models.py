import unittest
import numpy as np
import scipy.linalg as la
from models import *
class TestModels(unittest.TestCase):
    def test_edge_counts(self):
        self.assertEqual(len(square(.5,2,4).edges),10)
        self.assertEqual(len(square(.5,2,4,periodic_x=True).edges),14)
        self.assertEqual(len(square(.5,2,4,periodic_x=True,periodic_convention='simple').edges),10)
        c=columnar(.5,2,2,.02,.03)
        self.assertEqual(Counter(e.kind for e in c.edges),{'intracell':4,'strong':4,'transverse':4})
        self.assertEqual(len({tuple(sorted((e.i,e.j))) for e in c.edges}),12)
        self.assertEqual(Counter(e.kind for e in bilayer(.5,2,2,.1,.2).edges),{'rung':4,'inlayer_x':4,'inlayer_y':4})
    def test_spin_pair(self):
        for s in [.5,1.]:
            m=Model(s,2,(Edge(0,1,1.,'pair'),),'pair',{});e,_=full_spectrum(m)
            expected=np.repeat([(j*(j+1)-2*s*(s+1))/2 for j in range(int(2*s)+1)],[2*j+1 for j in range(int(2*s)+1)])
            np.testing.assert_allclose(e,expected,atol=2e-14)
    def test_dense_independent(self):
        for m in [square(.5,2,2,jy=.31),square(.5,2,3,jy=.23,periodic_x=True),square(1.,2,2,jy=.17),columnar(.5,2,2,.02,.03),bilayer(.5,2,2,.1,.2)]:
            H=independent_dense(m);e,sec=full_spectrum(m)
            np.testing.assert_allclose(e,la.eigvalsh(H),atol=1e-12)
            for m2,dim,mult in sec:
                ids,dig=basis(m.spin,m.nsites,m2)
                np.testing.assert_allclose(H[np.ix_(ids,ids)],hamiltonian(m,m2).toarray(),atol=1e-13)
            self.assertAlmostEqual(np.trace(H),0.,places=10)
    def test_large_d_dense(self):
        m=large_d_square(2,2,.02,.03)
        H=independent_dense(m);e,_=full_spectrum(m)
        np.testing.assert_allclose(e,la.eigvalsh(H),atol=1e-12)
        self.assertEqual(sum(abs(e-e[0])<1e-10),1)
    def test_su2(self):
        for m in [square(.5,2,3,jy=.27),square(1.,2,2,jy=.19),columnar(.5,2,2,.02,.03)]:
            for m2 in [0,2]:
                P=raising(m.spin,m.nsites,m2);C=hamiltonian(m,m2+2)@P-P@hamiltonian(m,m2)
                self.assertLess(np.max(abs(C.data),initial=0),2e-13)
    def test_decoupled_dimers(self):
        for s,n,w in [(.5,2,2),(.5,3,1),(1.,2,1)]:
            m=columnar(s,n,w,0.,0.);e,_=full_spectrum(m);ref=np.array([0.])
            pair=np.repeat([(j*(j+1)-2*s*(s+1))/2 for j in range(int(2*s)+1)],[2*j+1 for j in range(int(2*s)+1)])
            for i in range(n*w):ref=np.add.outer(ref,pair).ravel()
            np.testing.assert_allclose(e,np.sort(ref),atol=2e-12)
            self.assertEqual(sum(abs(e-e[0])<1e-10),1);self.assertAlmostEqual(e[1]-e[0],1.,places=11)
    def test_lanczos_tiny(self):
        m=columnar(.5,2,2,.02,.03);low=low_sector(m,0,k=10,dense_cut=0)
        ref=la.eigvalsh(hamiltonian(m,0).toarray())[:10]
        np.testing.assert_allclose(low['eigenvalues'],ref,atol=1e-11);self.assertLess(max(low['residuals']),1e-10)
if __name__=='__main__':unittest.main(verbosity=2)
