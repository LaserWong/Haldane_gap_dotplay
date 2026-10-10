"""Exact-input, all-beta obstruction for the three inequivalent small-seed orders.

Physical endpoints are those of the already accepted independent reconstruction.
This new scalar proof imports no producer recurrence, trace, or arithmetic code.
The only reused arithmetic is the separately reviewed rational exp enclosure.
"""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[name] = '1'
import sys
import resource
sys.dont_write_bytecode = True
resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
if hasattr(os, 'sched_setaffinity'):
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESEARCH = HERE.parent
sys.path.insert(0, str(RESEARCH / 'low_band_review'))
from fast_exp import exp_interval, up

HASHES = {}
ORDERS = ('xyt', 'xty', 'txy')


def digest(path):
    key = str(path.relative_to(ROOT))
    value = hashlib.sha256(path.read_bytes()).hexdigest()
    if key in HASHES:
        assert HASHES[key] == value
    HASHES[key] = value
    return value


def read(path):
    digest(path)
    return json.loads(path.read_text())


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: serial(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(val) for val in value]
    return value


def source_data(g, physical):
    answer = []
    for shape, n in (('2x2', 4), ('4x2', 8), ('4x4', 16)):
        path = RESEARCH / 'low_band' / 'frontier' / f'bilayer_{shape}_g{g}_symmetric_number_low_band.json'
        rec = read(path)
        assert HASHES[str(path.relative_to(ROOT))] == physical['input_sha256'][str(path.relative_to(ROOT))]
        assert rec['N'] == n
        assert rec['full_hilbert_dimension'] == 4**n
        assert rec['retained_full_band_dimension'] == 1 + 3*n
        base = F(rec['blocks'][0]['eigen_upper'][0])
        retained_upper, all_lower = [], []
        for block in rec['blocks']:
            assert len(block['eigen_lower']) == len(block['eigen_upper']) == block['k']
            for lower, upper in zip(block['eigen_lower'], block['eigen_upper']):
                assert F(lower) <= F(upper)
                retained_upper.append((F(upper)-base, block['multiplicity']))
                all_lower.append((F(lower)-base, block['multiplicity']))
        assert sum(m for _, m in retained_upper) == 1+3*n
        assert all(energy >= 0 for energy, _ in retained_upper)
        bins = rec['number_sector_bins']['bins']
        assert bins[2]['first_ordered_index'] == 2+3*n
        for row in bins[2:]:
            all_lower.append((F(row['lower'])-base, row['multiplicity']))
        assert sum(m for _, m in all_lower) == 4**n
        width = base-F(rec['blocks'][0]['eigen_lower'][0])
        assert width >= 0
        assert all(energy+width >= 0 for energy, _ in all_lower)
        answer.append(dict(shape=shape, N=n, E=F(rec['energy_shift'])+base,
                           ground_width=width, upper=retained_upper, lower=all_lower))
    return answer


def trace(terms, left, right, upper):
    result = F(0)
    for energy, multiplicity in terms:
        endpoint = (left if energy >= 0 else right) if upper else (right if energy >= 0 else left)
        result += multiplicity*exp_interval(-energy*endpoint)[int(upper)]
    return result


def emax(slope, left, right):
    return exp_interval(slope*(right if slope >= 0 else left))[1]


def inputs(data, left, right):
    """Uniform upper bounds on every physical quotient on [left,right]."""
    low = [trace(row['upper'], left, right, False) for row in data]
    low2 = [trace(row['upper'], 2*left, 2*right, False) for row in data]
    top = trace(data[2]['lower'], 2*left, 2*right, True)
    e0, e1, e2 = [row['E'] for row in data]
    j1 = emax(8*e0-2*e2, left, right)*top/low[0]**8
    j2space = emax(8*e1-4*e2, left, right)*top**2/low[1]**8
    j2time = emax(16*e0-4*e2, left, right)*top**2/low2[0]**8
    ctime = top/low[2]**2
    cspace = emax(4*e1-2*e2, left, right)*top/low2[1]**2
    raw = {'xyt': (j1, j2space, ctime),
           'xty': (j1, j2space, cspace),
           'txy': (j1, j2time, cspace)}
    return {order: [min(F(1), up(x)) for x in row] for order, row in raw.items()}


def G(x):
    assert 0 < x <= 1
    return 1-(1-x)**2/(2*x*x)


def failure(inp, limit=4):
    j1, j2, c0 = inp
    history, arguments = [], []
    for index in range(limit):
        if index == 0:
            arg = j1
        elif index == 1:
            arg = j2*history[0]
        elif index == 2:
            arg = c0**4*history[0]**2*history[1]
        else:
            arg = history[-3]**4*history[-2]**2*history[-1]
        assert 0 < arg <= 1
        value = up(G(arg))
        arguments.append(arg)
        history.append(value)
        if value <= 0:
            return dict(failed_update=index+1, nonpositive_upper=value,
                        arguments=arguments, history=history)
    return None


def edge_multiset(nx, ny):
    edges = Counter()
    for y in range(ny):
        for x in range(nx):
            for dx, dy in ((1, 0), (0, 1)):
                a, b = (x, y), ((x+dx) % nx, (y+dy) % ny)
                edges[tuple(sorted((a, b)))] += 1
    return edges


def check_exchange():
    """Executable instances of the analytic coordinate-exchange bijection."""
    result = []
    for nx, ny in ((2, 2), (4, 2), (4, 4)):
        mapped = Counter()
        for (a, b), multiplicity in edge_multiset(nx, ny).items():
            mapped[tuple(sorted(((a[1], a[0]), (b[1], b[0]))))] += multiplicity
        assert mapped == edge_multiset(ny, nx)
        result.append(dict(shape=[nx, ny], exchanged_shape=[ny, nx],
                           rung_edges=nx*ny, in_layer_edges_per_layer=2*nx*ny,
                           periodic_parallel_multiplicities_preserved=True))
    return result


def certify(g, physical):
    data = source_data(g, physical)
    # J1 = T_(2x2)(beta)^4 P_x(2x2,2beta)^2 P_y(4x2,2beta).
    # Each spatial factor <=1. Only the Gibbs purity T is monotone in beta.
    hot_t = min(F(1), up(trace(data[0]['lower'], F(8), F(8), True) /
                         trace(data[0]['upper'], F(4), F(4), False)**2))
    hot_j = up(hot_t**4)
    hot_failure = failure([hot_j, F(1), F(1)], limit=1)
    assert hot_failure is not None and hot_failure['nonpositive_upper'] < 0
    middle = {order: [] for order in ORDERS}
    for index in range(320):
        left, right = 4+F(index, 20), 4+F(index+1, 20)
        vals = inputs(data, left, right)
        for order in ORDERS:
            out = failure(vals[order], limit=4 if order == 'xyt' else 3)
            assert out is not None, (g, order, left, right, list(map(float, vals[order])))
            assert out['nonpositive_upper'] < 0
            middle[order].append(dict(beta_interval=[left, right], input_upper=vals[order], **out))
        if index % 80 == 79:
            print('CLOSED BOXES PASS', g, index+1, flush=True)
    # Rebase numerator at the physical ground lower endpoint. Every gap >=0.
    elo = data[2]['E']-data[2]['ground_width']
    slopes = {'J1': 2*elo-8*data[0]['E'],
              'J2_spatial_first': 4*elo-8*data[1]['E'],
              'J2_time_first': 4*elo-16*data[0]['E']}
    assert all(slope > 0 for slope in slopes.values())
    relative = [(gap+data[2]['ground_width'], m) for gap, m in data[2]['lower']]
    assert all(gap >= 0 for gap, _ in relative)
    cold_trace = trace(relative, F(40), F(40), True)
    cj = min(F(1), up(exp_interval(-20*slopes['J1'])[1]*cold_trace))
    cold = {}
    for order in ORDERS:
        name = 'J2_time_first' if order == 'txy' else 'J2_spatial_first'
        j2 = min(F(1), up(exp_interval(-20*slopes[name])[1]*cold_trace**2))
        inp = [cj, j2, F(1)]
        out = failure(inp, limit=2)
        assert out is not None and out['nonpositive_upper'] < 0
        cold[order] = dict(input_upper=inp, **out)
    orders = {}
    for order in ORDERS:
        rows = middle[order]
        maximum = max(row['failed_update'] for row in rows)
        orders[order] = dict(status='PASS all beta>=0 exact-input nonpositive-update obstruction',
                            maximum_global_failed_update=max(1, maximum, cold[order]['failed_update']),
                            maximum_middle_failed_update=maximum,
                            middle_failed_update_histogram=dict(Counter(str(row['failed_update']) for row in rows)),
                            closest_to_zero_middle_witness=max(rows, key=lambda row: row['nonpositive_upper']),
                            cold=cold[order], middle=rows)
    return dict(g=F(1, 25) if g == '1d25' else F(1, 20),
                beta_cover=[[0, 4], [4, 20], [20, 'infinity']],
                middle_step=F(1, 20), middle_closed_box_count=320,
                hot=dict(thermal_purity_2x2_at_beta4_upper=hot_t,
                         common_J1_upper=hot_j, **hot_failure),
                cold_positive_slopes=slopes, cold_relative_trace_at_40=cold_trace,
                orders=orders)


def main():
    start = time.monotonic()
    audit_dir = RESEARCH/'small_seed_exclusion_review'
    acceptance = read(audit_dir/'ACCEPTANCE.json')
    assert acceptance['status'] == 'PASS independent physical reconstruction and exact all-beta scalar obstruction'
    physical = read(audit_dir/'physical_results.json')
    assert HASHES[str((audit_dir/'physical_results.json').relative_to(ROOT))] == acceptance['physical_result_sha256']
    assert physical['status'] == 'PASS independently reconstructed all six physical complete bands and shell tails'
    # The proof relies on this completed reconstruction, not a fresh physical audit.
    for name, expected in physical['input_sha256'].items():
        assert digest(ROOT/name) == expected
    digest(RESEARCH/'low_band_review'/'fast_exp.py')
    digest(RESEARCH/'general_dimension_review'/'PROOF_REVIEW.md')
    result = dict(status='running', results={},
                  physical_input_status='reuses accepted independent complete-band and full-tail reconstruction; no new physical vectors',
                  exchange_checks=check_exchange())
    for g in ('1d25', '1d20'):
        result['results'][g] = certify(g, physical)
        (HERE/'results.json').write_text(json.dumps(serial(result), indent=2)+'\n')
        print('ALL BETA THREE ORDERS PASS', g, flush=True)
    for name, expected in HASHES.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected
    result.update(status='PASS all six fixed coordinate orders at g=1/25 and 1/20 for every beta>=0',
                  order_pairs={'xyt': 'yxt', 'xty': 'ytx', 'txy': 'tyx'},
                  original_spatial_seeds=['2x2', '4x2', '4x4'],
                  mirrored_spatial_seeds=['2x2', '2x4', '4x4'],
                  scope='specified correlated first cycle and same fixed cyclic recurrence; excludes exact inputs, not physical gaps or other methods',
                  input_sha256=HASHES, seconds=time.monotonic()-start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  limits=dict(cpu_count=1, BLAS_threads=1, address_space_bytes=1024**3),
                  new_physical_vectors=False, full_ED=False, remote_writes=False,
                  independent_review_status='new scalar extension awaiting independent review')
    (HERE/'results.json').write_text(json.dumps(serial(result), indent=2)+'\n')
    print(result['status'], result['seconds'], result['peak_rss_kib'], flush=True)


if __name__ == '__main__':
    main()
