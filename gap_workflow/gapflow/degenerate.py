"""Exact finite-spectrum diagnostics, not a spatial bootstrap adapter.

Excited weights are exp(-beta*(E-E0)), supplied as exact rationals for
fixtures. Ground multiplicity must be independently established.
"""
from fractions import Fraction as F
from math import comb


def _rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, str, F)):
        raise ValueError('Use an exact integer, rational string, or Fraction')
    try:
        return F(value)
    except (ValueError, ZeroDivisionError):
        raise ValueError('Invalid exact rational') from None


def temporal_defects(g, excited_weights):
    """Return exact defects at beta, 2 beta and a proved upper bound.

    This checks a supplied spectral fixture; it does not prove that the
    fixture exhausts a Hamiltonian spectrum or that its stated g is correct.
    Empty excited_weights means no excited states, not a finite gap.
    """
    if type(g) is not int or g < 1:
        raise ValueError('Ground multiplicity must be a positive integer')
    weights = tuple(_rational(x) for x in excited_weights)
    if any(not 0 < x < 1 for x in weights):
        raise ValueError('Finite positive-temperature excited weights must lie in (0,1)')
    s = sum(weights, F(0))
    q = sum((x*x for x in weights), F(0))
    r = sum((x**4 for x in weights), F(0))
    u = 1 - g*(g+q)/(g+s)**2
    doubled = 1 - g*(g+r)/(g+q)**2
    tail_bound = g*u/(1-u)
    quadratic_bound = 2*g*(u/(1-u))**2
    return {'defect': u, 'doubled_defect': doubled,
            'excited_weight_sum': s, 'excited_weight_sum_upper': tail_bound,
            'quadratic_upper': quadratic_bound,
            'has_excited_states': bool(weights)}


def ising_cycle_pair_polynomial(length):
    """Ground-shifted Z/2 coefficients in t=exp(-beta J/2).

    Positive-direction cycle convention, including two parallel bonds for
    length=2. This is an exact all-size combinatorial formula, not sampled
    finite-size evidence for a generic family theorem.
    """
    if type(length) is not int or length < 2:
        raise ValueError('Cycle length must be an integer >= 2')
    return tuple(comb(length, k) if k % 2 == 0 else 0
                 for k in range(length+1))


def ising_cycle_uniform_certificate(coupling):
    """Certificate for the specifically defined uniform ferromagnetic family.

    Does not certify arbitrary user-provided Hamiltonians as members of that
    family. J is the coefficient in -J sum Sz_i Sz_(i+1), Sz=+/-1/2.
    """
    j = _rational(coupling)
    if j <= 0:
        raise ValueError('Ferromagnetic coupling must be positive')
    return {'family': 'uniform_positive_direction_Ising_cycles',
            'lengths': 'all integers L >= 2', 'ground_multiplicity': 2,
            'gap_above_ground_space': str(j),
            'ground_energy': '-J*L/4',
            'first_excited_multiplicity': '2*binomial(L,2)',
            'proof': 'theory/DEGENERATE_PURITY.md#4-exact-ising-cycle-family',
            'spatial_bootstrap_claimed': False}
