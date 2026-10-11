#!/usr/bin/env python3
"""Floating proposal only; no physical work, no certified conclusion."""
import json,math,time,resource
from fractions import Fraction as F
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(5,5));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));start=time.process_time()
P=Path(__file__).resolve().parent
seeds=json.loads((P.parent/'uniform_smaller_second_initialization/certificate.json').read_text())['rows']
G=lambda x:1-(1-x)**2/(2*x*x)
def test(row,r,gap):
 L=row['n'];b=12.25;A=9/8*(b*L*r)**2;s=float(F(row['S']))*math.exp(-2*A);t=float(F(row['T']))*math.exp(-8*A)
 if (.0248-3*(L-2)*r)/(1+r)<gap:return False,'short'
 for j in range(16):
  C=min(s*math.sqrt(t),t)
  if C<=.5:return False,f'C{j}'
  if C<1 and math.log(C/(1-C))<=b*(1+r)*gap:return False,f'gap{j}'
  u=max(1-s,1-t)
  if u<=.01 and (u<=0 or math.log(1/(5*u))>b*(1+r)*gap):return True,f'close{j}'
  s=G(s*s*t)
  if s<=0:return False,f'S{j}'
  t=G(t*t*s)
  if t<=0:return False,f'T{j}'
  b*=2
 return False,'no_close'
out=[]
for row in seeds:
 for gap in [.005,.01,.015,.02]:
  lo,hi=0,.001
  if not test(row,lo,gap)[0]:out.append({'n':row['n'],'gap':gap,'baseline_failed':True});continue
  for _ in range(44):
   mid=(lo+hi)/2
   if test(row,mid,gap)[0]:lo=mid
   else:hi=mid
  rec={'n':row['n'],'gap':gap,'radius_display':lo,'failure':test(row,hi,gap)[1]};out.append(rec);print(rec)
result={'status':'FLOATING_PROPOSAL_ONLY','rows':out,'cpu_seconds':time.process_time()-start,'rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'design_results.json').write_text(json.dumps(result,indent=2)+'\n');print(result['cpu_seconds'],result['rss_kib'])
