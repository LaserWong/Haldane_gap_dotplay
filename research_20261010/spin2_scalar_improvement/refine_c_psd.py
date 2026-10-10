import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import resource
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
import json,mpmath as mp
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent
p=Path('/workspace/shared/haldane_optimization/upstream/extracted/cases/spin2_followup/inputs/trace_intervals.json')
rows=[r for r in json.loads(p.read_text())if r['beta']=='8']
(P/'copied_beta8_all_trace_intervals.json').write_text(json.dumps(rows,indent=2)+'\n')
d={(r['n'],r['twist']):(F(r['lower'])+F(r['upper']))/2 for r in rows}
old=json.loads((P.parent/'spin2_heat/seed_feasibility/exploratory_moment_inputs.json').read_text())[1]
seed=json.loads((P/'c_aware_psd_screen.json').read_text())
target={s:{}for s in ['I','O','R']}
for k in range(2,9):
 z,p,c=[d[k,t]for t in ['I','P','C']]
 target['I'][k]=(z+3*p+8*c)/12;target['O'][k]=(z+3*p-4*c)/12;target['R'][k]=(z-p)/4-target['O'][k]
fixed={'I':[F(103,100)],'O':[],'R':[F(51,50)]};items=[]
for s in target:
 for x in seed['sectors'][s]['nodes']:items.append((s,F(str(x))))
 items.extend([(s,F(1,100000)),(s,F(-1,100000))])
A=[];b=[]
for s in target:
 for k in range(2,9):
  A.append([x**k if t==s else F(0)for t,x in items]);b.append(target[s][k]-sum(x**k for x in fixed[s]))
for k in [9,10]:
 for s,co in [('J',{'I':1,'O':2,'R':0}),('N',{'I':0,'O':1,'R':1})]:
  A.append([co[t]*x**k for t,x in items]);b.append(F(str(old['moments'][s][str(k)]))-sum(co[t]*sum(x**k for x in fixed[t])for t in target))
assert len(A)==len(items)==25
mp.mp.dps=100;mm=lambda q:mp.mpf(q.numerator)/q.denominator
w=mp.lu_solve(mp.matrix([[mm(x)for x in row]for row in A]),mp.matrix(list(map(mm,b))))
wq=[F(mp.nstr(v,75))for v in w]
print('minweight',float(min(wq)),flush=True)
assert min(wq)>0
errors=[abs(sum(c*x for c,x in zip(row,wq))-bb)for row,bb in zip(A,b)]
assert max(errors)<F(1,10**50)
res={'status':'EXACT_RATIONAL_CHECKED_POSITIVE_MEASURE_RELAXATION','fixed_unit_atoms':{s:[str(x)for x in fixed[s]]for s in fixed},'residual_integer_multiplicity':False,'max_moment_error_upper':'1/10^50','moment_scope':'I/P/C orders2..8 and I/P orders9,10 at beta8','items':[{'sector':s,'node':str(x),'weight':str(v)}for (s,x),v in zip(items,wq)],'limits':['Residual weights are positive rational, not integer multiplicities.','No all-length trace positivity or cross-temperature consistency claim is made.']}
(P/'c_aware_psd_rational_witness.json').write_text(json.dumps(res,indent=2)+'\n')
print('maximum exact residual display',float(max(errors)))
