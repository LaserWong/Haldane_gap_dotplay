"""New small inputs and two-dimensional reweighting of saved M8 trials.
No large support expansion, new full residual, or large eigensolve.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys,json,math,hashlib,time,resource
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
from scipy.linalg import eigh
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OLD=HERE.parent/'chain_frontier'
sys.path.insert(0,str(HERE.parent/'chain_frontier_review'))
import independent_core as C
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
INPUT={}
def read(p):INPUT[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
def save(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def load(p):INPUT[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();return np.load(p,allow_pickle=False)
def matrices(paths,N):
 z=[load(p) for p in paths];basis=[tuple(map(int,s)) for s in z[0]['basis']]
 assert all(np.array_equal(zz['basis'],z[0]['basis']) for zz in z)
 vectors=[[int(x) for x in zz['vector']] for zz in z];d=len(vectors);weights=[math.prod(C.W[x] for x in s) for s in basis]
 ind=dict(zip(basis,range(len(basis))));G=[[0]*d for _ in range(d)];K0=[[0]*d for _ in range(d)];K1=[[0]*d for _ in range(d)]
 scale=math.lcm(*(c.denominator for row in C.K.values() for _,_,c in row));kernel={key:[(a,b,int(scale*c)) for a,b,c in row] for key,row in C.K.items()}
 for k,s in enumerate(basis):
  for i in range(d):
   for j in range(d):
    val=weights[k]*vectors[i][k]*vectors[j][k];G[i][j]+=val;K0[i][j]+=val*(-2*N+sum(C.EX[x] for x in s))
  for edge in range(N):
   left=(edge-1)%N
   for a,b,c in kernel[s[left],s[edge]]:
    ss=list(s);ss[left]=a;ss[edge]=b;t=ind.get(tuple(ss))
    if t is None:continue
    for i in range(d):
     factor=weights[t]*vectors[i][t]*c
     for j in range(d):K1[i][j]+=factor*vectors[j][k]
 assert G==list(map(list,zip(*G))) and K0==list(map(list,zip(*K0))) and K1==list(map(list,zip(*K1)))
 return dict(N=N,full_dimension=9**N,trial_support=len(basis),linear_combination_dimension=d,source_paths=[str(p.relative_to(ROOT)) for p in paths],G=[[str(x) for x in row] for row in G],K0=[[str(x) for x in row] for row in K0],K1_scaled=[[str(x) for x in row] for row in K1],weak_denominator=scale)

def evaluate(mat,g):
 G=[[Q(x) for x in r] for r in mat['G']];H=[[Q(x)+g*Q(y,mat['weak_denominator']) for x,y in zip(map(int,r),map(int,s))] for r,s in zip(mat['K0'],mat['K1_scaled'])]
 scale=float(G[0][0]);eig,v=eigh(np.array(H,dtype=float)/scale,np.array(G,dtype=float)/scale)
 c=[int(round(float(x)*10**12)) for x in v[:,0]]
 norm=sum(c[i]*G[i][j]*c[j] for i in range(len(c)) for j in range(len(c)))
 rho=sum(c[i]*H[i][j]*c[j] for i in range(len(c)) for j in range(len(c)))/norm
 options=[(rho,c)]+[(H[i][i]/G[i][i],[int(j==i) for j in range(len(c))]) for i in range(len(c))]
 rho,c=min(options)
 return dict(g=str(g),exact_rayleigh=str(rho),combination_integers=list(map(str,c)),matrix_file='M8_two_trial_moments.json',trial_support=mat['trial_support'],linear_combination_dimension=len(c),full_dimension=9**8,contract='Rayleigh-only; no claimed filtered residual, isolation, or tail')

def main():
 t=time.monotonic();mp=HERE/'M8_two_trial_moments.json'
 if mp.exists():mat=read(mp)
 else:
  mat=matrices([OLD/f'chain_s1_M8_g{tag}_depth4_trial.npz' for tag in ['7d40','1d5']],8);save(mp,mat)
 sys.path.insert(0,str(ROOT/'low_energy'));import dimer_subspace as ds;import local_relative_bound as lb
 ds.OUT=HERE
 records=[]
 for g in map(Q,['7/40','9/50','181/1000','91/500','183/1000','23/125','37/200','19/100','39/200','1/5']):
  tag=str(g).replace('/','d');p=HERE/f'small_g{tag}_ground.json'
  if p.exists():small=read(p)
  elif g in [Q(7,40),Q(1,5)]:small=read(OLD/f'chain_s1_M4_g{tag}_depth4_ground.json')
  else:small=ds.certify_sparse(Q(1),4,ds.columnar_bonds(4,1,g,Q(0)),tag=f'small_g{tag}',relative_bound=lb.optimize_bound(Q(1),g,'chain',4),support_depth=4)
  large=evaluate(mat,g)
  records.append(dict(g=str(g),small=small,small_folder=str((HERE if g not in [Q(7,40),Q(1,5)] else OLD).relative_to(ROOT)),large=large))
  print('INPUT',g,float(Q(large['exact_rayleigh'])-2*Q(small['exact_rayleigh'])),flush=True)
 save(HERE/'inputs.json',records);save(HERE/'INPUT_SHA256.json',INPUT)
 save(HERE/'input_resources.json',dict(seconds=time.monotonic()-t,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,AS_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0],cpu_affinity=sorted(os.sched_getaffinity(0))))
if __name__=='__main__':main()
