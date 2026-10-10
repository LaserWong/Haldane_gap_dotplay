"""One-Ritz-state deterministic heat-trace certificate for weakly coupled dimers.
All accepted energies, tails, and bootstrap inputs are rational. Float eigsh only
proposes a vector, rounded to an exact dyadic vector before verification.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
 os.environ[k]='1'
from pathlib import Path
import sys, math, time, json, argparse, resource
from fractions import Fraction as F
from functools import reduce
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
ORIGINAL=Path(__file__).resolve().parents[1]/'original/Haldane_extensions/code'
sys.path.insert(0,str(ORIGINAL))
from analytic_certificates import exp_bounds, down
from bootstrap_scalar import replay
OUT=Path(__file__).resolve().parent

def states_with_sum(d,L,total):
 """No full-Hilbert-space digit table is stored."""
 ids=[]; rows=[]; pw=[d**j for j in range(L)]
 def rec(j,left,idx,row):
  if j==L:
   if left==0: ids.append(idx); rows.append(tuple(row))
   return
  for a in range(max(0,left-(d-1)*(L-j-1)),min(d-1,left)+1):
   rec(j+1,left-a,idx+a*pw[j],row+[a])
 rec(0,total,0,[])
 return ids,rows,pw

def model_bonds(M,W,g,k):
 """Open transverse width; periodic x. Return exact graph edges."""
 index=lambda x,y,a:2*(W*(x%M)+y)+a
 strong=[]; weak=[]
 for x in range(M):
  for y in range(W):
   strong.append((index(x,y,1),index(x+1,y,0),F(1)))
   if g: weak.append((index(x,y,0),index(x,y,1),g))
  for y in range(W-1):
   for a in range(2):
    if k: weak.append((index(x,y,a),index(x,y+1,a),k))
 return strong,weak

def integer_sector(s,L,bonds,magnetization=0):
 assert s in [F(1,2),F(1)]
 d=int(2*s+1)
 ids,digits,pw=states_with_sum(d,L,int(s*L+magnetization))
 lookup={a:i for i,a in enumerate(ids)}
 den=reduce(math.lcm,[4*v.denominator for _,_,v in bonds],1)
 rr=[];cc=[];vv=[]
 for col,(idx,a) in enumerate(zip(ids,digits)):
  diag=F(0)
  for j,k,g in bonds:
   diag+=g*(a[j]-s)*(a[k]-s)
   off=g/(2 if s==F(1,2) else 1)
   val=int(off*den)
   if a[j]<d-1 and a[k]>0:
    rr.append(lookup[idx+pw[j]-pw[k]]);cc.append(col);vv.append(val)
   if a[j]>0 and a[k]<d-1:
    rr.append(lookup[idx-pw[j]+pw[k]]);cc.append(col);vv.append(val)
  assert (diag*den).denominator==1
  if diag: rr.append(col);cc.append(col);vv.append(int(diag*den))
 A=sp.coo_matrix((np.array(vv,dtype=np.int64),(rr,cc)),shape=(len(ids),len(ids))).tocsr()
 A.sum_duplicates();A.eliminate_zeros()
 assert (A-A.T).nnz==0
 return A,den

def exact_ritz(A,den,vector,bits=44):
 """Exact Rayleigh quotient and squared residual; vector scale cancels."""
 ints=[int(round(float(x)*2**bits)) for x in vector]
 norm=sum(x*x for x in ints)
 Av=[]
 for i in range(A.shape[0]):
  Av.append(sum(int(A.data[j])*ints[int(A.indices[j])] for j in range(A.indptr[i],A.indptr[i+1])))
 va=sum(v*w for v,w in zip(ints,Av))
 aa=sum(w*w for w in Av)
 rho=F(va,den*norm)
 res2=F(aa,den*den*norm)-rho*rho
 assert res2>=0
 return rho,res2,ints

def certify_model(s,M,W,g,k,bits=44):
 start=time.monotonic()
 strong,weak=model_bonds(M,W,g,k)
 N=M*W;L=2*N;D=int(2*s+1)**L
 E00=-N*s*(s+1)
 # Every weak AF bond has lower bound -g*s(s+1); ferromagnetic
 # bonds have lower bound g*s^2. This sum need not be tight.
 Vmin=sum((-g*s*(s+1) if g>=0 else g*s*s) for _,_,g in weak)
 Vmax=sum((g*s*s if g>=0 else -g*s*(s+1)) for _,_,g in weak)
 second_lower=E00+1+Vmin
 assert second_lower>E00, 'Simple deterministic completeness certificate is insufficient.'
 A,den=integer_sector(s,L,strong+weak)
 built=time.monotonic()
 H=A.astype(float)/den
 vals,vecs=eigsh(H,k=1,which='SA',tol=2e-13,v0=np.random.default_rng(1512).normal(size=H.shape[0]),maxiter=20000)
 solved=time.monotonic()
 rho,res2,ints=exact_ritz(A,den,vecs[:,0],bits)
 assert rho<second_lower
 elo=rho-res2/(second_lower-rho)
 ehi=rho
 # Existence of a ground eigenvalue <= E00 follows from the strong-dimer
 # product trial state, whose expectation of all distinct-dimer weak bonds is 0.
 # Weyl gives lambda_1 >= second_lower > E00, hence exactly one eigenvalue below.
 rec=dict(status='exact_rational_ground_and_dimer_tail_certificate',s=str(s),M=M,W=W,
  physical_sites=L,full_dimension=D,retained_states=1,ritz_sector_dimension=A.shape[0],
  sparse_nnz=A.nnz,g=str(g),k=str(k),E00=str(E00),Vmin=str(Vmin),Vmax=str(Vmax),
  second_eigenvalue_lower=str(second_lower),ground_lower=str(elo),ground_upper=str(ehi),
  ground_lower_display=float(elo),ground_upper_display=float(ehi),ground_width_display=float(ehi-elo),
  exact_rayleigh=str(rho),exact_residual_squared=str(res2),exact_residual_squared_display=float(res2),
  dyadic_vector_bits=bits,build_seconds=built-start,ritz_seconds=solved-built,
  verification_seconds=time.monotonic()-solved,total_seconds=time.monotonic()-start,
  peak_process_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  proof=dict(no_missed_state='Weyl lambda_1 >= E00+1+Vmin > E00; dimer-product trial gives lambda_0 <= E00',
   ground_enclosure='Temple: rho-residual_squared/(second_lower-rho) <= lambda_0 <= rho',
   omitted_spectrum='Ordered Weyl bounds lambda_j(H)>=lambda_j(H0)+Vmin for every j>=1',
   exact_arithmetic='Integer matrix; dyadic Ritz vector; Python integer dot products; Fraction endpoints'))
 # Persist the exact proposal, not just diagnostics, for independent replay.
 stem=f"s{s}_M{M}_W{W}_g{g}_k{k}".replace('/','d')
 np.savez_compressed(OUT/f'{stem}_ritz.npz',vector=np.array(ints,dtype=np.int64),bits=bits)
 (OUT/f'{stem}_ground.json').write_text(json.dumps(rec,indent=2))
 return rec

def q_tail(rec,beta):
 """Trace relative to the *certified upper ground energy*, with exact bounds."""
 s=F(rec['s']);N=rec['M']*rec['W'];E00=F(rec['E00']);vmin=F(rec['Vmin'])
 elo=F(rec['ground_lower']);ehi=F(rec['ground_upper'])
 zlo=F(1);zhi=F(1)
 for j in range(1,int(2*s)+1):
  lo,hi=exp_bounds(-beta*F(j*(j+1),2))
  zlo+=(2*j+1)*lo;zhi+=(2*j+1)*hi
 # All but H0's unique ground state count in (z^N-1).
 tail=exp_bounds(-beta*(E00+vmin-ehi))[1]*(zhi**N-1)
 ground_hi=exp_bounds(beta*(ehi-elo))[1]
 return F(1),ground_hi+tail,tail

def seed(rn,r2n,beta):
 beta=F(beta)
 assert r2n['M']==2*rn['M'] and rn['W']==r2n['W']
 an,bn,tn=q_tail(rn,beta);a2,b2,t2=q_tail(r2n,beta);a22,b22,t22=q_tail(r2n,2*beta)
 shift=F(r2n['ground_upper'])-2*F(rn['ground_upper'])
 S=down(exp_bounds(-beta*shift)[0]*a2/bn**2)
 T=down(a22/b2**2)
 # Numerical upper endpoints are also deterministic, if useful to exclude seeds.
 Sup=exp_bounds(-beta*shift)[1]*b2/an**2
 Tup=b22/a2**2
 boot=replay(str(S),str(T),rn['M'],str(beta)) if S>0 and T>0 else {'status':'purity_rounded_to_zero'}
 return dict(beta=str(beta),S_lower=str(S),T_lower=str(T),S_lower_display=float(S),T_lower_display=float(T),
  S_upper_display=float(Sup),T_upper_display=float(Tup),
  tail_n_upper_display=float(tn),tail_2n_upper_display=float(t2),
  energy_defect_upper=str(F(r2n['ground_upper'])-2*F(rn['ground_lower'])),
  bootstrap=boot)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--spin',default='1');ap.add_argument('--g',default='1/20');ap.add_argument('--k',default='0');ap.add_argument('--width',type=int,default=1);ap.add_argument('--betas',default='6,8,10,12,16,20');args=ap.parse_args()
 s,g,k=map(F,[args.spin,args.g,args.k]); W=args.width
 recs=[]
 for M in [2,4]:
  rec=certify_model(s,M,W,g,k);recs.append(rec)
  print('GROUND',s,M,W,g,k,{a:rec[a] for a in ['full_dimension','ritz_sector_dimension','ground_upper_display','ground_width_display','total_seconds']},flush=True)
 results=[seed(*recs,F(b)) for b in args.betas.split(',')]
 for r in results: print('SEED',r['beta'],r['S_lower_display'],r['T_lower_display'],r['bootstrap']['status'],r['bootstrap'].get('conditional_gap_lower_rational'),flush=True)
 output=dict(status='deterministic_exact_rational_certificates',model={'spin':str(s),'width':W,'g':str(g),'k':str(k)},ground_certificates=recs,seeds=results)
 path=OUT/('certificate_s%s_W%s_g%s_k%s.json'%(s,W,g,k)).replace('/','d')
 path.write_text(json.dumps(output,indent=2));print('SAVED',path,flush=True)
if __name__=='__main__': main()
