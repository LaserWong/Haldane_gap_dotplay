"""Exact rational enclosures for dyadic periodic TFI partition seeds.

No floating-point value is a proof input; no many-body spectrum is allocated.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt
from functools import lru_cache
from .bootstrap import rational, bootstrap_certificate, canonical_edges


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F

    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError('Reversed interval')

    def record(self):
        return {'lower': str(self.lo), 'upper': str(self.hi)}


class RationalIntervals:
    """Each arithmetic operation rounds outward onto denominator 10**digits."""
    def __init__(self, digits=50):
        if type(digits) is not int or not 20 <= digits <= 100:
            raise ValueError('digits must be an integer from 20 to 100')
        self.digits, self.scale = digits, 10**digits
        n, tail = 0, F(1)
        while 2*tail > F(1, self.scale):
            n += 1
            tail /= 2*n
        self.degree = n-1

    def point(self, x):
        x = rational(x)
        return Interval(x, x)

    def box(self, lo, hi):
        D = self.scale
        return Interval(F((lo.numerator*D)//lo.denominator, D),
                        F(-((-hi.numerator*D)//hi.denominator), D))

    def add(self, x, y):
        return self.box(x.lo+y.lo, x.hi+y.hi)

    def neg(self, x):
        return Interval(-x.hi, -x.lo)

    def sub(self, x, y):
        return self.add(x, self.neg(y))

    def mul(self, x, y):
        ends = [x.lo*y.lo, x.lo*y.hi, x.hi*y.lo, x.hi*y.hi]
        return self.box(min(ends), max(ends))

    def div(self, x, y):
        if y.lo <= 0 <= y.hi:
            raise ValueError('Divisor contains zero; increase precision')
        return self.mul(x, self.box(1/y.hi, 1/y.lo))

    def sqrt(self, x):
        if x.lo < 0:
            raise ValueError('Square root interval must be nonnegative')
        D = self.scale
        low = isqrt(x.lo.numerator*D*D//x.lo.denominator)
        high = isqrt(x.hi.numerator*D*D//x.hi.denominator)
        if F(high*high, D*D) < x.hi:
            high += 1
        return Interval(F(low,D), F(high,D))

    def _exp_point(self, x):
        if abs(x) > 4096:
            raise ValueError('Exponent resource cap exceeded')
        if x < 0:
            return self.div(self.point(1), self._exp_point(-x))
        r, squarings = x, 0
        while r > F(1,2):
            r /= 2
            squarings += 1
        term = total = self.point(1)
        for k in range(1, self.degree+1):
            term = self.mul(term, self.point(r/k))
            total = self.add(total, term)
        # For r<=1/2 successive omitted terms have ratio <=1/2.
        following = self.mul(term, self.point(r/(self.degree+1)))
        total = self.box(total.lo, total.hi+2*following.hi)
        for _ in range(squarings):
            total = self.mul(total,total)
        return total

    def exp(self, x):
        return Interval(self._exp_point(x.lo).lo, self._exp_point(x.hi).hi)

    @lru_cache(maxsize=1024)
    def cos_dyadic(self, m, p):
        """cos(pi*m/2**p), using exact symmetry and positive half angles."""
        if type(m) is not int or type(p) is not int or not 0 <= p <= 8:
            raise ValueError('Integer dyadic angle with 0<=p<=8 required')
        denominator = 1 << p
        m %= 2*denominator
        if m > denominator:
            m = 2*denominator-m
        if m == 0:
            return self.point(1)
        if m == denominator:
            return self.point(-1)
        if 2*m == denominator:
            return self.point(0)
        if 2*m > denominator:
            return self.neg(self.cos_dyadic(denominator-m,p))
        return self.sqrt(self.mul(self.point(F(1,2)),
                                 self.add(self.point(1),self.cos_dyadic(m,p-1))))


def _parameters(L,beta,J,h):
    if type(L) is not int or L < 2 or L > 128 or L & (L-1):
        raise ValueError('L must be a power of two from 2 to 128')
    beta,J,h = map(rational,(beta,J,h))
    if beta < 0 or J < 0:
        raise ValueError('Require beta>=0 and J>=0')
    return beta,J,abs(h)


def mode_intervals(L,J,h,ctx):
    """NS then R one-particle energies, each list of length L."""
    _,J,h = _parameters(L,0,J,h)
    p = L.bit_length()-1
    sectors=[]
    for ns in (1,0):
        modes=[]
        for m in range(L):
            c=ctx.cos_dyadic(2*m+ns,p)
            # (J-h)^2+2Jh(1-c) stays manifestly nonnegative.
            rad=ctx.add(ctx.point((J-h)**2),ctx.mul(ctx.point(2*J*h),
                       ctx.sub(ctx.point(1),c)))
            modes.append(ctx.mul(ctx.point(2),ctx.sqrt(rad)))
        sectors.append(modes)
    return sectors


def shifted_partition(L,beta,J=1,h=1,shift=0,digits=50,ctx=None,modes=None):
    """Enclose exp(-beta*shift*L) Z(L,beta), preserving both parity sectors."""
    beta,J,h = _parameters(L,beta,J,h)
    shift=rational(shift)
    ctx=ctx or RationalIntervals(digits)
    modes=modes or mode_intervals(L,J,h,ctx)
    sectors=[]
    for index, energies in enumerate(modes):
        even,odd,total = ctx.point(1),ctx.point(0),ctx.point(0)
        for eps in energies:
            weight=ctx.exp(ctx.mul(ctx.point(-beta),eps))
            even,odd=(ctx.add(even,ctx.mul(odd,weight)),
                      ctx.add(odd,ctx.mul(even,weight)))
            total=ctx.add(total,eps)
        selected=even if index==0 or h<J else odd
        exponent=ctx.mul(ctx.point(beta),ctx.sub(ctx.mul(ctx.point(F(1,2)),total),
                                                    ctx.point(shift*L)))
        sectors.append(ctx.mul(ctx.exp(exponent),selected))
    return ctx.add(*sectors)


def canonical_seed_interval(n,beta,J=1,h=1,digits=50):
    """Certified rational seeds plus conditional exact scalar bootstrap replay."""
    beta,J,h=_parameters(n,beta,J,h)
    if n>64 or beta<=0:
        raise ValueError('Seed requires n<=64 and beta>0')
    ctx=RationalIntervals(digits)
    small=mode_intervals(n,J,h,ctx)
    large=mode_intervals(2*n,J,h,ctx)
    density=ctx.div(_sum_intervals(large[0],ctx),ctx.point(4*n))
    shift=(density.lo+density.hi)/2
    z1=shifted_partition(n,beta,J,h,shift,ctx=ctx,modes=small)
    z2=shifted_partition(2*n,beta,J,h,shift,ctx=ctx,modes=large)
    z3=shifted_partition(2*n,2*beta,J,h,shift,ctx=ctx,modes=large)
    s=ctx.div(z2,ctx.mul(z1,z1))
    t=ctx.div(z3,ctx.mul(z2,z2))
    edges=canonical_edges([n],beta,[s.lo,t.lo])
    replay=bootstrap_certificate({'dimension':1,'lengths':[n],'beta':str(beta),
        'digits':min(digits,100),'edges':edges,'mode':'dedicated',
        'model_to_seed_proof':{'verified':True,'evidence':[
            'theory/QUANTUM_ISING_INTERVAL.md','theory/TRANSFER_ELIGIBILITY.md']}})
    return {'family':'periodic_quantum_ising','n':n,'beta':str(beta),'J':str(J),'h':str(h),
        'precision_digits':digits,'shift_per_site':str(shift),
        'shifted_partition_intervals':[x.record() for x in (z1,z2,z3)],
        'purity_intervals':[s.record(),t.record()],'edges':edges,'bootstrap':replay,
        'evidence_class':'EXACT_RATIONAL_PARTITION_SEED_ENCLOSURES',
        'partition_formula_scope':'periodic positive-direction bonds, including doubled L=2 bond',
        'physical_transfer_reference':'theory/TRANSFER_ELIGIBILITY.md',
        'small_size_bridge_verified':False,'uniform_family_claim':False,
        'scope':'Certified finite partition seeds; scalar bootstrap conditional on independent physical proof review; no L<n bridge',
        'many_body_eigenpairs_computed':0,'distinct_single_particle_modes_enclosed':6*n,
        'single_particle_mode_visits_partition':10*n}


def _sum_intervals(values,ctx):
    total=ctx.point(0)
    for value in values:
        total=ctx.add(total,value)
    return total
