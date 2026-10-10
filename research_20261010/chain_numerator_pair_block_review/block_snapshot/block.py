import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import sys,json,math,time,resource
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import numpy as np
from scipy.linalg import eigh
sys.set_int_max_str_digits(0)
P=Path(__file__).resolve().parent;O=P.parent/'chain_numerator_krylov_025';B=P.parent/'chain_numerator_pair_orbits_025'
sys.path.insert(0,str(P.parent/'chain_frontier_review'));import independent_core as C
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(590,600));START=time.process_time();level=int(sys.argv[1]);den=144
r=json.loads((B/'pair_extension.json').read_text()) if level==1 else json.loads((P/f'block_{level-1}.json').read_text())
parse=lambda a:{int(k):int(x) for k,x in a}
serialize=lambda a:[[k,str(x)] for k,x in sorted(a.items())]
vs=list(map(parse,r['bare_vectors'] if level==1 else r['small_vectors']));frontier=list(map(parse,r['bare_H_images_scaled'])) if level==1 else list(map(parse,r['next_frontier']))
G=[[F(x) for x in row] for row in r['Gram']];H=[[F(x) for x in row] for row in r['H']]
weights={}
def wt(k):
 if k not in weights:weights[k]=math.prod(C.W[(k>>(4*i))&15] for i in range(8))
 return weights[k]
def dot(a,b):
 if len(a)>len(b):a,b=b,a
 return sum(x*b.get(k,0)*wt(k) for k,x in a.items())
def primitive(v):
 z=math.gcd(*v.values());return {k:x//z for k,x in v.items()}
kernel={key:[(a,b,int(den*F(1,4)*c)) for a,b,c in row] for key,row in C.K.items()}
def action(v):
 out=defaultdict(int)
 for ix,(k,x) in enumerate(v.items()):
  out[k]+=den*(-16+sum(C.EX[(k>>(4*i))&15] for i in range(8)))*x
  for right in range(8):
   left=(right+7)%8;ls,rs=4*left,4*right;mask=~((15<<ls)|(15<<rs))
   for a,b,c in kernel[(k>>ls)&15,(k>>rs)&15]:out[(k&mask)|(a<<ls)|(b<<rs)]+=c*x
  if ix%2000==0 and time.process_time()-START>540:raise RuntimeError('budget stop')
 return {k:x for k,x in out.items() if x}
def ldl(M,positive=True):
 n=len(M);L=[[F(i==j) for j in range(n)] for i in range(n)];D=[]
 for i in range(n):
  d=M[i][i]-sum(L[i][k]**2*D[k] for k in range(i));D.append(d)
  if d==0 or (positive and d<0):return L,D
  for j in range(i+1,n):L[j][i]=(M[j][i]-sum(L[j][k]*L[i][k]*D[k] for k in range(i)))/d
 return L,D
# Compute exact physical overlaps of all candidates with original4 vectors by streaming.
candidates=list(map(primitive,frontier));need=set().union(*map(set,candidates));large=[]
def read_old(needed):
 ans=[]
 for name,skip in [('packed_input.txt',82),('packed_old_direction.txt',82),('full_image.txt',0),('second_image.txt',0)]:
  vals={}
  with (O/name).open() as f:
   for _ in range(skip):next(f)
   for line in f:
    k,x=map(int,line.split())
    if k in needed:vals[k]=x
  ans.append(vals)
 return ans
large=read_old(need);selected=[];ranklog=[]
for ci,v in enumerate(candidates):
 row=list(map(lambda z:F(dot(v,z)),large+vs));q=F(dot(v,v));trial=[G[i]+[row[i]] for i in range(len(G))]+[row+[q]];_,D=ldl(trial);ind=len(D)==len(trial) and D[-1]>0
 ranklog.append(dict(candidate=ci,support=len(v),independent=ind,last_Gram_pivot=str(D[-1])))
 if ind:
  assert len(G)<32;G=trial;vs.append(v);selected.append(v)
print('SELECT',level,'rank',len(G),'new',len(selected),'supports',[len(x) for x in selected],flush=True)
images=[]
for j,v in enumerate(selected):
 t=time.process_time();im=action(v);images.append(im);print('IMAGE',j,len(im),'cpu',time.process_time()-t,flush=True)
need=set().union(*map(set,images)) if images else set();large=read_old(need);oldn=len(H);n=len(G)
H=[row+[F(0)]*(n-oldn) for row in H]+[[F(0)]*n for _ in selected]
for i,im in enumerate(images,oldn):
 for j,v in enumerate(large+vs):H[i][j]=H[j][i]=F(dot(im,v),den)
assert H==list(map(list,zip(*H)))
L,D=ldl(G);assert len(D)==n and min(D)>0
Li=[[F(0)]*n for _ in range(n)]
for j in range(n):
 for i in range(n):Li[i][j]=F(i==j)-sum(L[i][k]*Li[k][j] for k in range(i))
Q=list(map(list,zip(*Li)));rec=json.loads((P.parent/'chain_frontier_rank195/expanded_inputs.json').read_text())[0];rho=F(rec['large']['exact_rayleigh']);rho4=F(rec['small']['exact_rayleigh']);target=2*rho4+F(19,1250)
K=[[H[i][j]-rho*G[i][j] for j in range(n)] for i in range(n)]
KQ=[[sum(K[i][j]*Q[j][a] for j in range(n)) for a in range(n)] for i in range(n)];KK=[[sum(Q[i][a]*KQ[i][b] for i in range(n)) for b in range(n)] for a in range(n)]
sc=np.sqrt(list(map(float,D)));nf=np.array(KK,dtype=float)/np.outer(sc,sc);assert np.max(abs(nf-nf.T))<1e-8
es,evec=eigh(nf);aa=evec[:,0]/sc;cf=np.array(Q,dtype=float)@aa
scale=[max(1,math.isqrt(int(G[i][i]))) for i in range(n)];cc=[cf[i]*scale[i] for i in range(n)];mx=max(map(abs,cc));c=[F(round(x/mx*10**14),z) for x,z in zip(cc,scale)]
bil=lambda M:sum(c[i]*M[i][j]*c[j] for i in range(n) for j in range(n));ray=bil(H)/bil(G);_,td=ldl([[H[i][j]-target*G[i][j] for j in range(n)] for i in range(n)],False);excluded=len(td)==n and min(td)>0
out=dict(level=level,trial_rank=n,previous_rank=oldn,new_rank=n-oldn,rank_tests=ranklog,small_vectors=list(map(serialize,vs)),next_frontier=list(map(serialize,images)),Gram=[[str(x) for x in row] for row in G],H=[[str(x) for x in row] for row in H],Gram_LDL_pivots=list(map(str,D)),coefficients=list(map(str,c)),exact_rayleigh=str(ray),new_delta=str(ray-2*rho4),improvement=str(rho-ray),gain_display=float(rho-ray),delta_display=float(ray-2*rho4),increment_display=float(F(r['exact_rayleigh'])-ray),necessary_target=str(target),span_target_LDL_pivots=list(map(str,td)),span_excluded=excluded,meets_necessary_target=ray<target,cpu_seconds=time.process_time()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(P/f'block_{level}.json').write_text(json.dumps(out,indent=2));print('RESULT',level,n,'gain',out['gain_display'],'delta',out['delta_display'],'increment',out['increment_display'],'excluded',excluded,'cpu',out['cpu_seconds'],'rss',out['peak_rss_kib'],flush=True)
