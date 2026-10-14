"""Exact arithmetic invariants and independent non-proof numerical checks."""
from fractions import Fraction as F
import unittest
import mpmath as mp
from gapflow.quantum_ising_interval import (
    RationalIntervals, Interval, shifted_partition, canonical_seed_interval)
from gapflow.quantum_ising import log_partition_mp


def mpf(x,ctx):
    return ctx.mpf(x.numerator)/x.denominator


class QuantumIsingIntervalTests(unittest.TestCase):
    def setUp(self):
        self.ctx=RationalIntervals(50)
        self.mp=mp.mp.clone(); self.mp.dps=100

    def assertEncloses(self,box,value):
        self.assertLessEqual(mpf(box.lo,self.mp),value)
        self.assertGreaterEqual(mpf(box.hi,self.mp),value)

    def test_sqrt_exact_inequalities(self):
        for x in (F(0),F(1),F(2),F(1,3),F(10**20+7,11)):
            box=self.ctx.sqrt(self.ctx.point(x))
            self.assertLessEqual(box.lo**2,x)
            self.assertGreaterEqual(box.hi**2,x)
            self.assertLessEqual(box.hi-box.lo,F(1,10**50))

    def test_all_dyadic_cosines(self):
        for p in range(1,8):
            for m in range(2*(1<<p)):
                box=self.ctx.cos_dyadic(m,p)
                # Exact known zeros avoid transcendental roundoff at pi/2.
                if 2*m % (2*(1<<p)) == (1<<p):
                    self.assertEqual(box,Interval(F(0),F(0)))
                else:
                    self.assertEncloses(box,self.mp.cos(self.mp.pi*m/(1<<p)))

    def test_exponentials_and_interval_operations(self):
        for x in (F(-200),F(-1,3),F(0),F(1,9),F(1),F(100)):
            self.assertEncloses(self.ctx.exp(self.ctx.point(x)),self.mp.exp(mpf(x,self.mp)))
        a=Interval(F(-3),F(2)); b=Interval(F(-4),F(5))
        self.assertEqual(self.ctx.mul(a,b),Interval(F(-15),F(12)))
        with self.assertRaises(ValueError): self.ctx.div(a,b)

    def test_partition_parities_critical_and_decoupled(self):
        for L in (2,4,8):
            for J,h in ((1,'3/2'),(1,'1/2'),(1,1),(0,1),(1,0),(1,'-3/2'),(0,0)):
                for beta in (0,1,8):
                    shift=F(J)+abs(F(h))
                    box=shifted_partition(L,beta,J,h,shift=shift,digits=60)
                    log=log_partition_mp(L,beta,J,str(float(F(h))),dps=100)
                    value=self.mp.exp(log-mpf(shift,self.mp)*beta*L)
                    # beta=0 is exactly 2**L; mp exp(log(integer)) may round.
                    if beta==0 or J==0 and F(h)==0: value=self.mp.mpf(2)**L
                    self.assertEncloses(box,value)

    def test_target_seed_and_bootstrap(self):
        c=canonical_seed_interval(16,8,1,'3/2',digits=50)
        logs=[log_partition_mp(L,b,1,'1.5',dps=100) for L,b in ((16,8),(32,8),(32,16))]
        for record,value in zip(c['purity_intervals'],
                (self.mp.exp(logs[1]-2*logs[0]),self.mp.exp(logs[2]-2*logs[1]))):
            self.assertEncloses(Interval(F(record['lower']),F(record['upper'])),value)
            self.assertLess(F(record['upper'])-F(record['lower']),F(1,10**40))
        self.assertEqual(c['bootstrap']['gap_lower'],str(F('0.484734263212')))
        self.assertEqual(c['bootstrap']['status'],'VERIFIED_CONDITIONAL')
        self.assertFalse(c['uniform_family_claim'])
        self.assertFalse(c['small_size_bridge_verified'])
        self.assertEqual(c['many_body_eigenpairs_computed'],0)

    def test_independent_hyperbolic_product_target(self):
        # Algebraically different from the positive parity recurrence, numerical only.
        c=canonical_seed_interval(16,8,1,'3/2')
        shift=mpf(F(c['shift_per_site']),self.mp)
        for (L,beta),record in zip(((16,8),(32,8),(32,16)),c['shifted_partition_intervals']):
            products=[]
            for s in (self.mp.mpf('0.5'),self.mp.mpf(0)):
                eps=[2*self.mp.sqrt(self.mp.mpf('3.25')-3*self.mp.cos(2*self.mp.pi*(m+s)/L)) for m in range(L)]
                products.append((self.mp.fprod(2*self.mp.cosh(beta*e/2) for e in eps),
                                 self.mp.fprod(2*self.mp.sinh(beta*e/2) for e in eps)))
            z=(products[0][0]+products[0][1]+products[1][0]-products[1][1])/2
            value=z*self.mp.exp(-beta*shift*L)
            self.assertEncloses(Interval(F(record['lower']),F(record['upper'])),value)

    def test_common_shift_cancellation(self):
        n,b=4,2
        ratios=[]
        for shift in (0,F(7,4),F(5,2)):
            a=shifted_partition(n,b,1,'3/2',shift=shift)
            c=shifted_partition(2*n,b,1,'3/2',shift=shift)
            ratios.append(self.ctx.div(c,self.ctx.mul(a,a)))
        self.assertLessEqual(max(x.lo for x in ratios),min(x.hi for x in ratios))

    def test_exact_inputs_and_budget_rejected(self):
        for n in (True,3,128):
            with self.assertRaises(ValueError): canonical_seed_interval(n,8,1,'3/2')
        for args in ((16,8.0,1,'3/2'),(16,8,1.0,'3/2'),(16,8,1,1.5),(16,0,1,1)):
            with self.assertRaises(ValueError): canonical_seed_interval(*args)
        with self.assertRaises(ValueError): RationalIntervals(10)
        with self.assertRaises(ValueError): self.ctx.exp(self.ctx.point(4097))


if __name__=='__main__': unittest.main()
