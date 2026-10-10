"""Independent physical/scalar verifier of the joint-purity chain extension.
Imports the pinned earlier physical kernel, never new producer modules.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys,json,math,resource,time,hashlib
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
old=HERE.parent/'chain_frontier_review';assert hashlib.sha256((old/'independent_core.py').read_bytes()).hexdigest()=='30c997e6e56135af60cd989ab22e31a8957346dc3ff2235ae8ac6b2c62916a19'
sys.path.insert(0,str(old));import independent_core as C
from functools import lru_cache
C.exp_bounds=lru_cache(maxsize=2048)(C.exp_bounds)
TRACE={}
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
def load(p):return json.loads(p.read_text())
def sqrtlo(x):
 den=10**60;k=math.isqrt(x.numerator*den*den//x.denominator)
 assert F(k*k,den*den)<=x<F((k+1)**2,den*den)
 return F(k,den)
def pure(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)
def momcheck(mat):
 # Independently reconstruct the returning-support first moments and Gram.
 arrays=[np.load(ROOT/p,allow_pickle=False) for p in mat['source_paths']]
 basis=[tuple(map(int,x)) for x in arrays[0]['basis']];N=mat['N'];d=len(arrays)
 assert len(set(basis))==mat['trial_support']==len(basis) and mat['full_dimension']==9**N and d==mat['linear_combination_dimension']
 assert all(np.array_equal(a['basis'],arrays[0]['basis']) for a in arrays)
 coeff=[[int(x) for x in a['vector']] for a in arrays];weight=[math.prod(C.W[x] for x in s) for s in basis]
 index={x:i for i,x in enumerate(basis)};out=[[[0]*d for _ in range(d)] for k in range(3)]
 den=math.lcm(*(x.denominator for row in C.K.values() for _,_,x in row))
 kk={s:[(a,b,int(x*den)) for a,b,x in row] for s,row in C.K.items()}
 for col,state in enumerate(basis):
  for i in range(d):
   for j in range(d):
    v=weight[col]*coeff[i][col]*coeff[j][col];out[0][i][j]+=v;out[1][i][j]+=v*(-2*N+sum(C.EX[x] for x in state))
  for right in range(N):
   left=(right-1)%N
   for x,y,a in kk[state[left],state[right]]:
    target=list(state);target[left]=x;target[right]=y;row=index.get(tuple(target))
    if row is not None:
     for i in range(d):
      for j in range(d):out[2][i][j]+=weight[row]*coeff[i][row]*a*coeff[j][col]
 for calc,key in zip(out,['G','K0','K1_scaled']):assert [[str(x) for x in row] for row in calc]==mat[key]
 assert den==mat['weak_denominator']
 return dict(N=N,trial_support=len(basis),full_dimension=9**N,linear_combination_dimension=d,exact_Gram_and_first_moments_identical=True,whole_residual_reconstructed=False)
def energy(mat,coeff,g):
 def bil(key):return sum(F(mat[key][i][j])*coeff[i]*coeff[j] for i in range(len(coeff)) for j in range(len(coeff)))
 norm=bil('G');assert norm>0
 return (bil('K0')+g*bil('K1_scaled')/mat['weak_denominator'])/norm

def verify_window(win,S,T,P,n,beta):
 assert win['cells']==[n,2*n] and F(win['beta'])==beta
 assert list(map(F,[win['S_lower'],win['T_lower'],win['joint_S2T_lower']]))==[S,T,P]
 assert P>=S*S*T and P>F(1,2)
 w=(1+sqrtlo(2*P-1))/2;r=(1-w)/w;D=T/(1+r*r);I=(1-r)*min(S*sqrtlo(D),D)
 saved=F(win['thermal_purity_lower']);gap=F(win['gap_lower'])
 assert F(1,2)<saved<=I and gap>0 and C.exp_bounds(beta*gap)[1]*(1-saved)<saved
 return gap

def verify_row(rec,row):
 s=rec['input']['small'];beta=F(row['beta']);shift=F(rec['input']['large']['exact_rayleigh'])-2*F(s['exact_rayleigh'])
 assert shift==F(row['Rayleigh_shift'])
 q1,q2=map(F,[row['small_Q_beta_upper'],row['small_Q_2beta_upper']]);key=(rec['g'],beta)
 if key not in TRACE:TRACE[key]=(C.trace_bound(s,beta)[0],C.trace_bound(s,2*beta)[0])
 assert TRACE[key][0]<=q1 and TRACE[key][1]<=q2
 L=C.exp_bounds(-2*beta*shift)[0];J=C.floor(L/q1**4);CC=C.floor(L/q2**2)
 assert [J,CC]==list(map(F,[row['J_lower'],row['C_lower']]))
 a=C.floor(pure(J));b=C.floor(pure(CC*CC*a));assert [a,b]==list(map(F,row['initial_time_pair']))
 n=8;be=2*beta;wi=0;gaps=[]
 for step in range(row['time_steps']):
  P=a*a*b;S=C.floor(a*sqrtlo(b));T=C.floor(P)
  state=row['states'][wi];assert state==dict(order='time-space',cells=n,beta=str(be),pair=list(map(str,[a,b])),canonical_joint=str(P))
  gaps.append(verify_window(row['windows'][wi],S,T,P,n,be));wi+=1
  a=C.floor(pure(P));b=C.floor(pure(b*b*a));n*=2;be*=2
 P=a*a*b;S=C.floor(a*sqrtlo(b));T=C.floor(P)
 conv=row['conversion'];assert conv==dict(cells=n,beta=str(be),time_pair=list(map(str,[a,b])),S_lower=str(S),T_lower=str(T),joint_S2T_lower=str(P))
 assert S*S<=P and T<=P
 for step in range(row['canonical_steps']):
  state=row['states'][wi];assert state==dict(order='space-time',cells=n,beta=str(be),pair=list(map(str,[S,T])),joint_S2T_lower=str(P))
  gaps.append(verify_window(row['windows'][wi],S,T,P,n,be));wi+=1
  # This first update uses the retained JOINT lower endpoint, not S*S*T.
  S=C.floor(pure(P));T=C.floor(pure(T*T*S));P=S*S*T;n*=2;be*=2
 assert wi==len(row['windows'])==len(row['states'])
 fin=row['final'];u=max(1-S,1-T);gap=F(fin['asymptotic_gap_lower'])
 assert fin==dict(cells=n,beta=str(be),S_lower=str(S),T_lower=str(T),common_defect_upper=str(u),asymptotic_gap_lower=str(gap))
 assert 0<u<=F(1,100) and C.exp_bounds(be*gap)[1]*5*u<1
 full=min([gap]+gaps);assert full==F(row['M_ge8_gap_lower'])
 return dict(beta=str(beta),time_steps=row['time_steps'],canonical_steps=row['canonical_steps'],joint_first_canonical_update_verified=True,all_integer_windows_verified=wi,M_ge8_gap_lower=str(full),asymptotic_from=n)

def ledger():
 def P(axis,w):
  nxt=list(w);nxt[axis]+=1
  return Counter({tuple(nxt):1,w:-2})
 def add(*terms):
  d={}
  for t in terms:
   for k,v in t.items():d[k]=d.get(k,0)+v
  return {k:v for k,v in d.items() if v}
 def scale(a,n):return {k:v*n for k,v in a.items()}
 for w in [(0,0),(1,1),(2,2),(5,5)]:
  dx=(w[0]+1,w[1]);dt=(w[0],w[1]+1)
  assert add(scale(P(0,w),2),P(1,dx))==add(scale(P(1,w),2),P(0,dt))
 return dict(identity='P_x(w)^2 P_t(D_x w) = P_t(w)^2 P_x(D_t w)',symbolic_exact_cancellation=True,coordinates='(log2 cell count, log2 inverse temperature)',tested_symbolic_basepoints=4)

def main():
 start=time.monotonic()
 for path,digest in load(HERE/'EXTERNAL_INPUT_SHA256.json').items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,('input changed',path)
 large=load(HERE/'M8_two_trial_moments.json');mcheck=momcheck(large)
 bridge_m={m:load(HERE/f'M{m}_bridge_moments.json') for m in [6,7]};bridge_checks=[momcheck(z) for z in bridge_m.values()]
 reports=[]
 for p in sorted(HERE.glob('candidate_g*.json')):
  rec=load(p);g=F(rec['g']);inp=rec['input'];C.DATA=ROOT/inp['small_folder'];small_check=C.check_ground(inp['small'])
  assert energy(large,list(map(int,inp['large']['combination_integers'])),g)==F(inp['large']['exact_rayleigh'])
  short=rec['short_bridge'];local=short['local'];psd=C.local_psd(local['local_certificate']);alpha=F(local['alpha']);b=F(local['local_certificate']['b']);sg=[]
  for m,row in zip(range(2,8),short['rows']):
   rho=min(-2*F(m),energy(bridge_m[m],[1],g)) if m in bridge_m else -2*F(m)
   cutoff=-2*m+alpha-m*b;gap=cutoff-rho
   assert gap>0 and row['M']==m and row['full_dimension']==9**m
   assert [rho,cutoff,gap]==list(map(F,[row['rayleigh_upper'],row['cutoff_lower'],row['gap_lower']]))
   sg.append(gap)
  assert min(sg)==F(short['gap_lower'])
  rows=[verify_row(rec,row) for row in rec['rows']]
  for row,chk in zip(rec['rows'],rows):assert F(row['all_M_ge2_gap_lower'])==min(F(chk['M_ge8_gap_lower']),min(sg))
  best=max(rec['rows'],key=lambda row:F(row['all_M_ge2_gap_lower']));assert best==rec['best']
  reports.append(dict(source=p.name,g=str(g),small_physical_check=small_check,short_local_check=psd,short_bridge_verified=True,rows=rows,all_M_ge2_gap_lower=best['all_M_ge2_gap_lower']))
  print('PASS',g,best['all_M_ge2_gap_lower'],flush=True)
 report=dict(status='PASS independent local verifier; external review still requested',joint_identity=ledger(),large_physical_check=mcheck,bridge_physical_checks=bridge_checks,results=reports,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,AS_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0],cpu_affinity=sorted(os.sched_getaffinity(0)))
 (HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
