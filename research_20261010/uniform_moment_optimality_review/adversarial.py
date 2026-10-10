#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import itertools,json,os,resource
os.sched_setaffinity(0,{5 if 5 in os.sched_getaffinity(0) else min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
P=Path(__file__).resolve().parent;data=json.loads((P/'independent_results.json').read_text());tests=[]
s=data['sectors']['trivial'];h,t=F(s['h']),F(s['t']);wh,wt=map(F,s['nu_weights']);counts=[wh/h**3,wt/t**3]
assert any(c.denominator!=1 for c in counts)
# Rounding fractional Radau counts is not a moment-preserving construction.
for j in (3,4,5):assert sum(round(c)*x**j for c,x in zip(counts,(h,t)))!=wh*h**(j-3)+wt*t**(j-3)
tests.append('rounding relaxed effective counts destroys exact fixed moments')
unit={s:[(r['count'],F(r['x'])) for r in v['integer_list']] for s,v in data['sectors'].items()}
small=unit['trivial'][:-1]
c2_without=sum(n*x for n,x in small)-sum(n*x for n,x in unit['complex'])
c2_with=sum(n*x for n,x in unit['trivial'])-sum(n*x for n,x in unit['complex'])
assert c2_without<0<c2_with
tests.append('without the tiny trivial block, C2 is negative')
# The tiny block contributes exactly1e-15 at length6, not zero.
assert sum(n*x**3 for n,x in unit['trivial'])-sum(n*x**3 for n,x in small)==F(1,10**15)
tests.append('dropping tiny high-order moment contributions is forbidden')
# Independent interval-box extremes need not meet correlated raw intervals.
raw=json.loads((P.parent/'uniform_transfer_moment_assessment/results.json').read_text());ex=lambda r:F(r['exact'])
violations=[]
for L in (6,8,10):
 vals=[ex(raw['hankel_caps'][s]['moment_intervals'][str(L//2)][1]) for s in ('trivial','complex','vector')]
 z=vals[0]+2*vals[1]+3*vals[2]
 if z>ex(raw['physical_inputs'][f'{L}_I']['upper']):violations.append(L)
assert violations
tests.append('independent sector upper corners can violate raw identity-trace interval')
# Missing copy factors produce the wrong physical total.
I,O,N=[sum(n*x**3 for n,x in unit[s]) for s in ('trivial','complex','vector')]
assert I+O+N!=I+2*O+3*N
tests.append('A4 physical multiplicities1,2,3 must be restored exactly once')
# Global slack quotient coefficients are positive, including the x=0 endpoint.
k=10;coeff=[sum((a+1)*t**a*h**(7-j-a) for a in range(8-j)) for j in range(8)]
assert all(c>0 for c in coeff) and coeff[0]>=h**7
for x in [F(0),t,h,t-F(1,100000),t+F(1,100000),h-F(1,100000)]:
 slack=x**3*(x-t)**2*(h-x)*sum(c*x**j for j,c in enumerate(coeff))
 assert slack>=0
assert h**3*(h-t)**2*(h-h)==0
tests.append('integer-correction slack proof includes x0,xh and near-node boundaries')
out={'status':'PASS','tests':tests,'sector_corner_violations_at_lengths':violations,'C2_without_tiny_block':str(c2_without),'C2_with_tiny_block':str(c2_with)}
(P/'adversarial_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
