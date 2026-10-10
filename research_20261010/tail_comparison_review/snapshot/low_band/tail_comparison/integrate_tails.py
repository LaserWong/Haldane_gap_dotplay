"""Recombine frozen physical moments with independently reviewed tail variants.
All new patch/trace/bridge records are separate candidates until their replay is
independently checked. No sparse trial vectors or geometry data are regenerated.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,argparse
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RESEARCH=BAND.parent
sys.path.insert(0,str(BAND/'translation_band'));sys.path.insert(0,str(BAND/'small_seed_orders'))
sys.path.insert(0,str(RESEARCH/'root_review'))
from translated_band import Quad
import low_band_certificate as L
from scan_transported import stages,score
from finite_window_2d import interpolate_2d,gap


def read(path,sources):
    sources[str(path.relative_to(RESEARCH))]=hashlib.sha256(path.read_bytes()).hexdigest()
    return json.loads(path.read_text())


def patch(nx,ny,g,variant,out):
    sources={};tag=f'{nx}x{ny}_g{g}'.replace('/','d')
    physical=BAND/'frontier_g006' if g==F(3,50) else BAND/'translation_band'
    ground=physical if g==F(3,50) else RESEARCH/'large_seed_moments'
    gr=read(ground/f'block1_{tag}.json',sources)
    four=read(physical/f'translated_{tag}_fourier.json',sources)
    if variant=='original':
        numberpath=physical/f'number_bins_{tag}.json' if g==F(3,50) else physical/'refined'/f'number_bins_{tag}.json'
    else:
        prefix='bosonic' if variant=='jacobi' else 'quadratic'
        dirname='bosonic_tail' if variant=='jacobi' else 'quadratic_boson'
        numberpath=BAND/dirname/f'{prefix}_bins_{tag}.json'
    number=read(numberpath,sources)
    rho=F(gr['exact_rayleigh'])-F(gr['E00']);r2=F(gr['exact_residual_squared'])
    a0,a1,a=[F(row['lower']) for row in number['bins'][:3]]
    assert rho<a1 and F(four['ritz_max_upper'])<a
    c=list(map(int,gr['coefficients']));den=gr['integer_matrix_denominator']
    def quadratic(key):return sum(c[i]*int(gr[key][i][j])*c[j] for i in range(len(c)) for j in range(len(c)))
    gn,ga,gb=[quadratic(k) for k in ('gram','shifted_hamiltonian_numerator','shifted_H2_numerator')]
    assert F(ga,den*gn)==rho and F(gb,den*den*gn)-rho*rho==r2
    ground_lower=rho-r2/(a-rho);lower=[];upper=[];endpoints=[]
    for mode in four['modes']:
        th=Quad(*map(F,mode['theta']));rr=Quad(*map(F,mode['residual_squared']))
        assert (a-th).sign()>0 and rr.sign()>=0
        endpoint=th-rr/(a-th);lo=L.down(endpoint.bounds(128)[0],digits=14)
        assert ((a-th)*(th-lo)-rr).sign()>=0
        lower.append(str(lo));upper.append(mode['theta_upper']);endpoints.append(endpoint.json())
    rec=dict(status='tail_recombination_candidate_pending_independent_review',tail_variant=variant,
        nx=nx,ny=ny,N=nx*ny,g=str(g),energy_shift=gr['E00'],full_hilbert_dimension=4**(nx*ny),
        retained_full_band_dimension=1+3*nx*ny,relative_form_bound=gr['relative_form_bound'],number_sector_bins=number,
        global_lambda_kplus1_lower=str(a),all_excited_global_lower=str(a1),global_ground_lower=str(a0),
        ground_width=str(rho-ground_lower),source_sha256=sources,
        blocks=[dict(k=1,multiplicity=1,eigen_lower=[str(ground_lower)],eigen_upper=[str(rho)]),
                dict(k=nx*ny,multiplicity=3,eigen_lower=lower,eigen_upper=upper,exact_Qsqrt2_Temple_endpoints=endpoints)])
    (out/f'temple_{tag}.json').write_text(json.dumps(rec,indent=2));return rec


def exact_seed(recs,beta,order,short):
    st=stages(recs,beta,order,True);assert 'canonical' in st
    abc=[L.down(x,digits=18) for x in st['canonical']]
    boot=L.replay(*abc,n=8,m=8,beta=2*beta,rounds=64,digits=18)
    out=dict(beta_initial=str(beta),order_before_transport=order,J1=str(st['J1']),J2=str(st['J2']),C0=str(st['C0']),
       permuted_first_purities=list(map(str,st['permuted_prefix'])),canonical_first_purities=list(map(str,abc)),
       canonical_base=dict(n=8,m=8,beta=str(2*beta)),bootstrap=boot,
       accepted=boot['status']=='accepted_analytic_scalar_certificate')
    if out['accepted']:
        states=[abc]+[[1-F(x) for x in r['defects']] for r in boot['updates']];windows=[]
        for j,state in enumerate(states):
            thermal,detail=interpolate_2d(*state);gg=gap(thermal,2*beta*2**j)
            assert gg is not None
            windows.append(dict(n=8*2**j,through=16*2**j,beta=str(2*beta*2**j),thermal_lower=str(thermal),
                                gap_lower=str(gg),details=detail))
        required=[F(w['gap_lower']) for w in windows if w['n']<boot['n']]
        final=min([F(boot['uniform_square_gap_lower']),short]+required)
        out.update(windows=windows,uniform_small_L2_through_L7_gap=str(short),
                   all_integer_L_ge2_gap=str(final),all_integer_gap_display=float(final))
    return out


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--variant',choices=['original','jacobi','quadratic'],default='jacobi');args=ap.parse_args()
    out=HERE/args.variant;out.mkdir(exist_ok=True)
    shortpath=BAND/'frontier_g006'/'all_size_bridges.json';shortdata=json.loads(shortpath.read_text())[0]['small_sizes']
    short=min(F(row['gap_lower']) for row in shortdata)
    # These same g=.06 compression bounds apply to every 0<=g<=.06: preserving
    # diagonals are larger and off-block norm upper bounds are no larger. This
    # is a comparison-form argument, not physical gap monotonicity in g.
    summary=[]
    for g in map(F,('3/100','1/25','1/20','3/50')):
        recs=[patch(nx,ny,g,args.variant,out) for nx,ny in ((4,4),(8,4),(8,8))];rows=[]
        for order in ('xyt','xty','txy'):
            proposals=[]
            for bi in range(100,601):
                beta=F(bi,20);st=stages(recs,float(beta),order);proposals.append((score(st,float(beta)),beta))
            value,beta=min(proposals)
            if value<0:
                row=exact_seed(recs,beta,order,short);row['float_proposal_score']=value
            else:row=dict(order_before_transport=order,status='no_successful_float_proposal')
            rows.append(row)
            print(args.variant,g,order,beta,row.get('all_integer_gap_display'),flush=True)
        rec=dict(g=str(g),tail_variant=args.variant,status='exact_recombination_candidate_pending_independent_review',
            grid_scope='beta5..30 step.05; three orders with proved canonical transport',results=rows,
            shared_short_size_source=str(shortpath.relative_to(RESEARCH)),
            shared_short_size_source_sha256=hashlib.sha256(shortpath.read_bytes()).hexdigest(),
            short_size_scope='All 0<=g<=.06 by the same g=.06 diagonal/off-block comparison; no assumed gap monotonicity')
        (out/f'recombined_g{g}.json'.replace('/','d')).write_text(json.dumps(rec,indent=2));summary.append(rec)
    (out/'summary.json').write_text(json.dumps(summary,indent=2))


if __name__=='__main__':main()
