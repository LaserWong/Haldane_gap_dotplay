"""Independent exact scalar replay; imports no project implementation.

The accepted physical-band audit is a declared dependency, not rerun here.
Exponential implementation: independently coded integer fixed-point intervals.
"""
import os
for _name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_name] = '1'
import resource
resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
if hasattr(os, 'sched_setaffinity'):
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
import hashlib
import itertools
import json
import time
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from functools import lru_cache

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NEW = HERE.parent
PRIOR = ROOT/'research_20261010/small_seed_exclusion_review'
PREC = 320
UNIT = 1 << PREC
SEEN = {}


def load(path):
    path = Path(path)
    key = str(path.relative_to(ROOT))
    dig = hashlib.sha256(path.read_bytes()).hexdigest()
    if key in SEEN:
        assert SEEN[key] == dig, ('mutated input', key)
    SEEN[key] = dig
    return json.loads(path.read_text())


def remember(path):
    key = str(path.relative_to(ROOT))
    dig = hashlib.sha256(path.read_bytes()).hexdigest()
    if key in SEEN:
        assert SEEN[key] == dig
    SEEN[key] = dig
    return dig


def ceildiv(n, d):
    assert d > 0
    return -((-n)//d)


def ceiling(x, bits=PREC):
    unit = 1 << bits
    return Q(ceildiv(x.numerator*unit, x.denominator), unit)


@lru_cache(maxsize=100000)
def exp_enclosure(z):
    """Integer-only Taylor enclosure, |reduced argument| <= 1/8.

    84 terms; remainder <= (8/7) times next term because every
    subsequent ratio <= 1/8. All rounding in recurrence/squaring is outward.
    """
    z = Q(z)
    y = abs(z)
    squares = 0
    while y > Q(1, 8):
        y /= 2
        squares += 1
    p, q = y.numerator, y.denominator
    lo_term = hi_term = lo_sum = hi_sum = UNIT
    for n in range(1, 85):
        lo_term = (lo_term*p)//(q*n)
        hi_term = ceildiv(hi_term*p, q*n)
        lo_sum += lo_term
        hi_sum += hi_term
    hi_sum += ceildiv(8*hi_term*p, 7*q*85)
    for _ in range(squares):
        lo_sum = lo_sum*lo_sum//UNIT
        hi_sum = ceildiv(hi_sum*hi_sum, UNIT)
    assert 0 < lo_sum <= hi_sum
    if z < 0:
        return Q(UNIT*UNIT//hi_sum, UNIT), Q(ceildiv(UNIT*UNIT, lo_sum), UNIT)
    return Q(lo_sum, UNIT), Q(hi_sum, UNIT)


def encode(obj):
    if isinstance(obj, Q):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [encode(v) for v in obj]
    return obj


def monomial(*pieces):
    answer = Counter()
    for poly, exponent in pieces:
        for key, value in poly.items():
            answer[key] += exponent*value
    return {key: value for key, value in answer.items() if value}


def ratio(a, b):
    return monomial(({a: 1}, 1), ({b: 1}, -2))


def double(v, axis):
    ans = list(v)
    ans['xyt'.index(axis)] += 1
    return tuple(ans)


def algebra_checks():
    ledger = {}
    v0 = (0, 0, 0)
    for chars in itertools.permutations('xyt'):
        points = [v0]
        for axis in chars:
            points.append(double(points[-1], axis))
        a, b, c = [ratio(points[i+1], points[i]) for i in range(3)]
        j1 = monomial((a, 4), (b, 2), (c, 1))
        j2 = monomial((b, 4), (c, 2))
        assert j1 == {(1, 1, 1): 1, v0: -8}
        assert j2 == {(1, 1, 1): 2, points[1]: -8}
        assert c == {(1, 1, 1): 1, points[2]: -2}
        ledger[''.join(chars)] = {'points': points, 'J1': j1, 'J2': j2, 'C0': c}
    vt = double(v0, 't')
    vtx = double(vt, 'x')
    hot = monomial((ratio(vt, v0), 4), (ratio(vtx, vt), 2), (ratio((1, 1, 1), vtx), 1))
    assert hot == {(1, 1, 1): 1, v0: -8}
    assert ledger['xyt']['points'][1:3] == [(1, 0, 0), (1, 1, 0)]
    assert ledger['xty']['points'][1:3] == [(1, 0, 0), (1, 0, 1)]
    assert ledger['txy']['points'][1:3] == [(0, 0, 1), (1, 0, 1)]
    return {'all_six_order_quotients': ledger, 'shared_hot_identity': hot}


def graph(nx, ny):
    edges = Counter()
    for x in range(nx):
        for y in range(ny):
            edges[('rung', tuple(sorted(((x, y, 0), (x, y, 1)))))] += 1
            for layer in range(2):
                for dx, dy in ((1, 0), (0, 1)):
                    endpoints = ((x, y, layer), ((x+dx)%nx, (y+dy)%ny, layer))
                    edges[('intralayer', tuple(sorted(endpoints)))] += 1
    return edges


def symmetry_checks():
    rows = []
    for nx, ny in ((2, 2), (4, 2), (4, 4), (2, 4)):
        original = graph(nx, ny)
        exchanged = Counter()
        for (kind, endpoints), count in original.items():
            exchanged[(kind, tuple(sorted((y, x, layer) for x, y, layer in endpoints)))] += count
        assert exchanged == graph(ny, nx)
        assert sum(n for (kind, _), n in original.items() if kind == 'rung') == nx*ny
        assert sum(n for (kind, _), n in original.items() if kind == 'intralayer') == 4*nx*ny
        rows.append({'shape': [nx, ny], 'spin_permutation_bijective': True,
                     'rung_and_all_layer_bond_multisets_equal': True,
                     'parallel_bonds_preserved': True})
    return rows


def verify_dependencies():
    frozen = load(NEW/'PRODUCER_FREEZE_SHA256.json')
    assert set(frozen) == {'certify_orders.py', 'PROOF.md', 'results.json'}
    for name, expected in frozen.items():
        assert remember(NEW/name) == expected, ('producer freeze mismatch', name)
    manifest = load(PRIOR/'MANIFEST_SHA256.json')
    for name, expected in manifest.items():
        assert remember(PRIOR/name) == expected, name
    sources = load(PRIOR/'SOURCE_MANIFEST_SHA256.json')
    for name, expected in sources.items():
        assert remember(ROOT/name) == expected, name
    accepted = load(PRIOR/'ACCEPTANCE.json')
    physical = load(PRIOR/'physical_results.json')
    assert accepted['status'].startswith('PASS independent physical reconstruction')
    assert physical['status'] == 'PASS independently reconstructed all six physical complete bands and shell tails'
    assert remember(PRIOR/'physical_results.json') == accepted['physical_result_sha256']
    for name, expected in physical['input_sha256'].items():
        assert remember(ROOT/name) == expected, name
    producer = load(NEW/'results.json')
    assert producer['status'] == 'PASS all six fixed coordinate orders at g=1/25 and 1/20 for every beta>=0'
    for name, expected in producer['input_sha256'].items():
        assert remember(ROOT/name) == expected, name
    remember(NEW/'certify_orders.py')
    return producer, {'accepted_manifest_entries': len(manifest), 'prior_source_entries': len(sources),
                      'physical_input_entries': len(physical['input_sha256']),
                      'producer_freeze_entries': len(frozen),
                      'physical_result_sha256': accepted['physical_result_sha256']}


def bands(tag):
    ans = []
    for shape, nx, ny in (('2x2', 2, 2), ('4x2', 4, 2), ('4x4', 4, 4)):
        doc = load(ROOT/f'research_20261010/low_band/frontier/bilayer_{shape}_g{tag}_symmetric_number_low_band.json')
        n = nx*ny
        assert doc['N'] == n and doc['nx'] == nx and doc['ny'] == ny
        assert Q(doc['g']) == Q(1, 25 if tag == '1d25' else 20)
        assert Q(doc['energy_shift']) == -Q(3*n, 4)
        assert doc['full_hilbert_dimension'] == 4**n
        assert doc['retained_full_band_dimension'] == 3*n+1
        u0 = Q(doc['blocks'][0]['eigen_upper'][0])
        l0 = Q(doc['blocks'][0]['eigen_lower'][0])
        low_terms, high_terms = [], []
        for block in doc['blocks']:
            assert len(block['eigen_upper']) == len(block['eigen_lower']) == block['k']
            for l, u in zip(block['eigen_lower'], block['eigen_upper']):
                l, u = Q(l), Q(u)
                assert l <= u and u >= u0
                low_terms.append((u-u0, block['multiplicity']))
                high_terms.append((l-u0, block['multiplicity']))
        shell = doc['number_sector_bins']['bins']
        assert shell[2]['first_ordered_index'] == 2+3*n
        high_terms += [(Q(row['lower'])-u0, row['multiplicity']) for row in shell[2:]]
        assert sum(m for _, m in low_terms) == 3*n+1
        assert sum(m for _, m in high_terms) == 4**n
        assert all(e+u0-l0 >= 0 for e, _ in high_terms)
        ans.append({'low': low_terms, 'high': high_terms, 'base': -Q(3*n,4)+u0, 'width': u0-l0})
    return ans


def sum_bounds(terms, left, right):
    """Enclose an exponential sum over a closed beta interval."""
    lower = upper = Q(0)
    for gap, multiplicity in terms:
        # Sort arguments, not thermal values; exp is increasing.
        a, b = sorted((-gap*left, -gap*right))
        lower += multiplicity*exp_enclosure(a)[0]
        upper += multiplicity*exp_enclosure(b)[1]
    return lower, upper


def exp_max(c, left, right):
    return exp_enclosure(max(c*left, c*right))[1]


def cap(x):
    return min(Q(1), ceiling(x))


def initial_upper(data, left, right):
    lower1 = [sum_bounds(patch['low'], left, right)[0] for patch in data]
    lower2 = [sum_bounds(patch['low'], 2*left, 2*right)[0] for patch in data]
    numerator = sum_bounds(data[2]['high'], 2*left, 2*right)[1]
    e4, e8, e16 = [patch['base'] for patch in data]
    first = exp_max(8*e4-2*e16, left, right)*numerator/lower1[0]**8
    second_space = exp_max(8*e8-4*e16, left, right)*numerator**2/lower1[1]**8
    second_time = exp_max(16*e4-4*e16, left, right)*numerator**2/lower2[0]**8
    final_time = numerator/lower1[2]**2
    final_space = exp_max(4*e8-2*e16, left, right)*numerator/lower2[1]**2
    return {o: [cap(x) for x in row] for o, row in
            {'xyt': (first, second_space, final_time), 'xty': (first, second_space, final_space),
             'txy': (first, second_time, final_space)}.items()}


def map_G(x):
    assert 0 < x <= 1
    return (x*x+2*x-1)/(2*x*x)


def propagate(values, max_steps, saved=None):
    first, second, last = values
    history = []
    arguments = []
    for k in range(max_steps):
        if k == 0:
            arg = first
        elif k == 1:
            arg = second*history[0]
        elif k == 2:
            arg = last**4*history[0]**2*history[1]
        else:
            queue = history[-3:]
            arg = queue[0]**4*queue[1]**2*queue[2]
        out = map_G(arg)
        if saved is not None:
            assert arg == Q(saved['arguments'][k])
            observed = Q(saved['history'][k])
            assert observed == ceiling(out, 256)
            out = observed
        else:
            out = ceiling(out)
        history.append(out)
        arguments.append(arg)
        if out <= 0:
            assert out < 0
            if saved is not None:
                assert k+1 == saved['failed_update']
                assert out == Q(saved['nonpositive_upper'])
                assert len(saved['history']) == len(saved['arguments']) == k+1
            return {'failed_update': k+1, 'nonpositive_upper': out, 'arguments': arguments, 'history': history}
    raise AssertionError(('No failure', values, max_steps))


def check_case(tag, proposal):
    data = bands(tag)
    hot_up = cap(sum_bounds(data[0]['high'], Q(8), Q(8))[1]/sum_bounds(data[0]['low'], Q(4), Q(4))[0]**2)
    assert hot_up <= Q(proposal['hot']['thermal_purity_2x2_at_beta4_upper'])
    hot_j = ceiling(hot_up**4)
    assert hot_j <= Q(proposal['hot']['common_J1_upper'])
    hot = propagate([hot_j, Q(1), Q(1)], 1)
    propagate([Q(proposal['hot']['common_J1_upper']), Q(1), Q(1)], 1, proposal['hot'])
    result = {'hot': {'purity_upper': hot_up, 'J1_upper': hot_j, **hot}, 'orders': {o: [] for o in ('xyt','xty','txy')}}
    for k in range(320):
        left, right = Q(80+k, 20), Q(81+k, 20)
        inputs = initial_upper(data, left, right)
        for order in result['orders']:
            supplied = proposal['orders'][order]['middle'][k]
            assert list(map(Q, supplied['beta_interval'])) == [left, right]
            saved_inputs = list(map(Q, supplied['input_upper']))
            assert all(new <= old for new, old in zip(inputs[order], saved_inputs)), (tag, order, k)
            max_steps = 4 if order == 'xyt' else 3
            propagate(saved_inputs, max_steps, supplied)
            result['orders'][order].append({'interval': [left,right], 'input_upper': inputs[order], **propagate(inputs[order], max_steps)})
        if k % 80 == 79:
            print('independent closed boxes', tag, k+1, flush=True)
    e4, e8, e16 = [patch['base'] for patch in data]
    ground_lower = e16-data[2]['width']
    slopes = {'J1': 2*ground_lower-8*e4, 'J2_spatial_first': 4*ground_lower-8*e8,
              'J2_time_first': 4*ground_lower-16*e4}
    assert all(x>0 for x in slopes.values())
    assert slopes == {k:Q(v) for k,v in proposal['cold_positive_slopes'].items()}
    relative = [(gap+data[2]['width'], n) for gap,n in data[2]['high']]
    assert all(gap>=0 for gap,n in relative)
    reltrace = sum_bounds(relative, Q(40), Q(40))[1]
    assert reltrace <= Q(proposal['cold_relative_trace_at_40'])
    cold_j1 = cap(exp_enclosure(-20*slopes['J1'])[1]*reltrace)
    cold = {}
    summaries = {}
    for order, rows in result['orders'].items():
        key = 'J2_time_first' if order == 'txy' else 'J2_spatial_first'
        inp = [cold_j1, cap(exp_enclosure(-20*slopes[key])[1]*reltrace**2), Q(1)]
        provided = proposal['orders'][order]['cold']
        prior_inp = list(map(Q, provided['input_upper']))
        assert all(x<=y for x,y in zip(inp,prior_inp))
        propagate(prior_inp,2,provided)
        cold[order] = {'input_upper':inp, **propagate(inp,2)}
        counts = Counter(row['failed_update'] for row in rows)
        assert {str(k):v for k,v in counts.items()} == proposal['orders'][order]['middle_failed_update_histogram']
        assert len(proposal['orders'][order]['middle']) == 320
        global_max = max(max(counts),cold[order]['failed_update'],1)
        assert global_max == proposal['orders'][order]['maximum_global_failed_update']
        summaries[order] = {'middle_count': 320, 'update_histogram': counts, 'max_global_failed_update': global_max,
                            'least_negative_middle_witness': max(rows,key=lambda r:r['nonpositive_upper'])}
    result.update(cold=cold, positive_slopes=slopes, relative_trace_at_40=reltrace, summaries=summaries,
                  all_saved_inputs_and_witnesses_verified=True, closed_cover=[[0,4],[4,20],[20,'infinity']])
    exp_enclosure.cache_clear()
    return result


def main():
    started=time.monotonic()
    proposal,dependency_counts=verify_dependencies()
    result={'status':'running', 'dependency_checks':dependency_counts,
            'algebra':algebra_checks(), 'unitary_exchange':symmetry_checks(), 'couplings':{}}
    for tag in ('1d25','1d20'):
        result['couplings'][tag]=check_case(tag,proposal['results'][tag])
        (HERE/'results.json').write_text(json.dumps(encode(result),indent=2)+'\n')
    for name,digest in SEEN.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest, ('final hash mismatch',name)
    result.update(status='PASS independent scalar review of all six fixed cyclic orders for all beta>=0',
                  physical_status='Inherited accepted complete-band and omitted-tail reconstruction; no physical reconstruction rerun',
                  exact_arithmetic='320-bit outward integer exponential intervals, 84-term reduced Taylor series; independent code',
                  tested_closed_boxes=1920, new_physical_vectors=False, full_ED=False, remote_writes=False,
                  seconds=time.monotonic()-started, peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  limits={'cpus':1,'BLAS_threads':1,'address_space_bytes':1024**3})
    (HERE/'INPUT_SHA256.json').write_text(json.dumps(SEEN,indent=2,sort_keys=True)+'\n')
    (HERE/'results.json').write_text(json.dumps(encode(result),indent=2)+'\n')
    print(result['status'], 'seconds',result['seconds'],'rss_kib',result['peak_rss_kib'],flush=True)

if __name__=='__main__':
    main()
