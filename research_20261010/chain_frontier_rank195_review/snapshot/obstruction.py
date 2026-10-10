"""Exact all-beta obstruction for the fixed g=1/4 initial time-first window recipe."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
import json,math,resource,time
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
HERE=Path(__file__).resolve().parent
SCALE=1<<96
def down(x):return F(x.numerator*SCALE//x.denominator,SCALE)
def up(x):return -down(-x)
@lru_cache(maxsize=8192)
def expbox(x):
 if x<0:
  lo,hi=expbox(-x);return down(1/hi),up(1/lo)
 n=0
 while x>F(1,16):x/=2;n+=1
 term=v=F(1)
 for j in range(1,25):term=term*x/j;v+=term
 nxt=term*x/25;lo=down(v);hi=up(v+nxt/(1-x/26))
 for _ in range(n):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi
def G(x):return 1-(1-x)**2/(2*x*x)
def main():
 started=time.monotonic();rec=json.loads((HERE/'expanded_inputs.json').read_text())[-1];assert rec['g']=='1/4';s=rec['small'];ep=s['expanded_band']['comparison_endpoints'];assert ep[1]['multiplicity']==3
 delta=F(rec['large']['exact_rayleigh'])-2*F(s['exact_rayleigh']);d=-8+F(ep[1]['lower'])-F(s['exact_rayleigh'])
 dl=F(delta.numerator*10**9//delta.denominator,10**9);du=F(-((-d.numerator*10**9)//d.denominator),10**9);assert 0<dl<=delta and du>=d>0
 records=[];best=F(0)
 for k in range(1200):
  low=F(k,100);high=low+F(1,100)
  L=expbox(-2*low*dl)[1];q1=1+3*expbox(-high*du)[0];q2=1+3*expbox(-2*high*du)[0]
  J=min(F(1),L/q1**4);cc=min(F(1),L/q2**2);a=max(F(0),G(J));z=cc*cc*a;bb=max(F(0),G(z)) if z>0 else F(0);pp=up(a*a*bb)
  assert pp<F(5,8),(low,float(pp))
  records.append(dict(beta=[str(low),str(high)],joint_after_first_cycle_upper=str(pp)))
  best=max(best,pp)
 tail=expbox(-4*12*dl)[1];assert tail<F(1,2)
 out=dict(status='EXACT_RECIPE_SCOPED_ALL_BETA_OBSTRUCTION',g='1/4',scope='Fixed saved 195D counted denominator and saved two-vector M8 numerator; initial time-first purification followed by its canonical [8,16] signed-transfer window at beta=2*initial_beta.',delta_exact=str(delta),triplet_excitation_exact=str(d),delta_lower=str(dl),triplet_excitation_upper=str(du),finite_beta_cover=[0,12],interval_width='1/100',intervals=records,maximum_postcycle_joint_upper=str(best),display=float(best),beta_ge12_second_argument_upper=str(tail),seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,consequence='On beta<=12, transported P=a^2*b<5/8. The ideal first-window purity is (sqrt(2P-1)+(2P-1))/2<=3/8 when P>1/2, otherwise its domain fails. On beta>=12, z<1/2 implies b<1/2 and P<1/2. Thus the fixed recipe cannot certify its first [8,16] window at any beta. This limits recipe outputs, not physical ratios.')
 (HERE/'obstruction_g1d4.json').write_text(json.dumps(out,indent=2)+'\n');print('ALL BETA OBSTRUCTION PASS',float(best),float(tail),'seconds',time.monotonic()-started,flush=True)
if __name__=='__main__':main()
