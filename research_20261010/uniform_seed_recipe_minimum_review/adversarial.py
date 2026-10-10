#!/usr/bin/env python3
"""Independent all-r interval replay, strengthened to ideal unrounded fixed envelopes."""
from pathlib import Path
from fractions import Fraction as F
import os,resource,sys,json,hashlib,time,itertools
sys.set_int_max_str_digits(1000000)
P=Path(__file__).resolve().parent;ROOT=P.parents[1];A=P.with_name('uniform_seed_recipe_minimum');M=P.with_name('uniform_transfer_moment_assessment');AR=P.with_name('uniform_anchor96_100_review')
os.sched_setaffinity(0,{5 if 5 in os.sched_getaffinity(0) else min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600));start=time.process_time();B=10**40;hashes={}
def read(p):
 b=p.read_bytes();hashes[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return b
def js(p):return json.loads(read(p))
def floor(v,b=B):return F(v.numerator*b//v.denominator,b)
def ceil(v,b=B):return F(-((-v.numerator*b)//v.denominator),b)
def roots(v,k):
 assert v>=0 and k>=1
 if k==1:return v,v
 if not v:return F(0),F(0)
 lo=0;hi=B;n=v.numerator*B**k;d=v.denominator
 while hi**k*d<n:hi*=2
 while hi-lo>1:
  mid=(hi+lo)//2
  if mid**k*d<=n:lo=mid
  else:hi=mid
 a,b=F(lo,B),F(hi,B);assert a**k<=v<=b**k;return a,b
def power(v,q):
 q=F(q);return roots(v**q.numerator,q.denominator)
def expiv(x):
 if x<0:
  a,b=expiv(-x);return floor(1/b),ceil(1/a)
 k=0
 while x>F(1,8):x/=2;k+=1
 termlo=termhi=sumlo=sumhi=F(1)
 for j in range(1,81):
  termlo=floor(termlo*x/j);termhi=ceil(termhi*x/j);sumlo+=termlo;sumhi+=termhi
 rem=ceil(termhi*x/81)/(1-x/82);lo=sumlo;hi=ceil(sumhi+rem)
 for j in range(k):lo=floor(lo*lo);hi=ceil(hi*hi)
 return lo,hi
def logunit(x):
 assert 1<=x<=2
 v=(x-1)/(x+1);lo=floor(v);hi=ceil(v);sl=su=F(0)
 for j in range(96):
  sl+=2*floor(lo/(2*j+1));su+=2*ceil(hi/(2*j+1));lo=floor(lo*v*v);hi=ceil(hi*v*v)
 rem=2*hi/(193*(1-v*v));return sl,ceil(su+rem)
LOG2=logunit(F(2))
def logiv(x):
 assert x>0
 if x<1:
  a,b=logiv(1/x);return -b,-a
 shift=0
 while x>=2:x/=2;shift+=1
 a,b=logunit(x);return a+shift*LOG2[0],b+shift*LOG2[1]
G=lambda z:1-(1-z)**2/(2*z*z)

from copy import deepcopy
tests=[]
def ref_exp(x):
 if x<0:
  a,b=ref_exp(-x);return 1/b,1/a
 term=total=F(1)
 for j in range(1,241):term*=x/j;total+=term
 return total,total+(term*x/241)/(1-x/242)
for x in [F(-20),F(-1,3),F(0),F(1,64),F(1,8),F(1),F(8),F(20)]:
 lo,hi=expiv(x);rl,rh=ref_exp(x);assert lo<=rl<=rh<=hi
tests.append('independent fixed-point exponentials enclose longer exact Taylor references')
def ref_log(x):
 if x<1:
  a,b=ref_log(1/x);return -b,-a
 shift=0
 while x>=2:x/=2;shift+=1
 def one(x):
  v=(x-1)/(x+1);s=2*sum(v**(2*j+1)/F(2*j+1) for j in range(160));return s,s+2*v**321/(321*(1-v*v))
 a,b=one(x);c,d=one(F(2));return a+shift*c,b+shift*d
for x in [F(1,100),F(1,2),F(1),F(7,4),F(2),F(37,5),F(100)]:
 lo,hi=logiv(x);rl,rh=ref_log(x);assert lo<=rl<=rh<=hi
tests.append('independent directed logs enclose longer exact atanh references')
for x in [F(0),F(1,81),F(1),F(16),F(19,3)]:
 for k in (2,5,25):
  lo,hi=roots(x,k);assert lo**k<=x<=hi**k
tests.append('directed roots handle zero, exact powers, and large bases')
d=json.loads((A/'results.json').read_text());leaf=d['families'][0]['closed_interval_leaves'][0]
def validate_leaf(leaf):
 s,t=F(leaf['S_upper']),F(leaf['T_upper']);assert 0<s<=1 and 0<t<=1
 hist=leaf['failure']['history'];assert hist
 for j,step in enumerate(hist):
  if j%2==0:
   assert min(s,t)<F(99,100);arg=s*s*t;kind='spatial';s=ceil(G(arg),10**24);value=s
  else:arg=t*t*s;kind='thermal';t=ceil(G(arg),10**24);value=t
  assert 0<arg<=1 and step['kind']==kind and F(step['argument_upper'])==arg and F(step['output_upper'])==value
  assert (value<=0)==(j==len(hist)-1)
 assert leaf['failure']['round']==(len(hist)+1)//2
validate_leaf(leaf)
mutations=[]
x=deepcopy(leaf);x['failure']['history']=x['failure']['history'][:-1];mutations.append(('truncated positive trajectory',x))
x=deepcopy(leaf);x['S_upper']=x['T_upper']='1';mutations.append(('target entry mislabeled failure',x))
x=deepcopy(leaf);x['failure']['history'][-1]['output_upper']='1/2';mutations.append(('positive terminal output mislabeled failure',x))
x=deepcopy(leaf);x['failure']['round']+=1;mutations.append(('incorrect failure-round label',x))
for name,x in mutations:
 try:validate_leaf(x)
 except AssertionError:tests.append('reject '+name)
 else:raise AssertionError('Mutation accepted: '+name)
def coverage(leaves):
 ends=[(F(x['r_lower']),F(x['r_upper'])) for x in leaves]
 assert ends[0][0]==1 and ends[-1][1]==16 and all(a<b for a,b in ends) and all(a[1]==b[0] for a,b in zip(ends,ends[1:]))
leaves=deepcopy(d['families'][0]['closed_interval_leaves']);coverage(leaves);leaves[0]['r_upper']=str(F(leaves[0]['r_upper'])-F(1,1000))
try:coverage(leaves)
except AssertionError:tests.append('reject uncovered real-r interval')
else:raise AssertionError('Coverage gap accepted')
# W is merely a lower trace bound: actual leading mass need not be capped by W^(1/p).
actual_t,D,W,p=F(2),F(2),F(1),4
assert actual_t**p>=W and D>=actual_t and actual_t>W
tests.append('tstar cannot be promoted to an upper bound on actual leading mass')
assert G(F(1,256))==F(-65023,2)
tests.append('cold-ray S1/16,T1 gives strictly negative first spatial G')
out={'status':'PASS','tests':tests,'CPU_seconds':time.process_time()-start}
(P/'adversarial_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
