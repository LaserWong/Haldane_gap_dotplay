"""Permanent obstruction for one conservative analytic Hoeffding seed family.

This bounds the seed estimate, not the physical partition-function ratios or gap.
All certification comparisons use outward rational arithmetic.
"""
from fractions import Fraction as F

THRESHOLD = F(2, 5)  # (1 + 2/5)^2 < 2 proves 2/5 < sqrt(2)-1.


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, str, F)):
        raise ValueError('Use exact rational strings or integers')
    return F(value)


def down(value, digits=40):
    scale = 10**digits
    return F(value.numerator*scale//value.denominator, scale)


def up(value, digits=40):
    return -down(-value, digits)


def exp_negative_bounds(x):
    """Enclose exp(-x) for 0 <= x <= 16 using a positive Taylor remainder."""
    x = rational(x)
    if not 0 <= x <= 16:
        raise ValueError('Exponential argument must be in [0,16]')
    terms = 128
    term = total = F(1)
    for k in range(1, terms+1):
        term *= x/k
        total += term
    first = term*x/(terms+1)
    upper = total + first/(1-x/(terms+2))
    return down(1/upper), up(1/total)


def split_bound(model, coupling, split_beta, minimum_cells=4):
    """Upper-bound the *ideal analytic seed* joint ratio for all beta > 0."""
    choices = {'bilayer_s_half': (4,3), 'square_spin_one_large_D': (6,2)}
    if model not in choices:
        raise ValueError('No Hoeffding seed comparison for this model')
    g, B = rational(coupling), rational(split_beta)
    if g < 0 or not 0 < B <= 16:
        raise ValueError('Require g >= 0 and 0 < split_beta <= 16')
    if isinstance(minimum_cells, bool) or not isinstance(minimum_cells,int) or not 4 <= minimum_cells <= 256:
        raise ValueError('minimum_cells must be an integer from 4 to 256. A certificate at 4 already covers all larger N')
    factor, c = choices[model]
    b = factor*g
    N = minimum_cells
    thermal_exp_lower, _ = exp_negative_bounds(B)
    # beta <= B implies exp(-beta) >= exp(-B). Drop the Gaussian factor.
    low_beta = up(1/(1+c*thermal_exp_lower)**(8*N))
    # beta >= B. Drop the thermal factor. Capping x at 1 weakens the
    # bound safely and keeps this simple certificate inexpensive.
    gaussian_exponent = 7*(B*b*N)**2
    _, high_beta = exp_negative_bounds(min(gaussian_exponent,F(1)))
    upper = max(low_beta,high_beta)
    return {'split_beta':str(B), 'minimum_cells':N,
            'thermal_exp_lower':str(thermal_exp_lower),
            'low_beta_upper':str(low_beta), 'high_beta_upper':str(high_beta),
            'gaussian_exponent_at_split':str(gaussian_exponent),
            'all_beta_joint_seed_upper':str(upper),
            'threshold':str(THRESHOLD), 'obstructed':upper <= THRESHOLD}


def diagnose_hoeffding_seed(model, coupling, minimum_cells=4, split_betas=None):
    """Bounded diagnostic. Failure to prove obstruction is only inconclusive.

    A successful result covers all beta>0, all integer cell counts N>=N_min,
    and all g>=the supplied coupling. It is specific to the original global
    spectral-width Hoeffding seed and canonical x,y,beta first update.
    """
    result = {'status':'INCONCLUSIVE', 'physical_gaplessness':False,
              'physical_seed_exclusion':False,
              'criterion':'global_width_hoeffding_canonical_2d_seed',
              'model':model, 'coupling':str(coupling), 'minimum_cells':minimum_cells,
              'arithmetic':'exact rational outward enclosures', 'checks':[]}
    try:
        g=rational(coupling)
        splits=list(split_betas) if split_betas is not None else [F(k,2) for k in range(1,21)]
        if not splits or len(splits)>64:
            raise ValueError('Supply between 1 and 64 split points')
        for B in splits:
            check=split_bound(model,g,B,minimum_cells)
            result['checks'].append(check)
            if check['obstructed']:
                result.update(status='CERTIFIED_CRITERION_OBSTRUCTION', certificate=check,
                    scope={'beta':'all positive real beta',
                           'cells':f'all integer N >= {minimum_cells}',
                           'couplings':f'all g >= {g}'},
                    reason='This analytic seed bound cannot produce a positive first canonical purity update at any larger seed size.',
                    next_step='Use a stronger heat-trace or omitted-spectrum bound. Enlarging N alone cannot rescue this seed family.')
                return result
        result.update(reason='No permanent obstruction was certified by the tested exact split bounds.',
                      next_step='Do not reject the seed. Try supported seed calculations or a sharper rigorous obstruction bound.')
        return result
    except (ValueError,TypeError,ZeroDivisionError) as exc:
        result.update(status='INVALID_INPUT',reason=str(exc))
        return result


def verify_obstruction(record):
    """Recompute a saved split certificate, ignoring saved acceptance flags."""
    try:
        c=record['certificate']
        rebuilt=split_bound(record['model'],record['coupling'],c['split_beta'],record['minimum_cells'])
        return rebuilt['obstructed'] and rebuilt == c
    except (KeyError,ValueError,TypeError,ZeroDivisionError):
        return False
