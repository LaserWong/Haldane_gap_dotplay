import os,resource
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
import json,ast,itertools,hashlib,time,sys
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import numpy as np
p=Path(__file__).resolve().parent;dest=Path(sys.argv[1]) if len(sys.argv)>1 else p;dest.mkdir(exist_ok=True);r=p.parent;s=r/'third_moment_review';ns=dict(F=F,np=np,Counter=Counter,defaultdict=defaultdict,itertools=itertools)
names={'mat','zero','graph','rebuild','rank_psd'};nodes=[x for x in ast.parse((s/'audit_matrices.py').read_text()).body if isinstance(x,ast.FunctionDef) and x.name in names];exec(compile(ast.Module(body=nodes,type_ignores=[]),'accepted_exact_rebuild','exec'),ns)
def mat(x):return np.array([[F(t) for t in row] for row in x],dtype=object)
def bil(c,M):return F(np.array(c,dtype=object)@M@np.array(c,dtype=object))
out=[]
for shape in ((4,2),(4,4)):
 tag='%dx%d'%shape;x=json.loads((p/f'matrix_{tag}.json').read_text());assert not x['partial'];geo=json.loads((s/'results'/f'geometry_{tag}.json').read_text());n=geo['orbits'];b=n+1;old=2*n+1;D=3*n+1
 mats={k:mat(x[k]) for k in ('PP','TT','CMCM','COMM')}
 for k,M in mats.items():assert np.array_equal(M,M.T),k
 for k in ('PP','TT','CMCM'):ns['rank_psd'](mats[k])
 ns['rank_psd'](mats['CMCM']+mats['COMM'])
 def assemble(g):
  z=ns['rebuild'](*shape,g,geo);G=z['G'];K=z['A'];J=np.zeros((D,D),dtype=object);J[:old,:]=z['Hmap'].T@K;J[:,:old]=J[:old,:].T
  S=mat(geo['S']);D2=S.T@np.diag([F(1,G[i,i]) for i in range(1,b)])@S
  V,W,X,Y,Z=[mat(geo[k]) for k in ('V','W','X','Y','Z')];t=g/2
  J[old:,old:]=16*V+36*W+t*(8*X+10*(Y+Y.T)+12*Z)+t*t*(D2+sum(mats.values()))
  assert np.array_equal(J,J.T);assert np.array_equal(J[:old,:old],z['J0'])
  return G,K,J
 G,K,J0=assemble(F(0));_,_,Jp=assemble(F(1));_,_,Jm=assemble(F(-1));lin=(Jp-Jm)/2;quad=(Jp+Jm)/2-J0
 # Exact coefficient identity at a physical, non-extraction coupling.
 g=F(21,200) if shape==(4,4) else F(1,10);G,K,J=assemble(g);assert np.array_equal(J,J0+g*lin+g*g*quad);ns['rank_psd'](J)
 if shape==(4,4):
  source=r/'bilayer_16d_4x4_residual_g0105';c=json.loads((source/'trial.json').read_text())['trial']['integer_coefficients'];raw=json.loads((source/'raw_residual.json').read_text());physical=json.loads((source/'physical_result.json').read_text());assert bil(c,J)/bil(c,G)==F(physical['second_moment'])
 else:
  source=r/'bilayer_complete_residual_8x4';vals=list(map(int,(source/'fixture_4x2_coefficients.txt').read_text().split()));den,hh=vals[:2];c=[17]+vals[2:2+n]+vals[2+n:2+2*n]+vals[2+2*n:2+3*n];raw=json.loads((source/'fixture_4x2_origin.json').read_text())
 cu=c[-n:]
 for k,key in [('PP','P_norm'),('TT','T_norm'),('CMCM','CM_norm'),('COMM','commutator_expectation')]:assert bil(cu,mats[k])==F(raw[key]),(tag,k)
 assert bil(cu,mats['CMCM']+mats['COMM'])==F(raw['q8_creation_norm'])
 serial=lambda M:[[str(z) for z in row] for row in M]
 (dest/f'complete_H2_polynomial_{tag}.json').write_text(json.dumps(dict(geometry=shape,dimension=D,gram=serial(G),H2_coefficients=[serial(t) for t in (J0,lin,quad)],coefficient_convention='Q², (QA+AQ)/2, A²/4; physical H=Q+(g/2)A'),indent=2)+'\n')
 out.append(dict(shape=shape,dimension=D,all_mixed_blocks_exact=True,old_J0_reproduced=True,complete_q8_PSD=True,saved_scalar_four_terms_exact=True,full_4x4_second_moment_exact=shape==(4,4)))
(dest/'fixture_checks.json').write_text(json.dumps(dict(status='PASS_PRODUCER_FIXTURES_PENDING_INDEPENDENT_AUDIT',results=out),indent=2)+'\n');print(out)
