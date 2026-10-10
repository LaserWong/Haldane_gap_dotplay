"""Independent exact signed-transfer interpolation for finite 2D windows.
Scalar bridge only: it does not independently verify the physical low-band inputs.
"""
from fractions import Fraction as F
from pathlib import Path
import math,json,hashlib,argparse
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[2]
D=10**40

def sqrt_lower(x):
 x=F(x);assert x>=0
 k=math.isqrt(x.numerator*D*D//x.denominator)
 assert F(k*k,D*D)<=x<F((k+1)**2,D*D)
 return F(k,D)

def interpolate_1d(S,T):
 S,T=F(S),F(T);assert 0<S<=1 and 0<T<=1
 p=S*S*T
 if p<=F(1,2):return F(0),{'failed':'inverse purity <=1/2','p':str(p)}
 w=(1+sqrt_lower(2*p-1))/2;r=(1-w)/w
 d=T/(1+r*r);ans=(1-r)*min(S*sqrt_lower(d),d)
 # Retain an outward 40-decimal lower bound to avoid huge nested denominators.
 ans=F((ans.numerator*D)//ans.denominator,D)
 return ans,{'p':str(p),'dominant_weight_lower':str(w),'tail_ratio_upper':str(r),'d_lower':str(d),'purity_lower':str(ans)}

def interpolate_2d(A,B,C):
 A,B,C=map(F,(A,B,C))
 assert all(0<x<=1 for x in (A,B,C))
 if B<=F(1,2):return F(0),{'failed':'B<=1/2'}
 SX=A*A*sqrt_lower(2*B-1)
 TY,y=interpolate_1d(B,C)
 if TY<=0:return F(0),{'failed':'transverse thermal','y':y}
 z,x=interpolate_1d(SX,TY)
 return z,{'spatial_lower':str(SX),'transverse_thermal_lower':str(TY),'y':y,'x':x}

def down(x,bits=192):return F((x.numerator<<bits)//x.denominator,1<<bits)
def up(x,bits=192):return -down(-x,bits)
@lru_cache(None)
def exp_upper(x):
 x=F(x);assert x>=0
 k=0
 while x>F(1,4):x/=2;k+=1
 t=F(1);s=F(1)
 for j in range(1,71):t*=x/j;s+=t
 s=up(s+(t*x/71)/(1-x/72))
 for _ in range(k):s=up(s*s)
 return s

def gap(C,beta):
 if C<=F(1,2):return F(0)
 if C==1:return None
 g=F(math.floor(math.log(float(C/(1-C)))/float(beta)*10**12)-1,10**12)
 g=max(g,F(0))
 while exp_upper(beta*g)*(1-C)>=C:g-=F(1,10**12)
 return g

def audit_record(rec):
 if not rec.get('accepted'):return None
 if rec.get('order','xyt')!='xyt':return None
 boot=rec['bootstrap'];inp=boot['input'];beta=F(inp['beta']);n=inp['n'];rows=[]
 states=[list(map(F,rec['first_purities']))]+[[1-F(x) for x in row['defects']] for row in boot['updates']]
 for j,state in enumerate(states):
  c,detail=interpolate_2d(*state);b=beta*2**j;nn=n*2**j;g=gap(c,b)
  rows.append({'n':nn,'through':2*nn,'beta':str(b),'purities':list(map(str,state)),'thermal_lower':str(c),'thermal_display':float(c),'gap_lower':str(g),'gap_display':float(g) if g is not None else None,'details':detail})
 asym=F(boot['uniform_square_gap_lower'])
 required=[r for r in rows if r['n']<boot['n']]
 # Periodic ordinary g=.03 bilayer: 4N straight spin-half edges, product energy zero,
 # hence local Weyl/minmax bound 1−3gN, minimum .19 on L=2,3.
 small=F(19,100)
 allgap=min([asym,small]+[F(r['gap_lower']) for r in required])
 return {'initial_beta':rec.get('beta_initial'),'asymptotic_start':boot['n'],'asymptotic_gap':str(asym),'windows':rows,'local_L2_L3_gap':str(small),'all_integer_L_ge2_gap':str(allgap),'all_integer_gap_display':float(allgap),'physical_input_status':'producer certificate, requires independent physical/shell-tail audit'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('source',nargs='?',default='research_20261010/low_band/correlated_full_low_band_g3d100_number.json');a=ap.parse_args();p=ROOT/a.source;d=json.loads(p.read_text())
 records=d['exact_results'] if isinstance(d,dict) and 'exact_results' in d else d
 if isinstance(records,dict):records=records.get('results',[records])
 out=[r for rec in records if (r:=audit_record(rec)) is not None]
 result={'status':'PASS exact finite-window scalar interpolation, conditional on physical-input audit','source':str(p.relative_to(ROOT)),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'results':out}
 q=Path(__file__).with_name('finite_window_'+p.stem+'.json');q.write_text(json.dumps(result,indent=2)+'\n')
 for r in out:print(r['initial_beta'],r['asymptotic_start'],r['all_integer_gap_display'],[(x['n'],x['gap_display']) for x in r['windows']])
if __name__=='__main__':main()
