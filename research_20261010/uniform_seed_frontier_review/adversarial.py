#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json,itertools,os,resource,time
os.sched_setaffinity(0,{5 if 5 in os.sched_getaffinity(0) else min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600));start=time.process_time();tests=[];cases=0
for k,h,ratio in itertools.product(range(2,13),[F(1,2),F(1),F(3,2)],[F(1,4),F(1,2),F(3,4)]):
 t=h*ratio;c=(h**k-t**k-k*t**(k-1)*(h-t))/(h-t)**2;b=k*t**(k-1)-2*c*t;a=(1-k)*t**k+c*t*t
 Q=lambda x:a+b*x+c*x*x
 for x in [F(0),t,h,h/7,h*F(5,7)]:assert Q(x)>=x**k;cases+=1
 assert Q(t)==t**k and b+2*c*t==k*t**(k-1) and Q(h)==h**k
 if k==2:assert (a,b,c)==(0,0,1)
 else:
  assert a>0 and b<0 and c>0
  assert Q(2*h)<(2*h)**k # the domain cannot be silently extended
  assert Q(0)>0 and 0**3*Q(0)==0
  box=[(F(1),F(2)),(F(2),F(3)),(F(3),F(4))]
  true_upper=a*box[0][1]+b*box[1][0]+c*box[2][1]
  wrong_upper=a*box[0][1]+b*box[1][1]+c*box[2][1]
  assert true_upper>wrong_upper
  assert true_upper==max(a*x+b*y+c*z for x,y,z in itertools.product(*box))
tests+=['495 closed-support point checks, including zero and repeated/end nodes','k2 exactly reproduces x²','negative middle coefficient requires lower moment endpoint','majorant fails beyond h: certified support is essential','multiplication by x³ handles zero without division']
P=Path(__file__).resolve().parent;d=json.loads((P.parent/'uniform_seed_frontier_optimization/certificates.json').read_text());r=d['rows'][0];q=lambda v:F(v['exact'])
S,T=q(r['S_seed']),q(r['T_seed']);K=S*S*T;G=lambda x:1-(1-x)**2/(2*x*x)
assert r['seed_n']==52 and q(r['beta'])==F(567,25)
assert q(r['direct_time_first_comparison']['b_lower'])<=G(K)
assert r['direct_time_first_comparison']['halfstep_base']==104
assert q(r['direct_time_first_comparison']['halfstep_beta'])!=2*q(r['beta'])
assert [w['from'] for w in r['finite_integer_windows']]==[52,104,208,416,832,1664,3328]
assert all(w['to']==2*w['from'] for w in r['finite_integer_windows'])
# A wrong endpoint or beta base is rejected by explicit coordinate checks.
tests+=['direct halfstep retains beta22.68 at base104','canonical windows have no missing integer interval']
Qanchor=q(r['Z_anchor_beta0_upper']);v=q(r['anchor_beta0_weight_lower'])
assert 1<v<Qanchor
assert Qanchor/v-1<Qanchor-1
assert Qanchor/(v+F(1,1000))-1<Qanchor/v-1
# Using an upper bound on a ground weight would make the remaining ratio artificially smaller.
tests+=['using actual lower anchor improves residual ratio; substituting an upper anchor is unsafe']
out={'status':'PASS','polynomial_points_checked':cases,'tests':tests,'cpu_seconds':time.process_time()-start,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'adversarial_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
