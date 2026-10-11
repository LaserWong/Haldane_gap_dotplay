import os,resource
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
import ast,json,itertools,math,time
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import numpy as np
p=Path(__file__).resolve().parent;r=p.parent;s=r/'third_moment_review';ns=dict(F=F,np=np,Counter=Counter,defaultdict=defaultdict,itertools=itertools)
names={'mat','zero','graph','rebuild','rank_psd'};nodes=[x for x in ast.parse((s/'audit_matrices.py').read_text()).body if isinstance(x,ast.FunctionDef) and x.name in names];exec(compile(ast.Module(body=nodes,type_ignores=[]),'cached_matrices','exec'),ns)
def mat(x):return np.array([[F(t) for t in row] for row in x],dtype=object)
g=F(11,100);geo=json.loads((s/'results/geometry_8x4.json').read_text());z=ns['rebuild'](8,4,g,geo);data=json.loads((r/'bilayer_complete_H2_8x4/complete_H2_polynomial_8x4.json').read_text());J=sum(g**i*mat(M) for i,M in enumerate(data['H2_coefficients']));K=z['A'];G=z['G'];w=next(x for x in json.loads((r/'bilayer_residual_pencil_optimization/result.json').read_text())['results'] if x['shape']==[8,4] and F(x['g'])==g);a=F(w['cutoff']);rho=F(w['rayleigh']);out=[]
for t in json.loads((p/'result.json').read_text())['results'][0]['hypothetical_ground32_targets']:
 ell=F(t['target_ground32_lower']);M=J-(a+ell)*K+a*ell*G;selected,piv=ns['rank_psd'](M);assert len(selected)==43
 out.append(dict(beta=t['beta'],target_lower=str(ell),positive_LDL_pivots=piv,dimension=43,positive_definite=True,scope='Chosen sufficient target impossible for any current43D Temple-pencil witness at this fixed cutoff; not an all-method obstruction',variance_budget_for_saved_endpoint_vector=str((rho-ell)*(a-rho)),current_variance=w['variance']))
(p/'target_limit.json').write_text(json.dumps(dict(status='EXACT_CONDITIONAL_LDL_LIMIT_PENDING_FULL_MATRIX_REVIEW',results=out),indent=2)+'\n');print([(t['beta'],t['positive_definite'],float(F(t['variance_budget_for_saved_endpoint_vector']))) for t in out])
