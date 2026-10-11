#!/usr/bin/env python3
"""Read-only exact scalar audit. No physical contractions or scientific imports."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import hashlib,json,math,resource,time,sys,re
P=Path(__file__).resolve().parent; R=P.parent; ROOT=R.parent
resource.setrlimit(resource.RLIMIT_CPU,(60,60))
resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
sys.set_int_max_str_digits(1000000)
start=time.process_time(); pins={}; B=10**160

def read(rel):
 p=R/rel; raw=p.read_bytes(); pins[str(p.relative_to(ROOT))]=hashlib.sha256(raw).hexdigest(); return raw

def js(rel): return json.loads(read(rel))
def floor(x):return F(x.numerator*B//x.denominator,B)
def ceil(x):return -floor(-x)
def evalp(a,x):
 z=F(0)
 for v in reversed(a): z=z*x+v
 return z

def interval_dot(a,m):return sum((x*(hi if x>=0 else lo) for x,(lo,hi) in zip(a,m)),F())
def affine(a,offset,scale):
 return [sum((a[j]*math.comb(j,k)*offset**(j-k)*scale**k for j in range(k,len(a))),F()) for k in range(len(a))]

@lru_cache(None)
def pow_bounds(x,p):
 assert x>=0 and p>0; p=F(p); q=p.denominator; target=x**p.numerator
 num=target.numerator*B**q//target.denominator
 if q==1: k=num
 elif q==2:k=math.isqrt(num)
 else:
  lo=0; hi=1<<((num.bit_length()+q-1)//q)
  while lo+1<hi:
   mid=(lo+hi)//2
   if mid**q<=num:lo=mid
   else:hi=mid
  k=lo
 lo,hi=F(k,B),F(k+1,B);assert lo**q<=target<=hi**q;return lo,hi

@lru_cache(None)
def exp_bounds(x):
 if x<0:
  lo,hi=exp_bounds(-x);return floor(1/hi),ceil(1/lo)
 count=0
 while x>F(1,8):x/=2;count+=1
 term=total=F(1)
 for j in range(1,101):term=term*x/j;total+=term
 lo=floor(total);hi=ceil(total+term*x/101/(1-x/102))
 for _ in range(count):lo=floor(lo*lo);hi=ceil(hi*hi)
 return lo,hi

@lru_cache(None)
def pack(m,h,r):
 assert m>=0 and h>0 and r>=1;q=m//h
 return ceil(q*pow_bounds(h,r)[1]+pow_bounds(m-q*h,r)[1])

def certify_nonnegative(coeff,left,right):
 # Full-degree power-to-Bernstein conversion, followed by exact bisection.
 degree=len(coeff)-1; a=affine(coeff,left,right-left)
 row=[sum((a[k]*F(math.comb(i,k),math.comb(degree,k)) for k in range(i+1)),F()) for i in range(degree+1)]
 todo=[(row,0)];leaves=depth=0
 while todo:
  row,d=todo.pop()
  if min(row)>=0:leaves+=1;depth=max(depth,d);continue
  assert d<30 and row[0]>=0 and row[-1]>=0
  triangle=[row]
  while len(triangle[-1])>1:triangle.append([(x+y)/2 for x,y in zip(triangle[-1],triangle[-1][1:])])
  todo.append(([v[0] for v in triangle],d+1));todo.append(([v[-1] for v in reversed(triangle)],d+1))
 return leaves,depth

def ints(rel):return {k:int(v) for k,v in (line.split('=') for line in read(rel).decode().splitlines())}
def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)
def seal(name,want):
 raw=read(name+'/MANIFEST_SHA256.json');assert hashlib.sha256(raw).hexdigest()==want
 for rel,h in json.loads(raw).items():assert hashlib.sha256(read(name+'/'+rel)).hexdigest()==h
 return want

seals={}
for name,h in [
 ('uniform_gap_0248_all_sizes_review','5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf'),
 ('uniform_smaller_second_initialization_review','54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f'),
 ('uniform_small_lengths_completion_review','b5225681662482e5ed219fe85d0cc9247703b21b183f6e6441dd081b7bc9d984'),
 ('uniform_n24_second_coverage_review','9d31eeb0dc44f24047943a4ad4dd06e4f8f82aced5ca321857a1aaedf82b8282'),
 ('uniform_direct25_coverage_review','a70156f108be662bbb9873ce12f9701701efd0b6680d2d187e677fa1e37b3cc9'),
 ('uniform_second_thermal_full_review','792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94'),
 ('uniform_second_moment_review','dbdea168300fa8a014c4a1fcbb72a6f64d1f8ddb3250949eeeed067d55c329de')]:seals[name]=seal(name,h)

# Physical error propagation is recalculated from every accepted integer W.
a=F(700741,500000);beta=F(49,4);gap=F(31,1250)
thermal=js('uniform_second_thermal_campaign_complete/thermal_inputs.json')['thermal_inputs']
assert {(r['n'],r['twist']) for r in thermal}=={(n,t) for n in range(4,13) for t in 'IP'}
endpoints={}
for r in thermal:
 n=r['n'];w=int(r['W']);root=math.isqrt(w);d=math.isqrt(3**n)+1;err=d*(281*(d+1)+1)
 x=beta*n*(F(3,2)-a);assert 0<x<15
 term=total=F(1)
 for j in range(1,101):term*=x/j;total+=term
 lo=total*max(0,root-err)**2/2**110;hi=(total+term)*(root+1+err)**2/2**110
 assert lo==F(r['lower']) and hi==F(r['upper'])
 endpoints[n,r['twist']]=(F((lo*10**18).__floor__(),10**18),F((hi*10**18).__ceil__(),10**18))
 assert r['physical_dimension']==3**n
C=js('uniform_second_moment_optimization/certificate.json');M={'J':[],'N':[]}
for n in range(4,13):
 il,iu=endpoints[n,'I'];pl,pu=endpoints[n,'P']
 M['J'].append(((il+3*pl)/4,(iu+3*pu)/4));M['N'].append(((il-pu)/4,(iu-pl)/4))
assert {s:[[str(x),str(y)] for x,y in m] for s,m in M.items()}==C['moment_intervals']
assert all(M['N'][n-4][1]<0 for n in [5,7,9,11])
assert M['J'][-1][1]==F(66606415448354239,62500000000000000)
assert M['N'][-1][1]==F(556584262998464971,2000000000000000000)
assert 76*2*2**55<2**63-1
# Four complete exterior rays, not just their endpoints.
filter_margins={};caps={}
for key,v in C['filters'].items():
 q=list(map(F,v['q']));r=F(v['cap']);sign=1 if key[-1]=='+' else -1
 squared=[sum((q[i]*q[k-i] for i in range(len(q)) if 0<=k-i<len(q)),F()) for k in range(9)]
 upper=interval_dot(squared,M[key[0]]);assert upper==F(v['upper_filter_sum'])
 margin=r**4*evalp(q,sign*r)**2-upper;assert margin==F(v['exterior_margin'])>0
 shifted=affine(q,sign*r,F(sign));assert min(shifted)>0 and shifted==list(map(F,v['positive_shift_coefficients']))
 filter_margins[key]=str(margin);caps[key]=r
long=js('uniform_smaller_second_initialization/long_certificate.json');short=js('uniform_small_lengths_completion/long_certificate.json')
assert len(long)==26 and len(short)==14
polys={**long,**short};checks={}
for key,v in polys.items():
 n=int(key[1:]);q=list(map(F,v['coeff']));assert len(q)==9
 coeff=q+[F()]*(n-3-len(q));coeff[n-4]-=1
 counts=certify_nonnegative(coeff,-caps[key[0]+'-'],caps[key[0]+'+'])
 assert counts==(v['bernstein_leaf_count'],v['bernstein_max_depth'])
 val=interval_dot(q,M[key[0]]);assert val==F(v['bound'])
 if key[0]=='N' and n%2:assert val<0
 checks[key]={'leaves':counts[0],'depth':counts[1],'bound':str(val)}
U=max(caps['J+'],caps['J-']);V=max(caps['N+'],caps['N-'])
@lru_cache(None)
def sector(s,n):
 bound=pack(M[s][-1][1],(U if s=='J' else V)**12,F(n,12));key=s+str(n)
 return min(bound,F(polys[key]['bound'])) if key in polys else bound

def trace(n):return sector('J',n)+3*sector('N',n)

def own_ray(rel,lengths):
 vals=ints(rel);out={}
 for n in lengths:
  assert vals[f'N0_{n}']>0
  out[n]=F(vals[f'H0_{n}'],vals[f'N0_{n}'])+a*n
 return out
# Exact signs and finite Rayleigh quotients use archived accepted own-length integers.
small=js('uniform_small_lengths_completion/certificate.json');rays=own_ray('uniform_small_lengths_completion_review/anchors.out',range(4,24))
finite={}
for row in small['rows']:
 n=row['L'];ray=rays[n];assert ray==F(row['shifted_total_Rayleigh'])
 Q=endpoints[n,'I'][1] if n<=12 else trace(n)
 assert Q<=F(row['trace_upper'])
 numerator=F(row['numerator_lower']);assert 0<numerator<=exp_bounds(-2*beta*ray)[0]
 purity=F(row['purity_lower']);assert F(1,2)<purity<=numerator/F(row['trace_upper'])**2<=1
 finite[n]=purity
# L24 specifically uses parity and MPS48. It is not an own-length MPS24 certificate.
r24=js('uniform_n24_second_coverage/length_resolved_certificate.json');r24seed=js('uniform_n24_second_coverage/certificate.json')['zero_gap_window']
ray48=own_ray('uniform_n28_second_initialization_review/anchor48.out',[48])[48]
assert ray48==F(r24seed['anchor_shifted_Rayleigh'])<0
ell=F(r24seed['ell']);assert 1-pack(M['J'][-1][1],ell**12,F(4))-3*sector('N',48)>0
assert ell>max(caps['J-'],V) and 0<M['J'][-1][1]-ell**12<ell**12
S=(1+((M['J'][-1][1]-ell**12)**2+3*sector('N',24))/ell**24)**-2;T=trace(48)**-2
s,t=F(r24['S']),F(r24['T']);assert 0<s<=S and 0<t<=T
K=s*s*t;assert K>F(1,2);root=pow_bounds(2*K-1,F(1,2))[0];rho=(1-root)/(1+root);d=t/(1+rho*rho)
p24=F(next(r for r in r24['rows'] if r['L']==24)['purity_lower']);assert p24<=s*pow_bounds(d,F(1,2))[0]
finite[24]=p24
# Length25 keeps the positive-energy exponential penalty.
r25=js('uniform_direct25_coverage_review/results.json');ray25=F(r25['fresh_MPS25_shifted_total_Rayleigh'])
assert ray25>0
# Full direct25 certificate fields are tested below after reading its original data.
r25c=js('uniform_direct25_coverage/certificate.json')
assert F(r25c['shifted_total_Rayleigh'])==ray25
assert F(r25c['Z25_2beta_lower'])<=exp_bounds(-2*beta*ray25)[0]<1
assert trace(24)*trace(26)<=F(r25c['Z25_squared_upper'])
finite[25]=F(r25['purity_lower']);assert finite[25]<=F(r25c['Z25_2beta_lower'])/F(r25c['Z25_squared_upper'])
new=js('uniform_gap_0248_all_sizes/certificate.json');rays.update(own_ray('uniform_gap_0248_all_sizes_review/anchors.out',range(26,34)))
for row in new['new_rows']:
 n=row['L'];assert F(row['shifted_total_Rayleigh'])==rays[n]
 need=[n-1,n+1] if n%2 else [n];assert set(row['trace_inputs'])==set(map(str,need))
 for k in need:assert 0<trace(k)<=F(row['trace_inputs'][str(k)])
 den=F(row['trace_inputs'][str(n-1)])*F(row['trace_inputs'][str(n+1)]) if n%2 else F(row['trace_inputs'][str(n)])**2
 assert den==F(row['trace_squared_upper'])
 num=F(row['numerator_lower']);assert 0<num<=exp_bounds(-2*beta*rays[n])[0]
 cc=F(row['purity_lower']);assert F(1,2)<cc<=num/den<=1;finite[n]=cc
assert set(finite)==set(range(4,34))
finite_margins={n:str(cc-exp_bounds(beta*gap)[1]*(1-cc)) for n,cc in finite.items()}
assert all(F(v)>0 for v in finite_margins.values())
# Spin addition exact low-volume multiplicities.
def couple(mult):
 nxt={}
 for j,m in mult.items():
  for k in range(abs(j-1),j+2):nxt[k]=nxt.get(k,0)+m
 return nxt
m2=couple({1:1});m3=couple(m2);assert m2=={0:1,1:1,2:1} and m3=={0:1,1:3,2:2,3:1}
assert sum((2*j+1)*v for j,v in m2.items())==9 and sum((2*j+1)*v for j,v in m3.items())==27
assert [j*(j+1)-4 for j in range(3)]==[-4,-2,2]
assert [F(j*(j+1)-6,2) for j in range(4)]==[-3,-2,0,3]
# Strong n34 initialization and every saved window, then analytic closure.
boot=js('uniform_smaller_second_initialization/certificate.json')['rows'];b34=next(v for v in boot if v['n']==34)
assert F(b34['gap'])==gap and F(next(v for v in boot if v['n']==30)['gap'])==F(179,10000)<gap
assert F(next(v for v in boot if v['n']==32)['gap'])==F(49,2000)
ray68=own_ray('uniform_smaller_second_initialization_review/anchors.out',[68])[68]
assert ray68==F(b34['shifted_Rayleigh'])<0
ell=F(b34['ell']);assert ell==F(9999962631,10**10)
force=1-pack(M['J'][-1][1],ell**12,F(68,12))-3*sector('N',68);assert 0<F(b34['forcing_margin'])<=force
residual=M['J'][-1][1]-ell**12;assert 0<residual<ell**12 and ell>max(caps['J-'],V)
tail=pow_bounds(residual,F(34,12))[1]+3*sector('N',34)
assert F(b34['S'])<=(1+tail/ell**34)**-2 and F(b34['T'])<=trace(68)**-2
prev=None;windows=[]
for j,(st,w) in enumerate(zip(b34['states'],b34['windows'])):
 s,t=F(st['S']),F(st['T']);n=34*2**j;b=beta*2**j
 assert st['n']==n and F(st['beta'])==b and (w['from'],w['to'])==(n,2*n)
 if prev:assert s<=G(prev[0]**2*prev[1]) and t<=G(prev[1]**2*s)
 else:assert s==F(b34['S']) and t==F(b34['T'])
 k=s*s*t;assert k>F(1,2);root=pow_bounds(2*k-1,F(1,2))[0];rho=(1-root)/(1+root);d=t/(1+rho*rho)
 c=(1-rho)*min(s*pow_bounds(d,F(1,2))[0],d);saved=F(w['purity']);assert F(1,2)<saved<=c
 margin=saved-exp_bounds(b*gap)[1]*(1-saved);assert 0<F(w['margin'])<=margin
 windows.append({'from':n,'to':2*n,'margin':str(margin)});prev=s,t
assert len(windows)==10 and n==17408 and b==6272
u=max(1-s,1-t);assert 0<u<=F(1,100) and 5*u*exp_bounds(b*gap)[1]<1
# Explicit rational domain proofs for the whole interval 0<=u<=.01.
e=F(1,100);assert F(9,2)/(1-e)**6<5
assert (2+5*e)**2/(2*(1-2*e-5*e*e)**2)<=5
assert e<=F(4,49) and e<=F(1,63)
assert 1+F(81,25)*e<=F(26,25)
assert F(9,5)+F(51,25)<4 and 4/(1-4*e)<=5
# Original-source Git blob identity and exact quoted theorem expressions.
for name,entry in js('uniform_second_moment_review/SOURCE_PROVENANCE.json').items():
 raw=read('uniform_second_moment_review/sources/'+name)
 assert hashlib.sha256(raw).hexdigest()==entry['sha256']
 assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==entry['git_blob_sha1']
intro=read('uniform_source_scope_review/sources/introduction.tex').decode()
assert r'\frac4{105}\log\frac{80}{79}' in intro and r'\frac{\log20}{784}' in intro
assert 'every even $L\\ge60$' in intro and 'every even }L\\ge2304' in intro

for entry in js('uniform_source_scope_review/SOURCES.json')['sources']:
 raw=read('uniform_source_scope_review/sources/'+Path(entry['path']).name)
 assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==entry['blob']
# Independent rational logarithm enclosure: scale to [1,2] and atanh series.
def log_between(x):
 k=0
 while x>2:x/=2;k+=1
 def unit(z):
  y=(z-1)/(z+1);assert 0<=y<=F(1,3)
  total=sum((2*y**(2*j+1)/(2*j+1) for j in range(160)),F())
  return total,total+2*y**321/(321*(1-y*y))
 l,u=unit(x);l2,u2=unit(F(2));return l+k*l2,u+k*u2
l,u=log_between(F(80,79));first=(4*l/105,4*u/105)
l,u=log_between(F(20));asym=(l/784,u/784)
ratios={'first':[str(gap/first[1]),str(gap/first[0])],'asymptotic':[str(gap/asym[1]),str(gap/asym[0])]}
out={'status':'PASS exact independent scalar audit','thermal_intervals':18,'whole_ray_filters':4,'global_majorants':checks,'finite_purities':{str(k):str(v) for k,v in finite.items()},'finite_gap_margins':finite_margins,'L24_route':'parity-resolved S24/T48 using physical MPS48; no MPS24 numerator','L25_positive_Rayleigh':str(ray25),'n34_negative_Rayleigh':str(ray68),'n34_forcing_margin':str(force),'n34_windows':windows,'n34_terminal_defect':str(max(1-s,1-t)),'n34_analytic_tail_closure':True,'small_volume_multiplicities':{'2':m2,'3':m3},'original_bound_ratio_intervals':ratios,'dependency_seals':seals,'scope':'scalar replay and source audit only; no new physical MPS contractions or heat columns','resources':{'cpu_seconds':time.process_time()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
(P/'INPUT_SHA256.json').write_text(json.dumps(pins,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:out[k] for k in ['status','thermal_intervals','whole_ray_filters','L24_route','resources']},indent=2))
