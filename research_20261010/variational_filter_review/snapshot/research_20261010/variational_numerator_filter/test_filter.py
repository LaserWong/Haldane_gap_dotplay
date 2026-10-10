"""Exact producer tests for local normalization, support, and filter algebra.

This is not the independent audit. Tiny physical vectors are test fixtures only;
no production candidate is expanded into physical configurations.
"""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import resource
resource.setrlimit(resource.RLIMIT_AS, (1024 ** 3, 1024 ** 3))
if hasattr(os, 'sched_setaffinity'):
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
import sys
sys.dont_write_bytecode = True
import json
import itertools
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import sympy as S
import filter_rayleigh as C


def inertia(matrix):
    a = [[F(v) for v in row] for row in matrix]
    negative = positive = 0
    while a:
        n = len(a)
        i = next((i for i in range(n) if a[i][i]), None)
        if i is None:
            pair = next(((i, j) for i in range(n) for j in range(i + 1, n) if a[i][j]), None)
            if pair is None:
                return [negative, n, positive]
            i, j = pair
            for k in range(n):
                a[i][k] += a[j][k]
            for k in range(n):
                a[k][i] += a[k][j]
        a[0], a[i] = a[i], a[0]
        for row in a:
            row[0], row[i] = row[i], row[0]
        p = a[0][0]
        negative += p < 0
        positive += p > 0
        a = [[a[i][j] - a[i][0] * a[0][j] / p for j in range(1, n)] for i in range(1, n)]
    return [negative, 0, positive]


def local_kernel():
    # Computational spin order is down-down, down-up, up-down, up-up.
    # Columns are singlet, t-, t0, t+; all are orthonormal.
    U = S.Matrix([[0, 1, 0, 0], [-1 / S.sqrt(2), 0, 1 / S.sqrt(2), 0],
                  [1 / S.sqrt(2), 0, 1 / S.sqrt(2), 0], [0, 0, 0, 1]])
    assert U.T * U == S.eye(4)
    T = S.kronecker_product(U, U)
    raw = S.zeros(16)
    for c in range(16):
        for i, j in ((0, 2), (1, 3)):
            bi, bj = (c >> (3 - i)) & 1, (c >> (3 - j)) & 1
            raw[c, c] += S.Rational((2 * bi - 1) * (2 * bj - 1), 4)
            if bi != bj:
                raw[c ^ (1 << (3 - i)) ^ (1 << (3 - j)), c] += S.Rational(1, 2)
    K = (T.T * raw * T).applyfunc(S.simplify)
    assert K == K.T and all(v.is_Rational for v in K)
    k = [[F(str(K[i, j])) for j in range(16)] for i in range(16)]
    q = [int(i // 4 != 0) + int(i % 4 != 0) for i in range(16)]
    assert all(not k[i][j] or abs(q[i] - q[j]) in (0, 2) for i in range(16) for j in range(16))
    preserving = [[k[i][j] if q[i] == q[j] else F(0) for j in range(16)] for i in range(16)]
    upper_diff = [[F(q[i], 2) * (i == j) - preserving[i][j] for j in range(16)] for i in range(16)]
    lower_diff = [[F(q[i], 2) * (i == j) + preserving[i][j] for j in range(16)] for i in range(16)]
    upper_inertia, lower_inertia = inertia(upper_diff), inertia(lower_diff)
    assert upper_inertia[0] == lower_inertia[0] == 0
    actual = {(i // 4, i % 4): k[i][0] for i in range(16) if q[i] == 2 and k[i][0]}
    assert actual == {(1, 3): -F(1, 2), (2, 2): F(1, 2), (3, 1): -F(1, 2)}
    # Verify support theorem at the operator-kernel level, not only on trials.
    for source_q in (0, 2, 4):
        for i in range(16):
            for j in range(16):
                if k[i][j] and q[j] <= source_q:
                    target_q = source_q - q[j] + q[i]
                    assert target_q <= source_q + 2 and target_q % 2 == source_q % 2
    return k, dict(normalized_local_kernel=[[str(x) for x in row] for row in k],
                   upper_local_inertia=upper_inertia, lower_local_inertia=lower_inertia,
                   orthonormal_basis_verified=True, all_local_number_changes_zero_or_two=True,
                   production_trial_support_even_q_le4_implies_residual_even_q_le6=True)


def physical_tests(kernel):
    # Small 2x2 periodic test includes the genuine doubled-edge convention.
    edges = C.graph(2, 2)
    g = F(1, 10)
    def apply(vector):
        out = defaultdict(F)
        for state, coefficient in vector.items():
            out[state] += sum(x != 0 for x in state) * coefficient
            for (i, j), w in edges.items():
                source = 4 * state[i] + state[j]
                for target in range(16):
                    if kernel[target][source]:
                        new = list(state)
                        new[i], new[j] = divmod(target, 4)
                        out[tuple(new)] += coefficient * g * w * kernel[target][source]
        return {state: value for state, value in out.items() if value}
    def inner(v, w):
        return sum((a * w.get(s, 0) for s, a in v.items()), F(0))
    def combine(v, w, t):
        return {s: v.get(s, 0) + t * w.get(s, 0) for s in v.keys() | w.keys()
                if v.get(s, 0) + t * w.get(s, 0)}
    fixtures = [{(0, 0, 0, 0): F(1)},
                {(0, 0, 0, 0): F(5), (1, 3, 0, 0): F(-1), (2, 2, 0, 0): F(1),
                 (3, 1, 0, 0): F(-1), (1, 3, 1, 3): F(1, 5)},
                {s: F((sum((i + 2) * x for i, x in enumerate(s)) % 7) - 3, 5)
                 for s in itertools.product(range(4), repeat=4) if sum(x != 0 for x in s) % 2 == 0}]
    upper = F(C.compressed_upper(2, 2, g)['compressed_H_upper'])
    out = []
    for v in fixtures:
        norm = inner(v, v)
        Hv = apply(v)
        rho = inner(v, Hv) / norm
        r = combine(Hv, v, -rho)
        variance = inner(r, r) / norm
        assert variance > 0 and inner(v, r) == 0
        Hr = apply(r)
        assert inner(r, Hr) <= upper * inner(r, r)
        f = C.optimize_filter(rho, variance, upper)
        t = F(f['t'])
        phi = combine(v, r, -t)
        norm_phi = inner(phi, phi)
        assert norm_phi / norm == F(f['normalization_squared'])
        actual_rayleigh = inner(phi, apply(phi)) / norm_phi
        assert actual_rayleigh <= F(f['shifted_rayleigh_upper']) < rho
        out.append(dict(original_rayleigh=str(rho), variance=str(variance),
                        actual_filtered_rayleigh=str(actual_rayleigh),
                        proved_filtered_upper=f['shifted_rayleigh_upper'],
                        exact_normalization_checked=True, exact_residual_orthogonality_checked=True))
    return out


def main():
    kernel, local = local_kernel()
    physical = physical_tests(kernel)
    algebra = []
    for rho, variance, upper in ((F(-3), F(1, 100), F(7)),
                                 (F(0), F(4), F(3)),
                                 (F(-1, 8), F(1, 10 ** 60), F(4))):
        f = C.optimize_filter(rho, variance, upper)
        delta, t = F(f['improvement']), F(f['t'])
        assert delta * (upper - rho + delta) <= variance
        assert rho + variance * (-2 * t + (upper - rho) * t * t) / (1 + t * t * variance) <= rho - delta
        algebra.append(f)
    assert C.optimize_filter(F(1), F(0), F(2))['shifted_rayleigh_upper'] == '1'
    replay = []
    for path in sorted(C.HERE.glob('filtered_*x*_g*.json')):
        saved = json.loads(path.read_text())
        source = C.ROOT / saved['source']
        geometry_source = C.ROOT / saved['geometry_source']
        recreated = C.certificate(json.loads(source.read_text()), source,
                                  json.loads(geometry_source.read_text()), geometry_source)
        assert recreated == saved
        replay.append(path.name)
    assert len(replay) == 21
    result = dict(status='producer_exact_tests_pass_not_independent_audit', local=local,
                  small_physical_filters=physical, filter_algebra_edge_cases=algebra,
                  exact_replayed_candidate_files=replay, all_21_sector_norm_sums_exact=True)
    (C.HERE / 'test_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print('PASS: normalized physical local bound, parity/support, three physical filter fixtures,',
          'zero/tiny-variance algebra, and all 21 exact candidate replays.', flush=True)


if __name__ == '__main__':
    main()
