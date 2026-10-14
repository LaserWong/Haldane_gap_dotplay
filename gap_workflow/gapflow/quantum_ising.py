"""O(L) finite periodic TFI partition functions and numerical bootstrap seeds.

H=-J sum_i Z_i Z_(i+1)-h sum_i X_i. L=2 retains both bonds.
No many-body levels are computed. These numerical values are NOT certificates.
"""
import math
from fractions import Fraction


def _as_rational(value):
    """Parse decimal/scientific/rational text without a binary64 round trip."""
    if isinstance(value, bool):
        raise ValueError('parameters must be finite real numbers')
    try:
        return value if isinstance(value, Fraction) else Fraction(str(value))
    except (ValueError, TypeError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError('parameters must be finite real numbers or rational strings') from exc


def _to_mp(ctx, value):
    value = _as_rational(value)
    return ctx.mpf(value.numerator) / ctx.mpf(value.denominator)


def _validate(L, beta, J, h):
    if type(L) is not int or L < 2:
        raise ValueError('L must be an integer >= 2')
    beta,J,h = (_as_rational(v) for v in (beta,J,h))
    if beta < 0 or J < 0:
        raise ValueError('require beta >= 0 and J >= 0')
    return beta,J,h


def _logadd(a, b, ctx):
    a, b = max(a, b), min(a, b)
    if a == -ctx.inf:
        return a
    return a + ctx.log1p(ctx.exp(b-a))


def _log_partition(L, beta, J, h, ctx):
    """Positive parity recurrence in log coordinates; O(L) operations."""
    h = abs(h)  # conjugation by product Z_i changes the field sign
    sectors = []
    for shift in (ctx.mpf('0.5'), ctx.mpf(0)):
        even, odd, vacuum = ctx.mpf(0), -ctx.inf, ctx.mpf(0)
        for m in range(L):
            k = 2*ctx.pi*(m+shift)/L
            # Stable at criticality, including the exact zero momentum mode.
            eps = 2*ctx.sqrt((J-h)**2 + 4*J*h*ctx.sin(k/2)**2)
            x = beta*eps
            even, odd = _logadd(even, odd-x, ctx), _logadd(odd, even-x, ctx)
            vacuum += x/2
        # NS physical even; R physical odd. R vacuum parity changes at h=J.
        selected = even if shift or h < J else odd
        sectors.append(vacuum + selected)
    return _logadd(*sectors, ctx)


class _FloatContext:
    mpf = staticmethod(float)
    inf, pi = math.inf, math.pi
    log1p, exp, sin, sqrt = map(staticmethod, (math.log1p, math.exp, math.sin, math.sqrt))


def log_partition(L, beta, J=1, h=1):
    """Stable binary64 log Z, for either sign of h and beta >= 0."""
    values = _validate(L, beta, J, h)
    try:
        values = tuple(float(v) for v in values)
    except OverflowError as exc:
        raise ValueError('parameters exceed binary64 range; use log_partition_mp') from exc
    if not all(math.isfinite(v) for v in values):
        raise ValueError('parameters exceed binary64 range; use log_partition_mp')
    return _log_partition(L, *values, _FloatContext)


def log_partition_mp(L, beta, J=1, h=1, dps=80):
    """Arbitrary precision candidate; no directed rounding/error certificate."""
    import mpmath
    _validate(L, beta, J, h)
    if type(dps) is not int or dps < 20:
        raise ValueError('dps must be an integer >= 20')
    ctx = mpmath.mp.clone()
    ctx.dps = dps
    return _log_partition(L, *(_to_mp(ctx,v) for v in (beta,J,h)), ctx)


def canonical_seed(n, beta, J=1, h=1, dps=80):
    """Three exact-formula evaluations, two numerical canonical purities.

    P_x(n,beta)=Z(2n,beta)/Z(n,beta)^2;
    P_beta(2n,beta)=Z(2n,2beta)/Z(2n,beta)^2.
    Strings preserve arbitrary precision values. They are not rational bounds.
    """
    import mpmath
    _validate(n, beta, J, h)
    if n % 2 or _as_rational(beta) <= 0:
        raise ValueError('canonical seed requires even n and beta > 0')
    if type(dps) is not int or dps < 20:
        raise ValueError('dps must be an integer >= 20')
    ctx = mpmath.mp.clone(); ctx.dps = dps
    b,j,g = (_to_mp(ctx,x) for x in (beta,J,h))
    logs = [_log_partition(n,b,j,g,ctx), _log_partition(2*n,b,j,g,ctx),
            _log_partition(2*n,2*b,j,g,ctx)]
    logps = [logs[1]-2*logs[0], logs[2]-2*logs[1]]
    ps = [ctx.exp(x) for x in logps]
    defects = [-ctx.expm1(x) for x in logps]
    u = max(defects)
    return {'family':'periodic_quantum_ising','n':n,'beta':str(beta),'J':str(J),'h':str(h),
            'bond_convention':'positive_direction_multigraph',
            'log_partition_values':[str(x) for x in logs],
            'edges':[{'axis':'x1','base_lengths':[n],'base_beta':str(beta),'candidate':str(ps[0])},
                     {'axis':'beta','base_lengths':[2*n],'base_beta':str(beta),'candidate':str(ps[1])}],
            'defects':[str(x) for x in defects],'u_candidate':str(u),
            'dedicated_entry_candidate':bool(0 < u <= ctx.mpf('0.01')),
            'gap_candidate':str(ctx.log(1/(5*u))/b) if 0 < u <= ctx.mpf('0.01') else None,
            'evidence_class':'ARBITRARY_PRECISION_CANDIDATE_NOT_INTERVAL_CERTIFIED',
            'precision_digits':dps,'many_body_eigenpairs_computed':0,
            'single_particle_modes_evaluated':10*n,
            'uniform_family_claim':False}


def replay_candidate(seed, max_rounds=16):
    """Numerical scouting of the dedicated d=1 recurrence, never a certificate."""
    import mpmath
    if type(max_rounds) is not int or max_rounds < 0:
        raise ValueError('max_rounds must be a nonnegative integer')
    ctx=mpmath.mp.clone(); ctx.dps=seed['precision_digits']
    q=[ctx.mpf(edge['candidate']) for edge in seed['edges']]
    beta=_to_mp(ctx,seed['beta']); n=seed['n']
    for r in range(max_rounds+1):
        u=max(1-x for x in q)
        if not all(0<x<=1 for x in q) or u<=0:
            return {'status':'NUMERICAL_INCONCLUSIVE','rounds':r,'uniform_family_claim':False}
        if u<=ctx.mpf('.01'):
            return {'status':'NUMERICAL_ENTRY_CANDIDATE','rounds':r,'n':n,'beta':str(beta),
                    'u_candidate':str(u),'gap_candidate':str(ctx.log(1/(5*u))/beta),
                    'uniform_family_claim':False}
        if r==max_rounds: break
        for _ in range(2):
            z=q[0]**2*q[1]
            new=1-(1-z)**2/(2*z*z)
            if new<=0:
                return {'status':'NUMERICAL_RECURRENCE_INCONCLUSIVE','rounds':r,'uniform_family_claim':False}
            q=q[1:]+[new]
        beta*=2; n*=2
    return {'status':'NUMERICAL_ROUND_LIMIT','rounds':max_rounds,'uniform_family_claim':False}


def shifted_partition_mp(L, beta, J=1, h=1, dps=80):
    """Candidate Tr exp[-beta*(H_L+(J+|h|)*L)] via positive bounded factors.

    Uses a_k=exp[-beta*(c-eps_k/2)], b_k=exp[-beta*(c+eps_k/2)]
    with c=J+|h|, so both factors are <=1. Every update is positive.
    The common linear-in-L shift cancels exactly in both canonical ratios.
    This is the preferred algebraic form for a separate interval implementation.
    """
    import mpmath
    _validate(L,beta,J,h)
    if type(dps) is not int or dps<20:
        raise ValueError('dps must be an integer >= 20')
    ctx=mpmath.mp.clone();ctx.dps=dps
    beta,J,h=(_to_mp(ctx,x) for x in (beta,J,h));h=abs(h);c=J+h
    total=ctx.mpf(0)
    for shift in (ctx.mpf('.5'),ctx.mpf(0)):
        E,O=ctx.mpf(1),ctx.mpf(0)
        for m in range(L):
            omega=ctx.sqrt((J-h)**2+4*J*h*ctx.sin(ctx.pi*(m+shift)/L)**2)
            a=ctx.exp(-beta*(c-omega));b=ctx.exp(-beta*(c+omega))
            E,O=a*E+b*O,a*O+b*E
        total+=E if shift or h<J else O
    return total
