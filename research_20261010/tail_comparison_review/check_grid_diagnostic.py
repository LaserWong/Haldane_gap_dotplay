"""Independent floating diagnostic for the single producer grid without success.
This is neither an all-beta exclusion nor part of mathematical acceptance.
"""
from independent_math import *
HERE=Path(__file__).resolve().parent;SRC=HERE/'snapshot/low_band/tail_comparison/original'
recs=[json.loads((SRC/f'temple_{x}x{y}_g3d50.json').read_text()) for x,y in [(4,4),(8,4),(8,8)]]
prepared=[]
for r in recs:
 shift=F(r['blocks'][0]['eigen_upper'][0]);lo=[];hi=[]
 for b in r['blocks']:
  lo.extend((b['multiplicity'],float(F(z)-shift)) for z in b['eigen_upper'])
  hi.extend((b['multiplicity'],float(F(z)-shift)) for z in b['eigen_lower'])
 hi.extend((q['multiplicity'],float(F(q['lower'])-shift)) for q in r['number_sector_bins']['bins'][2:])
 prepared.append((lo,hi,float(F(r['energy_shift'])+shift)))
def trace(i,beta):
 lo,hi,_=prepared[i];return sum(m*math.exp(-beta*z) for m,z in lo),sum(m*math.exp(-beta*z) for m,z in hi)
def score(beta):
 q0,q1,q2=[trace(i,beta) for i in range(3)];q3=trace(2,2*beta);e=[r[2] for r in prepared]
 j1=math.exp(-2*beta*e[2]+8*beta*e[0])*q3[0]/q0[1]**8
 j2=math.exp(-4*beta*e[2]+8*beta*e[1])*q3[0]**2/q1[1]**8
 c0=q3[0]/q2[1]**2
 def GG(x):return 1-(1-x)**2/(2*x*x)
 abc=[]
 for i in range(3):
  p=j1 if i==0 else j2*abc[0] if i==1 else c0**4*abc[0]**2*abc[1]
  if p<=0:return 1.
  z=GG(p);abc.append(z)
  if z<=0:return 1.
 for k in range(16):
  u=max(1-z for z in abc)
  if u<=.002:return -math.log(1/(32*u))/(2**(k+1)*beta) if u>0 else -1.
  for _ in range(3):
   z=GG(abc[0]**4*abc[1]**2*abc[2])
   if z<=0:return 1+u
   abc=abc[1:]+[z]
 return max(1-z for z in abc)
rows=[(score(i/20),str(F(i,20))) for i in range(100,601)];assert all(s>=0 for s,b in rows)
out=dict(status='INDEPENDENT FLOAT DIAGNOSTIC ONLY',variant='original',g='3/50',order='xyt',grid='beta 5..30 in steps .05',sample_count=len(rows),successful_proposals=0,all_beta_exclusion=False,minimum_score=min(s for s,b in rows))
(HERE/'results/grid_no_success_diagnostic.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
