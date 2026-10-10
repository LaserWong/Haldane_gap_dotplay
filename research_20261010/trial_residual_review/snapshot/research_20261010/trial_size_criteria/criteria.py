"""Self-contained rational trace budgets and canonical-bootstrap exclusion tests.
Input physical certificates are read-only; no project arithmetic code is imported.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'): os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
import json,hashlib,time,resource,math
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
BITS=160; M=1<<BITS
READ_HASHES={}
def read(path):
 path=ROOT/path; raw=path.read_bytes(); rel=str(path.relative_to(ROOT)); h=hashlib.sha256(raw).hexdigest()
 assert rel not in READ_HASHES or READ_HASHES[rel]==h
 READ_HASHES[rel]=h; return json.loads(raw)
def ceil_div(a,b):return -((-a)//b)
def down(x):return F((x.numerator*M)//x.denominator,M)
def up(x):return F(ceil_div(x.numerator*M,x.denominator),M)
@lru_cache(maxsize=100000)
def exp_bounds(x):
 x=F(x)
 if x<0:
  l,u=exp_bounds(-x);return down(1/u),up(1/l)
 s=0;y=x
 while y>F(1,8):y/=2;s+=1
 tl=tu=sl=su=M
 for n in range(1,41):
  tl=(tl*y.numerator)//(y.denominator*n)
  tu=ceil_div(tu*y.numerator,y.denominator*n)
  sl+=tl;su+=tu
 next_up=F(tu)*y/41
 rem=next_up/(1-y/42)
 su+=ceil_div(rem.numerator,rem.denominator)
 for _ in range(s):sl=sl*sl//M;su=ceil_div(su*su,M)
 return F(sl,M),F(su,M)
def G(x):return 1-(1-x)**2/(2*x*x)
def load_band(g):
 base='research_20261010/low_band/' if g=='3d100' else 'research_20261010/low_band/frontier/'
 return [read(base+f'bilayer_{s}_g{g}_symmetric_number_low_band.json') for s in ('2x2','4x2','4x4')]
def spectrum_terms(rec):
 shift=F(rec['blocks'][0]['eigen_upper'][0]);lo={};hi={};tail={}
 for b in rec['blocks']:
  for x in b['eigen_upper']:
   z=F(x)-shift;lo[z]=lo.get(z,0)+b['multiplicity']
  for x in b['eigen_lower']:
   z=F(x)-shift;hi[z]=hi.get(z,0)+b['multiplicity']
 for b in rec['number_sector_bins']['bins'][2:]:
  z=F(b['lower'])-shift;tail[z]=tail.get(z,0)+b['multiplicity']
 return lo,hi,tail

def sum_exp(terms,beta,upper=False):
 return sum((v*exp_bounds(-beta*x)[int(upper)] for x,v in terms.items()),F(0))
def trace(rec,beta):
 lo,hi,tail=spectrum_terms(rec);tl=sum_exp(lo,beta);tr=sum_exp(hi,beta,True);tt=sum_exp(tail,beta,True)
 return tl,tr+tt,tt,tr

def trace_interval_upper(rec,blo,bhi):
 _,hi,tail=spectrum_terms(rec)
 return sum(v*exp_bounds(-(blo if x>=0 else bhi)*x)[1] for d in (hi,tail) for x,v in d.items())
def energy_shifts(recs):return [F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs]
def exp_interval_upper(slope,bl,bh):return exp_bounds((bh if slope>=0 else bl)*slope)[1]
def input_upper(recs,bl,bh):
 es=energy_shifts(recs);ls=[trace(r,bh)[0] for r in recs];u2=trace_interval_upper(recs[2],2*bl,2*bh)
 return [min(F(1),up(exp_interval_upper(-2*es[2]+8*es[0],bl,bh)*u2/ls[0]**8)),
         min(F(1),up(exp_interval_upper(-4*es[2]+8*es[1],bl,bh)*u2**2/ls[1]**8)),
         min(F(1),up(u2/ls[2]**2))]
def input_lower(recs,beta):
 es=energy_shifts(recs);ts=[trace(r,beta) for r in recs];l2=trace(recs[2],2*beta)[0]
 return [down(exp_bounds(beta*(-2*es[2]+8*es[0]))[0]*l2/ts[0][1]**8),
         down(exp_bounds(beta*(-4*es[2]+8*es[1]))[0]*l2**2/ts[1][1]**8),
         down(l2/ts[2][1]**2)]
def recursion(inputs,upper=False,max_steps=60,threshold=F(1,500)):
 rounder=up if upper else down;j1,j2,c=inputs;states=[]
 A=rounder(G(j1));states.append(A)
 if A<=0:return dict(status='nonpositive_update',step=1,bound=A)
 B=rounder(G(j2*A));states.append(B)
 if B<=0:return dict(status='nonpositive_update',step=2,bound=B)
 C=rounder(G(c**4*A*A*B));states.append(C)
 if C<=0:return dict(status='nonpositive_update',step=3,bound=C)
 p=[A,B,C];first=p[:]
 for n in range(max_steps):
  if min(p)>=1-threshold:return dict(status='entered_small_defect_domain',step=n+3,first=first,final=p)
  x=rounder(G(p[0]**4*p[1]**2*p[2]))
  if x<=0:return dict(status='nonpositive_update',step=n+4,bound=x,first=first)
  p=p[1:]+[x]
 return dict(status='inconclusive',step=max_steps+3,first=first,final=p)
def serial(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [serial(y) for y in x]
 return x

def exclude_all_beta(recs,step=F(1,20)):
 hot=F(4);cold=F(20);tc=trace(recs[2],hot);C_hot=up(tc[1]/tc[0]**2) # numerator must be at 2*beta
 C_hot=up(trace(recs[2],2*hot)[1]/tc[0]**2)
 hot_final_upper=up(G(min(F(1),C_hot)**4));assert hot_final_upper<0
 es=energy_shifts(recs);w=F(recs[2]['blocks'][0]['eigen_upper'][0])-F(recs[2]['blocks'][0]['eigen_lower'][0]);elow=es[2]-w
 d1=2*elow-8*es[0];d2=4*elow-8*es[1];assert d1>0 and d2>0
 # All shifted retained/tail lower gaps relative to the ground lower endpoint are nonnegative.
 _,ht,tt=spectrum_terms(recs[2]);assert all(z+w>=0 for z in list(ht)+list(tt))
 relative_terms={}
 for d in (ht,tt):
  for z,v in d.items():relative_terms[z+w]=relative_terms.get(z+w,0)+v
 Urel=sum_exp(relative_terms,2*cold,True)
 cold_input=[min(F(1),up(exp_bounds(-cold*d1)[1]*Urel)),min(F(1),up(exp_bounds(-cold*d2)[1]*Urel**2)),F(1)]
 cr=recursion(cold_input,True);assert cr['status']=='nonpositive_update'
 rows=[];bl=hot
 while bl<cold:
  bh=min(cold,bl+step);inp=input_upper(recs,bl,bh);res=recursion(inp,True)
  if res['status']!='nonpositive_update':
   raise AssertionError(('interval not excluded',str(bl),str(bh),serial(inp),serial(res)))
  rows.append(dict(beta_interval=[bl,bh],input_upper=inp,failed_update=res['step'],nonpositive_upper=res['bound']))
  bl=bh
 return dict(status='PASS all beta>=0 canonical recursion exclusion conditional on physical input certificates',
  hot_range=[0,hot],thermal_purity_upper=C_hot,hot_third_update_upper=hot_final_upper,
  cold_range=[cold,'infinity'],cold_slopes=[d1,d2],cold_inputs_upper=cold_input,cold_recursion=cr,
  middle_range=[hot,cold],step=step,interval_count=len(rows),maximum_failed_update=max(x['failed_update'] for x in rows),intervals=rows)

if __name__=='__main__':
 start=time.monotonic();results={}
 for g in ['1d25','1d20']:
  recs=load_band(g);res=exclude_all_beta(recs);results[g]=res
  print(g,res['status'],'intervals',res['interval_count'],'latest failure step',res['maximum_failed_update'],flush=True)
 for p,h in READ_HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
 result=dict(status='PASS new exact scalar deduction from saved complete-band certificates; physical inputs not independently reconstructed here',results=results,input_sha256=READ_HASHES,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (OUT/'all_beta_exclusions.json').write_text(json.dumps(serial(result),indent=2)+'\n')
 print('time',result['seconds'],'RSS',result['peak_rss_kib'],flush=True)
