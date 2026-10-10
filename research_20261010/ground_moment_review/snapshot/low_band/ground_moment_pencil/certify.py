"""Indefinite full-ground-space moment pencils; exact rational acceptance only.
No new physical vectors, Hamiltonian actions or higher moments are generated.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
import json,math,hashlib,time,copy,resource
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.linalg import eigh
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RES=BAND.parent
sys.path.insert(0,str(BAND));sys.path.insert(0,str(BAND/'tail_comparison'))
from low_band_certificate import exact_inertia
from propose import paths


def certify_pencil(G,A,B,a,external_low_count=1,digits=13):
    """Certify lowest usable bounds with m unrestricted independent columns.

    Caller must establish: these exact full moments belong to one invariant
    sector with exactly external_low_count eigenvalues strictly below a.
    A-aG may be indefinite. If r negative Ritz values occur, obtain lower
    bounds for sector levels k+1-r,...,k (one-based), k=external_low_count.
    """
    G,A,B=[np.asarray(x,dtype=object) for x in (G,A,B)];a=F(a);m=len(G);k=int(external_low_count)
    assert 1<=k and all(x.shape==(m,m) and np.array_equal(x,x.T) for x in (G,A,B))
    gi=exact_inertia(G);assert gi==(0,0,m)
    K=A-a*G;S=B-2*a*A+a*a*G
    ki=exact_inertia(K);si=exact_inertia(S);assert si==(0,0,m)
    r=ki[0];assert 0<r<=k
    scale=np.sqrt(np.diag(np.array(S,float)))
    sf=np.array(S,float)/scale[:,None]/scale[None,:]
    kf=np.array(K,float)/scale[:,None]/scale[None,:]
    mus,vecs=eigh(kf,sf);unit=F(1,10**digits);rows=[]
    def inertia_at(endpoint):return exact_inertia(B-(a+endpoint)*A+a*endpoint*G)
    for j in range(r):
        value=float(a)+1/mus[j]
        lo=min(F(math.floor(value*10**digits)-8,10**digits),a-unit)
        stride=unit
        while inertia_at(lo)[0]<j+1:
            lo-=stride;stride*=2
        hi=min(F(math.ceil(value*10**digits)+8,10**digits),a-unit)
        stride=unit
        while inertia_at(hi)[0]>=j+1:
            hi+=stride;stride*=2
            assert hi<a
        witness=None
        if j==0:
            vf=vecs[:,j]/scale;vf/=max(abs(vf))
            v=np.array([int(round(x*2**50)) for x in vf],dtype=object)
            q=F(v@(B-(a+lo)*A+a*lo*G)@v)
            assert q<0
            witness=dict(coefficients=list(map(int,v)),bits=50,exact_endpoint_quadratic_form=str(q),
              explanation='Exact negative direction supplies an independent scalar acceptance check for j=1.')
        rows.append(dict(sector_eigenvalue_index_one_based=k-j,lower=str(lo),negative_direction_witness=witness,
          endpoint_pencil_inertia=list(inertia_at(lo)),floating_proposal=value,
          optimal_pencil_endpoint_upper=str(hi),upper_pencil_inertia=list(inertia_at(hi)),
          pencil_root_bracket_width=str(hi-lo)))
    return dict(external_cutoff=str(a),external_low_count_required=k,trial_dimension=m,
      gram_inertia=list(gi),cutoff_ritz_inertia=list(ki),shifted_squared_moment_inertia=list(si),
      negative_inverse_ritz_count=r,endpoints=rows)


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def build(g,nx,ny):
    start=time.monotonic();gp,bp,op=paths(g,nx,ny)
    gr,br,old=[json.loads(p.read_text()) for p in (gp,bp,op)]
    G,K,J=[np.array(gr[key],dtype=object) for key in ('gram','shifted_hamiltonian_numerator','shifted_H2_numerator')]
    d=gr['integer_matrix_denominator'];A=K*F(1,d);B=J*F(1,d*d)
    a0,a1,a=[F(row['lower']) for row in br['bins'][:3]]
    rho=F(gr['exact_rayleigh'])-F(gr['E00']);c=np.array(gr['coefficients'],dtype=object)
    norm=F(c@G@c);assert F(c@A@c)/norm==rho
    r2=F(c@B@c)/norm-rho*rho;assert r2==F(gr['exact_residual_squared'])
    # Complete audited physical band + all-state comparison provide the sector
    # count. These explicit inequalities are rechecked, not inferred from GAB.
    assert rho<a1<a and len(old['blocks'][1]['eigen_upper'])==nx*ny
    assert old['blocks'][1]['multiplicity']==3
    assert max(map(F,old['blocks'][1]['eigen_upper']))<a
    assert F(old['global_lambda_kplus1_lower'])==a
    cert=certify_pencil(G,A,B,a)
    lo=F(cert['endpoints'][0]['lower']);oldlo=F(old['blocks'][0]['eigen_lower'][0]);assert oldlo<lo<=rho
    tag=f'{nx}x{ny}_g{g}'.replace('/','d')
    sources={str(p.relative_to(RES)):sha(p) for p in (gp,bp,op)}
    rec=dict(status='exact_candidate_pending_independent_review',nx=nx,ny=ny,g=str(g),
      N=nx*ny,physical_spin_count=2*nx*ny,full_hilbert_dimension=4**(nx*ny),
      energy_shift=gr['E00'],retained_ground_states=1,ground_trial_dimension=len(G),
      source_sha256=sources,ground_upper=str(rho),ground_lower=str(lo),
      old_ground_lower=str(oldlo),old_ground_width=str(rho-oldlo),ground_width=str(rho-lo),
      improvement=str(lo-oldlo),pencil=cert,
      external_count_basis='Audited complete 1+3N band below a: one even ground trial, 3N odd triplet directions. Full-spectrum lambda_(2+3N)>=a leaves exactly one even level below a. rho<a1 identifies it as global ground.',
      whole_band_count_cutoff_margin=str(a-max(map(F,old['blocks'][1]['eigen_upper']))),
      certificate_wall_seconds=time.monotonic()-start)
    (HERE/f'ground_{tag}.json').write_text(json.dumps(rec,indent=2))
    patched=copy.deepcopy(old);patched['status']='full_ground_space_moment_pencil_candidate_pending_independent_review'
    patched['method']='Full indefinite 11/29-direction ground inverse-moment pencil; unchanged triplet endpoints and all-state bins.'
    patched['blocks'][0]['previous_eigen_lower']=patched['blocks'][0]['eigen_lower'][:]
    patched['blocks'][0]['eigen_lower']=[str(lo)];patched['ground_width']=str(rho-lo)
    patched['ground_moment_pencil_source']=f'ground_{tag}.json';patched['ground_moment_pencil_source_sha256']=sha(HERE/f'ground_{tag}.json')
    (HERE/f'temple_{tag}.json').write_text(json.dumps(patched,indent=2))
    print('CERTIFIED',g,nx,ny,'width',float(rho-lo),'improvement',float(lo-oldlo),'seconds',rec['certificate_wall_seconds'],flush=True)
    return rec


if __name__=='__main__':
    rows=[build(g,nx,ny) for g in map(F,('3/100','1/25','1/20','3/50','7/100','2/25','1/10')) for nx,ny in ((4,4),(8,4),(8,8))]
    summary=dict(status='exact_candidate_pending_independent_review',method='indefinite inverse-moment pencil, one external low state, trial m=11 or29',
      no_new_physical_inputs=True,patches=rows,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (HERE/'ground_summary.json').write_text(json.dumps(summary,indent=2))
