#!/usr/bin/env python3
"""Independent rational audit of all four second-moment bootstrap certificates."""
import copy,ctypes,hashlib,json,math,os,resource,signal,time
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
assert resource.getrlimit(resource.RLIMIT_CPU)==(8,8) and resource.getrlimit(resource.RLIMIT_AS)==(256*1024**2,)*2
assert os.sched_getaffinity(0)=={5} and signal.getsignal(signal.SIGXCPU)==signal.SIG_DFL and signal.SIGXCPU not in signal.pthread_sigmask(signal.SIG_BLOCK,set())
death=ctypes.c_int();assert ctypes.CDLL(None).prctl(2,ctypes.byref(death),0,0,0)==0 and death.value==signal.SIGKILL
START=time.process_time();P=Path(__file__).resolve().parent;R=P.parents[1];prod=R/'research_20261010/uniform_alternating_variance_refined_robustness';pins={};GRID=1<<1600;DEC=10**400
def read(p,wanted=None):
 raw=p.read_bytes();h=hashlib.sha256(raw).hexdigest()
 if wanted is not None:assert h==wanted,str(p)
 pins[str(p.relative_to(R))]=h
 return json.loads(raw)
manifest=read(prod/'MANIFEST_SHA256.json','3c6bfbaedd753160c7b22bf3fd0839ce64330735e1c4ec8437d5e37ae0129d56')
for name,h in manifest.items():
 raw=(prod/name).read_bytes();assert hashlib.sha256(raw).hexdigest()==h;pins[str((prod/name).relative_to(R))]=h
for name,h in read(prod/'INPUT_SHA256.json').items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==h;pins[name]=h
observable=R/'research_20261010/uniform_alternating_h2_review';m=read(observable/'MANIFEST_SHA256.json','cca4335ac42dd34b2e75528a89a2834998d9126c5abcb73df965a344da669f60')
for name,h in m.items():assert hashlib.sha256((observable/name).read_bytes()).hexdigest()==h
new_effects={x['physical_length']:x for x in read(observable/'scalar_results.json')['rows']}
for L,k in [(32,F(969,10000)),(64,F(119,1000))]:assert F(new_effects[L]['Gibbs_kappa_upper'])<k
cert=read(prod/'certificate.json');seed=next(x for x in read(R/'research_20261010/uniform_smaller_second_initialization/certificate.json')['rows'] if x['n']==32)
accepted=next(x for x in read(R/'research_20261010/uniform_smaller_second_initialization_review/scalar_results.json')['rows'] if x['n']==32)
assert F(seed['S'])==F(accepted['S_seed']) and F(seed['T'])==F(accepted['T_2n_seed'])
assert F(seed['shifted_Rayleigh'])==F(accepted['anchor_shifted_total_Rayleigh'])<0 and seed['anchor_length']==64
bridge=read(R/'research_20261010/uniform_gap_0248_all_sizes_review/results.json');assert F(bridge['gap'])==F(31,1250) and bridge['all_integer_L_at_least']==2 and bridge['unique_ground_state']
def down(x):return F(x.numerator*GRID//x.denominator,GRID)
def up(x):return -down(-x)
def decdown(x):return F(x.numerator*DEC//x.denominator,DEC)
@lru_cache(None)
def exponential(x):
 if x<0:
  a,b=exponential(-x);return down(1/b),up(1/a)
 halves=0
 while x>F(1,4):x/=2;halves+=1
 term=s=F(1)
 for k in range(1,251):term=term*x/k;s+=term
 lo=down(s);hi=up(s+(term*x/251)/(1-x/252))
 for _ in range(halves):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi
def sqrt_lower(x):
 assert x>=0;k=math.isqrt(x.numerator*GRID*GRID//x.denominator);z=F(k,GRID);assert z*z<=x<=(z+F(1,GRID))**2;return z
def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)
SPECS=[(F(751,5000000),F(1,50)),(F(2089,10000000),F(3,200)),(F(99,400000),F(1,100)),(F(109,400000),F(1,200))]
required=list(range(4,32,2));purities={x['L']:F(x['purity_lower']) for x in bridge['cached_prefix_4_to25']+bridge['new_direct26_to33']}
assert [x['physical_length'] for x in cert['uniform_finite_gap_bounds']]==required
finite_bounds={}
for entry in cert['uniform_finite_gap_bounds']:
 L=entry['physical_length'];C=purities[L];assert F(entry['purity_lower'])==C and F(1,2)<C<1 and F(entry['beta'])==F(49,4) and entry['cell_length']==L//2
 w=F(entry['ground_weight_lower']);assert F(1,2)<w<=(1+sqrt_lower(2*C-1))/2<1
 delta=F(entry['uniform_finite_gap_lower']);assert delta>0
 margin=w-exponential(F(49,4)*delta)[1]*(1-w);assert 0<F(entry['finite_gap_margin'])<=margin
 if L==24:assert entry['provenance']=='physical24 parity certificate with MPS48'
 finite_bounds[L]=(w,delta)
def verify(row,r,gap):
 assert F(row['eta_radius'])==r and F(row['physical_gap_target'])==gap
 assert F(row['g_lower'])==(1-r)/(1+r) and F(row['g_upper'])==(1+r)/(1-r)
 assert (row['initial_cell_base'],row['initial_physical_base'],row['anchor_physical_length'])==(16,32,64)
 assert F(row['initial_normalized_beta'])==F(49,4) and row['shift_per_physical_site']=='c * 700741/500000'
 assert F(row['uniform_S_lower'])==F(seed['S']) and F(row['uniform_T_lower'])==F(seed['T']) and F(row['shifted_anchor_Rayleigh'])==F(seed['shifted_Rayleigh'])
 factor={}
 for L,kappa in [(32,F(969,10000)),(64,F(119,1000))]:
  assert F(row['gibbs_kappa_upper'][str(L)])==kappa
  x=F(49,4)*r*F(3*L,2);ch=(exponential(x)[1]+exponential(-x)[1])/2
  factor[L]=F(row['trace_factors_upper'][str(L)]);assert factor[L]>=1+kappa*(ch-1)
 s0,t0=F(row['S_lower']),F(row['T_lower']);assert 0<s0<=F(seed['S'])/factor[32]**2 and 0<t0<=F(seed['T'])/factor[64]**2
 prior=None;out=[]
 for j,st in enumerate(row['states']):
  n=16*2**j;beta=F(49,4)*2**j;tau=beta*(1+r)
  assert (st['round'],st['cell_base'],st['physical_base'])==(j,n,2*n)
  assert F(st['normalized_beta'])==beta and F(st['physical_beta_upper'])==tau
  s,t=F(st['S_lower']),F(st['T_lower']);assert 0<s<=1 and 0<t<=1 and s==decdown(s) and t==decdown(t)
  if prior is None:assert (s,t)==(s0,t0)
  else:
   assert s==decdown(G(prior[2]))
   assert t==decdown(G(decdown(prior[1]**2*s)))
  K=F(st['K_lower']);assert K==decdown(s*s*t) and 0<K<=1
  C=F(st['window_purity_lower']);assert F(1,2)<C<=min(s*sqrt_lower(t),t) and C==decdown(C)
  assert (st['window_cell_from'],st['window_cell_to'])==(n,2*n)
  margin=C-exponential(tau*gap)[1]*(1-C);assert 0<F(st['window_margin'])<=margin
  out.append({'cells':[n,2*n],'physical_even_lengths':[2*n,4*n],'margin':str(margin)});prior=s,t,K
 assert out
 u=max(1-s,1-t);term=row['terminal'];assert term['cell_from']==n and term['physical_from']==2*n and F(term['defect'])==u<=F(1,100)
 margin=1-5*u*exponential(tau*gap)[1];assert 0<F(term['margin'])<=margin
 fb=row['finite_bridge'];assert (fb['cell_min'],fb['cell_max'],fb['physical_min'],fb['physical_max'])==(2,15,4,30)
 assert [x['physical_length'] for x in fb['rows']]==required
 bridge_checks=[]
 for item in fb['rows']:
  L=item['physical_length'];w,delta=finite_bounds[L];assert item['cell_length']==L//2 and F(item['uniform_finite_gap_lower'])==delta
  low=(delta-3*L*r)/(1+r);needed=(1+r)*gap+3*L*r
  direct=w-exponential(F(49,4)*needed)[1]*(1-w)
  assert F(item['perturbed_gap_lower'])==low>=gap and F(item['margin'])==low-gap>=0
  assert F(item['required_normalized_gap'])==needed and 0<F(item['direct_purity_weight_margin'])<=direct and item['passed']
  bridge_checks.append({'physical_length':L,'cell_length':L//2,'gap_lower':str(low),'direct_margin':str(direct)})
 low=min(F(x['gap_lower']) for x in bridge_checks);bottleneck=min(bridge_checks,key=lambda x:F(x['gap_lower']))['physical_length']
 assert F(fb['worst_gap_lower'])==low and fb['bottleneck_physical_length']==bottleneck
 assert row['all_integer_cells_at_least']==2 and row['unique_ground_state']
 return {'status':'ACCEPTED','eta_radius':str(r),'g_closed_interval':[row['g_lower'],row['g_upper']],'gap':str(gap),'cells_from':2,'unique_ground_state':True,'windows':out,'terminal_cells_from':n,'terminal_margin':str(margin),'finite_bridge_gap_lower':str(low),'finite_bridge_rows':bridge_checks,'bottleneck_physical_length':bottleneck}
assert len(cert['rows'])==4 and cert['all_previous_intervals_and_seals_preserved']  and cert['linear_trial_dimension']==1 and cert['MPS_bond_dimension']==26
result=[verify(row,*spec) for row,spec in zip(cert['rows'],SPECS)]
u=F(1,100);assert F(9,2)/(1-3*u)**2<5 and 2*u+5*u*u<=3*u and (F(3,2)*u)/(1-F(3,2)*u)<=2*u
mutations=[]
def reject(label,change):
 row=copy.deepcopy(cert['rows'][0]);change(row)
 try:verify(row,*SPECS[0])
 except (AssertionError,KeyError,IndexError):mutations.append(label);return
 raise AssertionError('mutation not detected: '+label)
reject('omit32 trace loss',lambda r:r['trace_factors_upper'].__setitem__('32','1'))
reject('omit64 trace loss',lambda r:r['trace_factors_upper'].__setitem__('64','1'))
reject('swap Gibbs bound length',lambda r:r['gibbs_kappa_upper'].__setitem__('32','119/1000'))
reject('wrong endpoint',lambda r:r.__setitem__('g_upper','1'))
reject('physical-cell confusion',lambda r:r.__setitem__('initial_cell_base',32))
reject('forgot temperature rescaling',lambda r:r['states'][0].__setitem__('physical_beta_upper','49/4'))
reject('missing interior window',lambda r:r['states'].pop(1))
reject('inflated spatial update',lambda r:r['states'][1].__setitem__('S_lower','1'))
reject('inflated thermal update',lambda r:r['states'][1].__setitem__('T_lower','1'))
reject('terminal scale error',lambda r:r['terminal'].__setitem__('physical_from',r['terminal']['cell_from']))
reject('missing finite cell15',lambda r:r['finite_bridge'].__setitem__('cell_max',14))
reject('strictly overclaimed bridge',lambda r:r['finite_bridge'].__setitem__('worst_gap_lower','1/40'))
reject('missing physical24 bridge',lambda r:r['finite_bridge']['rows'].pop(10))
reject('missing Weyl loss',lambda r:r['finite_bridge']['rows'][-1].__setitem__('perturbed_gap_lower',r['finite_bridge']['rows'][-1]['uniform_finite_gap_lower']))
reject('missing finite physical c rescaling',lambda r:r['finite_bridge']['rows'][-1].__setitem__('required_normalized_gap',str(SPECS[0][1]+90*SPECS[0][0])))
reject('400-digit late endpoint inflated',lambda r:r['states'][-1].__setitem__('window_purity_lower','1'))
output={'status':'ACCEPTED_ALL_FOUR_VARIANCE_REFINED_CLOSED_INTERVALS','rows':result,'adversarial_rejections':mutations,'producer_manifest':'3c6bfbaedd753160c7b22bf3fd0839ce64330735e1c4ec8437d5e37ae0129d56','observable_review_manifest':'cca4335ac42dd34b2e75528a89a2834998d9126c5abcb73df965a344da669f60','physical_work':False,'search_candidates_not_replayed':True,'CPU_seconds':time.process_time()-START,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'results.json').write_text(json.dumps(output,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(pins,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':output['status'],'rows':[{k:v for k,v in row.items() if k not in ('windows','terminal_margin')} for row in result],'mutation_count':len(mutations),'CPU_seconds':output['CPU_seconds']},indent=2))
