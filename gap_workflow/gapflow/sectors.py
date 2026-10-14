"""Full-Hilbert finite certificates by exhaustive conserved magnetization blocks.

Every nonempty sector is counted. No subset of sectors establishes coverage.
A process-level time/memory limit must be supplied by an external runner.
"""
from fractions import Fraction as F
import time
import math
from .model import Model, _integer
from .certify import rational, pencil_inertia, _exact_pencil, Inertia


def _prepare(model,max_sector_dimension):
    if not isinstance(model,Model):
        model = Model.from_dict(model)
    cap = _integer(max_sector_dimension,'max_sector_dimension',1)
    if not model.preserves_total_sz:
        raise ValueError('Exhaustive total_m2 certification requires conserved total Sz')
    dims = model.sector_dimensions()
    if not dims or any(d <= 0 for d in dims.values()) or sum(dims.values()) != model.hilbert_dimension:
        raise ValueError('Exact sector dimension coverage is inconsistent')
    return model,cap,dict(sorted(dims.items()))


def _base(model,dims,cap):
    return {'certified':False,'status':'NOT_CERTIFIED','coverage_complete':False,
            'full_hilbert_dimension':model.hilbert_dimension,
            'covered_dimension':0,'sector_dimensions':dims,
            'largest_sector_dimension':max(dims.values()),'max_sector_dimension':cap,
            'sector_evidence':[], 'model':model.summary(),
            'evidence':'exact_rational_exhaustive_symmetry_pencil_inertia',
            'scope':'incomplete sector evidence only until coverage_complete is true',
            'budget_note':'Time checked between blocks. External process limits enforce hard runtime and memory caps.'}


def _aggregate(model,dims,cap,thresholds,report,start,max_seconds):
    if max_seconds is not None and (not math.isfinite(max_seconds) or max_seconds < 0):
        raise ValueError('max_seconds must be finite and nonnegative')
    sums = [[0,0,0] for _ in thresholds]
    scalar_energies = []
    if max(dims.values()) > cap:
        report['status'] = 'SECTOR_DIMENSION_BUDGET_EXCEEDED'
        return None
    for q,d in dims.items():
        if max_seconds is not None and time.monotonic()-start >= max_seconds:
            report['status'] = 'TIME_BUDGET_EXHAUSTED'
            return None
        A,w = model.exact_pencil(total_m2=q,max_dimension=cap)
        if len(A) != d or len(w) != d:
            raise ValueError('Built sector dimension disagrees with exact DP coverage')
        scalar = A[0][0]/w[0]
        is_scalar = all(A[i][j] == (scalar*w[i] if i == j else 0) for i in range(d) for j in range(d))
        scalar_energies.append(scalar if is_scalar else None)
        counts = [pencil_inertia(A,w,t,max_dimension=cap) for t in thresholds]
        for total,count in zip(sums,counts):
            if count.negative+count.zero+count.positive != d:
                raise ValueError('Inertia count disagrees with sector dimension')
            total[0] += count.negative
            total[1] += count.zero
            total[2] += count.positive
        report['sector_evidence'].append({'total_m2':q,'dimension':d,
            'thresholds':list(thresholds),'inertias':counts,'scalar_energy':scalar if is_scalar else None})
        report['covered_dimension'] += d
    report['coverage_complete'] = report['covered_dimension'] == model.hilbert_dimension and len(report['sector_evidence']) == len(dims)
    if not report['coverage_complete']:
        raise ValueError('Full-Hilbert coverage failed')
    report['scope'] = 'full finite Hilbert space via every conserved total_m2 sector; no thermodynamic extrapolation'
    report['elapsed_seconds'] = time.monotonic()-start
    report['has_excited_space'] = any(e is None for e in scalar_energies) or len(set(scalar_energies)) > 1
    return [Inertia(*total) for total in sums]


def certify_sectors_gap(model, ground_energy, gap_lower_bound,
                        max_sector_dimension=128,max_seconds=None):
    """Exact gap above a possibly degenerate ground, using all Sz sectors."""
    start = time.monotonic()
    model,cap,dims = _prepare(model,max_sector_dimension)
    e,g = rational(ground_energy),rational(gap_lower_bound)
    if g <= 0:
        raise ValueError('Gap lower bound must be positive')
    report = _base(model,dims,cap)
    report.update(ground_energy=e,requested_gap_lower_bound=g,gap_lower_bound=None)
    counts = _aggregate(model,dims,cap,[e,e+g],report,start,max_seconds)
    if counts is None:
        return report
    low,high = counts
    n = model.hilbert_dimension
    passed = low.negative == 0 and 0 < low.zero < n and high.negative == low.zero
    report.update(certified=passed,
        status='CERTIFIED' if passed else ('NO_EXCITED_SPACE' if not report['has_excited_space'] else 'NOT_CERTIFIED'),
        ground_multiplicity=low.zero if low.negative == 0 else None,
        ground_inertia=low,gap_threshold_inertia=high,gap_lower_bound=g if passed else None)
    return report


def certify_sectors_gap_from_vector(model,trial_sector,vector,threshold,
                                    max_sector_dimension=128,max_seconds=None):
    """Exact sector Rayleigh upper, then global threshold count over EVERY sector.

    vector uses the exact_pencil weighted coordinates of trial_sector. It can
    be an explicitly rationalized numerical trial. It need not be an eigenstate.
    """
    start = time.monotonic()
    model,cap,dims = _prepare(model,max_sector_dimension)
    q = _integer(trial_sector,'trial_sector')
    if q not in dims:
        raise ValueError('Trial sector is empty')
    t = rational(threshold)
    report = _base(model,dims,cap)
    report.update(trial_sector=q,threshold=t,gap_lower_bound=None)
    if max(dims.values()) > cap:
        report['status'] = 'SECTOR_DIMENSION_BUDGET_EXCEEDED'
        return report
    A,w = model.exact_pencil(total_m2=q,max_dimension=cap)
    A,w = _exact_pencil(A,w,cap)
    v = [rational(x) for x in vector]
    if len(v) != dims[q]:
        raise ValueError('Trial vector dimension disagrees with its sector')
    norm = sum(wi*vi*vi for wi,vi in zip(w,v))
    if norm == 0:
        raise ValueError('Trial vector must be nonzero')
    Av = [sum(a*vi for a,vi in zip(row,v)) for row in A]
    u = sum(vi*ai for vi,ai in zip(v,Av))/norm
    residual = sum((ai-u*wi*vi)**2/wi for ai,wi,vi in zip(Av,w,v))/norm
    report.update(trial_vector=v,trial_norm_squared=norm,ground_energy_upper=u,residual_squared=residual)
    counts = _aggregate(model,dims,cap,[t],report,start,max_seconds)
    if counts is None:
        return report
    count = counts[0]
    passed = report['has_excited_space'] and count.negative == 1 and t>u
    report.update(certified=passed,status='CERTIFIED' if passed else ('NO_EXCITED_SPACE' if not report['has_excited_space'] else 'NOT_CERTIFIED'),
                  threshold_inertia=count,gap_lower_bound=t-u if passed else None,
                  ground_multiplicity=1 if passed else None)
    return report
