import os,resource
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
import ast,json,itertools,sys
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import numpy as np
p=Path(__file__).resolve().parent;r=p.parent;dest=Path(sys.argv[1]) if len(sys.argv)>1 else p;dest.mkdir(exist_ok=True);s=r/'third_moment_review';ns=dict(F=F,np=np,Counter=Counter,defaultdict=defaultdict,itertools=itertools);names={'mat','zero','graph','rebuild','rank_psd'};nodes=[x for x in ast.parse((s/'audit_matrices.py').read_text()).body if isinstance(x,ast.FunctionDef) and x.name in names];exec(compile(ast.Module(body=nodes,type_ignores=[]),'accepted_cached','exec'),ns)
def mat(x):return np.array([[F(t) for t in row] for row in x],dtype=object)
def serial(M):return [[str(x) for x in row] for row in M]
checks=[]
for tag,newfile,oldfile in [('4x4','matrix_4x4.json','matrix_4x4.json'),('8x4','sample_8x4.json','sample_8x4.json')]:
 new=json.loads((p/newfile).read_text());old=json.loads((r/'bilayer_residual_pencil_fixture'/oldfile).read_text());a,b,c,d,e=[mat(new[k]) for k in ('R4R4','R4CM','R6R6','R6M6','M6M6')];assert np.array_equal(a+b+b.T+mat(old['CMCM']),mat(old['PP']));assert np.array_equal(c+d+d.T+e,mat(old['TT']));checks.append(dict(geometry=tag,partial=new['partial'],PP_and_TT_recombination_exact=True))
shape=(4,4);tag='4x4';geo=json.loads((s/'results/geometry_4x4.json').read_text());new=json.loads((p/'matrix_4x4.json').read_text());old=json.loads((r/'bilayer_residual_pencil_fixture/matrix_4x4.json').read_text());n=geo['orbits'];b=n+1;D=4*n+1;od=3*n+1;initial=2*n+1
z=ns['rebuild'](*shape,F(0),geo);o=ns['rebuild'](*shape,F(1),geo);G=np.zeros((D,D),dtype=object);A=G.copy();G[:b,:b]=z['G'][:b,:b];A[:b,:b]=2*(o['A']-z['A'])[:b,:b]
for i in range(n):
 for j in range(n):
  f,ss,v,w,x,y,zz=[F(geo[k][i][j]) for k in ('F','S','V','W','X','Y','Z')];li,ri,mi=b+i,b+n+i,b+2*n+i;lj,rj,mj=b+j,b+n+j,b+2*n+j
  G[li,lj]=f;G[li,rj]=G[rj,li]=ss;G[ri,rj]=v;G[mi,mj]=w;A[1+i,lj]=A[lj,1+i]=f;A[1+i,rj]=A[rj,1+i]=ss;A[li,lj]=ss;A[li,rj]=A[rj,li]=v;A[li,mj]=A[mj,li]=w;A[ri,rj]=x;A[ri,mj]=A[mj,ri]=y;A[mi,mj]=zz
q=[0]+[2]*n+[4]*(2*n)+[6]*n;Q=np.array([[G[i,j]*q[j] for j in range(D)] for i in range(D)],dtype=object);embed=np.zeros((D,od),dtype=object);embed[:od,:]=np.eye(od,dtype=object);embed[od:,initial:]=np.eye(n,dtype=object);assert len(ns['rank_psd'](G)[0])==D
S,V,W,X,Y,Z=[mat(geo[k]) for k in ('S','V','W','X','Y','Z')];D2=S.T@np.diag([F(1,G[i,i]) for i in range(1,b)])@S;a,b4,c,d,e=[mat(new[k]) for k in ('R4R4','R4CM','R6R6','R6M6','M6M6')];cm=mat(old['CMCM']);q8=cm+mat(old['COMM']);aRR=D2+a+c;aRM=b4+d;aMM=cm+e+q8
oldpoly=json.loads((r/'bilayer_residual_pencil_fixture/complete_H2_polynomial_4x4.json').read_text());oldcs=list(map(mat,oldpoly['H2_coefficients']))
def assembly(g):
 K=Q+g*A/2;orig=ns['rebuild'](*shape,g,geo);J=np.zeros((D,D),dtype=object);J[:initial,:]=(embed@orig['Hmap']).T@K;J[:,:initial]=J[:initial,:].T;t=g/2;ri=slice(initial,initial+n);mi=slice(initial+n,D);J[ri,ri]=16*V+8*t*X+t*t*aRR;J[ri,mi]=10*t*Y+t*t*aRM;J[mi,ri]=J[ri,mi].T;J[mi,mi]=36*W+12*t*Z+t*t*aMM
 assert np.array_equal(J,J.T) and np.array_equal(embed.T@G@embed,orig['G']) and np.array_equal(embed.T@K@embed,orig['A']);assert np.array_equal(embed.T@J@embed,sum(g**i*x for i,x in enumerate(oldcs)))
 return K,J
_,J0=assembly(F(0));_,Jp=assembly(F(1));_,Jm=assembly(F(-1));cs=[J0,(Jp-Jm)/2,(Jp+Jm)/2-J0];K,J=assembly(F(21,200));assert np.array_equal(J,sum(F(21,200)**i*x for i,x in enumerate(cs)));ns['rank_psd'](J);ns['rank_psd'](np.block([[G,K],[K,J]]));checks.append(dict(geometry=tag,trial_dimension=D,full_Hilbert_dimension=str(4**16),full_G_K_J_compression_exact=True,full_unprojected_residual_PSD=True,q8_MM_only=True))
(dest/'complete_H2_polynomial_4x4.json').write_text(json.dumps(dict(geometry=shape,dimension=D,gram=serial(G),H_coefficients=[serial(Q),serial(A/2)],H2_coefficients=[serial(M) for M in cs]),indent=2)+'\n');(dest/'checks.json').write_text(json.dumps(dict(status='PRODUCER_SPLIT_FIXTURE_PASSES_PENDING_INDEPENDENT_REVIEW',checks=checks),indent=2)+'\n');print(checks)
