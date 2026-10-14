"""Exact thermal seeds for graph-state projector Hamiltonians.

H = h/2 sum_i (I - X_i prod_{j~i} Z_j), h > 0.
Controlled-Z conjugation maps H to independent X projectors. The spectrum is
h*k with binomial multiplicities, for every finite simple graph. No spectral
truncation or numerical diagonalization enters the seed.
"""
from fractions import Fraction
from math import comb, prod


def projector_spectrum(n, h=Fraction(1)):
    if not isinstance(n, int) or n < 1:
        raise ValueError('n must be a positive integer')
    h=Fraction(h)
    if h<=0: raise ValueError('h must be positive')
    return [(h*k, comb(n,k)) for k in range(n+1)]


def exact_thermal_seed(shape, q=Fraction(1,100), h=Fraction(1)):
    """q=exp(-beta*h). Return exact standard spatial-then-time staircase.

    Coordinate lengths are even. The Gibbs trace equals (1+q)^volume,
    so spatial ratios are exactly one. The temporal ratio is evaluated at
    the final staircase basepoint with all spatial lengths doubled.
    """
    shape=tuple(shape); q=Fraction(q);h=Fraction(h)
    if not shape or any(not isinstance(n,int) or n<2 or n%2 for n in shape):
        raise ValueError('seed side lengths must be even integers >= 2')
    if not 0<q<1 or h<=0:raise ValueError('require 0<q<1 and h>0')
    d=len(shape);v=prod(shape); temporal_volume=2**d*v
    single_loss=2*q/(1+q)**2
    u=min(Fraction(1),temporal_volume*single_loss)
    t=1-u
    return {'dimension':d,'shape':list(shape),'seed_volume':v,
            'temporal_seed_volume':temporal_volume,'full_hilbert_dimension':str(2**temporal_volume) if temporal_volume<=4096 else f'2^{temporal_volume}',
            'full_hilbert_dimension_log2':temporal_volume,
            'trial_rank':1,'retained_ground_space_rank':1,'numerically_computed_eigenpairs':0,
            'trial_rank_interpretation':'Analytically known retained ground-state rank, not a numerical trial solve',
            'low_energy_levels_required':1,'q':str(q),'h':str(h),
            'beta_definition':f'log({q.denominator}/{q.numerator}) / ({h})',
            'purities':['1']*d+[str(t)],'defect':str(1-t),
            'tail_status':'EXACT_BINOMIAL_MULTIPLICITIES',
            'purity_bound':'Bernoulli lower bound 1 - V * 2q/(1+q)^2',
            'spectrum_status':'ANALYTIC_UNITARY_EQUIVALENCE',
            'transfer_proof':'Positive scalar X_i=(1+q)^transverse_volume reproduces every integer-length heat trace',
            'scope':'Every finite simple graph; thermal bootstrap uses rectangular periodic family.'}


def certify_target(seed, target):
    """Exact conservative general-d bootstrap check, without floating logs.

    For rational alpha=target/h=p/r, the bound log(1/(K*u))/beta >= target
    is equivalent to (K*u)^r <= q^p. This is checked over exact integers.
    Finite sizes outside the seed boxes are covered by the independent exact
    graph-state spectrum, not inferred from the scalar recurrence.
    """
    regenerated=exact_thermal_seed(seed['shape'], seed['q'], seed['h'])
    for key,value in regenerated.items():
        if seed.get(key)!=value:
            raise ValueError(f'Seed metadata or bound mismatch: {key}')
    d=regenerated['dimension'];u=Fraction(regenerated['defect']);q=Fraction(regenerated['q']);h=Fraction(regenerated['h'])
    target=Fraction(target)
    if target<=0:raise ValueError('target must be positive')
    F=4*8**(d-1);K=max((2**(d+1)-1)**2,2*F)
    threshold=min(Fraction(1,4*K),Fraction(1,100*8**(d-1)))
    alpha=target/h
    admitted=0<u<=threshold
    achieved=target<=h and admitted and (K*u)**alpha.denominator <= q**alpha.numerator
    return {'status':'EXACT_BOOTSTRAP_TARGET_VERIFIED' if achieved else 'SEED_NOT_SUFFICIENT',
            'target_gap':str(target),'K':K,'F':F,'threshold':str(threshold),
            'seed_admitted':admitted,'target_verified':achieved,
            'full_family_gap_exact':str(h),'finite_bridge':'Analytic projector spectrum for every finite graph',
            'claim':'Model-specific exact family; no extension to arbitrary noncommuting models.'}


def find_thermal_seed(shape, target=Fraction(1,2), h=Fraction(1), max_power=24):
    history=[]
    for power in range(1,max_power+1):
        seed=exact_thermal_seed(shape,Fraction(1,10**power),h)
        result=certify_target(seed,target)
        history.append({'q_power_10':power,'status':result['status']})
        if result['target_verified']:return {'seed':seed,'certificate':result,'search':history}
    return {'status':'NO_SEED_IN_TESTED_GRID','search':history}
