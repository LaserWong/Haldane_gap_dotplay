"""Inductive exact block verification without importing the construction script."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import sys,json,math,time,resource
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
sys.set_int_max_str_digits(0);P=Path(__file__).resolve().parent;O=P.parent/'chain_numerator_krylov_025';B=P.parent/'chain_numerator_pair_orbits_025'
sys.path.insert(0,str(P.parent/'chain_frontier_review'));import independent_core as C
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(590,600));start=time.process_time()
parse=lambda a:{int(k):int(x) for k,x in a};weights={}
def wt(k):
 if k not in weights:weights[k]=math.prod(C.W[(k>>(4*i))&15] for i in range(8))
 return weights[k]
def dot(a,b):
 if len(a)>len(b):a,b=b,a
 return sum(x*b.get(k,0)*wt(k) for k,x in a.items())
def read(need):
 out=[]
 for name,skip in [('packed_input.txt',82),('packed_old_direction.txt',82),('full_image.txt',0),('second_image.txt',0)]:
  v={}
  with (O/name).open() as f:
   for _ in range(skip):next(f)
   for line in f:
    k,x=map(int,line.split())
    if k in need:v[k]=x
  out.append(v)
 return out
kernel={key:[(a,b,int(36*c)) for a,b,c in row] for key,row in C.K.items()}
def action(v):
 out=defaultdict(int)
 for key,x in v.items():
  out[key]+=144*(-16+sum(C.EX[(key>>(4*i))&15] for i in range(8)))*x
  for i in range(8):
   j=(i-1)%8;a=(key>>(4*j))&15;b=(key>>(4*i))&15;mask=~((15<<(4*i))|(15<<(4*j)))
   for aa,bb,c in kernel[a,b]:out[(key&mask)|(aa<<(4*j))|(bb<<(4*i))]+=c*x
 return {k:x for k,x in out.items() if x}
def pivot(M):
 A=[row[:] for row in M];out=[]
 for i in range(len(A)):
  x=A[i][i];out.append(x)
  if not x:return out
  for j in range(i+1,len(A)):
   for k in range(i+1,len(A)):A[j][k]-=A[j][i]*A[i][k]/x
 return out
previous=json.loads((B/'pair_extension.json').read_text());reports=[]
for level in [1,2]:
 r=json.loads((P/f'block_{level}.json').read_text());vs=list(map(parse,r['small_vectors']));front=list(map(parse,previous['bare_H_images_scaled'] if level==1 else previous['next_frontier']));oldvs=list(map(parse,previous['bare_vectors'] if level==1 else previous['small_vectors']));oldn=len(previous['Gram']);n=len(r['Gram']);G=[[F(x) for x in row] for row in previous['Gram']];H=[[F(x) for x in row] for row in previous['H']];cands=[]
 for v in front:
  z=math.gcd(*v.values());cands.append({k:x//z for k,x in v.items()})
 large=read(set().union(*map(set,cands)));selected=[]
 for i,v in enumerate(cands):
  row=[F(dot(v,z)) for z in large+oldvs];trial=[G[j]+[row[j]] for j in range(len(G))]+[row+[F(dot(v,v))]];pv=pivot(trial);ind=len(pv)==len(trial) and pv[-1]>0
  assert r['rank_tests'][i]==dict(candidate=i,support=len(v),independent=ind,last_Gram_pivot=str(pv[-1]))
  if ind:G=trial;oldvs.append(v);selected.append(v)
 assert oldvs==vs and len(G)==n and n<=32
 images=list(map(parse,r['next_frontier']));assert len(images)==len(selected)
 for v,im in zip(selected,images):assert action(v)==im
 need=set().union(*map(set,images));large=read(need);savedH=[[F(x) for x in row] for row in r['H']]
 for i in range(oldn):
  for j in range(oldn):assert savedH[i][j]==H[i][j]
 for i,im in enumerate(images,oldn):
  for j,v in enumerate(large+vs):assert savedH[i][j]==savedH[j][i]==F(dot(im,v),144)
 assert G==[[F(x) for x in row] for row in r['Gram']];assert pivot(G)==list(map(F,r['Gram_LDL_pivots'])) and min(pivot(G))>0
 c=list(map(F,r['coefficients']));bil=lambda M:sum(c[i]*M[i][j]*c[j] for i in range(n) for j in range(n));q=bil(savedH)/bil(G);assert q==F(r['exact_rayleigh'])
 rec=json.loads((P.parent/'chain_frontier_rank195/expanded_inputs.json').read_text())[0];rho=F(rec['large']['exact_rayleigh']);rho4=F(rec['small']['exact_rayleigh']);target=2*rho4+F(19,1250)
 assert target==F(r['necessary_target']) and q>target and q-2*rho4==F(r['new_delta']) and rho-q==F(r['improvement'])
 pv=pivot([[savedH[i][j]-target*G[i][j] for j in range(n)] for i in range(n)]);assert pv==list(map(F,r['span_target_LDL_pivots'])) and min(pv)>0
 reports.append(dict(level=level,rank=n,independent_directions=len(selected),full_new_images_verified=True,Gram_and_H_verified=True,whole_span_target_excluded=True));previous=r
print(json.dumps(dict(status='PASS',blocks=reports,cpu_seconds=time.process_time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2))
