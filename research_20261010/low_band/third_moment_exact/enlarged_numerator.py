"""Exact one-state Rayleigh numerator from span(B,H'B,H'^2B).

Uses B,L,U=A44L+A64L, with maximum triplet number six. No residual of
the enlarged trial, H'^6 base moment, or denominator bound is evaluated.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys,json,time,hashlib,resource
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import scipy.linalg as la
from exact_filter import HERE,RES,third_moment,dot
sys.dont_write_bytecode=True
sys.path.insert(0,str(RES/'symmetry'))
from symmetric_ground import independent_indices

def build(record,geom):
    n=geom['pair_orbits'];d=n+1;den=record['integer_matrix_denominator'];h=F(record['coupling'])*den/2;assert h.denominator==1;h=int(h)
    gb=np.array(record['gram'],dtype=object)[:d,:d]
    hb=np.array(record['shifted_hamiltonian_numerator'],dtype=object)[:d,:d]
    ff,ss,vv,ww=[np.array(geom[k],dtype=object) for k in ('F','S','V','W')]
    tt=np.array(geom['X'],dtype=object)+np.array(geom['Y'],dtype=object)+np.array(geom['Y'],dtype=object).T+np.array(geom['Z'],dtype=object)
    fe=np.vstack([np.zeros((1,n),dtype=object),ff]);se=np.vstack([np.zeros((1,n),dtype=object),ss]);zero=np.zeros((d,n),dtype=object)
    G=np.block([[gb,zero,zero],[zero.T,ff,ss],[zero.T,ss,vv+ww]])
    K=np.block([[hb,h*fe,h*se],[h*fe.T,4*den*ff+h*ss,4*den*ss+h*(vv+ww)],[h*se.T,4*den*ss+h*(vv+ww),4*den*vv+6*den*ww+h*tt]])
    assert np.array_equal(G,G.T) and np.array_equal(K,K.T)
    C=np.array([[F(hb[i,j],gb[i,i]) for j in range(d)] for i in range(d)],dtype=object)
    BfromL=np.array([[F(h*fe[i,j],gb[i,i]) for j in range(n)] for i in range(d)],dtype=object)
    E=np.column_stack([np.zeros(n,dtype=object),np.eye(n,dtype=object)])
    T_old=np.block([[C,BfromL],[h*E,4*den*np.eye(n,dtype=object)],[np.zeros((n,d),dtype=object),h*np.eye(n,dtype=object)]])
    J3=T_old.T@K@T_old
    coef=np.array([int(x) for x in record['coefficients']],dtype=object)
    indices=record['selected_basis_indices'];J3selected=J3[np.ix_(indices,indices)]
    known=third_moment(record,geom)
    assert F(coef@J3selected@coef,den**3)/known['norm']==known['m3']
    B0=np.vstack([np.eye(d,dtype=object),np.zeros((2*n,d),dtype=object)])
    B1=T_old[:,:d]
    B2=T_old@B1[:d+n,:]
    powers=[B0,B1,B2]
    moments=[np.array(a,dtype=object) for a in record['shifted_integer_moments_M0_to_M4']]
    for i in range(3):
        for j in range(3):assert np.array_equal(powers[i].T@G@powers[j],moments[i+j]),(i,j,'G')
    for i in range(3):
        for j in range(3):
            if i+j+1<=4:assert np.array_equal(powers[i].T@K@powers[j],moments[i+j+1]),(i,j,'K')
    M5=B2.T@K@B2
    assert all(F(x).denominator==1 for x in M5.flat)
    return G,K,np.vectorize(int,otypes=[object])(M5)

def main():
    start=time.monotonic();source=Path(sys.argv[1]).resolve();gp=Path(sys.argv[2]).resolve();out=Path(sys.argv[3])
    record=json.loads(source.read_text());geom=json.loads(gp.read_text());G,K,M5=build(record,geom)
    indices=independent_indices(G.tolist());GG=G[np.ix_(indices,indices)];KK=K[np.ix_(indices,indices)];den=record['integer_matrix_denominator']
    scales=np.sqrt(np.diag(GG).astype(float));Gn=GG.astype(float)/scales[:,None]/scales[None,:];Kn=KK.astype(float)/scales[:,None]/scales[None,:]/den
    vals,vecs=la.eigh(Kn,Gn,check_finite=True);v=vecs[:,0]/scales;v/=max(abs(v));bits=56;ints=[int(round(x*2**bits)) for x in v]
    norm=dot(ints,GG.tolist());mean=dot(ints,KK.tolist())/den/norm
    original=F(record['exact_rayleigh'])-F(record['E00']);assert norm>0 and mean<original
    r=dict(status='exact_rational_enlarged_numerator_candidate_pending_independent_review',
      nx=record['nx'],ny=record['ny'],coupling=record['coupling'],physical_spins=2*record['nx']*record['ny'],full_dimension=record['full_dimension'],
      basis='B vacuum/pair orbits, L=A42B, U=A44L+A64L; inner products divided by 2**N',
      span_identity='For g>0 this equals span(B,Hprime B,Hprime^2 B).',
      proposed_basis_columns=len(G),exact_gram_rank=len(indices),selected_basis_indices=indices,
      retained_numerator_states=1,max_triplet_number=6,no_q8_support_constructed=True,
      no_enlarged_trial_residual_claim=True,no_base_M6_claim=True,denominator_lower_bounds_unchanged=True,
      integer_matrix_denominator=den,gram=GG.tolist(),shifted_H_numerator=KK.tolist(),coefficients=ints,coefficient_rounding_bits=bits,
      exact_norm=str(norm),shifted_rayleigh_upper=str(mean),energy_rayleigh_upper=str(mean+F(record['E00'])),
      shifted_rayleigh_upper_display=float(mean),unrounded_float_ritz_diagnostic=float(vals[0]),
      improvement_over_original_display=float(original-mean),
      exact_integer_base_M5=M5.tolist(),old_M0_through_M4_all_hankel_blocks_reproduced=True,
      original_trial_H3_agrees_with_separate_sector_formula=True,
      source_sha256={str(p.relative_to(RES)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (source,gp)},
      seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ('nx','ny','exact_gram_rank','shifted_rayleigh_upper_display','seconds','peak_rss_kib')}),flush=True)
if __name__=='__main__':main()
