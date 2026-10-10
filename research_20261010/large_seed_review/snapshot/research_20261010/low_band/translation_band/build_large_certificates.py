import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,math,hashlib
from translated_band import HERE,BAND,RESEARCH,Quad
sys.path.insert(0,str(BAND))
import number_sector_tail as NT
import low_band_certificate as L
import correlated_low_band as C
NT.OUT=HERE

def bipartite_counts(nx,ny):
    assert nx>=4 and ny>=4 and nx%2==ny%2==0
    n=nx*ny
    upper=[]
    for q in range(n+1):
        direct=min(2*q,(q*q)//4,2*n)
        rem=n-q;complement=4*q-2*n+min(2*rem,(rem*rem)//4,2*n)
        upper.append(min(direct,complement))
    empty=[2*n-4*q+upper[q] for q in range(n+1)];assert all(x>=0 for x in empty)
    return dict(N=n,degrees=[4]*n,occupied_edge_max=upper,empty_edge_max=empty,enumeration_size=0,
      counts_status='certified upper bounds, not exact occupancy maxima',
      proof='Simple degree-four bipartite graph: e(S)<=min(2q,floor(q²/4)), and e(S)=4q-2N+e(S complement).')

def scalar_schur(theta,r2,b):
    proposal=(float(theta)+float(b)-math.sqrt((float(b)-float(theta))**2+4*float(r2)))/2
    lo=L.lower_round(proposal,digits=12)
    while (b-lo)*(theta-lo)<r2:lo-=F(1,10**10)
    return lo

def build(nx,ny,g):
    tag=f'translated_{nx}x{ny}_g{g}'.replace('/','d');fourier=json.loads((HERE/f'{tag}_fourier.json').read_text())
    if nx==ny==4:
        ground_path=RESEARCH/'symmetry'/f'symmetry_4x4_g{g}_block1.json'.replace('/','d')
    else:ground_path=RESEARCH/'symmetry'/f'analytic_{nx}x{ny}_g{g}.json'.replace('/','d')
    ground=json.loads(ground_path.read_text());rho=F(ground['exact_rayleigh'])-F(ground['E00']);r2=F(ground['exact_residual_squared'])
    count=NT.certify_bins(nx,ny,g);a=F(count['bins'][2]['lower']);L0=F(count['bins'][0]['lower'])
    r=max(rho,F(fourier['ritz_max_upper']));eps=max(r2,F(fourier['residual_squared_bound']));assert a>r
    sin2=min(F(1),eps/(a-r)**2);b=a-(a-L0)*sin2;assert b>r
    grouplo=scalar_schur(rho,r2,b)
    lower=[];upper=[];checks=[]
    for mode in fourier['modes']:
        th=Quad(*map(F,mode['theta']));rr=Quad(*map(F,mode['residual_squared']))
        proposal=(float(th)+float(b)-math.sqrt((float(b)-float(th))**2+4*float(rr)))/2
        lo=L.lower_round(proposal,digits=12)
        while ((b-lo)*(th-lo)-rr).sign()<0:lo-=F(1,10**10)
        lower.append(str(lo));upper.append(mode['theta_upper']);checks.append(((b-lo)*(th-lo)-rr).json())
    n=nx*ny
    blocks=[dict(k=1,multiplicity=1,eigen_lower=[str(grouplo)],eigen_upper=[str(rho)],trial_dimension=ground['trial_subspace_dimension']),
            dict(k=n,multiplicity=3,eigen_lower=lower,eigen_upper=upper,schur_Qsqrt2_margins=checks)]
    rec=dict(status='translation_compressed_full_band_candidate_pending_independent_review',nx=nx,ny=ny,N=n,g=str(g),
       energy_shift=str(-F(3*n,4)),full_hilbert_dimension=4**n,retained_full_band_dimension=1+3*n,
       relative_form_bound=ground['relative_form_bound'],number_sector_bins=count,blocks=blocks,
       global_lambda_kplus1_lower=str(a),global_ground_lower=str(L0),ritz_max_upper=str(r),residual_squared_bound=str(eps),
       orthogonal_complement_lower=str(b),ground_source=str(ground_path.relative_to(RESEARCH)),
       ground_source_sha256=hashlib.sha256(ground_path.read_bytes()).hexdigest(),fourier_source=f'{tag}_fourier.json',
       ground_width=str(rho-grouplo),full_band_gap_widths=[str(F(u)-F(l)) for l,u in zip(lower,upper)])
    (HERE/f'{tag}_low_band.json').write_text(json.dumps(rec,indent=2))
    print('LARGE CERT',nx,ny,'a',float(a),'b',float(b),'groundwidth',float(rho-grouplo),'eta2',float(eps),flush=True)
    return rec

if __name__=='__main__':
    NT.occupation_counts=bipartite_counts
    r=[build(nx,ny,F(3,100)) for nx,ny in [(4,4),(8,4),(8,8)]]
    # Correlated ratio formulas use rung-index roles only and remain unchanged.
    best=[]
    for order in ['xyt','xty','txy']:
        grid=sorted((C.float_score(r,b/20,order),F(b,20)) for b in range(100,601))
        ok=[(score,b) for score,b in grid if score<0]
        best.append(dict(order=order,best=([float(ok[0][0]),str(ok[0][1])] if ok else None),accepted_float=len(ok),scope='beta5..30 step.05, diagnostic not exclusion'))
    (HERE/'large_seed_float_diagnostics_g003.json').write_text(json.dumps(best,indent=2));print('LARGE SEED PROPOSALS',best,flush=True)
