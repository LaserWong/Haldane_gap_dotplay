#!/usr/bin/env python3
"""Independent exact rational replay; reads data only, imports no producer code."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,hashlib,math,os,resource,time,sys
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(30,30));sys.set_int_max_str_digits(100000);start=time.process_time()
P=Path(__file__).resolve().parent;R=P.parent;A=R/'uniform_small_lengths_completion';ROOT=R.parent;B=10**140;H={}
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
for name,h in [('uniform_small_lengths_completion','71606fa80898fb73b6f0fffb359480a1d3e716d98c47791d16d3470618c4af08'),('uniform_second_thermal_full_review','792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94'),('uniform_smaller_second_initialization_review','54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f'),('uniform_direct25_coverage_review','a70156f108be662bbb9873ce12f9701701efd0b6680d2d187e677fa1e37b3cc9')]:seals[name]=seal(R/name,h)
C=js(R/'uniform_second_moment_optimization/certificate.json');physical=js(R/'uniform_second_thermal_full_review/provenance_results.json');assert physical['thermal_inputs']==18 and physical['all_exact_W_and_refined_endpoints_match'] and physical['signed_moment_intervals']==C['moment_intervals'];M={s:[tuple(map(F,x)) for x in v] for s,v in C['moment_intervals'].items()}
I={int(r['case'].split('_')[0][1:]):F(r['refined_rounded_interval'][1]) for r in physical['cases'] if r['case'].endswith('_I')};assert set(I)==set(range(4,13))
L=js(A/'long_certificate.json');assert set(L)=={f'{s}{k}' for s in ['J','N'] for k in [13,14,15,17,19,21,23]};polys={}
for key,v in L.items():
 s=key[0];k=int(key[1:]);q=list(map(F,v['coeff']));assert len(q)==9
 a=-F(C['filters'][s+'-']['cap']);b=F(C['filters'][s+'+']['cap']);poly=q+[F(0)]*(k-3-len(q));poly[-1]-=1
 count,depth=bernstein(poly,a,b);bound=sum(c*(u if c>=0 else l) for c,(l,u) in zip(q,M[s]));assert bound==F(v['bound']) and (count,depth)==(v['bernstein_leaf_count'],v['bernstein_max_depth'])
 if s=='N' and k%2:assert bound<0
 polys[key]={'bound':str(bound),'leaves':count,'depth':depth}
old=js(R/'uniform_smaller_second_initialization/long_certificate.json');core=js(R/'uniform_smaller_second_initialization_review/scalar_results.json')
for key,v in old.items():assert F(v['bound'])==F(core['all_signed_majorants'][key]['bound'])
old.update(L);U=max(F(C['filters']['J+']['cap']),F(C['filters']['J-']['cap']));V=max(F(C['filters']['N+']['cap']),F(C['filters']['N-']['cap']))
def sector(s,n):
 bound=pack(M[s][-1][1],(U if s=='J' else V)**12,F(n,12));key=f'{s}{n}'
 return min(bound,F(old[key]['bound'])) if key in old else bound
def trace(n):
 if n<=12:return I[n],'PHYSICAL_UNTWISTED_I'
 q=sector('J',n)+3*sector('N',n);assert q>0
 if n%2:
  left=I[n-1] if n-1<=12 else sector('J',n-1)+3*sector('N',n-1);right=sector('J',n+1)+3*sector('N',n+1);cs=power(left*right,F(1,2))[1]
  return (q,'SIGNED_MOMENT_POLYNOMIAL') if q<=cs else (cs,'EVEN_NEIGHBOR_CAUCHY_SCHWARZ')
 return q,'EVEN_SIGNED_MOMENT_OR_PACKING'
ours=ints(P/'anchors.out');assert ours==ints(A/'anchors.out') and set(ours)=={f'{t}_{n}' for t in ['H0','N0'] for n in range(4,24)}
prior=R/'uniform_smaller_second_initialization_review'
for f in ['contract_sequential','contract_sequential.cpp']:assert rd(P/f)==rd(prior/f)
assert rd(P/'rebuild_d26.py')==rd(prior/'rebuild_d26.py').replace(b'(60,60)',b'(30,30)')
assert rd(P/'d26_blocks.txt')==rd(ROOT/'audit/mps/mps_blocks.txt');rebuild=js(P/'independent_d26.json');assert rebuild['D']==26 and rebuild['status']=='PASS'
cert=js(A/'certificate.json');assert [r['L'] for r in cert['rows']]==list(range(4,24)) and cert['failed_bound_lengths']==[]
rows=[];beta=F(49,4);gap=F(23,10000)
for r in cert['rows']:
 n=r['L'];norm=ours[f'N0_{n}'];assert norm>0;ray=F(ours[f'H0_{n}'],norm)+n*F(700741,500000);assert ray==F(r['shifted_total_Rayleigh']);Q,method=trace(n);assert Q<=F(r['trace_upper']) and method==r['trace_method']
 if n<=12:assert Q==F(r['trace_upper'])
 num=F(r['numerator_lower']);assert 0<num<=exp_lower(-2*beta*ray);cc=F(r['purity_lower']);assert F(1,2)<cc<=num/F(r['trace_upper'])**2<=1;assert r['passed'] and F(r['gap'])==gap
 margin=cc-exp_upper(beta*gap)*(1-cc);assert 0<F(r['margin'])<=margin
 rows.append({'L':n,'shifted_total_Rayleigh':str(ray),'trace_method':method,'trace_upper':r['trace_upper'],'purity_lower':str(cc),'gap':'23/10000','strict_margin':str(margin)})
# Independent finite angular momentum multiplicities, without any transfer
# identity below4 or numerical diagonalization.
def couple(mult):
 nxt={}
 for j,m in mult.items():
  for total in range(abs(j-1),j+2):nxt[total]=nxt.get(total,0)+m
 return nxt
m2=couple({1:1});m3=couple(m2);assert m2=={0:1,1:1,2:1} and m3=={0:1,1:3,2:2,3:1};assert sum((2*j+1)*m for j,m in m2.items())==9 and sum((2*j+1)*m for j,m in m3.items())==27
e2={j:j*(j+1)-4 for j in m2};e3={j:F(j*(j+1)-6,2) for j in m3};assert sorted(e2.values())==[-4,-2,2] and sorted(e3.values())==[-3,-2,0,3] and m2[0]==m3[0]==1
assert F(cert['analytic_small_lengths']['2']['gap'])==2 and F(cert['analytic_small_lengths']['3']['gap'])==1
rd(ROOT/'audit/APPENDIX_A_BRIDGE.md');rd(R/'MODELS_AND_NORMALIZATION.md')
tail=js(R/'uniform_direct25_coverage_review/results.json');assert tail['all_integer_L_at_least']==24 and F(tail['gap'])>=gap and tail['bootstrap_initialization']==30
assert cert['combined_claim']=={'all_integer_L_at_least':2,'gap':'23/10000','unique_ground_state':True,'bootstrap_initialization':30,'coverage_onset':2,'union':['analytic2,3','direct thermal4..23','inherited24..infinity']}
checks=[]
def must(x):assert x
def reject(name,f):
 try:f()
 except AssertionError:checks.append(name);return
 raise RuntimeError(name)
for key in ['N13','N15','N17','N19','N21','N23']:reject(key+'_replaced_by_unsigned',lambda key=key:must(F(L[key]['bound'])==abs(F(L[key]['bound']))))
for n in range(4,13):
 Pupper=F(next(x for x in physical['cases'] if x['case']==f'L{n}_P')['refined_rounded_interval'][1]);reject(f'wrong_P_seam_at{n}',lambda:must(I[n]==Pupper))
reject('L2_single_bond_gap_substitution',lambda:must(F(e2[1]-e2[0])==1))
reject('L3_singlet_multiplicity_error',lambda:must(m3[0]==3))
reject('coverage2_as_bootstrap2',lambda:must(tail['bootstrap_initialization']==2))
reject('missing_integer23',lambda:must(set(range(2,23))|set(range(24,30))==set(range(2,30))))
guard=js(P/'guard_resources.json');assert guard['exit_code']==0 and not guard['wall_watchdog_fired'] and guard['wait4_total_cpu_seconds']<=30 and guard['wall_seconds']<25 and guard['wait4_maxrss_kib']<102400
assert guard['postexec_observations'];obs=guard['postexec_observations'][0];assert next(x for x in obs['limits'].splitlines() if x.startswith('Max cpu time')).split()[3:5]==['30','30'];assert next(x for x in obs['limits'].splitlines() if x.startswith('Max address space')).split()[3:5]==['104857600','104857600'];assert any('Threads:' in x and x.split()[-1]=='1' for x in obs['status_fields']);assert any('Cpus_allowed_list:' in x and x.split()[-1]=='5' for x in obs['status_fields'])
out={'status':'ACCEPTED full finite prefix and all-integer composition','gap':'23/10000','all_integer_L_at_least':2,'unique_ground_state':True,'bootstrap_initialization':30,'finite_direct_lengths':list(range(4,24)),'analytic_small_lengths':{'2':{'gap':'2','ground_multiplicity':1},'3':{'gap':'1','ground_multiplicity':1}},'rows':rows,'signed_majorants':polys,'all18_physical_input_mapping_verified':True,'seals':seals,'adversarial_rejections':checks,'prior_direct25_resource_anomaly_still_unresolved':True,'new_guarded_run':guard,'resources':{'scalar_CPU_seconds':time.process_time()-start,'scalar_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(H,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','all_integer_L_at_least','bootstrap_initialization','resources']},indent=2))
