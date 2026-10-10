#!/usr/bin/env python3
"""Float proposal only: exact results are in a separate replay."""
from pathlib import Path
from fractions import Fraction as F
import json,math,time
P=Path(__file__).resolve().parent;B=P.parent;src=B/'mps_commutator_assessment/fused_current/pi_trace_cases.json';x=json.loads(src.read_text());delta=float(F(x['delta']));rows=[]
def G(x):return 1-(1-x)**2/(2*x*x)
for case in x['cases']:
 groups=[(r['multiplicity'],float(F(r['gap_upper']))) for r in case['groups']]
 best=(-1,None);survive=0;maxcycles=0;failure={}
 for i in range(1,16001):
  beta=i/200;num=math.exp(-2*beta*delta);j=num/(1+sum(m*math.exp(-beta*g) for m,g in groups))**4;c=num/(1+sum(m*math.exp(-2*beta*g) for m,g in groups))**2
  a=G(j)
  if a<=0:continue
  b=G(c*c*a)
  if b<=0:continue
  w=a*a*math.sqrt(max(0,2*b-1))
  if w>best[0]:best=(w,beta,a,b)
  if w>.5:survive+=1
  for k in range(16):
   maxcycles=max(maxcycles,k)
   if a*a*b>=.99:failure['optimistic closure candidate']=failure.get('optimistic closure candidate',0)+1;break
   if a*a*math.sqrt(max(0,2*b-1))<=.5:failure['direct window']=failure.get('direct window',0)+1;break
   a=G(a*a*b)
   if a<=0:failure['next thermal G']=failure.get('next thermal G',0)+1;break
   b=G(b*b*a)
   if b<=0:failure['next spatial G']=failure.get('next spatial G',0)+1;break
 rows.append({'retained_states':case['retained_denominator_states'],'best_initial_direct_window_display':best,'initial_window_grid_passes':survive,'maximum_completed_extra_cycles':maxcycles,'terminal_grid_counts':failure})
out={'status':'BOUNDED FLOAT DIAGNOSTIC ONLY','beta_grid':['1/200','80','1/200'],'rows':rows};(P/'bounded_scan.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
