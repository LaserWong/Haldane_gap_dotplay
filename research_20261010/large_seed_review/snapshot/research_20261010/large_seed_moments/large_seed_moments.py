"""Exact geometry-only one-block Krylov moments for ordinary half-spin bilayers.

Q4 trial basis L=A_42 B is g independent. Inner products remove 2**N.
For H'=Q+t A, t=g/2, the basis (B,L) spans (B,H'B) when g!=0.
All H-applied leakage through q6 is retained in J, without physical states.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS'):os.environ[key]='1'
import sys,json,time,math,subprocess,argparse,resource
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import scipy.linalg as la
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research_20261010'/'symmetry'))
from symmetric_ground import Model,independent_indices
from local_relative_bound import optimize_bound

def geometry(nx,ny,force=False):
    path=OUT/f'geometry_{nx}x{ny}.json'
    if path.exists() and not force:return json.loads(path.read_text())
    m=Model(nx,ny,'1/2');_,orbits=m.q2_basis();ids={pair:i for i,orb in enumerate(orbits) for pair in orb}
    inp=OUT/f'geometry_{nx}x{ny}.txt'
    inp.write_text(f'{m.N} {len(orbits)}\n{len(m.edges)}\n'+''.join(f'{a//2} {b//2} {mul}\n' for a,b,mul in m.edges)+' '.join(str(ids[i,j]) for i in range(m.N) for j in range(i+1,m.N))+'\n')
    start=time.monotonic()
    subprocess.run([str(OUT/'contract_geometry'),str(inp),str(path)],check=True,timeout=600)
    rec=json.loads(path.read_text());rec.update(nx=nx,ny=ny,wall_seconds=time.monotonic()-start,geometry_process_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,pair_orbit_sizes=[len(o) for o in orbits])
    assert rec['S']==list(map(list,zip(*rec['S'])))
    for key in ['F','V','W']:assert rec[key]==list(map(list,zip(*rec[key])))
    path.write_text(json.dumps(rec,indent=2));return rec

def matrices(nx,ny,g,geom=None):
    m=Model(nx,ny,g);_,orbits=m.q2_basis();n=len(orbits);d=n+1;N=m.N;p=m.g.numerator;den=m.den;h=2*p
    ids={pair:i+1 for i,orb in enumerate(orbits) for pair in orb}
    mm=np.zeros((N,N),dtype=object)
    for i,j,mul in m.edges:mm[i//2,j//2]=mm[j//2,i//2]=mul
    diag=[1]+[3*len(o) for o in orbits];G=np.diag(diag).astype(object);C=np.zeros((d,d),dtype=object)
    for j,orb in enumerate(orbits,1):C[0,j]=6*p*sum(mm[a,b] for a,b in orb)
    for row,orb in enumerate(orbits,1):
        i,j=orb[0];C[row,0]=h*mm[i,j];C[row,row]=2*den-4*p*mm[i,j]
        for k in range(N):
            if k not in (i,j):C[row,ids[tuple(sorted((k,j)))]]+=h*mm[i,k];C[row,ids[tuple(sorted((k,i)))]]+=h*mm[j,k]
    if geom is None:geom=geometry(nx,ny)
    ff,ss,vv,ww=[np.array(geom[k],dtype=object) for k in ['F','S','V','W']]
    FE=np.vstack([np.zeros((1,n),dtype=object),ff]);FF=np.column_stack([np.zeros(d,dtype=object),FE])
    temp=FE.copy()
    for i in range(d):
        for j in range(n):assert temp[i,j]%diag[i]==0;temp[i,j]//=diag[i]
    Gblock=np.block([[G,np.zeros((d,n),dtype=object)],[np.zeros((n,d),dtype=object),ff]])
    Kblock=np.block([[G@C,h*FE],[h*FE.T,4*den*ff+h*ss]])
    JBB=C.T@G@C+h*h*FF
    JBL=h*C.T@FE+h*np.vstack([np.zeros((1,n),dtype=object),4*den*ff+h*ss])
    JLL=h*h*(FE.T@temp)+16*den*den*ff+8*den*h*ss+h*h*(vv+ww)
    Jblock=np.block([[JBB,JBL],[JBL.T,JLL]])
    assert np.array_equal(Kblock,Kblock.T)
    X=np.vstack([C,h*np.column_stack([np.zeros(n,dtype=object),np.eye(n,dtype=object)])])
    moments=[G,G@C,JBB,X.T@Kblock@X,X.T@Jblock@X]
    return m,Gblock,Kblock,Jblock,moments

def bilinear(v,A):return int(np.array(v,dtype=object)@A@np.array(v,dtype=object))

def certify(nx,ny,g,bits=48):
    start=time.monotonic();geom=geometry(nx,ny);m,G,K,J,moments=matrices(nx,ny,g,geom)
    inds=independent_indices(G.tolist());G=G[np.ix_(inds,inds)];K=K[np.ix_(inds,inds)];J=J[np.ix_(inds,inds)]
    scale=np.sqrt(np.diag(G).astype(float));GG=G.astype(float)/scale[:,None]/scale[None,:];KK=K.astype(float)/scale[:,None]/scale[None,:]/m.den
    vals,vecs=la.eigh(KK,GG);v=vecs[:,0]/scale;v/=max(abs(v));v=[int(round(x*2**bits)) for x in v]
    norm=bilinear(v,G);mean=F(bilinear(v,K),m.den*norm);ray=m.E00+mean;r2=F(bilinear(v,J),m.den**2*norm)-mean**2;assert r2>=0
    bound=optimize_bound(F(1,2),m.g,'bilayer',m.N);a=m.E00+F(bound['second_shift_lower'])
    lo=ray-r2/(a-ray) if ray<a else None
    rec=dict(status='exact_rational_geometry_contracted_block1_candidate' if lo is not None else 'exact_trial_moments_affine_Temple_cutoff_insufficient',s='1/2',nx=nx,ny=ny,N_dimers=m.N,physical_sites=2*m.N,coupling=str(m.g),full_dimension=4**m.N,
      q2_space_invariant_dimension=len(moments[0]),trial_subspace_dimension=len(inds),retained_states=1,block_krylov_depth=1,selected_basis_indices=inds,
      basis='B vacuum/pair orbits, followed by g-independent L=A42 pair orbit vectors; inner products divided by 2**N',
      gram_common_factor_removed=str(2**m.N),gram=G.tolist(),shifted_hamiltonian_numerator=K.tolist(),shifted_H2_numerator=J.tolist(),integer_matrix_denominator=m.den,
      shifted_integer_moments_M0_to_M4=[a.tolist() for a in moments],coefficients=v,bits=bits,E00=str(m.E00),second_eigenvalue_lower=str(a),ground_lower=str(lo) if lo is not None else None,ground_upper=str(ray),exact_rayleigh=str(ray),exact_residual_squared=str(r2),
      ground_lower_display=float(lo) if lo is not None else None,ground_upper_display=float(ray),ground_width_display=float(ray-lo) if lo is not None else None,exact_residual_squared_display=float(r2),relative_form_bound=bound,
      geometry_file=f'geometry_{nx}x{ny}.json',geometry_seconds=geom['total_seconds'],certificate_seconds=time.monotonic()-start,peak_process_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      proof='Exact q4 matching action and q6 Gram contractions retain all H-applied sectors. Temple uses the existing all-sector relative-form comparison. Independent audit pending.')
    tag=f'block1_{nx}x{ny}_g{m.g}'.replace('/','d');(OUT/f'{tag}.json').write_text(json.dumps(rec,indent=2))
    print(json.dumps({k:rec[k] for k in ['nx','ny','coupling','trial_subspace_dimension','ground_upper_display','ground_width_display','exact_residual_squared_display','geometry_seconds','certificate_seconds','peak_process_rss_kib']}),flush=True)
    return rec

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--nx',type=int,default=4);ap.add_argument('--ny',type=int,default=4);ap.add_argument('--g',default='3/100');args=ap.parse_args();certify(args.nx,args.ny,args.g)
