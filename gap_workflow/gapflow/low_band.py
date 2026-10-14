"""Certify a bottom spectral cluster without assuming ground-state degeneracy.

Cluster rank is NOT ground multiplicity. Optional exact squarefree polynomial
root counts can establish equality of every energy in the cluster. No roots
are numerically solved and no full eigenspectrum is computed.
"""
from .certify import rational, _exact_pencil, exact_matrix, pencil_inertia
from .sectors import _prepare, _base, _aggregate
from .model import _integer
import time


def _bounds(lower,upper,threshold):
    a,b,t = map(rational,(lower,upper,threshold))
    if not a < b < t:
        raise ValueError('Require rational lower < upper < threshold')
    return a,b,t


def _summary(counts,n,a,b,t):
    low,high,cut = counts
    # Strict upper bracket simplifies exact distinct-root endpoint semantics.
    valid = low.negative == 0 and high.zero == 0 and high.negative >= 1 and cut.negative == high.negative
    rank = high.negative if valid else None
    has_complement = valid and rank < n
    return {'certified':has_complement,
            'status':'CERTIFIED_LOW_BAND' if has_complement else ('NO_SPECTRUM_ABOVE_CLUSTER' if valid else 'NOT_CERTIFIED'),
            'lower':a,'upper':b,'threshold':t,
            'lower_inertia':low,'upper_inertia':high,'threshold_inertia':cut,
            'low_band_rank':rank,'low_band_width_upper':b-a if valid else None,
            'gap_above_cluster_lower':t-b if has_complement else None,
            'ground_multiplicity':None,'true_ground_multiplicity':None,'ground_multiplicity_status':'unknown',
            'true_ground_gap_lower':None,
            'distinct_ground_cluster_roots':None,
            'multiplicity_evidence':'not_requested',
            'evidence':'exact_rational_inertia_low_cluster',
            'scope':'finite input only; cluster rank does not establish ground degeneracy'}


def _root_union_count(pencils,a,b):
    """Exact squarefree union polynomial and Sturm root count on [a,b]."""
    import sympy as sp
    x = sp.Symbol('energy')
    union = sp.Poly(1,x,domain=sp.QQ)
    degrees = []
    for A,w in pencils:
        M = sp.Matrix([[sp.Rational(v.numerator,v.denominator)/sp.Rational(w[i].numerator,w[i].denominator)
                        for v in row] for i,row in enumerate(A)])
        poly = sp.Poly(M.charpoly(x).as_expr(),x,domain=sp.QQ)
        degrees.append(poly.degree())
        union = sp.lcm(union,poly.sqf_part()).monic()
    count = int(union.count_roots(sp.Rational(a.numerator,a.denominator),sp.Rational(b.numerator,b.denominator)))
    return count, {'method':'exact_squarefree_characteristic_polynomial_Sturm_count',
        'characteristic_degrees':degrees,'squarefree_union_degree':union.degree(),
        'squarefree_union_coefficients':[str(c) for c in union.all_coeffs()],
        'distinct_roots_in_closed_bracket':count}


def _infer(report,pencils,a,b):
    count,evidence = _root_union_count(pencils,a,b)
    report['distinct_ground_cluster_roots'] = count
    report['multiplicity_evidence'] = evidence
    if count == 1:
        report['ground_multiplicity'] = report['low_band_rank']
        report['true_ground_multiplicity'] = report['low_band_rank']
        report['ground_multiplicity_status'] = 'certified_by_single_distinct_root'
        if not report['certified']:
            report['status']='NO_EXCITED_SPACE'
        if report['certified']:
            report['status'] = 'CERTIFIED_GROUND_MULTIPLICITY'
            report['true_ground_gap_lower'] = report['gap_above_cluster_lower']
    elif count > 1:
        report['ground_multiplicity_status'] = 'unknown_cluster_contains_distinct_energies'
    else:
        raise ArithmeticError('Exact root count contradicts exact inertia cluster count')


def certify_low_band(A,lower,upper,threshold,Wdiag=None,max_dimension=64,
                     infer_multiplicity=False,distinct_root_max_dimension=16):
    """Full finite pencil low-cluster certificate with unknown multiplicity by default.

    The upper bracket must not coincide with an eigenvalue. The lower bracket
    may coincide with the ground. A gap at threshold is inclusive.
    """
    distinct_root_max_dimension = _integer(distinct_root_max_dimension,'distinct_root_max_dimension',1)
    a,b,t = _bounds(lower,upper,threshold)
    if Wdiag is None:
        A = exact_matrix(A,max_dimension)
        Wdiag = [1]*len(A)
    A,w = _exact_pencil(A,Wdiag,max_dimension)
    counts = [pencil_inertia(A,w,s,max_dimension) for s in (a,b,t)]
    report = _summary(counts,len(A),a,b,t)
    report.update(full_dimension=len(A),coverage_complete=True,metric_diagonal=w)
    if infer_multiplicity and report['low_band_rank'] is not None:
        if len(A)>distinct_root_max_dimension:
            report['multiplicity_evidence'] = 'distinct_root_dimension_budget_exceeded'
        else:
            _infer(report,[(A,w)],a,b)
    return report


def certify_sector_low_band(model,lower,upper,threshold,max_sector_dimension=128,
                            max_seconds=None,infer_multiplicity=False,
                            distinct_root_max_dimension=16):
    """Exhaust all conserved Sz sectors, then optionally count distinct union roots.

    The root-count cap applies to full Hilbert dimension, not largest block.
    Time is checked between blocks. External process limits enforce hard budgets.
    """
    start = time.monotonic()
    distinct_root_max_dimension = _integer(distinct_root_max_dimension,'distinct_root_max_dimension',1)
    a,b,t = _bounds(lower,upper,threshold)
    model,cap,dims = _prepare(model,max_sector_dimension)
    report = _base(model,dims,cap)
    report.update(lower=a,upper=b,threshold=t,low_band_rank=None,
                  ground_multiplicity=None,true_ground_multiplicity=None,ground_multiplicity_status='unknown',
                  gap_above_cluster_lower=None,true_ground_gap_lower=None)
    counts = _aggregate(model,dims,cap,[a,b,t],report,start,max_seconds)
    if counts is None:
        return report
    scope = report['scope']
    report.update(_summary(counts,model.hilbert_dimension,a,b,t))
    report['scope'] = scope+'; cluster rank alone does not establish ground degeneracy'
    if infer_multiplicity and report['certified'] and report['low_band_rank']==2:
        symmetry=kramers_symmetry_certificate(model)
        report['kramers_symmetry']=symmetry
        if symmetry['certified']:
            report.update(ground_multiplicity=2,true_ground_multiplicity=2,
                ground_multiplicity_status='certified_by_Kramers_and_exhaustive_rank_two_cluster',
                multiplicity_evidence=symmetry,status='CERTIFIED_GROUND_MULTIPLICITY',
                distinct_ground_cluster_roots=1,
                true_ground_gap_lower=report['gap_above_cluster_lower'])
            return report
    if infer_multiplicity and report['low_band_rank'] is not None:
        if model.hilbert_dimension>distinct_root_max_dimension:
            report['multiplicity_evidence'] = 'distinct_root_dimension_budget_exceeded'
        else:
            pencils = []
            for q in dims:
                if max_seconds is not None and time.monotonic()-start>=max_seconds:
                    report['multiplicity_evidence'] = 'distinct_root_time_budget_exhausted'
                    return report
                A,w = model.exact_pencil(total_m2=q,max_dimension=cap)
                pencils.append(_exact_pencil(A,w,cap))
            _infer(report,pencils,a,b)
    return report


def kramers_symmetry_certificate(model):
    """Conservative exact termwise time-reversal check for the supported model.

    Every local spin component is odd under time reversal. Real bilinears and
    single-ion Sz^2 are even. Nonzero odd spin products or fields are rejected.
    This certifies a structural double-degeneracy floor, not an exact rank.
    """
    from .model import Model
    if not isinstance(model,Model):
        model=Model.from_dict(model)
    invariant=True
    failures=[]
    for index,term in enumerate(model.terms):
        kind=term[0]
        if kind in ('exchange','onsite_d'):
            continue
        if kind=='field_z':
            if term[2]:
                invariant=False
                failures.append(index)
        elif kind=='spin_product':
            if term[1] and len(term[2])%2:
                invariant=False
                failures.append(index)
        else:
            invariant=False
            failures.append(index)
    odd=sum(model.spins2)%2==1
    return {'certified':bool(invariant and odd),'time_reversal_invariant':invariant,
            'theta_squared':-1 if odd else 1,'symmetry_breaking_or_unsupported_term_indices':failures,
            'evidence':'exact_model_termwise_time_reversal_and_half_integer_total_spin_parity',
            'conclusion':'Every full-Hilbert energy has even multiplicity' if invariant and odd else 'Kramers degeneracy not certified'}
