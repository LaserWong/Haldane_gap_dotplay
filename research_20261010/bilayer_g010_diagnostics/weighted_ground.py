import os,sys,resource,json,math,hashlib,copy,time
from pathlib import Path
from fractions import Fraction as F
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
cpus=os.sched_getaffinity(0);os.sched_setaffinity(0,{5 if 5 in cpus else min(cpus)})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(300,300))
import numpy as np
from scipy.linalg import eigh
HERE=Path(__file__).resolve().parent;RES=HERE.parent;BAND=RES/'low_band'
sys.path.insert(0,str(BAND/'third_moment_exact'))
from enlarged_numerator import build

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def encode(a):return [[str(x) for x in row] for row in a]
def moment_pencil(gr,geom):
 # The exact build checks every M0..M4 block. M5 is then from the full first
 # Hamiltonian moment on span(B,H B,H^2 B); never H^2 on that enlarged span.
 G,K,M5=build(gr,geom)
 den=gr['integer_matrix_denominator']; n=geom['pair_orbits'];d=n+1;h=F(gr['coupling'])*den/2
 gb=np.array(gr['gram'],dtype=object)[:d,:d];hb=np.array(gr['shifted_hamiltonian_numerator'],dtype=object)[:d,:d]
 ff,ss=[np.array(geom[k],dtype=object) for k in ('F','S')]
 fe=np.vstack([np.zeros((1,n),dtype=object),ff])
 C=np.array([[F(hb[i,j],gb[i,i]) for j in range(d)] for i in range(d)],dtype=object)
 D=np.array([[F(h*fe[i,j],gb[i,i]) for j in range(n)] for i in range(d)],dtype=object)
 E=np.column_stack([np.zeros(n,dtype=object),np.eye(n,dtype=object)])
 T=np.block([[C,D],[h*E,4*den*np.eye(n,dtype=object)],[np.zeros((n,d),dtype=object),h*np.eye(n,dtype=object)]])
 ids=gr['selected_basis_indices']; C3=(T.T@K@T)[np.ix_(ids,ids)]*F(1,den**3)
 moments=[np.array(gr[k],dtype=object)*scale for k,scale in [('gram',F(1)),('shifted_hamiltonian_numerator',F(1,den)),('shifted_H2_numerator',F(1,den**2))]]+[C3]
 return moments,M5

def propose(mom,a,U):
 G,A,B,C=mom;gg=U*G-A;aa=U*A-B;bb=U*B-C
 K=aa-a*gg;S=bb-2*a*aa+a*a*gg
 scale=np.sqrt(np.array(np.diag(S),float));kn=np.array(K,float)/scale[:,None]/scale[None,:];sn=np.array(S,float)/scale[:,None]/scale[None,:]
 mu,v=eigh(kn,sn);assert mu[0]<0 and mu[1]>=0
 lo_float=float(a)+1/mu[0];lo=F(math.floor(lo_float*10**12)-4,10**12)
 c=v[:,0]/scale;c/=max(abs(c));c=np.array([int(round(x*2**50)) for x in c],dtype=object)
 vals=[F(c@m@c) for m in mom];q=U*vals[2]-vals[3]-(a+lo)*(U*vals[1]-vals[2])+a*lo*(U*vals[0]-vals[1])
 assert q<0 and lo<a and vals[0]>0
 assert q==F(c@(bb-(a+lo)*aa+a*lo*gg)@c)
 return dict(lower=str(lo),lower_display=float(lo),U=str(U),a=str(a),coefficients=list(map(int,c)),quadratic_moments_0_to_3=list(map(str,vals)),negative_polynomial_witness=str(q),float_root=lo_float,trial_dimension=len(c),no_M6_used=True)

def main():
 out=[]
 for shape in ['4x4','8x4','8x8']:
  start=time.monotonic();gp=BAND/'frontier_g007_g010'/'g1d10'/f'block1_{shape}_g1d10.json';geompath=BAND/'third_moment_exact'/f'geometry_{shape}_origin.json';patchpath=BAND/'combined_ground_bounds'/'combined'/f'patch_{shape}_g1d10.json'
  gr,geom,patch=[json.loads(p.read_text()) for p in (gp,geompath,patchpath)]
  mom,M5=moment_pencil(gr,geom);a=F(patch['global_lambda_kplus1_lower']);N=patch['N'];U=N*(1+F(patch['g']))
  # Required sector-count inequalities; complete odd family already audited.
  assert max(map(F,patch['blocks'][1]['eigen_upper']))<a
  assert F(gr['exact_rayleigh'])-F(gr['E00'])<F(patch['all_excited_global_lower'])<a
  r=propose(mom,a,U);old=F(patch['blocks'][0]['eigen_lower'][0]);r.update(shape=shape,old_lower=str(old),improvement=str(F(r['lower'])-old),improvement_display=float(F(r['lower'])-old),sources={str(p.relative_to(RES)):sha(p) for p in (gp,geompath,patchpath)},status='exact_polynomial_candidate_pending_independent_review',seconds=time.monotonic()-start)
  assert F(r['lower'])>old
  (HERE/f'weighted_ground_{shape}.json').write_text(json.dumps(r,indent=2)+'\n')
  (HERE/f'moments_{shape}.json').write_text(json.dumps(dict(moments_G_A_B_C=[encode(m) for m in mom],integer_M5=M5.tolist(),integer_denominator=gr['integer_matrix_denominator']),indent=2)+'\n')
  p=copy.deepcopy(patch);p['blocks'][0]['eigen_lower']=[r['lower']];p['weighted_ground_witness']=r
  (HERE/f'patch_{shape}_g1d10.json').write_text(json.dumps(p,indent=2)+'\n')
  out.append(r);print(shape,r['old_lower'],r['lower_display'],r['improvement_display'],r['seconds'],flush=True)
 (HERE/'weighted_summary.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
