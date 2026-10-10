"""Exact producer replay, with separately implemented sealed review scalar arithmetic."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
import sys,json,math,resource,time,importlib.util,hashlib
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict,Counter
import numpy as np
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,str(HERE.parent/'chain_frontier_review'));import independent_core as C
sys.path.insert(0,str(ROOT/'original/Haldane_extensions/code'));from inertia_trace import inertia
A=load('review_scalar',HERE.parent/'chain_low_band_review/audit_certificate.py')
def trace_upper(ss,beta):
 s=json.loads(ss);info=s['expanded_band'];rho=F(s['exact_rayleigh']);lo=F(s['ground_lower']);alpha=F(info['alpha']);B=F(info['B'])
 terms=[A.expbox(beta*(rho-lo))[1]]
 terms += [m['multiplicity']*A.expbox(-beta*(-8+F(m['lower'])-rho))[1] for m in info['comparison_endpoints'][1:]]
 terms += [mult*A.expbox(-beta*(-8+alpha*e-B-rho))[1] for e,mult in info['complete_reference_bins'] if e>=3]
 return sum(terms)
A.trace_upper=trace_upper

def main():
 start=time.monotonic();mom=json.loads((HERE/'expanded_moments.json').read_text());states=list(map(tuple,mom['basis']));assert len(states)==len(set(states))==67
 assert all(sum(C.EX[x] for x in s)<3 for s in states)
 weights=[math.prod(C.W[x] for x in s) for s in states];assert list(map(str,weights))==mom['Gram_diagonal']
 acts=[]
 for s in states:
  out=defaultdict(F)
  for right in range(4):
   left=(right-1)%4
   for x,y,c in C.K[s[left],s[right]]:
    ss=list(s);ss[left]=x;ss[right]=y;out[tuple(ss)]+=c
  acts.append({ss:c for ss,c in out.items() if c})
 K=[[weights[i]*acts[j].get(states[i],F(0)) for j in range(67)] for i in range(67)]
 J=[[sum((math.prod(C.W[x] for x in s)*c*acts[j].get(s,0) for s,c in acts[i].items()),F(0)) for j in range(67)] for i in range(67)]
 R=[[J[i][j]-sum((K[i][k]*K[k][j]/weights[k] for k in range(67)),F(0)) for j in range(67)] for i in range(67)]
 for name,mat in [('unit_K',K),('unit_J',J),('unit_residual_Gram',R)]:assert [[str(x) for x in row] for row in mat]==mom[name]
 mags=[sum(C.MAG[x] for x in s) for s in states];blocks=[[i for i,m in enumerate(mags) if m==z] for z in sorted(set(mags))]
 assert all(K[i][j]==R[i][j]==0 for i in range(67) for j in range(67) if mags[i]!=mags[j])
 bins=Counter({0:1})
 for _ in range(4):
  new=Counter()
  for e,c in bins.items():
   for f,m in [(0,1),(1,3),(3,5)]:new[e+f]+=c*m
  bins=new
 assert sum(bins.values())==6561 and sum(c for e,c in bins.items() if e>=3)==6494
 matrix=json.loads((HERE.parent/'chain_filter_extension/M8_two_trial_moments.json').read_text());checks=[]
 for path in sorted(HERE.glob('candidate_g*.json')):
  rec=json.loads(path.read_text());small=rec['input']['small'];info=small['expanded_band'];g=F(rec['g']);C.DATA=HERE;ground=C.check_ground(small)
  assert sorted(bins.items())==[tuple(z) for z in info['complete_reference_bins']]
  lc=info['local_comparison'];C.local_psd(lc);alpha=1-2*F(lc['a']);B=4*F(lc['b']);cut=3*alpha-B
  assert [alpha,B,cut]==list(map(F,[info['alpha'],info['B'],info['omitted_cutoff']])) and alpha>0
  endpoints=info['comparison_endpoints'];count=0;inertias=[]
  for row in endpoints:
   t=F(row['lower']);assert t<cut;neg=zero=0
   for ids in blocks:
    mat=[[(cut-t)*((F(sum(C.EX[x] for x in states[i]))-t)*weights[i]*(i==j)+g*K[i][j])-g*g*R[i][j] for j in ids] for i in ids]
    den=math.lcm(*(x.denominator for rr in mat for x in rr));nn,zz=inertia(np.array([[int(x*den) for x in rr] for rr in mat],dtype=object));neg+=nn;zero+=zz
   assert neg==count==row['negative_inertia'] and zero==row['zero_inertia']==0
   inertias.append([str(t),neg,zero]);count+=row['multiplicity']
  assert count==67 and endpoints[0]['multiplicity']==1 and all(F(x['lower'])<F(y['lower']) for x,y in zip(endpoints,endpoints[1:]))
  assert F(endpoints[0]['lower'])<F(small['ground_lower'])+8<F(endpoints[1]['lower'])
  large=rec['input']['large'];assert A.expectation(matrix,list(map(int,large['combination_integers'])),g)==F(large['exact_rayleigh'])
  paths=[]
  for row in rec['rows']:
   report=A.scalar(rec,row);bb=row['all_size_bridge'];j=F(row['J_lower']);initial=A.window(bb['initial_M4_M8_window'],A.floor(A.root(j)),j,j,4,F(row['beta']))
   local=bb['local_comparison'];C.local_psd(local)
   short=[]
   for sr in bb['M2_M3']:
    n=sr['M'];assert n in [2,3];gap=1-2*F(local['a'])-n*F(local['b']);assert F(sr['gap_lower'])==gap>0 and F(sr['second_eigenvalue_lower'])==-2*n+gap;short.append(gap)
   assert sorted(sr['M'] for sr in bb['M2_M3'])==[2,3]
   target=min(F(report['M_ge8_gap_lower']),F(initial['gap_lower']),*short);assert target==F(row['all_M_ge2_gap_lower'])==F(bb['all_M_ge2_gap_lower'])
   paths.append(dict(scalar=report,initial_window=initial,gap=str(target)))
  assert rec['best'] in rec['rows'] and F(rec['best']['all_M_ge2_gap_lower'])==max(F(r['all_M_ge2_gap_lower']) for r in rec['rows'])
  checks.append(dict(g=str(g),gap=rec['best']['all_M_ge2_gap_lower'],ground_replay=ground,exact_inertias=inertias,paths=paths));print('REPLAY PASS',g,checks[-1]['gap'],flush=True)
 report=dict(status='PRODUCER_REPLAY_PASS_PENDING_EXTERNAL_REVIEW',checks=checks,reference_dimension=67,full_dimension=6561,omitted_count=6494,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (HERE/'verification.json').write_text(json.dumps(report,indent=2))
if __name__=='__main__':main()
