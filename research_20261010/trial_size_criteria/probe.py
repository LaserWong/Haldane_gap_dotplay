import os
for key in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[key]='1'
import json,math
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2]
def load(g):return [json.loads((ROOT/f'research_20261010/low_band/frontier/bilayer_{s}_g{g}_symmetric_number_low_band.json').read_text()) for s in ['2x2','4x2','4x4']]
def trace(r,b):
 s=float(F(r['blocks'][0]['eigen_upper'][0]));l=u=0.
 for bl in r['blocks']:
  l+=bl['multiplicity']*sum(math.exp(-b*(float(F(x))-s)) for x in bl['eigen_upper'])
  u+=bl['multiplicity']*sum(math.exp(-b*(float(F(x))-s)) for x in bl['eigen_lower'])
 u+=sum(row['multiplicity']*math.exp(-b*(float(F(row['lower']))-s)) for row in r['number_sector_bins']['bins'][2:])
 return l,u

def inp(recs,b):
 s=[float(F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0])) for r in recs]
 ts=[trace(r,b) for r in recs];t2=trace(recs[2],2*b)
 return [min(1,math.exp(b*(-2*s[2]+8*s[0]))*t2[1]/ts[0][0]**8),min(1,math.exp(b*(-4*s[2]+8*s[1]))*t2[1]**2/ts[1][0]**8),min(1,t2[1]/ts[2][0]**2)]
def G(x):return 1-(1-x)**2/(2*x*x)
def run(inp):
 j1,j2,c=inp;A=G(j1)
 if A<=0:return ('fail',1)
 B=G(j2*A)
 if B<=0:return ('fail',2)
 C=G(c**4*A*A*B)
 if C<=0:return ('fail',3)
 p=[A,B,C]; best=min(p)
 for n in range(100):
  if min(p)>=.998:return ('possible',n)
  x=G(p[0]**4*p[1]**2*p[2])
  if x<=0:return ('fail',n+4)
  p=p[1:]+[x];best=max(best,min(p))
 return ('unknown',best)
for g in ['1d25','1d20']:
 r=load(g);print(g)
 for b in [0.1,1,2,4,6,8,9,10,12,15,20,30]:
  v=inp(r,b);print(b,v,run(v))
 out={};maxstage=0
 for j in range(40,201):
  b=j/10;v=run(inp(r,b));out[v[0]]=out.get(v[0],0)+1;maxstage=max(maxstage,v[1])
 print(out,maxstage)
