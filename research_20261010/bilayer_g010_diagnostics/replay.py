"""Exact no-eigensolver replay via a separate block-Hankel coordinate formula."""
import os,sys,json,hashlib,resource
from fractions import Fraction as F
from pathlib import Path
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
cpus=os.sched_getaffinity(0);os.sched_setaffinity(0,{5 if 5 in cpus else min(cpus)})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(300,300))
HERE=Path(__file__).resolve().parent;RES=HERE.parent
import numpy as np

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def arr(x):return np.array([[F(v) for v in row] for row in x],dtype=object)
def main():
 results=[]
 for shape in ['4x4','8x4','8x8']:
  r=load(HERE/f'weighted_ground_{shape}.json');ex=load(HERE/f'moments_{shape}.json')
  for p,h in r['sources'].items():assert sha(RES/p)==h,(p,'changed')
  gp=next(p for p in r['sources'] if '/block1_' in p);gr=load(RES/gp)
  d=gr['integer_matrix_denominator'];h=F(gr['coupling'])*d/2
  ms=[arr(m) for m in gr['shifted_integer_moments_M0_to_M4']]+[arr(ex['integer_M5'])];n=len(ms[0]);m=2*n-1
  C=np.array([[ms[1][i,j]/ms[0][i,i] for j in range(n)] for i in range(n)],dtype=object)
  T=np.zeros((2*n,m),dtype=object)
  for i in range(n):T[i,i]=F(1)
  for j in range(1,n):
   for i in range(n):T[i,n+j-1]=-C[i,j]/h
   T[n+j,n+j-1]=1/h
  T=T[:,gr['selected_basis_indices']]
  mm=[]
  for k in range(4):
   bk=np.block([[ms[k],ms[k+1]],[ms[k+1],ms[k+2]]]);z=T.T@bk@T*F(1,d**k)
   assert np.array_equal(z,arr(ex['moments_G_A_B_C'][k]))
   if k<3:
    key=['gram','shifted_hamiltonian_numerator','shifted_H2_numerator'][k];assert np.array_equal(z,arr(gr[key])*F(1,d**k))
   mm.append(z)
  c=np.array(r['coefficients'],dtype=object);v=[F(c@z@c) for z in mm];assert list(map(str,v))==r['quadratic_moments_0_to_3']
  a,l,U=map(F,[r['a'],r['lower'],r['U']]);N=gr['nx']*gr['ny'];assert U==N*(1+F(gr['coupling']))
  q=-v[3]+(U+a+l)*v[2]-(U*(a+l)+a*l)*v[1]+U*a*l*v[0]
  assert q==F(r['negative_polynomial_witness'])<0 and l<a and F(r['old_lower'])<l
  patch=load(RES/next(p for p in r['sources'] if '/patch_' in p));assert a==F(patch['global_lambda_kplus1_lower'])
  assert len(patch['blocks'][1]['eigen_upper'])==N and patch['blocks'][1]['multiplicity']==3
  assert max(map(F,patch['blocks'][1]['eigen_upper']))<a
  assert F(gr['exact_rayleigh'])-F(gr['E00'])<F(patch['all_excited_global_lower'])<a
  # Endpoint-sign regression, including cutoff/upper-end eigenvalues.
  for e in [l-1,l,a,U]:assert (U-e)*(e-a)*(e-l)>=0
  for e in [(l+a)/2]:assert (U-e)*(e-a)*(e-l)<0
  results.append(dict(shape=shape,lower=str(l),exact_witness_negative=True,all_M0_to_M5_Hankel_transforms_match=True,external_count_checks=True))
 out=dict(status='exact_self_replay_pass_independent_review_required',results=results)
 (HERE/'replay_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
