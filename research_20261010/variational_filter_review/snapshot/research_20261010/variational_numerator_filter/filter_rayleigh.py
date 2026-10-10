"""Exact optional Rayleigh filtering from existing G, H, H² matrices only.

No physical vector, H³ or H⁴ moment is formed or read. Acceptance uses Fraction.
The old first-moment-only consumer is unchanged. See PROOF.md for the support
and orthonormal-coordinate argument behind the q<=6 operator upper bound.
"""
import os
for _key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_key] = '1'
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
ROOT = RESEARCH.parent


def graph(nx, ny):
    assert nx >= 2 and ny >= 2
    edges = Counter()
    for x in range(nx):
        for y in range(ny):
            i = x * ny + y
            for j in (((x + 1) % nx) * ny + y, x * ny + (y + 1) % ny):
                edges[tuple(sorted((i, j)))] += 1
    assert all(i != j for i, j in edges)
    assert all(sum(w for e, w in edges.items() if i in e) == 4 for i in range(nx * ny))
    return edges


def positive_upper_pivots(diagonal, off_squared, upper):
    """Return LDL pivots for upper*I-J, or None if not strictly positive."""
    assert len(diagonal) == len(off_squared) + 1
    out = []
    for i, d in enumerate(diagonal):
        p = upper - d - (off_squared[i - 1] / out[-1] if i else 0)
        if p <= 0:
            return None
        out.append(p)
    return out


def compressed_upper(nx, ny, g, max_q=6, digits=16):
    """Rational upper bound on even-number compression 0<=Q<=max_q.

    The positive Jacobi offdiagonal is sqrt(off_squared); roots are never
    approximated in the acceptance test. The extra precision is optional.
    """
    g = F(g)
    assert 0 <= g and max_q >= 0 and max_q % 2 == 0
    edges = graph(nx, ny)
    numbers = list(range(0, min(max_q, nx * ny) + 1, 2))
    v = F(3, 4) * g * g * sum(w * w for w in edges.values())
    kappa2 = 4 * g * g
    diagonal = [(1 + 2 * g) * q for q in numbers]
    off_squared = [(q // 2 + 1) * v + kappa2 * ((q + 1) ** 2 // 4) for q in numbers[:-1]]
    # sqrt(x)<=max(1,x) gives a rational, deliberately loose row-sum bracket.
    row_brackets = [d + sum(max(F(1), off_squared[j]) for j in (i - 1, i)
                          if 0 <= j < len(off_squared)) for i, d in enumerate(diagonal)]
    scale = 10 ** digits
    low = math.floor(max(diagonal) * scale)
    high = math.ceil((max(row_brackets) + 1) * scale)
    assert positive_upper_pivots(diagonal, off_squared, F(high, scale))
    while high - low > 1:
        mid = (high + low) // 2
        if positive_upper_pivots(diagonal, off_squared, F(mid, scale)):
            high = mid
        else:
            low = mid
    upper = F(high, scale)
    pivots = positive_upper_pivots(diagonal, off_squared, upper)
    assert pivots and all(p > 0 for p in pivots)
    return dict(number_indices=numbers, diagonal=list(map(str, diagonal)),
                offdiagonal_squared=list(map(str, off_squared)),
                vacuum_creation_norm_squared=str(v), creation_matrix_norm_squared_upper=str(kappa2),
                weighted_edge_square_sum=sum(w * w for w in edges.values()),
                compressed_H_upper=str(upper), upper_LDL_positive_pivots=list(map(str, pivots)),
                rounding_digits=digits)


def optimize_filter(rho, variance, upper, digits=24):
    """Upper Rayleigh endpoint of span{psi,(H-rho)psi}, using only rHr<=R||r||².

    A rational delta satisfies delta*(C+delta)<=variance. Taking t=delta/variance
    proves the normalized vector's Rayleigh<=rho-delta without any square root.
    """
    rho, variance, upper = map(F, (rho, variance, upper))
    assert variance >= 0
    C = upper - rho
    assert C > 0
    if variance == 0:
        return dict(shifted_rayleigh_upper=str(rho), improvement='0', t='0',
                    C=str(C), variance='0', normalization_squared='1',
                    quadratic_slack='0', achieved_bound=str(rho))
    # floor(sqrt(C²+4 variance)) is obtained by integer arithmetic after scaling.
    scale = 10 ** digits
    radicand = C * C + 4 * variance
    root_floor = math.isqrt((radicand.numerator * scale * scale) // radicand.denominator)
    delta = max(F(0), (F(root_floor, scale) - C) / 2)
    # If the chosen decimal grid is coarser than the tiny gain, a direct rational
    # t=1/C construction still gives a strictly positive certified improvement.
    elementary_gain = variance * C / (C * C + variance)
    delta = max(delta, elementary_gain)
    slack = variance - delta * (C + delta)
    assert delta > 0 and slack >= 0
    t = delta / variance
    norm2 = 1 + t * t * variance
    achieved = rho + variance * (-2 * t + C * t * t) / norm2
    assert achieved <= rho - delta < rho
    return dict(shifted_rayleigh_upper=str(rho - delta), improvement=str(delta),
                t=str(t), C=str(C), variance=str(variance), normalization_squared=str(norm2),
                quadratic_slack=str(slack), achieved_bound=str(achieved),
                elementary_t_one_over_C_gain=str(elementary_gain), rounding_digits=digits)


def bilinear(coefficients, matrix):
    return sum(c * int(matrix[i][j]) * d for i, c in enumerate(coefficients)
               for j, d in enumerate(coefficients))


def quadratic(left, matrix, right=None):
    if right is None:
        right = left
    return sum(c * int(matrix[i][j]) * d for i, c in enumerate(left)
               for j, d in enumerate(right))


def sqrt_upper(x, digits=36):
    x = F(x)
    assert x >= 0
    scale = 10 ** digits
    low = math.isqrt((x.numerator * scale * scale) // x.denominator)
    if F(low, scale) ** 2 == x:
        return F(low, scale)
    return F(low + 1, scale)


def residual_sector_bound(record, geometry, rho, variance, norm):
    """Use existing F/S/V/W to resolve ||P_q r||², never construct r."""
    g = F(record['coupling'])
    n = geometry['pair_orbits']
    d = n + 1
    c = list(map(int, record['coefficients']))
    selected = record['selected_basis_indices']
    assert len(c) == len(selected) and selected[:d] == list(range(d))
    full = [F(0)] * (2 * n + 1)
    for i, v in zip(selected, c):
        full[i] = F(v)
    cb, cl = full[:d], full[d:]
    den = record['integer_matrix_denominator']
    G, K = record['gram'], record['shifted_hamiltonian_numerator']
    diagonal = [int(G[i][i]) for i in range(d)]
    assert all(int(G[i][j]) == (diagonal[i] if i == j else 0)
               for i in range(d) for j in range(d))
    low = [sum(F(int(K[i][j]) * c[j], den * diagonal[i]) for j in range(len(c)))
           - rho * cb[i] for i in range(d)]
    masses = [F(diagonal[0]) * low[0] ** 2 / norm,
              sum(diagonal[i] * low[i] ** 2 for i in range(1, d)) / norm]
    h = [g * cb[i + 1] / 2 + (4 - rho) * cl[i] for i in range(n)]
    masses += [(quadratic(h, geometry['F']) + g * quadratic(h, geometry['S'], cl)
                + g * g * quadratic(cl, geometry['V']) / 4) / norm,
               g * g * quadratic(cl, geometry['W']) / (4 * norm)]
    assert all(x >= 0 for x in masses)
    assert sum(masses) == variance
    comparison = compressed_upper(record['nx'], record['ny'], g)
    diagonal_upper = list(map(F, comparison['diagonal']))
    off_squared = list(map(F, comparison['offdiagonal_squared']))
    assert comparison['number_indices'] == [0, 2, 4, 6]
    products = [off_squared[i] * masses[i] * masses[i + 1] for i in range(3)]
    cross_upper = list(map(sqrt_upper, products))
    numerator_upper = sum(x * w for x, w in zip(diagonal_upper, masses)) + 2 * sum(cross_upper)
    assert variance > 0
    R = numerator_upper / variance
    assert all(x * x >= p for x, p in zip(cross_upper, products))
    return dict(number_indices=[0, 2, 4, 6], residual_norm_squared_by_number=list(map(str, masses)),
                variance_sum_exact=str(sum(masses)),
                cross_term_squared=list(map(str, products)), cross_term_sqrt_upper=list(map(str, cross_upper)),
                residual_H_expectation_numerator_upper=str(numerator_upper),
                residual_normalized_H_expectation_upper=str(R),
                residual_number_fractions_display=[float(x / variance) for x in masses])


def certificate(record, source=None, geometry=None, geometry_source=None):
    nx, ny = record['nx'], record['ny']
    g = F(record['coupling'])
    assert record['s'] == '1/2' and record['block_krylov_depth'] == 1
    assert record['basis'] == 'B vacuum/pair orbits, followed by g-independent L=A42 pair orbit vectors; inner products divided by 2**N'
    c = list(map(int, record['coefficients']))
    d = int(record['integer_matrix_denominator'])
    norm = bilinear(c, record['gram'])
    assert norm > 0 and d > 0
    rho = F(bilinear(c, record['shifted_hamiltonian_numerator']), d * norm)
    variance = F(bilinear(c, record['shifted_H2_numerator']), d * d * norm) - rho * rho
    assert variance >= 0
    E00 = F(record['E00'])
    assert E00 == -F(3 * nx * ny, 4)
    assert rho + E00 == F(record['exact_rayleigh'])
    assert variance == F(record['exact_residual_squared'])
    comparison = compressed_upper(nx, ny, g)
    filtered = optimize_filter(rho, variance, F(comparison['compressed_H_upper']))
    result = dict(status='exact_optional_variational_filter_candidate_pending_independent_review',
                  nx=nx, ny=ny, coupling=str(g), physical_spins=2 * nx * ny,
                  full_dimension=4 ** (nx * ny), original_trial_dimension=len(c),
                  implicit_filtered_trial_states=1, original_trial_max_triplet_number=4,
                  residual_max_triplet_number=min(6, nx * ny), residual_parity='even',
                  energy_shift=str(E00), exact_original_shifted_rayleigh=str(rho),
                  exact_original_variance=str(variance), original_squared_norm_reduced=str(norm),
                  original_gram_common_factor_removed=record['gram_common_factor_removed'],
                  compressed_upper_certificate=comparison, filter=filtered,
                  shifted_rayleigh_upper=filtered['shifted_rayleigh_upper'],
                  energy_rayleigh_upper=str(E00 + F(filtered['shifted_rayleigh_upper'])),
                  strict_improvement_display=float(F(filtered['improvement'])),
                  old_shifted_rayleigh_display=float(rho),
                  new_shifted_rayleigh_upper_display=float(F(filtered['shifted_rayleigh_upper'])),
                  new_residual_claim=False, reads_higher_moments=False,
                  source_matrix_fields=['gram', 'shifted_hamiltonian_numerator', 'shifted_H2_numerator'])
    if geometry is not None and variance:
        sector = residual_sector_bound(record, geometry, rho, variance, norm)
        R = min(F(sector['residual_normalized_H_expectation_upper']),
                F(comparison['compressed_H_upper']))
        sector_filtered = optimize_filter(rho, variance, R)
        assert F(sector_filtered['shifted_rayleigh_upper']) <= F(filtered['shifted_rayleigh_upper'])
        result.update(global_upper_filter=filtered, residual_sector_certificate=sector,
                      filter=sector_filtered, shifted_rayleigh_upper=sector_filtered['shifted_rayleigh_upper'],
                      energy_rayleigh_upper=str(E00 + F(sector_filtered['shifted_rayleigh_upper'])),
                      strict_improvement_display=float(F(sector_filtered['improvement'])),
                      new_shifted_rayleigh_upper_display=float(F(sector_filtered['shifted_rayleigh_upper'])))
    if geometry_source:
        result['geometry_source'] = str(geometry_source.relative_to(ROOT))
        result['geometry_source_sha256'] = hashlib.sha256(geometry_source.read_bytes()).hexdigest()
    if source:
        result['source'] = str(source.relative_to(ROOT))
        result['source_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
    return result


def input_path(nx, ny, g):
    g = F(g)
    name = f'block1_{nx}x{ny}_g{g}.json'.replace('/', 'd')
    if g < F(3, 50):
        return RESEARCH / 'large_seed_moments' / name
    if g == F(3, 50):
        return RESEARCH / 'low_band' / 'frontier_g006' / name
    return RESEARCH / 'low_band' / 'frontier_g007_g010' / f'g{g}'.replace('/', 'd') / name


def main():
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (1024 ** 3, 1024 ** 3))
    if hasattr(os, 'sched_setaffinity'):
        os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    rows = []
    for g in map(F, ('3/100', '1/25', '1/20', '3/50', '7/100', '2/25', '1/10')):
        for nx, ny in ((4, 4), (8, 4), (8, 8)):
            path = input_path(nx, ny, g)
            record = json.loads(path.read_text())
            geometry_path = RESEARCH / 'large_seed_moments' / f'geometry_{nx}x{ny}.json'
            geometry = json.loads(geometry_path.read_text())
            result = certificate(record, path, geometry, geometry_path)
            name = f'filtered_{nx}x{ny}_g{g}.json'.replace('/', 'd')
            (HERE / name).write_text(json.dumps(result, indent=2) + '\n')
            rows.append(dict(geometry=[nx, ny], g=str(g), file=name,
                             old_shifted_rayleigh=result['exact_original_shifted_rayleigh'],
                             shifted_rayleigh_upper=result['shifted_rayleigh_upper'],
                             improvement=result['filter']['improvement'],
                             improvement_display=result['strict_improvement_display'],
                             compressed_H_upper=result['compressed_upper_certificate']['compressed_H_upper']))
            print(nx, ny, g, result['strict_improvement_display'], flush=True)
    (HERE / 'summary.json').write_text(json.dumps(rows, indent=2) + '\n')


if __name__ == '__main__':
    main()
