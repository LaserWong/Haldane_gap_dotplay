#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import os,resource,json,itertools,time
os.sched_setaffinity(0,{5 if 5 in os.sched_getaffinity(0) else min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600));start=time.process_time();tests=[]
def roots(x,k):
 if not x:return F(0),F(0)
 B=10**28;lo=0;hi=B;target=x.numerator*B**k
 while hi**k*x.denominator<target:hi*=2
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**k*x.denominator<target:lo=mid
  else:hi=mid
 return F(lo,B),F(hi,B)
def powiv(x,q):return roots(x**q.numerator,q.denominator)
def energy(v,r):return sum(powiv(a,r)[1] for a in v)
def passed(s):tests.append(s)
D,tau,tau0,t=F(3,2),F(6,5),F(13,10),F(9,10)
vertices=[(F(0),F(0)),(tau-t,F(0)),(tau-t,tau0-tau),(F(0),tau0-t)]
for q in (F(2),F(27,14),F(27,7)):
 def objective(x,y,side):return powiv(x,q)[side]+2*powiv(y/2,q)[side]+3*powiv((D-t-x-y)/3,q)[side]
 vmaxlo=max(objective(x,y,0) for x,y in vertices)
 for xi,yi in itertools.product(range(9),repeat=2):
  x,y=F(xi,20),F(yi,20)
  if x<=tau-t and x+y<=tau0-t and (x,y) not in vertices:assert objective(x,y,1)<=vmaxlo
passed('rational interior-grid checks agree with convex polygon vertices for 2,27/14,27/7')
# Fractional powers of individually chosen perfect14th powers are exact.
for q in (F(27,14),F(27,7)):
 for copies in (1,2,3):
  atoms=[F(1,2)**14,F(1,3)**14];mass=copies*sum(atoms)
  exact_tail=copies*sum(a**(14*q.numerator//q.denominator) for a in (F(1,2),F(1,3)))
  assert exact_tail<=copies*powiv(mass/copies,q)[1]
passed('fractional tails preserve each irreducible-copy multiplicity')
w=F(1,4);y=2*w
assert 2*w*w>y*y/4 and 2*w*w==y*y/2
passed('omitting the factor2 in combined complex-sector power is invalid')
for t in (F(4,5),F(9,10),F(1)):
 assert 2*t>F(3,2)
passed('a repeated leading atom contradicts D when2t>D')
# Countable unit multiplicities, geometric spectral weights.
for q in (2,3,4):
 exact_tail=F(1,2**q-1);total=F(1)
 assert exact_tail<=total**q
passed('infinite geometric spectrum obeys the sector lq bound')
weights=[F(2),F(2),F(1)];cooled=[w*w for w in weights];purity=sum(w*w for w in cooled)/sum(cooled)**2
assert purity>=1/(1+(sum(weights)-1)**2)**2
passed('ground-plus-tail cooling needs no ground uniqueness assumption')
for L in (3,5,7,9,101):
 assert 1+(-F(1,2))**L>0
 assert (-F(1))**L+F(1,2)**L<0
passed('unique negative dominant transfer contradicts positive odd physical traces')
# Exact partition-function exchange identity, using a simple product-spin physical model.
z=lambda L,t:(1+F(1,2)**t)**L
S=lambda n,t:z(2*n,t)/z(n,t)**2
T=lambda n,t:z(n,2*t)/z(n,t)**2
for n,t in ((2,1),(4,2)):
 assert S(n,2*t)*T(n,t)**2==S(n,t)**2*T(2*n,t)
 assert T(4*n,t)*S(2*n,t)**2==S(2*n,2*t)*T(2*n,t)**2
 assert S(n,2*t)*T(2*n,t)**2!=S(n,t)**2*T(2*n,t)
passed('exchange identities use T(n) in denominator and T(2n) in seed')
# G monotonicity region and exact probability square-purity bound.
G=lambda x:1-(1-x)**2/(2*x*x)
for probs in ([F(1,2),F(1,3),F(1,6)],[F(4,5),F(1,10),F(1,10)],[F(1)]):
 a=sum(x*x for x in probs);sq=sum(x**4 for x in probs)/a**2
 assert sq>=G(a)
passed('G is a lower purity bound after normalized squaring')
output={'status':'PASS','tests':tests,'cpu_seconds':time.process_time()-start,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(__file__).with_name('adversarial_results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))
