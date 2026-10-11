#!/usr/bin/env python3
"""Independent exact rational replay; reads data only, imports no producer code."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,hashlib,math,os,resource,time,sys
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(60,60));sys.set_int_max_str_digits(100000);start=time.process_time()
P=Path(__file__).resolve().parent;R=P.parent;A=R/'uniform_n26_second_coverage';ROOT=R.parent;B=10**140;H={}
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
for name,h in [('uniform_n26_second_coverage','c723bca65e315ad2c2d296a9b0cc6cf51dc67240749bd06ee812b49ec8a9e609'),('uniform_n28_second_initialization_review','e22c642a814744fed23e45e799b58be4d31da7c4e1b341e2d4c39b95bb474ead'),('uniform_smaller_second_initialization_review','54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f'),('uniform_second_thermal_full_review','792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94')]:seals[name]=seal(R/name,h)
C=js(R/'uniform_second_moment_optimization/certificate.json');L=js(R/'uniform_smaller_second_initialization/long_certificate.json');core=js(R/'uniform_smaller_second_initialization_review/scalar_results.json');cert=js(A/'length_resolved_certificate.json');failed=js(A/'certificate.json')['zero_gap_window']
assert F(L['N26']['bound'])==F(core['all_signed_majorants']['N26']['bound'])
M={k:[tuple(map(F,v)) for v in rows] for k,rows in C['moment_intervals'].items()};U=max(F(C['filters']['J+']['cap']),F(C['filters']['J-']['cap']));V=max(F(C['filters']['N+']['cap']),F(C['filters']['N-']['cap']));mj=M['J'][-1][1];mn=M['N'][-1][1]
def sector(s,n):
 m,h=(mj,U**12) if s=='J' else (mn,V**12);v=pack(m,h,F(n,12));return min(v,F(L[f'{s}{n}']['bound'])) if f'{s}{n}' in L else v
anchor=ints(R/'uniform_n28_second_initialization_review/anchor52.out');assert anchor==ints(A/'anchor52.out');norm=anchor['N0_52'];assert norm>0;ray=F(anchor['H0_52'],norm)+52*F(700741,500000);assert ray==F(failed['anchor_shifted_Rayleigh'])<0
ell=F(failed['ell']);force=1-pack(mj,ell**12,F(52,12))-3*sector('N',52);assert 0<F(failed['forcing_margin'])<=force and ell>max(V,F(C['filters']['J-']['cap'])) and 0<mj-ell**12<ell**12
Q=sector('J',52)+3*sector('N',52);tail=power(mj-ell**12,F(26,12))[1]+3*sector('N',26);S=(1+tail/ell**26)**-2;T=Q**-2;s=F(cert['S']);t=F(cert['T']);assert s==F(failed['S'])<=S and t==F(failed['T'])<=T
assert cert['n']==26 and F(cert['beta'])==F(49,4);K=F(cert['K']);assert F(1,2)<K<=s*s*t;w=F(cert['w_lower']);assert F(1,2)<w<1 and w<=(1+power(2*K-1,F(1,2))[0])/2;rho=F(cert['rho_upper']);assert rho==(1-w)/w;d=F(cert['D_lower']);assert 0<d<=t/(1+rho*rho)
rows=[]
assert [r['L'] for r in cert['rows']]==[26,27]
for row in cert['rows']:
 length=row['L'];p=F(length,26);assert F(row['p'])==p and 1<=p<=2
 base=power(s,2-p)[0]*power(d,p/2)[0];factor=1-power(rho,p)[1] if length%2 else F(1);assert F(row['base_lower'])<=base and F(row['factor_lower'])<=factor
 assert row['parity']==('odd_signed_tail' if length%2 else 'even_nonnegative_tail')
 cc=F(row['purity_lower']);assert F(1,2)<cc<=F(row['base_lower'])*F(row['factor_lower']);gap=F(row['gap']);assert gap==F(23,10000)
 margin=cc-exp_upper(F(49,4)*gap)*(1-cc);assert 0<F(row['margin'])<=margin
 rows.append({'L':length,'p':str(p),'purity_lower':str(cc),'parity_factor_lower':row['factor_lower'],'gap':str(gap),'strict_margin':str(margin)})
# Preserve failed conservative full-window constant, never a physical upper bound.
assert failed['status']=='FAIL_window' and failed['round']==0 and F(failed['gap'])==0 and F(failed['purity'])<F(1,2)
# Its exact recorded100-digit arithmetic is independently reconstructed.
BB=10**100;dn=lambda x:F(x.numerator*BB//x.denominator,BB);sq=lambda x:F(math.isqrt(x.numerator*BB**2//x.denominator),BB)
k=dn(s*s*t);rr=sq(2*k-1);rh=(1-rr)/(1+rr);dd=dn(t/(1+rh*rh));uniform=dn((1-rh)*min(s*sq(dd),dd));assert uniform==F(failed['purity'])
tailclaim=js(R/'uniform_n28_second_initialization_review/results.json');assert tailclaim['all_integer_L_at_least']==28 and F(tailclaim['gap'])>=F(23,10000) and tailclaim['bootstrap_initialization']==30
assert cert['combined_claim']['all_integer_L_at_least']==26 and cert['combined_claim']['bootstrap_initialization']==30
rd(R/'root_review/FINITE_WINDOW_INTERPOLATION.md')
checks=[]
def must(x):assert x
def reject(name,f):
 try:f()
 except AssertionError:checks.append(name);return
 raise RuntimeError(name)
reject('odd_length_tail_discarded',lambda:must(F(cert['rows'][1]['factor_lower'])==1))
reject('wrong_parity_at27',lambda:must(27%2==0))
reject('coverage_as_startup26',lambda:must(cert['combined_claim']['bootstrap_initialization']==26))
reject('failed_uniform_bound_as_no_gap',lambda:must(cert.get('physical_gap_upper_bound')==0))
reject('per_bond_anchor_substituted',lambda:must(ray==ray/52))
reject('missing_length27',lambda:must([r['L'] for r in rows]==[26]))
out={'status':'ACCEPTED parity-resolved finite prefix and composition','gap':'23/10000','individual_lengths':[26,27],'all_integer_L_at_least':26,'unique_ground_state':True,'bootstrap_initialization':30,'anchor52_shifted_total_Rayleigh':str(ray),'rows':rows,'uniform_window_failed_lower_purity':str(uniform),'failure_scope':'only this simplified full-window lower bound; no physical no-go or minimum claim','seals':seals,'adversarial_rejections':checks,'resources':{'CPU_seconds':time.process_time()-start,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(H,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','all_integer_L_at_least','bootstrap_initialization','resources']},indent=2))
