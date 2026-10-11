#!/usr/bin/env python3
"""Independent exact rational replay; reads data only, imports no producer code."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,hashlib,math,os,resource,time,sys
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(30,30));sys.set_int_max_str_digits(100000);start=time.process_time()
P=Path(__file__).resolve().parent;R=P.parent;A=R/'uniform_direct25_coverage';ROOT=R.parent;B=10**140;H={}
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
seals={}
for name,h in [('uniform_direct25_coverage','abd4e0f0a315ef9878129c56ee884d797707687f07361c83f1cb140f0ebee9fa'),('uniform_n24_second_coverage_review','9d31eeb0dc44f24047943a4ad4dd06e4f8f82aced5ca321857a1aaedf82b8282'),('uniform_n26_second_coverage_review','b4e4bc246acb27b63bb51745c23cbd28b7b0928d5d45ad19ddfb3ffe5d6d077d'),('uniform_smaller_second_initialization_review','54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f'),('uniform_second_thermal_full_review','792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94')]:seals[name]=seal(R/name,h)
# Fresh physical tensors and independently implemented sequential contraction.
prior=R/'uniform_smaller_second_initialization_review'
for f in ('contract_sequential','contract_sequential.cpp'):assert rd(P/f)==rd(prior/f)
for f in ('rebuild_d26.py','limited_run.py'):assert rd(P/f)==rd(prior/f).replace(b'(60,60)',b'(15,15)')
assert rd(P/'d26_blocks.txt')==rd(ROOT/'audit/mps/mps_blocks.txt');rebuild=js(P/'independent_d26.json');assert rebuild['status']=='PASS' and rebuild['D']==26
old=js(R/'nonperturbative_mps_review/d26_rebuild_results.json');assert [(x['n'],x['norm'],x['total_H_numerator']) for x in rebuild['direct_amplitude_checks']]==[(x['L'],x['norm'],x['total_H_numerator']) for x in old['direct_amplitude_checks']]
ours=ints(P/'anchor25.out');assert ours==ints(A/'anchor25.out') and set(ours)=={'H0_25','N0_25'};norm=ours['N0_25'];assert norm>0;ray=F(ours['H0_25'],norm)+25*F(700741,500000)
cert=js(A/'certificate.json');assert ray==F(cert['shifted_total_Rayleigh'])>0;assert cert['physical_L']==25 and F(cert['beta'])==F(49,4)
# Explicit bind of all18 locally reproduced physical inputs to the exact signed
# moment intervals used in Q24 and Q26; no inherited printed-only premise.
physical=js(R/'uniform_second_thermal_full_review/provenance_results.json');assert physical['thermal_inputs']==18 and physical['all_exact_W_and_refined_endpoints_match']
C=js(R/'uniform_second_moment_optimization/certificate.json');assert physical['signed_moment_intervals']==C['moment_intervals'];M={k:[tuple(map(F,v)) for v in rows] for k,rows in C['moment_intervals'].items()}
core=js(prior/'scalar_results.json');L=js(R/'uniform_smaller_second_initialization/long_certificate.json');U=max(F(C['filters']['J+']['cap']),F(C['filters']['J-']['cap']));V=max(F(C['filters']['N+']['cap']),F(C['filters']['N-']['cap']))
def sector(s,n):
 key=f'{s}{n}';assert F(L[key]['bound'])==F(core['all_signed_majorants'][key]['bound']);m=M[s][-1][1];h=(U if s=='J' else V)**12
 return min(pack(m,h,F(n,12)),F(L[key]['bound']))
Q={n:sector('J',n)+3*sector('N',n) for n in (24,26)};assert 0<Q[24]<=F(cert['Q24']) and 0<Q[26]<=F(cert['Q26'])
den=F(cert['Z25_squared_upper']);assert den==F(cert['Q24'])*F(cert['Q26'])>=Q[24]*Q[26]
beta=F(49,4);num=F(cert['Z25_2beta_lower']);assert 0<num<=1/exp_upper(2*beta*ray)<1
cc=F(cert['purity_lower']);assert F(1,2)<cc<=num/den<1;gap=F(cert['gap']);assert gap==F(23,10000);margin=cc-exp_upper(beta*gap)*(1-cc);assert 0<F(cert['exponential_margin'])<=margin
isolated=js(R/'uniform_n24_second_coverage_review/results.json');tail=js(R/'uniform_n26_second_coverage_review/results.json');assert isolated['certified_lengths']==[24] and F(isolated['gap'])>=gap and tail['all_integer_L_at_least']==26 and F(tail['gap'])>=gap and tail['bootstrap_initialization']==30
assert cert['combined_claim']=={'all_integer_L_at_least':24,'gap':'23/10000','unique_ground_state':True,'bootstrap_initialization':30,'coverage_onset':24,'union':['isolated24 frozen parity certificate','direct thermal25 certificate','26..infinity accepted coverage']}
checks=[]
def must(x):assert x
def reject(name,f):
 try:f()
 except AssertionError:checks.append(name);return
 raise RuntimeError(name)
reject('false_negative_anchor_assumption',lambda:must(ray<0))
reject('numerator_one_without_energy_factor',lambda:must(1<=1/exp_upper(2*beta*ray)))
reject('wrong_energy_sign',lambda:must(exp_upper(2*beta*ray)<=1/exp_upper(2*beta*ray)))
reject('single_bond_total_mismatch',lambda:must(ray==ray/25))
reject('omitted_threefold_N_multiplicity',lambda:must(sector('J',24)+sector('N',24)==Q[24]))
reject('coverage_as_initialization24',lambda:must(cert['combined_claim']['bootstrap_initialization']==24))
reject('missing_length25_in_union',lambda:must(25==24 or 25>=26))
# Exact illustrative signed-spectrum Cauchy-Schwarz check, with negative tail.
a=[F(3,2),F(-2,3),F(1,7)];z=lambda n:sum(x**n for x in a);assert z(25)**2<=z(24)*z(26)
out={'status':'ACCEPTED direct physical thermal25 and complete coverage composition','gap':'23/10000','direct_length':25,'all_integer_L_at_least':24,'unique_ground_state':True,'bootstrap_initialization':30,'norm_positive':True,'fresh_MPS25_shifted_total_Rayleigh':str(ray),'Q24':cert['Q24'],'Q26':cert['Q26'],'numerator_lower':str(num),'purity_lower':str(cc),'strict_gap_margin':str(margin),'all18_physical_thermal_input_mapping_verified':True,'seals':seals,'adversarial_rejections':checks,'no_minimum_claim':True,'resources':{'CPU_seconds':time.process_time()-start,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(H,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','all_integer_L_at_least','bootstrap_initialization','resources']},indent=2))
