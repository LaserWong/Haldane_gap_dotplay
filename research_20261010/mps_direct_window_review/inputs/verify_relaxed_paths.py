#!/usr/bin/env python3
"""Exact relaxed-path exclusion; every finite window is granted for free."""
from pathlib import Path
from fractions import Fraction as F
import json,time,resource,hashlib
P=Path(__file__).resolve().parent;B=P.parent;BASE=B/'mps_excited_seed_witnesses'
source=(BASE/'verify_scalar.py').read_text().split('rows=[]\nfor r in')[0];ns={'__file__':str(BASE/'verify_scalar.py')};exec(source,ns)
G,up,sqrt_up,canonical=[ns[x] for x in ['G','up','sqrt_up','canonical']];resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));t0=time.process_time()
files=['mps_excited_seed_witnesses/verify_scalar.py','mps_excited_seed_witnesses/scalar_results.json','mps_seed_even_completion/results.json','mps_commutator_assessment/fused_current/pi_scalar_results.json','uniform_seed_size_diagnostics/uniform_seed_size_diagnostics.json']
inputs={f:hashlib.sha256((B/f).read_bytes()).hexdigest() for f in files}
def state_paths(a,b,n):
 history=[]
 for delay in range(32):
  assert 0<a<=1 and 0<b<=1
  joint=up(a*a*b);direct_sq=up(a**4*(2*b-1)) if b>F(1,2) else F(0)
  row={'extra_time_cycles':delay,'physical_length':2**(delay+1)*n,'physical_beta_multiplier':2**(delay+1),'a_upper':str(a),'b_upper':str(b),'joint_P_upper':str(joint),'direct_window_purity_square_upper':str(direct_sq),'direct_window_can_be_positive':direct_sq>F(1,4),'prior_windows':'all granted for this necessary relaxed screen'}
  history.append(row)
  # 1-P is the common defect because 0<P<=1 => sqrt(P)>=P.
  if joint>=F(99,100):
   return {'outcome':'inconclusive','reason':'optimistic direct small-defect closure survives','history':history}
  row['canonical_continuation']=canonical(a,b)
  if row['canonical_continuation']['outcome']!='excluded':
   return {'outcome':'inconclusive','reason':'optimistic canonical path survives','history':history}
  arg=a*a*b;a=up(G(arg))
  if a<=0:return {'outcome':'excluded','failure':'continued time-first thermal G','argument_upper':str(arg),'output_upper':str(a),'history':history}
  arg=b*b*a;b=up(G(arg))
  if b<=0:return {'outcome':'excluded','failure':'continued time-first spatial G','argument_upper':str(arg),'output_upper':str(b),'history':history}
 return {'outcome':'inconclusive','reason':'finite32-cycle cap','history':history}
def replay(j,c,n):
 a=up(G(j))
 if a<=0:return {'outcome':'excluded','failure':'initial thermal G','output_upper':str(a)}
 b=up(G(c*c*a))
 if b<=0:return {'outcome':'excluded','failure':'initial spatial G','output_upper':str(b)}
 return state_paths(a,b,n)
def hot_cold(r):
 for name in ['hot_J_upper','cold_J_upper']:assert F(r[name])<F(2,5) and G(F(2,5))<0
 return {k:r[k] for k in ['hot_closed_interval','hot_J_upper','cold_closed_interval','cold_J_upper']}
rows=[]
# Existing exact closed boxes are upper envelopes over their entire interval.
regular=[]
for r in json.loads((B/files[1]).read_text())['rows']:
 if r['n']!=24:regular.append((r['n'],3,r,files[1]))
for r in json.loads((B/files[2]).read_text())['rows']:
 if r['retained_denominator_states']==3:regular.append((r['n'],3,r,files[2]))
for r in json.loads((B/files[3]).read_text())['cases']:regular.append((24,r['retained_denominator_states'],r,files[3]))
for n,count,r,origin in sorted(regular,key=lambda x:(x[0],x[1])):
 tails=hot_cold(r);boxes=[]
 for b in r['warm_boxes']:
  lo,hi=F(b['beta_lower']),F(b['beta_upper']);j,c=F(b['J_upper']),F(b['C_upper']);result=replay(j,c,n)
  boxes.append({'initial_beta_lower':str(lo),'initial_beta_upper':str(hi),'J_upper':str(j),'C_upper':str(c),'replay':result})
 assert F(boxes[0]['initial_beta_lower'])==F(tails['hot_closed_interval'][1])
 assert F(boxes[-1]['initial_beta_upper'])==F(tails['cold_closed_interval'][0])
 assert all(boxes[i]['initial_beta_upper']==boxes[i+1]['initial_beta_lower'] for i in range(len(boxes)-1))
 unresolved=[{'initial_beta_lower':b['initial_beta_lower'],'initial_beta_upper':b['initial_beta_upper']} for b in boxes if b['replay']['outcome']!='excluded']
 row={'n':n,'denominator_trial_count':count,'origin':origin,'status':'PASS all-beta relaxed-path exclusion' if not unresolved else 'BOUNDED screen only','tails':tails,'unresolved_boxes':unresolved,'boxes':boxes};rows.append(row);print(n,count,row['status'],len(unresolved),flush=True)
small=json.loads((B/files[4]).read_text())['rows']
for r in small:
 n=r['n']
 if n in [6,8]:
  assert F(r['early_J_upper'])<F(2,5)
  j=F(r['J_global_cap']);c=F(r['late_C_cap']);result=replay(j,c,n)
  row={'n':n,'denominator_trial_count':r['denominator_orthogonal_trials'],'origin':files[4],'status':'PASS all-beta relaxed-path exclusion' if result['outcome']=='excluded' else 'BOUNDED screen only','early_closed_interval':['0',r['early_beta_end']],'early_J_upper':r['early_J_upper'],'late_closed_interval':[r['early_beta_end'],'infinity'],'late_J_upper':str(j),'late_C_upper':str(c),'replay':result}
 else:
  cap=F(r['J_global_cap']);assert G(cap)<0
  row={'n':n,'denominator_trial_count':r['denominator_orthogonal_trials'],'origin':files[4],'status':'PASS all-beta relaxed-path exclusion','global_J_upper':str(cap),'first_G_upper':str(G(cap))}
 rows.append(row);print(n,row['status'],flush=True)
rows.sort(key=lambda x:(x['n'],x['denominator_trial_count']))
out={'status':'Producer exact relaxed-path screens; independent review pending','input_sha256':inputs,'scope':'Fixed archived D26 single-Rayleigh numerator at2n, existing G time-first startup, any fixed number of whole time-first cycles, then direct same-base small-defect closure or accepted joint-aware canonical continuation. All short/intermediate finite windows are optimistically granted. No inference about physical gaps, true purities, universal seed sizes, arbitrary adaptive switching, or stronger recursion/closure formulas.','physical_indexing':'At initial beta beta0, startup gives (2n,2beta0); afterk extra full time-first cycles gives (2^(k+1)n,2^(k+1)beta0).','rows':rows,'cpu_seconds':time.process_time()-t0,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};(P/'exact_results.json').write_text(json.dumps(out,indent=2)+'\n');print('CPU',out['cpu_seconds'],'peakKiB',out['peak_KiB'])
