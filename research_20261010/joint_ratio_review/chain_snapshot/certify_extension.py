"""Exact candidate using a retained joint purity lower bound after direction swap.
No largest residual, isolation, or complete trace is used.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys,json,math,time,resource,hashlib
from pathlib import Path
from fractions import Fraction as Q
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OLD=HERE.parent/'chain_frontier'
sys.path.insert(0,str(HERE.parent/'chain_frontier_review'));import independent_core as C
sys.path.insert(0,str(ROOT/'low_energy'));import local_relative_bound as lb
from build_inputs import matrices,evaluate
from functools import lru_cache
C.exp_bounds=lru_cache(maxsize=2048)(C.exp_bounds)
TRACE={}
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
def save(name,z):(HERE/name).write_text(json.dumps(z,indent=2)+'\n')
def G(x):
 assert 0<x<=1
 return 1-(1-x)**2/(2*x*x)
def sqrt_lower(x):
 D=10**50;k=math.isqrt(x.numerator*D*D//x.denominator);q=Q(k,D)
 assert q*q<=x<(q+Q(1,D))**2
 return q

def gap_purity(p,beta):
 if p<=Q(1,2):return Q(0)
 proposal=Q(math.floor(math.log(float(p/(1-p)))/float(beta)*10**12)-1,10**12)
 assert C.exp_bounds(beta*proposal)[1]*(1-p)<p
 return proposal

def window(S,T,P,beta,n):
 # A joint lower endpoint can equal the product after canonical rounds.
 assert 0<S<=1 and 0<T<=1 and 0<P<=1
 assert P>=S*S*T and P>Q(1,2)
 w=(1+sqrt_lower(2*P-1))/2;r=(1-w)/w;D=T/(1+r*r)
 I=C.floor((1-r)*min(S*sqrt_lower(D),D),40)
 return dict(cells=[n,2*n],beta=str(beta),S_lower=str(S),T_lower=str(T),joint_S2T_lower=str(P),
  dominant_weight_lower=str(w),absolute_tail_ratio_upper=str(r),D_lower=str(D),thermal_purity_lower=str(I),gap_lower=str(gap_purity(I,beta)))

def cycle(rec,beta,tsteps,csteps):
 small=rec['small'];shift=Q(rec['large']['exact_rayleigh'])-2*Q(small['exact_rayleigh'])
 key=(rec['g'],beta)
 if key not in TRACE:TRACE[key]=(C.ceil(C.trace_bound(small,beta)[0],30),C.ceil(C.trace_bound(small,2*beta)[0],30))
 q1,q2=TRACE[key]
 L=C.exp_bounds(-2*beta*shift)[0];J=C.floor(L/q1**4);C0=C.floor(L/q2**2)
 a=C.floor(G(J));b=C.floor(G(C0*C0*a)) if a>0 else Q(-1)
 out=dict(beta=str(beta),time_steps=tsteps,canonical_steps=csteps,small_Q_beta_upper=str(q1),small_Q_2beta_upper=str(q2),Rayleigh_shift=str(shift),J_lower=str(J),C_lower=str(C0),initial_time_pair=list(map(str,[a,b])))
 if b<=0:return dict(**out,status='rejected_initial')
 n=8;be=2*beta;wins=[];states=[]
 for step in range(tsteps):
  P=a*a*b;S=C.floor(a*sqrt_lower(b));T=C.floor(P)
  try:wins.append(window(S,T,P,be,n))
  except AssertionError:return dict(**out,status='rejected_window')
  states.append(dict(order='time-space',cells=n,beta=str(be),pair=list(map(str,[a,b])),canonical_joint=str(P)))
  a=C.floor(G(P));b=C.floor(G(b*b*a)) if a>0 else Q(-1)
  if b<=0:return dict(**out,status='rejected_time_cycle')
  n*=2;be*=2
 P=a*a*b;S=C.floor(a*sqrt_lower(b));T=C.floor(P)
 conversion=dict(cells=n,beta=str(be),time_pair=list(map(str,[a,b])),S_lower=str(S),T_lower=str(T),joint_S2T_lower=str(P))
 for step in range(csteps):
  try:wins.append(window(S,T,P,be,n))
  except AssertionError:return dict(**out,status='rejected_window')
  states.append(dict(order='space-time',cells=n,beta=str(be),pair=list(map(str,[S,T])),joint_S2T_lower=str(P)))
  S=C.floor(G(P));T=C.floor(G(T*T*S)) if S>0 else Q(-1)
  if T<=0:return dict(**out,status='rejected_canonical_cycle')
  P=S*S*T;n*=2;be*=2
 u=max(1-S,1-T)
 if not 0<u<=Q(1,100):return dict(**out,status='rejected_terminal')
 gap=Q(math.floor(math.log(float(1/(5*u)))/float(be)*10**12)-1,10**12)
 assert gap>0 and C.exp_bounds(be*gap)[1]*5*u<1
 overall=min([gap]+[Q(w['gap_lower']) for w in wins])
 return dict(**out,status='exact_scalar_and_windows_candidate',conversion=conversion,states=states,windows=wins,final=dict(cells=n,beta=str(be),S_lower=str(S),T_lower=str(T),common_defect_upper=str(u),asymptotic_gap_lower=str(gap)),M_ge8_gap_lower=str(overall))

def affine(mat,g):
 return (Q(mat['K0'][0][0])+g*Q(int(mat['K1_scaled'][0][0]),mat['weak_denominator']))/Q(mat['G'][0][0])
def short_bridge(g):
 local=lb.optimize_bound(Q(1),g,'chain',7);C.local_psd(local['local_certificate']);a=Q(local['alpha']);b=Q(local['local_certificate']['b']);rows=[]
 for M in range(2,8):
  rho=-2*Q(M);src='singlet product'
  if M in [6,7]:
   path=HERE/f'M{M}_bridge_moments.json'
   if path.exists():mat=json.loads(path.read_text())
   else:
    tag='7d40_depth3' if M==6 else '129d800_depth2'
    mat=matrices([OLD/f'chain_s1_M{M}_g{tag}_trial.npz'],M);save(path.name,mat)
   er=affine(mat,g)
   if er<rho:rho=er;src=path.name
  cutoff=-2*M+a-M*b;gap=cutoff-rho
  rows.append(dict(M=M,full_dimension=9**M,cutoff_lower=str(cutoff),rayleigh_upper=str(rho),trial_source=src,gap_lower=str(gap)))
 assert all(Q(x['gap_lower'])>0 for x in rows)
 return dict(local=local,rows=rows,gap_lower=str(min(Q(x['gap_lower']) for x in rows)))

def main():
 t=time.monotonic();inputs=json.loads((HERE/'inputs.json').read_text());scans=json.loads((HERE/'float_orders.json').read_text());out=[]
 for rec,scan in zip(inputs,scans):
  assert rec['g']==scan['g']
  if scan['best'] is None:continue
  b=scan['best'];beta=Q(str(b['beta']));ts=b['time_steps'];cs=b['canonical_steps'];rows=[]
  # Refine the proposal locally, and test additional valid rounds rather than
  # stopping at first threshold acceptance.
  for j in [-1,0,1]:
   for count in range(max(0,cs-2),cs+3):rows.append(cycle(rec,beta+Q(j,20),ts,count))
  rows=[r for r in rows if r.get('M_ge8_gap_lower') and Q(r['M_ge8_gap_lower'])>0]
  bridge=short_bridge(Q(rec['g']))
  for row in rows:row['all_M_ge2_gap_lower']=str(min(Q(row['M_ge8_gap_lower']),Q(bridge['gap_lower'])))
  best=max(rows,key=lambda r:Q(r['all_M_ge2_gap_lower']));result=dict(g=rec['g'],status='CANDIDATE_REQUIRES_INDEPENDENT_REVIEW',input=rec,short_bridge=bridge,rows=rows,best=best)
  save('candidate_g'+rec['g'].replace('/','d')+'.json',result)
  out.append(dict(g=rec['g'],gap_lower=best['all_M_ge2_gap_lower'],gap_display=float(Q(best['all_M_ge2_gap_lower'])),beta=best['beta'],time_steps=best['time_steps'],canonical_steps=best['canonical_steps'],asymptotic_from=best['final']['cells'],short_gap_display=float(Q(bridge['gap_lower']))));print(out[-1],flush=True)
 save('summary.json',dict(status='CANDIDATES_PENDING_REVIEW',results=out,seconds=time.monotonic()-t,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,AS_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0],cpu_affinity=sorted(os.sched_getaffinity(0))))
if __name__=='__main__':main()
