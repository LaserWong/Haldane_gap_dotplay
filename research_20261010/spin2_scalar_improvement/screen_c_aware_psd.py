"""Bounded finite-support moment relaxation, not an integer-spectrum certificate."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import resource
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
import numpy as np,json
from scipy.optimize import linprog
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent
src=Path('/workspace/shared/haldane_optimization/upstream/extracted/cases/spin2_followup/inputs/trace_intervals.json')
r=[r for r in json.loads(src.read_text()) if r['beta']=='8']
d={(q['n'],q['twist']):(F(q['lower'])+F(q['upper']))/2 for q in r}
o=json.loads((P.parent/'spin2_heat/seed_feasibility/exploratory_moment_inputs.json').read_text())[1]
target={s:{}for s in ['I','O','R']}
for k in range(4,9):
 z,p,c=[float(d[k,t])for t in ['I','P','C']]
 target['I'][k]=(z+3*p+8*c)/12
 target['O'][k]=(z+3*p-4*c)/12
 target['R'][k]=(z-p)/4-target['O'][k]
nodes=np.r_[np.linspace(-.99,-.06,220),np.linspace(.06,.99,220)];m=len(nodes)
fixed={'I':[1.03],'O':[],'R':[1.02]};A=[];bb=[];labels=[]
for si,s in enumerate(target):
 for k in range(4,9):
  a=np.zeros(3*m);a[si*m:(si+1)*m]=nodes**(k-4)
  A.append(a);bb.append(target[s][k]-sum(x**k for x in fixed[s]));labels.append(f'{s}{k}')
for k in [9,10]:
 for s,coef in [('J',[1,2,0]),('N',[0,1,1])]:
  A.append(np.concatenate([c*nodes**(k-4) for c in coef]));bb.append(o['moments'][s][str(k)]-sum(c*sum(x**k for x in fixed[t])for c,t in zip(coef,target)));labels.append(f'{s}{k}')
A=np.array(A);bb=np.array(bb);scale=np.maximum(abs(bb),1)
lp=linprog(np.tile(1/nodes**4,3),A_eq=A/scale[:,None],b_eq=bb/scale,bounds=(0,None),method='highs',options={'threads':1,'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
result={'status':'EXPLORATORY_FINITE_SUPPORT_PSD_RELAXATION','success':lp.success,'message':lp.message,'fixed_unit_atoms':fixed,'moment_scope':'All I/P/C moments 4..8 and I/P moments 9,10; I spin0, R spin1, O spin2','unit_multiplicity_on_residual':False}
if lp.success:
 result['max_abs_residual']=float(max(abs(A@lp.x-bb)))
 result['sectors']={}
 for si,s in enumerate(target):
  weights=lp.x[si*m:(si+1)*m]/nodes**4;ix=np.flatnonzero(weights>1e-8)
  result['sectors'][s]={'nodes':nodes[ix].tolist(),'weights':weights[ix].tolist()}
(P/'c_aware_psd_screen.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
