"""Separate direct-Temple variant of frozen large translated-band candidates.

No physical input is regenerated or changed. Every source is hashed. Once the
global count proves one low state in each invariant symmetry sector, the scalar
Temple endpoint uses the full counted cutoff, with no angle degradation.
"""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from fractions import Fraction as F
import hashlib, json, argparse
HERE = Path(__file__).resolve().parent
BAND = HERE.parent
TRANSLATION = BAND/'translation_band'
sys.path.insert(0, str(TRANSLATION))
from translated_band import Quad
import large_refined_pipeline as P
import correlated_low_band as C
import low_band_certificate as L


def read_source(path, sources):
    sources[str(path.relative_to(BAND.parent))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return json.loads(path.read_text())


def build(nx, ny, g):
    sources = {}
    tag = f'translated_{nx}x{ny}_g{g}'.replace('/', 'd')
    old = read_source(TRANSLATION/'refined'/f'{tag}_block1_low_band.json', sources)
    fourier = read_source(TRANSLATION/f'{tag}_fourier.json', sources)
    gr = read_source(BAND.parent/old['ground_source'], sources)
    a = F(old['global_lambda_kplus1_lower'])
    rho = F(gr['exact_rayleigh'])-F(gr['E00'])
    rr = F(gr['exact_residual_squared'])
    assert rho < F(old['all_excited_global_lower']) < a
    assert F(fourier['ritz_max_upper']) < a
    # Audit the ground scalar independently from its full stored moment matrices.
    c = list(map(int, gr['coefficients']))
    den = int(gr['integer_matrix_denominator'])
    def quadratic(key):
        return sum(c[i]*int(gr[key][i][j])*c[j] for i in range(len(c)) for j in range(len(c)))
    gn, ga, gb = [quadratic(key) for key in ('gram', 'shifted_hamiltonian_numerator', 'shifted_H2_numerator')]
    assert F(ga, den*gn) == rho
    assert F(gb, den*den*gn)-rho*rho == rr
    gl = rho-rr/(a-rho)
    lower, upper, exact_endpoints, margins = [], [], [], []
    for mode in fourier['modes']:
        th = Quad(*map(F, mode['theta']))
        r2 = Quad(*map(F, mode['residual_squared']))
        assert (a-th).sign() > 0 and r2.sign() >= 0
        endpoint = th-r2/(a-th)
        lbound, _ = endpoint.bounds(bits=128)
        lo = L.down(lbound, digits=14)
        margin = (a-th)*(th-lo)-r2
        assert margin.sign() >= 0
        lower.append(str(lo)); upper.append(mode['theta_upper'])
        exact_endpoints.append(endpoint.json()); margins.append(margin.json())
    assert gl >= F(old['blocks'][0]['eigen_lower'][0])
    assert all(F(l)>=F(o) for l,o in zip(lower,old['blocks'][1]['eigen_lower']))
    rec = {k:old[k] for k in ('nx','ny','N','g','energy_shift','full_hilbert_dimension',
                            'retained_full_band_dimension','relative_form_bound','number_sector_bins',
                            'global_lambda_kplus1_lower','global_ground_lower','all_excited_global_lower')}
    rec.update(status='direct_sector_Temple_candidate_pending_independent_review',
               method='counted full band plus rank-one invariant-sector Temple',
               ground_width=str(rho-gl), source_sha256=sources,
               blocks=[dict(k=1, multiplicity=1, eigen_lower=[str(gl)], eigen_upper=[str(rho)],
                            trial_dimension=gr['trial_subspace_dimension']),
                       dict(k=nx*ny,multiplicity=3,eigen_lower=lower,eigen_upper=upper,
                            exact_Qsqrt2_Temple_endpoints=exact_endpoints,
                            exact_Qsqrt2_Temple_margins=margins)])
    (HERE/f'{tag}_temple_low_band.json').write_text(json.dumps(rec,indent=2))
    print('TEMPLE PATCH',nx,ny,g,'ground width',float(rho-gl),'triplet max width',
          max(float(F(u)-F(l)) for l,u in zip(lower,upper)),flush=True)
    return rec


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--couplings',default='3/100,1/25,1/20')
    args=parser.parse_args()
    summary=[]
    for g in map(F,args.couplings.split(',')):
        recs=[build(nx,ny,g) for nx,ny in [(4,4),(8,4),(8,8)]]
        proposals=sorted((C.float_score(recs,b/20,'xyt'),F(b,20)) for b in range(100,601))
        row=dict(g=str(g),status='direct_moment_large_seed_candidate_pending_independent_review',
                 grid_scope='beta5..30 step.05; floating proposals only')
        if proposals[0][0]<0:
            score,beta=proposals[0]
            row.update(float_proposal_score=score,exact=P.exact_seed(recs,beta))
            print('TEMPLE SEED',g,beta,row['exact'].get('bootstrap'),flush=True)
        (HERE/f'temple_seed_g{g}.json'.replace('/','d')).write_text(json.dumps(row,indent=2))
        summary.append(row)
    (HERE/'temple_seed_summary.json').write_text(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
