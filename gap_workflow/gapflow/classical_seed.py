"""Exact counted seeds for pinned ferromagnetic classical Ising families.

H = J/2 sum_edges (1-Z_i Z_j) + h/2 sum_i (1-Z_i), J>=0, h>0.
Z_i has eigenvalues +/-1. Periodic directions retain both length-two bonds.
The analytic physical gap is at least h, and need not equal h when J>0.
"""
from fractions import Fraction
from math import prod


def analytic_thermal_seed(shape, q=Fraction(1, 100), J=Fraction(1), h=Fraction(1)):
    """Return complete rational seed metadata, with q=exp(-beta*h)."""
    shape=tuple(shape)
    if not shape or any(type(n) is not int or n<2 or n%2 for n in shape):
        raise ValueError('seed lengths must be even integers >= 2')
    if any(isinstance(x,bool) for x in (q,J,h)):
        raise ValueError('q, J and h must be rational numbers, not booleans')
    q,J,h=Fraction(q),Fraction(J),Fraction(h)
    if not 0<q<1 or J<0 or h<=0:
        raise ValueError('require 0<q<1, J>=0 and h>0')
    d=len(shape)
    volume=prod(shape)
    terminal_volume=2**d*volume
    defect=min(Fraction(1),2*terminal_volume*q)
    return {
        'family':'pinned_ferromagnetic_ising', 'dimension':d, 'shape':list(shape),
        'J':str(J),'h':str(h),'q':str(q),
        'seed_volume':volume,'temporal_seed_volume':terminal_volume,
        'bond_convention':'positive_direction_multigraph',
        'beta_definition':f'log({q.denominator}/{q.numerator}) / ({h})',
        'full_hilbert_dimension_log2':terminal_volume,
        'retained_ground_space_rank':1,'trial_rank':1,
        'trial_rank_interpretation':'Analytically known retained ground state, no numerical trial solve',
        'numerically_computed_eigenpairs':0,
        'purities':[str(1-defect)]*(d+1),'defect':str(defect),
        'tail_status':'EXACT_COUNTED_COMPARISON_BOUND',
        'trace_bound':'1 <= Z(beta) <= (1+q)^N from E(configuration) >= h * flipped_spin_count',
        'purity_bound':'P >= (1+q)^(-2 * temporal_seed_volume) >= 1 - 2 * temporal_seed_volume * q',
        'transfer_proof':'Exact real symmetric classical column transfer for symmetric nearest-neighbor bond tables',
        'analytic_gap_lower_bound':str(h),
        'ground_multiplicity':1,
        'scope':'Homogeneous periodic rectangular Ising family in any spatial dimension; analytic gap lower bound holds on every finite graph with nonnegative bonds.'}


def certify_target(seed, target):
    """Verify the canonical seed and exact rational bootstrap target."""
    if not isinstance(seed,dict):
        raise ValueError('seed must be a canonical analytic seed dictionary')
    try:
        expected=analytic_thermal_seed(seed['shape'],seed['q'],seed['J'],seed['h'])
    except (KeyError,TypeError,ValueError,ZeroDivisionError) as error:
        raise ValueError('invalid analytic seed metadata') from error
    if seed!=expected:
        raise ValueError('seed metadata does not match its exact analytic reconstruction')
    if isinstance(target,bool):
        raise ValueError('target must be positive rational')
    target=Fraction(target)
    if target<=0:
        raise ValueError('target must be positive rational')
    d=seed['dimension'];u=Fraction(seed['defect']);q=Fraction(seed['q']);h=Fraction(seed['h'])
    F=4*8**(d-1)
    K=max((2**(d+1)-1)**2,2*F)
    threshold=min(Fraction(1,4*K),Fraction(1,100*8**(d-1)))
    alpha=target/h
    admitted=0<u<=threshold
    verified=admitted and (K*u)**alpha.denominator<=q**alpha.numerator
    return {'status':'EXACT_BOOTSTRAP_TARGET_VERIFIED' if verified else 'SEED_NOT_SUFFICIENT',
            'seed_admitted':admitted,'target_verified':verified,'target_gap':str(target),
            'K':K,'F':F,'threshold':str(threshold),'analytic_gap_lower_bound':str(h),
            'physical_gap_is_claimed_exact':False,
            'finite_bridge':'E(configuration) >= h * flipped_spin_count on every finite graph',
            'claim':'Model-specific analytic comparison benchmark, not a new Ising gap theorem.'}


def find_thermal_seed(shape, target=Fraction(1,2), J=Fraction(1), h=Fraction(1), max_power=24):
    """Search q=10^-power. First success is only minimal on this tested grid."""
    if type(max_power) is not int or max_power<1:
        raise ValueError('max_power must be a positive integer')
    history=[]
    for power in range(1,max_power+1):
        seed=analytic_thermal_seed(shape,Fraction(1,10**power),J,h)
        result=certify_target(seed,target)
        history.append({'q_power_10':power,'status':result['status']})
        if result['target_verified']:
            return {'seed':seed,'certificate':result,'search':history}
    return {'status':'NO_SEED_IN_TESTED_GRID','search':history}
