"""Small scalar moment fit; no Hamiltonian or transfer matrix is diagonalized."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import resource
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
import json,mpmath as mp,numpy as np
from scipy.linalg import qr
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent
source=Path('/workspace/shared/haldane_optimization/upstream/extracted/cases/spin2_followup/inputs/trace_intervals.json')
trace_rows=[r for r in json.loads(source.read_text()) if r['beta']=='8' and r['n'] in range(2,9) and r['twist'] in ['I','P']]
(P/'copied_beta8_lower_trace_intervals.json').write_text(json.dumps(trace_rows,indent=2)+'\n')
d={(r['n'],r['twist']):(F(r['lower'])+F(r['upper']))/2 for r in trace_rows}
old=json.loads((P.parent/'spin2_heat/seed_feasibility/exploratory_moment_inputs.json').read_text())[1]
rows=json.loads((P/'positive_witnesses.json').read_text())
mp.mp.dps=90
out=[]
for row in rows:
 sec=row['sector'];target={}
 for k in range(2,11):
  target[k]=((d[k,'I']+3*d[k,'P'])/4 if sec=='J' else (d[k,'I']-d[k,'P'])/4) if k<=8 else F(str(old['moments'][sec][str(k)]))
 n=row['counts'];xs=list(map(F,row['nodes']));t=F(1,2**17)
 a=target[2]-sum(nn*x*x for nn,x in zip(n,xs));b=target[3]-sum(nn*x*x*x for nn,x in zip(n,xs))
 np_=round((a/t**2+b/t**3)/2);nm=round((a/t**2-b/t**3)/2)
 assert min(np_,nm)>0
 n=n+[np_,nm];xs=xs+[t,-t]
 # Select a nonsingular nine-column moment Jacobian, always keeping both tiny tails.
 free=list(range(1,len(xs)-2));tail=[len(xs)-2,len(xs)-1]
 jac=np.array([[n[j]*k*float(xs[j])**(k-1)/max(float(abs(target[k])),1) for j in free]for k in range(4,11)])
 piv=qr(jac,pivoting=True)[2];idx=[free[j]for j in piv[:7]]+tail
 mm=lambda z:mp.mpf(z.numerator)/z.denominator
 yy=list(map(mm,xs));ts={k:mm(v)for k,v in target.items()}
 scales={k:max(abs(ts[k]),mp.mpf(1))for k in ts}
 unit=[mp.mpf(1)]*7+[mm(t)]*2
 start=[yy[j]/u for j,u in zip(idx,unit)]
 def equations(*vv):
  xx=yy.copy()
  for j,u,v in zip(idx,unit,vv):xx[j]=u*v
  return [(sum(nn*x**k for nn,x in zip(n,xx))-ts[k])/scales[k]for k in range(2,11)]
 root=mp.findroot(equations,tuple(start),tol=mp.mpf('1e-75'),maxsteps=40)
 for j,u,v in zip(idx,unit,root):yy[j]=u*v
 nodes=[mp.nstr(x,65)for x in yy]
 xx=list(map(F,nodes))
 errs={k:sum(nn*x**k for nn,x in zip(n,xx))-target[k]for k in target}
 assert max(map(abs,errs.values()))<F(1,10**48)
 assert max(abs(x)for x in xx[1:])<1
 rec={'beta':8,'a':'5951/1250','sector':sec,'counts':n,'nodes':nodes,'targets':{str(k):str(v)for k,v in target.items()},'moment_absolute_error_upper':'1/10^48','free_indices':idx}
 out.append(rec);print(sec,'unit atoms',sum(n),'max_error',float(max(map(abs,errs.values()))),flush=True)
(P/'full_integer_witnesses.json').write_text(json.dumps(out,indent=2)+'\n')
