"""Budgeted packed-state benchmark for a new numerator-only Hamiltonian image."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
import sys,time,resource,json,math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'chain_frontier_review'));import independent_core as C
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(590,600))
rec=json.loads((HERE.parent/'chain_frontier_rank195/expanded_inputs.json').read_text())[0];g=F(1,4);coeff=list(map(int,rec['large']['combination_integers']));paths=[HERE.parent/'chain_frontier'/f'chain_s1_M8_g{t}_depth4_trial.npz' for t in ['7d40','1d5']];zs=[np.load(p,allow_pickle=False) for p in paths];assert np.array_equal(zs[0]['basis'],zs[1]['basis']);basis=zs[0]['basis'];vectors=[z['vector'] for z in zs];keys=[sum(int(x)<<(4*i) for i,x in enumerate(s)) for s in basis];vec=[sum(c*int(v[j]) for c,v in zip(coeff,vectors)) for j in range(len(keys))]
den=math.lcm(*((g*c).denominator for r in C.K.values() for _,_,c in r));kernel={key:[(a,b,int(den*g*c)) for a,b,c in row] for key,row in C.K.items()};edges=[(4*((i-1)%8),4*i) for i in range(8)];mask=[~((15<<l)|(15<<r)) for l,r in edges]
def ex(key):return sum(C.EX[(key>>(4*i))&15] for i in range(8))
def weight(key):return math.prod(C.W[(key>>(4*i))&15] for i in range(8))
def full_action(keys,vec):
 out={};visits=0
 for key,x in zip(keys,vec):
  if not x:continue
  out[key]=out.get(key,0)+den*(-16+ex(key))*x
  for (l,r),msk in zip(edges,mask):
   for a,b,c in kernel[(key>>l)&15,(key>>r)&15]:
    target=(key&msk)|(a<<l)|(b<<r);out[target]=out.get(target,0)+c*x;visits+=1
 return {k:v for k,v in out.items() if v},visits
if __name__=='__main__':
 selected=np.random.default_rng(381).choice(len(keys),1000,replace=False);start=time.process_time();out,visits=full_action([keys[i] for i in selected],[vec[i] for i in selected]);elapsed=time.process_time()-start
 norm=sum(weight(k)*v*v for k,v in zip(keys,vec));matrix=json.loads((HERE.parent/'chain_filter_extension/M8_two_trial_moments.json').read_text());expected=sum(coeff[i]*F(matrix['G'][i][j])*coeff[j] for i in range(2) for j in range(2));assert norm==expected
 report=dict(status='COST_PROBE_ONLY',input_support=len(keys),benchmark_columns=1000,benchmark_weak_transitions=visits,benchmark_unique_outputs=len(out),benchmark_cpu_seconds=elapsed,estimated_full_first_action_cpu_seconds=elapsed*len(keys)/1000,known_same_graph_union_upper=245870,conservative_next_contraction_transition_estimate=visits*245870/1000,estimated_next_contraction_cpu_seconds=elapsed*245870/1000*4,packed_state_bits=32,integer_coefficient_max_bits=max(abs(x).bit_length() for x in vec),H_integer_denominator=den,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,AS_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0],cpu_affinity=sorted(os.sched_getaffinity(0)),next_design='Compute full phi=den*H*psi on packed states; contract <phi,H phi> only within phi support, without materializing H^2 psi or a new residual; exact Gram and first moments certify a 2D Rayleigh-only span.')
 (HERE/'probe.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
