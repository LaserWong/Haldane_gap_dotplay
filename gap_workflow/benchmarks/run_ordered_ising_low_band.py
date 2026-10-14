"""Bounded independent matrix-free audit. No dense matrix or full spectrum.
Run: OPENBLAS_NUM_THREADS=1 python benchmarks/run_ordered_ising_low_band.py
"""
import json, math, os, resource, time
from pathlib import Path
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh

ROOT = Path(__file__).resolve().parents[1]
MEMORY_CAP = 256 * 2**20
WALL_CAP = 20.0

def mode_prediction(L):
    sectors = []
    for shift in (0.5, 0.0):
        eps = sorted(2 * math.sqrt(0.25 + 2 * math.sin(math.pi*(m+shift)/L)**2)
                     for m in range(L))
        vacuum = -sum(eps)/2
        # Retain only four smallest even/odd subset sums at each step.
        even, odd = [0.0], []
        for e in eps:
            even, odd = (sorted(even + [x+e for x in odd])[:4],
                         sorted(odd + [x+e for x in even])[:4])
        sectors.append({'sector': 'NS' if shift else 'R', 'vacuum': vacuum,
                        'lowest_even_occupation_levels': [vacuum+x for x in even]})
    return sectors, sorted(e for s in sectors for e in s['lowest_even_occupation_levels'])[:4]

def run():
    start = time.perf_counter()
    rows = []
    for L in range(4,13):
        D = 1 << L
        # Deliberately conservative allowance, including solver work buffers.
        estimated_incremental_bytes = 8*D*(L + 4*32 + 64)
        assert estimated_incremental_bytes < MEMORY_CAP
        assert time.perf_counter()-start < WALL_CAP
        t = time.perf_counter()
        labels = np.arange(D, dtype=np.int64)
        diag = np.zeros(D)
        for i in range(L):
            a, b = (labels >> i)&1, (labels >> ((i+1)%L))&1
            diag -= (1-2*a)*(1-2*b)
        def mv(x):
            y = diag*x
            for i in range(L):
                y -= 0.5*x[labels ^ (1<<i)]
            return y
        H = LinearOperator((D,D), matvec=mv, dtype=np.float64)
        rng = np.random.default_rng(20261014 + L)
        vals, vecs = eigsh(H, k=4, which='SA', ncv=min(32,D),
                           tol=1e-12, maxiter=2000, v0=rng.normal(size=D))
        ix = np.argsort(vals); vals, vecs = vals[ix], vecs[:,ix]
        residuals = [float(np.linalg.norm(mv(v)-e*v)) for e,v in zip(vals,vecs.T)]
        parity = [float(v @ v[labels ^ (D-1)]) for v in vecs.T]
        sectors, predicted = mode_prediction(L)
        discrepancy = float(max(abs(vals-np.array(predicted))))
        assert discrepancy < 1e-8 and max(residuals) < 1e-8
        rows.append({'L':L,'full_dimension':D,'working_dimension':D,
                     'computed_eigenpairs':4,'eigenvalues':vals.tolist(),
                     'ritz_residual_norms':residuals,'spin_flip_parity_expectations':parity,
                     'true_ground_gap_candidate':float(vals[1]-vals[0]),
                     'rank_two_band_width_candidate':float(vals[1]-vals[0]),
                     'complement_separation_from_band_top_candidate':float(vals[2]-vals[1]),
                     'complement_separation_from_ground_candidate':float(vals[2]-vals[0]),
                     'mode_sectors':sectors,'mode_lowest_four':predicted,
                     'max_eigsh_mode_discrepancy':discrepancy,
                     'estimated_incremental_bytes':estimated_incremental_bytes,
                     'elapsed_seconds':time.perf_counter()-t})
        print(L, rows[-1]['true_ground_gap_candidate'],
              rows[-1]['complement_separation_from_band_top_candidate'], flush=True)
    out = {'model':{'formula':'-sum_i Z_i Z_(i+1) - (1/2)sum_i X_i',
                    'normalization':'Pauli eigenvalues +/-1',
                    'bond_convention':'periodic positive-direction; L=2 doubled bonds'},
           'evidence_class':'FLOATING_PARTIAL_SPECTRUM_AND_FLOATING_MODE_CROSSCHECK',
           'exact_results_source':'theory/ORDERED_ISING_GAP_DEFINITIONS.md',
           'floating_values_are_interval_certificates':False,
           'full_spectrum_computed':False,'memory_admission_bytes':MEMORY_CAP,
           'wall_admission_seconds':WALL_CAP,
           'total_seconds':time.perf_counter()-start,
           'process_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
           'rows':rows}
    assert out['total_seconds'] < WALL_CAP
    assert out['process_peak_rss_bytes'] < MEMORY_CAP
    (ROOT/'benchmarks/ordered_ising_low_band.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__ == '__main__':
    run()
