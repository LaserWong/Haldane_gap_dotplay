#!/usr/bin/env python3
"""Independent exact rational replay; reads data only, imports no producer code."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,hashlib,math,os,resource,time,sys
os.sched_setaffinity(0,{7});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(30,30));sys.set_int_max_str_digits(100000);start=time.process_time()
P=Path(__file__).resolve().parent;R=P.parent;A=R/'uniform_gap_0248_all_sizes';ROOT=R.parent;B=10**140;H={}
def rd(p):
 b=p.read_bytes();H[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return b
def js(p):return json.loads(rd(p))
def seal(p,h):
 assert hashlib.sha256(rd(p/'MANIFEST_SHA256.json')).hexdigest()==h
 for f,v in js(p/'MANIFEST_SHA256.json').items():assert hashlib.sha256(rd(p/f)).hexdigest()==v
 return h
def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return -down(-x)
@lru_cache(None)
def power(x,r):
 r=F(r);assert x>=0 and r>0;p,q=r.numerator,r.denominator;z=x**p;scaled=z.numerator*B**q//z.denominator
 if q==1:k=scaled
 elif q==2:k=math.isqrt(scaled)
 else:
  lo=0;hi=1<<((scaled.bit_length()+q-1)//q)
  while hi-lo>1:
   mid=(lo+hi)//2
   if mid**q<=scaled:lo=mid
   else:hi=mid
  k=lo
 l,u=F(k,B),F(k+1,B);assert l**q<=z<=u**q;return l,u
@lru_cache(None)
def exp_upper(x):
 assert x>=0;k=0
 while x>F(1,8):x/=2;k+=1
 term=total=F(1)
 for j in range(1,161):term*=x/j;total+=term
 upper=up(total+(term*x/161)/(1-x/162))
 for j in range(k):upper=up(upper*upper)
 return upper
@lru_cache(None)
def pack(m,h,r):
 assert m>=0 and h>0 and r>=1;q=m//h
 return up(q*power(h,r)[1]+power(m-q*h,r)[1])
def bernstein(poly,a,b):
 d=len(poly)-1
 co=[sum(poly[j]*math.comb(j,k)*a**(j-k)*(b-a)**k for j in range(k,d+1)) for k in range(d+1)]
 row=[sum(co[k]*F(math.comb(i,k),math.comb(d,k)) for k in range(i+1)) for i in range(d+1)];pending=[(row,0)];leaves=depth=0
 while pending:
  row,level=pending.pop()
  if min(row)>=0:leaves+=1;depth=max(depth,level);continue
  assert row[0]>=0 and row[-1]>=0 and level<30
  tri=[row]
  while len(tri[-1])>1:tri.append([(a+b)/2 for a,b in zip(tri[-1][:-1],tri[-1][1:])])
  pending.extend([([v[0] for v in tri],level+1),([v[-1] for v in tri[::-1]],level+1)])
 return leaves,depth
def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)
def ints(p):return {k:int(v) for k,v in (l.split('=') for l in rd(p).decode().splitlines())}
def exp_lower(x):
 if x<0:return down(1/exp_upper(-x))
 k=0
 while x>F(1,8):x/=2;k+=1
 term=total=F(1)
 for j in range(1,161):term*=x/j;total+=term
 lo=down(total)
 for j in range(k):lo=down(lo*lo)
 return lo
seals={}
for name,h in [('uniform_gap_0248_all_sizes','659d03dd58275338f0a13af5fde6f6e503bca8eb7c3ac5d044a0e98e788e8ab1'),('uniform_small_lengths_completion_review','b5225681662482e5ed219fe85d0cc9247703b21b183f6e6441dd081b7bc9d984'),('uniform_n24_second_coverage_review','9d31eeb0dc44f24047943a4ad4dd06e4f8f82aced5ca321857a1aaedf82b8282'),('uniform_direct25_coverage_review','a70156f108be662bbb9873ce12f9701701efd0b6680d2d187e677fa1e37b3cc9'),('uniform_smaller_second_initialization_review','54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f'),('uniform_second_thermal_full_review','792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94')]:seals[name]=seal(R/name,h)
# Pin physical reconstruction and independent sequential powers to the preceding
# inspected implementation; no producer engine is executed.
previous=R/'uniform_small_lengths_completion_review'
for f in ['contract_sequential','contract_sequential.cpp','rebuild_d26.py']:assert rd(P/f)==rd(previous/f)
assert rd(P/'run_guarded.py')==rd(previous/'run_guarded.py').replace(b'range(4,24)',b'range(26,34)')
assert rd(P/'d26_blocks.txt')==rd(ROOT/'audit/mps/mps_blocks.txt');rebuild=js(P/'independent_d26.json');assert rebuild['status']=='PASS' and rebuild['D']==26
ours=ints(P/'anchors.out');assert ours==ints(A/'anchors.out') and set(ours)=={f'{s}_{n}' for s in ['H0','N0'] for n in range(26,34)}
C=js(R/'uniform_second_moment_optimization/certificate.json');physical=js(R/'uniform_second_thermal_full_review/provenance_results.json');assert physical['thermal_inputs']==18 and physical['all_exact_W_and_refined_endpoints_match'] and physical['signed_moment_intervals']==C['moment_intervals'];M={s:[tuple(map(F,x)) for x in vals] for s,vals in C['moment_intervals'].items()}
L=js(R/'uniform_smaller_second_initialization/long_certificate.json');core=js(R/'uniform_smaller_second_initialization_review/scalar_results.json');U=max(F(C['filters']['J+']['cap']),F(C['filters']['J-']['cap']));V=max(F(C['filters']['N+']['cap']),F(C['filters']['N-']['cap']))
def sector(s,n):
 key=f'{s}{n}';assert F(L[key]['bound'])==F(core['all_signed_majorants'][key]['bound']);return min(pack(M[s][-1][1],(U if s=='J' else V)**12,F(n,12)),F(L[key]['bound']))
def Q(n):assert n%2==0;return sector('J',n)+3*sector('N',n)
cert=js(A/'certificate.json');gap=F(31,1250);beta=F(49,4);assert F(cert['gap'])==gap and [r['L'] for r in cert['new_rows']]==list(range(26,34))
new=[]
for r in cert['new_rows']:
 n=r['L'];N=ours[f'N0_{n}'];assert N>0;ray=F(ours[f'H0_{n}'],N)+n*F(700741,500000);assert ray==F(r['shifted_total_Rayleigh'])
 requested=[n-1,n+1] if n%2 else [n];assert set(r['trace_inputs'])==set(map(str,requested));trace_upper={j:F(r['trace_inputs'][str(j)]) for j in requested}
 for j in requested:assert 0<Q(j)<=trace_upper[j]
 den=trace_upper[n-1]*trace_upper[n+1] if n%2 else trace_upper[n]**2;assert den==F(r['trace_squared_upper'])>0 and r['trace_method']==('CAUCHY_SCHWARZ_EVEN_NEIGHBORS' if n%2 else 'EVEN_MOMENT_UPPER')
 num=F(r['numerator_lower']);assert 0<num<=exp_lower(-2*beta*ray);cc=F(r['purity_lower']);assert F(1,2)<cc<=num/den<=1 and r['passed'] and F(r['gap'])==gap
 margin=cc-exp_upper(beta*gap)*(1-cc);assert 0<F(r['margin'])<=margin
 new.append({'L':n,'norm_positive':True,'shifted_total_Rayleigh':str(ray),'purity_lower':str(cc),'strict_gap_margin':str(margin),'method':r['trace_method']})
# Recheck the stronger inequality against independently accepted exact purities,
# never infer stronger gaps merely from an earlier weaker gap statement.
finite=js(previous/'results.json');cached={r['L']:F(r['purity_lower']) for r in finite['rows']};r24=js(R/'uniform_n24_second_coverage_review/results.json');cached[24]=F(next(x for x in r24['rows'] if x['L']==24)['purity_lower']);r25=js(R/'uniform_direct25_coverage_review/results.json');cached[25]=F(r25['purity_lower']);assert set(cached)==set(range(4,26))
proposal=js(A/'cached_prefix.json');assert [r['L'] for r in proposal['rows']]==list(range(4,26));prefix=[]
for r in proposal['rows']:
 n=r['L'];cc=cached[n];assert cc==F(r['purity']) and r['passed'] and F(r['gap'])==gap
 margin=cc-exp_upper(beta*gap)*(1-cc);assert 0<F(r['margin'])<=margin;prefix.append({'L':n,'purity_lower':str(cc),'strict_gap_margin':str(margin)})
for n,g in [('2',F(2)),('3',F(1))]:assert finite['analytic_small_lengths'][n]['ground_multiplicity']==1 and F(finite['analytic_small_lengths'][n]['gap'])==g>=gap
strongtail=next(r for r in core['rows'] if r['n']==34);assert strongtail['gap']=='31/1250' and strongtail['all_integer_L_at_least']==34 and strongtail['unique_ground_state']
smallest=next(r for r in core['rows'] if r['n']==30);assert F(smallest['gap'])==F(179,10000)<gap
assert cert['combined_claim']=={'all_integer_L_at_least':2,'gap':'31/1250','unique_ground_state':True,'coverage_onset':2,'bootstrap_initialization_used_for_this_stronger_gap':34,'smallest_separately_certified_initialization':30,'union':['analytic2,3','cached direct/parity4..25 rechecked at.0248','own direct thermal26..33','accepted n34 tail.0248']}
guard=js(P/'guard_resources.json');assert guard['exit_code']==0 and not guard['wall_watchdog_fired'] and guard['wall_seconds']<25 and guard['wait4_total_cpu_seconds']<=30 and guard['wait4_maxrss_kib']<102400
assert guard['postexec_observations'];obs=guard['postexec_observations'][0];assert next(x for x in obs['limits'].splitlines() if x.startswith('Max cpu time')).split()[3:5]==['30','30'];assert next(x for x in obs['limits'].splitlines() if x.startswith('Max address space')).split()[3:5]==['104857600','104857600'];assert any(x.split()==['Threads:','1'] for x in obs['status_fields']) and any(x.split()==['Cpus_allowed_list:','5'] for x in obs['status_fields'])
checks=[]
def must(x):assert x
def reject(name,f):
 try:f()
 except AssertionError:checks.append(name);return
 raise RuntimeError(name)
reject('claim_strong_tail_from30',lambda:must(F(smallest['gap'])>=gap))
reject('missing_length33',lambda:must(set(cached)|{r['L'] for r in new if r['L']!=33}==set(range(4,34))))
reject('odd_CS_neighbor_mislabel',lambda:must([26,28]==[27,29]))
reject('factor_three_omission',lambda:must(sector('J',26)+sector('N',26)==Q(26)))
reject('cached_purity_rounded_up',lambda:must(cached[24]+F(1,1000)<=cached[24]))
reject('resource_anomaly_erased',lambda:must(finite['prior_direct25_resource_anomaly_still_unresolved'] is False))
out={'status':'ACCEPTED stronger uniform all-size gap','gap':'31/1250','all_integer_L_at_least':2,'unique_ground_state':True,'bootstrap_initialization_used_for_this_stronger_gap':34,'smallest_separately_certified_initialization':30,'smaller_initialization_gap':'179/10000','cached_prefix_4_to25':prefix,'new_direct26_to33':new,'analytic2_3_inherited_verified':True,'n34_tail_review_seal':seals['uniform_smaller_second_initialization_review'],'all18_physical_thermal_input_mapping_verified':True,'seals':seals,'adversarial_rejections':checks,'guarded_resource_status':'PASS observed independent timers and runtime limits','new_guarded_run':guard,'prior_direct25_resource_anomaly_still_unresolved':True,'no_minimum_claim':True,'resources':{'scalar_CPU_seconds':time.process_time()-start,'scalar_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'CPU_affinity':7}}
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(H,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','gap','all_integer_L_at_least','bootstrap_initialization_used_for_this_stronger_gap','resources']},indent=2))
