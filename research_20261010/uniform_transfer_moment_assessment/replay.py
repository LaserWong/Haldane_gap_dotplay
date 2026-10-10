#!/usr/bin/env python3
"""Bounded exact-rational refinement of sealed spin-one thermal-transfer moments."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,os,resource,time
P=Path(__file__).resolve().parent; ROOT=P.parents[1]
allowed=os.sched_getaffinity(0); cpu=next((c for c in (0,5) if c in allowed),min(allowed));os.sched_setaffinity(0,{cpu})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(180,180))
t0=time.process_time(); hashes={}; B=10**30

def read(rel):
 p=ROOT/rel; raw=p.read_bytes();hashes[rel]=hashlib.sha256(raw).hexdigest();return raw

def down(x,b=B):return F(x.numerator*b//x.denominator,b)
def up(x,b=B):return F(-(-x.numerator*b//x.denominator),b)
def expi(x):
 if x<0:
  l,u=expi(-x);return down(1/u),up(1/l)
 k=0
 while x>F(1,16):x/=2;k+=1
 term=s=F(1)
 for j in range(1,41):term=term*x/j;s+=term
 nxt=term*x/41;l=down(s);u=up(s+nxt/(1-x/42))
 for _ in range(k):l=down(l*l);u=up(u*u)
 return l,u

def rootup(x,q,b=10**24):
 lo=0;hi=b
 while F(hi,b)**q<x:hi*=2
 while hi-lo>1:
  mid=(hi+lo)//2
  if F(mid,b)**q>=x:hi=mid
  else:lo=mid
 r=F(hi,b);assert r**q>=x;return r

def row(x):return {'exact':str(x),'display':float(x)}
audit=json.loads(read('audit/independent/streamed_heat_audit.json'))
assert audit['all_9_appendix_A_physical_inputs_verified']
trusted={r['certificate']:r['sha256'] for r in audit['independent_aggregate_intervals']}
physical={}; moments={s:{} for s in ['trivial','complex','vector']}
for L in (6,8,10):
 vals=[]
 for twist in ['I','P','C']:
  rel=f'heat_trace/results/A_L{L}_{twist}_full/certificate.json';d=json.loads(read(rel));assert hashes[rel]==trusted[rel]
  assert d['L']==L and d['twist']==twist and d['beta']=='21/2' and d['energy_shift_a']=='700741/500000'
  iv=[F(int(d['interval'][t]['numerator']),int(d['interval'][t]['denominator'])) for t in ['lower','upper']]
  vals.append(iv);physical[f'{L}_{twist}']={'lower':row(iv[0]),'upper':row(iv[1]),'theta':d['theta']}
 for s,co in [('trivial',[F(1,12),F(1,4),F(2,3)]),('complex',[F(1,12),F(1,4),F(-1,3)]),('vector',[F(1,4),F(-1,4),F(0)])]:
  low=sum(c*v[0 if c>=0 else 1] for c,v in zip(co,vals));high=sum(c*v[1 if c>=0 else 0] for c,v in zip(co,vals))
  moments[s][L//2]=(down(low,10**12),up(high,10**12))
caps={};checks={}
for s,m in moments.items():
 a=m[3][1];b=m[4][0];c=m[5][1]
 # On the complete feasible domain x^5<=c, x^4<b; no max() branch ambiguity.
 assert c**4<b**5
 f=lambda x:a*c-b*b-c*x**3+2*b*x**4-a*x**5
 lo=max(F(4)*b/(5*a),F(0));assert f(lo)>0
 hi=rootup(c,5)
 for _ in range(70):
  mid=(lo+hi)/2
  if f(mid)>=0:lo=mid
  else:hi=mid
 cap=up(hi,10**10)
 assert f(cap)<0 and cap>=4*b/(5*a)
 deriv=-3*c+8*b*cap-5*a*cap*cap;assert deriv<0
 # derivative quadratic decreases thereafter; F stays negative, excluding all x>=cap.
 caps[s]=cap;checks[s]={'x_cap':row(cap),'lambda_cap_upper':row(rootup(cap,2)),'F_at_cap':row(f(cap)),'derivative_quadratic_at_cap':row(deriv),'moment_intervals':{str(j):[row(v) for v in iv] for j,iv in m.items()}}

def sector_bound(s,L):
 h=caps[s]**5;M=moments[s][5][1];q=M//h;rest=M-q*h
 assert 0<=rest<h
 return up(q*caps[s]**(L//2)+rootup(rest**(L//2),5)),int(q)
def trace_bound(L):return sum(mult*sector_bound(s,L)[0] for s,mult in [('trivial',1),('complex',2),('vector',3)])
lengths=list(range(10,122,2));bounds={str(L):{'Z_upper':row(trace_bound(L)),'sectors':{s:{'upper':row(sector_bound(s,L)[0]),'packed_full_atoms':sector_bound(s,L)[1]} for s in caps}} for L in lengths}
# Existing exact D26 energies only. No new contraction or spectral calculation.
def ints(rel):return {k:int(v) for l in read(rel).decode().splitlines() if '=' in l for k,v in [l.split('=',1)]}
g=ints('research_20261010/mps_excited_seed_witnesses/ground_lengths.out')
manifest=json.loads(read('research_20261010/mps_excited_seed_witnesses/PHYSICAL_MANIFEST_SHA256.json'))
assert hashes['research_20261010/mps_excited_seed_witnesses/ground_lengths.out']==manifest['files']['ground_lengths.out']
rays={int(k[3:]):F(v,g['N0_'+k[3:]]) for k,v in g.items() if k.startswith('H0_')}
old=ints('audit/mps/contraction.out')
for L in (72,120):rays[L]=L*F(old[f'U{L}'],old[f'V{L}'])
G=lambda x:1-(1-x)**2/(2*x*x)
scan=[]
for L,R in sorted(rays.items()):
 n=L//2
 if L%4 or n<10:continue
 U=trace_bound(n);Rshift=R+F(700741,500000)*L;lo,hi=expi(-21*Rshift);j=down(lo/U**4);jhi=up(hi/U**4);a=G(j);ahi=G(jhi)
 entry={'n':n,'numerator_length':L,'R_shifted':row(Rshift),'U_beta':row(U),'U_2beta_by_cooling':row(U*U),'J_lower_C_lower':row(j),'first_G':row(a),'J_C_recipe_upper':row(jhi),'first_G_recipe_upper':row(ahi)}
 if a<=0:
  assert ahi<0
  entry['outcome']='no startup: first lower-bound G is nonpositive'
 else:
  z=j*j*a;b=G(z);bhi=G(jhi*jhi*ahi);assert bhi<0;entry.update(second_argument=row(z),second_G=row(b));entry['outcome']='no startup: second lower-bound G is nonpositive' if b<=0 else 'positive initial pair; requires continued replay'
 if n==24:
  assert ahi<F(2,5) and G(F(2,5))<0
  entry['even_C_equal_one_fails']=True
 scan.append(entry)
assert all('no startup' in r['outcome'] for r in scan)
output={'status':'PASS exact bounds; no new gap or seed certificate','beta':'21/2','energy_shift':'700741/500000','physical_inputs':physical,'hankel_caps':checks,'all_even_trace_bounds':bounds,'fixed_D26_cooling_scan':scan,'best_even_envelope':min(((float(trace_bound(L)),L) for L in lengths)),'resources':{'cpu':cpu,'cpu_seconds':time.process_time()-t0,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'memory_limit_bytes':1024**3}}
(P/'results.json').write_text(json.dumps(output,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n')
print(json.dumps({'status':output['status'],'caps':{s:float(rootup(c,2)) for s,c in caps.items()},'Z24':float(trace_bound(24)),'Z48':float(trace_bound(48)),'scan':[(r['n'],r['J_lower_C_lower']['display'],r['outcome']) for r in scan],'resources':output['resources']},indent=2))
