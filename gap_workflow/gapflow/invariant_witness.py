"""Exact finite-pencil multiplicity from a supplied rational invariant witness.

This verifies a witness, never discovers one from rounded Ritz vectors. Full
inertia remains mandatory. Dimension/input-bit caps are preflight guards;
cooperative time checks do not replace external hard process limits.
"""
from fractions import Fraction as F
import math
import time
from .certify import rational, exact_matrix, _inertia
from .model import _integer


def _rectangular(raw,rows,cols,name):
    if len(raw)!=rows or any(len(row)!=cols for row in raw):
        raise ValueError(name+' has incorrect shape')
    return [[rational(x) for x in row] for row in raw]


def _multiply(A,B):
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*B)] for row in A]


def _transpose(A):
    return [list(col) for col in zip(*A)]


def _shift(A,W,t):
    return [[x-t*y for x,y in zip(ar,wr)] for ar,wr in zip(A,W)]


def _bits_ok(values,cap):
    return all(max(x.numerator.bit_length(),x.denominator.bit_length())<=cap for x in values)


def verify_invariant_witness(A,W,V,T,polynomial_coefficients,lower,upper,threshold,
                             max_dimension=64,max_witness_dimension=16,
                             max_polynomial_degree=16,max_input_bits=4096,
                             max_seconds=10):
    """Infer ground multiplicity only after every exact witness/completeness check.

    W accepts a positive diagonal vector or a symmetric positive-definite matrix.
    V is n by k, T is k by k, and polynomial coefficients are highest degree
    first. All mathematical inputs must be rational, never floating point.
    Malformed inputs raise. Well-formed false witnesses return certified=False.
    """
    start=time.monotonic()
    ncap=_integer(max_dimension,'max_dimension',1)
    kcap=_integer(max_witness_dimension,'max_witness_dimension',1)
    dcap=_integer(max_polynomial_degree,'max_polynomial_degree',1)
    bcap=_integer(max_input_bits,'max_input_bits',1)
    if not math.isfinite(max_seconds) or max_seconds<0:
        raise ValueError('max_seconds must be finite and nonnegative')
    A=exact_matrix(A,ncap)
    n=len(A)
    if len(W)!=n:
        raise ValueError('Metric dimension does not match A')
    if hasattr(W[0],'__len__') and not isinstance(W[0],str):
        W=exact_matrix(W,ncap)
    else:
        diagonal=[rational(x) for x in W]
        W=[[diagonal[i] if i==j else F(0) for j in range(n)] for i in range(n)]
    if len(V)!=n or not hasattr(V[0],'__len__'):
        raise ValueError('V must be a nonempty n by k array')
    k=len(V[0])
    if not 1<=k<=min(n,kcap):
        raise ValueError('Witness dimension exceeds budget or full dimension')
    V=_rectangular(V,n,k,'V')
    T=_rectangular(T,k,k,'T')
    if not 2<=len(polynomial_coefficients)<=dcap+1:
        raise ValueError('Annihilator degree must be positive and within budget')
    coefficients=[rational(x) for x in polynomial_coefficients]
    if coefficients[0]==0:
        raise ValueError('Annihilator leading coefficient must be nonzero')
    a,b,t=map(rational,(lower,upper,threshold))
    if not a<b<t:
        raise ValueError('Require lower < upper < threshold')
    values=[x for M in (A,W,V,T) for row in M for x in row]+coefficients+[a,b,t]
    if not _bits_ok(values,bcap):
        raise ValueError('Exact input numerator/denominator bit budget exceeded')
    result={'certified':False,'status':'NOT_CERTIFIED','full_dimension':n,
            'witness_dimension':k,'polynomial_degree':len(coefficients)-1,
            'polynomial_coefficients':coefficients,'lower':a,'upper':b,'threshold':t,
            'ground_multiplicity':None,'true_ground_multiplicity':None,
            'gap_lower_bound':None,'checks':{},'coverage_complete':False,
            'evidence':'exact_rational_invariant_subspace_annihilator_and_full_inertia',
            'scope':'complete supplied finite pencil only; no thermodynamic extrapolation',
            'budget':{'max_dimension':ncap,'max_witness_dimension':kcap,
                      'max_polynomial_degree':dcap,'max_input_bits':bcap,'max_seconds':max_seconds},
            'budget_limitations':'Input-bit cap does not bound intermediate coefficient growth. Time is checked between phases, not within arithmetic or Sturm operations.'}
    def finish(status):
        result['status']=status
        result['elapsed_seconds']=time.monotonic()-start
        return result
    def expired():
        return time.monotonic()-start>=max_seconds
    if expired(): return finish('TIME_BUDGET_EXHAUSTED')
    wi=_inertia(W)
    result['metric_inertia']=wi
    result['checks']['positive_metric']=wi.positive==n
    if wi.positive!=n: return finish('NONPOSITIVE_METRIC')
    WV=_multiply(W,V)
    G=_multiply(_transpose(V),WV)
    gi=_inertia(G)
    result['gram_matrix']=G
    result['gram_inertia']=gi
    result['checks']['full_rank_positive_gram']=gi.positive==k
    if gi.positive!=k: return finish('RANK_DEFICIENT_WITNESS')
    if expired(): return finish('TIME_BUDGET_EXHAUSTED')
    AV=_multiply(A,V)
    WVT=_multiply(WV,T)
    invariant=AV==WVT
    result['checks']['exact_invariance']=invariant
    if not invariant: return finish('NONINVARIANT_WITNESS')
    C=_multiply(_transpose(V),AV)
    result['restricted_matrix']=C
    # Horner evaluation checks the proposed annihilator without any charpoly.
    pT=[[F(0) for _ in range(k)] for _ in range(k)]
    for coefficient in coefficients:
        pT=_multiply(pT,T)
        for i in range(k): pT[i][i]+=coefficient
    annihilates=all(x==0 for row in pT for x in row)
    result['checks']['annihilates_restriction']=annihilates
    if not annihilates: return finish('WRONG_ANNIHILATOR')
    if expired(): return finish('TIME_BUDGET_EXHAUSTED')
    import sympy as sp
    x=sp.Symbol('energy')
    p=sp.Poly.from_list([sp.Rational(c.numerator,c.denominator) for c in coefficients],x,domain=sp.QQ)
    squarefree=sp.gcd(p,p.diff()).degree()==0
    result['checks']['squarefree_polynomial']=squarefree
    if not squarefree: return finish('POLYNOMIAL_NOT_SQUAREFREE')
    roots=int(p.count_roots(sp.Rational(a.numerator,a.denominator),sp.Rational(b.numerator,b.denominator)))
    result['distinct_polynomial_roots_in_bracket']=roots
    result['checks']['single_distinct_root']=roots==1
    if roots!=1: return finish('NOT_ONE_DISTINCT_ROOT')
    if expired(): return finish('TIME_BUDGET_EXHAUSTED')
    restricted=[_inertia(_shift(C,G,s)) for s in (a,b)]
    result['restricted_inertias']=restricted
    r=restricted[1].negative
    result['restricted_cluster_rank']=r
    restricted_ok=restricted[0].negative==0 and restricted[1].zero==0 and r>=1
    result['checks']['restricted_bottom_cluster']=restricted_ok
    if not restricted_ok: return finish('RESTRICTED_CLUSTER_NOT_ESTABLISHED')
    full=[]
    for s in (a,b,t):
        if expired(): return finish('TIME_BUDGET_EXHAUSTED')
        full.append(_inertia(_shift(A,W,s)))
    result['full_inertias']=full
    result['coverage_complete']=True
    complete=full[0].negative==0 and full[1].zero==0 and full[1].negative==r and full[2].negative==r
    result['checks']['full_cluster_completeness']=complete
    if not complete: return finish('FULL_COMPLETENESS_FAILED')
    if r==n: return finish('NO_SPECTRUM_ABOVE_CLUSTER')
    result.update(certified=True,ground_multiplicity=r,true_ground_multiplicity=r,
                  gap_lower_bound=t-b,ground_energy_bracket=[a,b])
    return finish('CERTIFIED_GROUND_MULTIPLICITY')
