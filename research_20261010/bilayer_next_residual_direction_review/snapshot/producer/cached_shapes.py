import os,resource
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
from pathlib import Path
from fractions import Fraction as F
import json,numpy as np
p=Path(__file__).resolve().parent;r=p.parent
m=lambda x:np.array([[F(v) for v in row] for row in x],dtype=object)
geo=json.loads((r/'third_moment_review/results/geometry_8x4.json').read_text());old=json.loads((r/'bilayer_complete_H2_8x4/matrix_8x4.json').read_text());new=json.loads((r/'bilayer_complete_split_H2_8x4/matrix_8x4.json').read_text());FF,S,V,W,X,Y,Z=[m(geo[k]) for k in ('F','S','V','W','X','Y','Z')];r4,b4,r6,b6,m6=[m(new[k]) for k in ('R4R4','R4CM','R6R6','R6M6','M6M6')];cm=m(old['CMCM']);q8=cm+m(old['COMM']);G4=np.block([[FF,S],[S.T,V]])
def solve(A,v):
 A=[[F(z) for z in row] for row in A];v=list(map(F,v));n=len(v)
 for k in range(n):
  a=A[k][k];assert a>0
  for i in range(k+1,n):
   f=A[i][k]/a
   for j in range(k+1,n):A[i][j]-=f*A[k][j]
   v[i]-=f*v[k]
 x=[F(0)]*n
 for i in range(n-1,-1,-1):x[i]=(v[i]-sum(A[i][j]*x[j] for j in range(i+1,n)))/A[i][i]
 return np.array(x,dtype=object)
out=[]
for w in json.loads((r/'bilayer_split_pencil_optimization/result.json').read_text())['results']:
 c=np.array(list(map(F,w['integer_coefficients'])),dtype=object);cr=c[29:43];ct=c[43:57];norm=F(w['norm']);t=F(w['g'])/2;hp=np.concatenate([V@cr+W@ct,X@cr+Y@ct]);ht=Y.T@cr+Z@ct
 pn=F(cr@r4@cr+2*cr@b4@ct+ct@cm@ct);tn=F(cr@r6@cr+2*cr@b6@ct+ct@m6@ct);ps=pn-F(hp@solve(G4,hp));ts=tn-F(ht@solve(W,ht));assert min(ps,ts)>0
 parts={'q4_outside57':t*t*ps/norm,'q6_outside57':t*t*ts/norm,'q8_outside57':t*t*F(ct@q8@ct)/norm};v=F(w['variance']);parts['inside57_residual']=v-sum(parts.values());assert min(parts.values())>=0
 out.append(dict(g=w['g'],trial_source_dimension=57,P_integer_R_coefficients=list(map(str,cr)),P_integer_M_coefficients=list(map(str,ct)),T_integer_R_coefficients=list(map(str,cr)),T_integer_M_coefficients=list(map(str,ct)),P_schur_norm=str(ps),T_schur_norm=str(ts),T_only_dimension=58,P_and_T_dimension=59,residual_parts={k:str(z) for k,z in parts.items()},residual_fractions={k:float(z/v) for k,z in parts.items()},scope='Exact cached Gram/rank and residual-sector algebra only; no new H or H2 contractions for proposed shapes'))
(p/'cached_shapes.json').write_text(json.dumps(dict(status='EXACT_CACHED_POSITIVE_SCHUR_NORMS',results=out),indent=2)+'\n');print([(x['g'],x['residual_fractions']) for x in out])
