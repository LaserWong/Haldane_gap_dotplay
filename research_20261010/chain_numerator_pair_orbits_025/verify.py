"""Exact replay of saved pair-orbit contractions; no eigensolver or producer imports."""
import os
for x in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[x]='1'
import sys,json,math,resource,time
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
P=Path(__file__).resolve().parent; OLD=P.parent/'chain_numerator_krylov_025'
sys.path.insert(0,str(P.parent/'chain_frontier_review'));import independent_core as C
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(590,600));t=time.process_time()
r=json.loads((P/'pair_extension.json').read_text());d=r['H_integer_denominator'];assert d==144
unpack=lambda k:[(k>>(4*i))&15 for i in range(8)]
pack=lambda a:sum(x<<(4*i) for i,x in enumerate(a))
w=lambda k:math.prod(C.W[x] for x in unpack(k))
dot=lambda a,b:sum(x*b.get(k,0)*w(k) for k,x in a.items())
b=[]
for sep in range(5):
 v={0:1} if sep==0 else {}
 if sep:
  pairs={tuple(sorted((i,(i+sep)%8))) for i in range(8)}
  assert len(pairs)==(4 if sep==4 else 8)
  for i,j in pairs:
   for x,y,c in [(1,3,1),(2,2,-1),(3,1,1)]:
    a=[0]*8;a[i]=x;a[j]=y;v[pack(a)]=c
 b.append(v)
 assert v=={int(k):int(x) for k,x in r['bare_vectors'][sep]}
 for op in ['+','-']:
  out=defaultdict(F)
  for k,c in v.items():
   a=unpack(k)
   for i in range(8):
    for z in range(9):
     coef=C.OPS[0,op][z][a[i]]+C.OPS[1,op][z][a[i]]
     if coef:
      aa=a[:];aa[i]=z;out[pack(aa)]+=c*coef
  assert all(x==0 for x in out.values())
 assert {pack(unpack(k)[-1:]+unpack(k)[:-1]):x for k,x in v.items()}==v
 assert {pack(unpack(k)[::-1]):x*(-1)**sum(z in (1,2,3) for z in unpack(k)) for k,x in v.items()}==v
 assert all(sum(C.MAG[z] for z in unpack(k))==0 and sum(C.EX[z] for z in unpack(k))==(2 if sep else 0) for k in v)
images=[]
for v,saved in zip(b,r['bare_H_images_scaled']):
 out=defaultdict(F)
 for k,c in v.items():
  a=unpack(k);out[k]+=d*(-16+sum(C.EX[z] for z in a))*c
  for right in range(8):
   left=(right-1)%8
   for x,y,coef in C.K[a[left],a[right]]:
    aa=a[:];aa[left]=x;aa[right]=y;out[pack(aa)]+=d*F(1,4)*coef*c
 out={k:x for k,x in out.items() if x};assert out=={int(k):F(x) for k,x in saved};images.append(out)
need=set().union(*map(set,b),*map(set,images));large=[]
for j,(name,skip) in enumerate([('packed_input.txt',82),('packed_old_direction.txt',82),('full_image.txt',0),('second_image.txt',0)]):
 vals={}
 with (OLD/name).open() as f:
  for _ in range(skip):next(f)
  for line in f:
   k,x=map(int,line.split())
   if k in need:vals[k]=x
 assert vals=={int(k):int(x) for k,x in r['old_vector_values_on_needed_support'][j]};large.append(vals)
G=[[F(x) for x in row] for row in r['Gram']];H=[[F(x) for x in row] for row in r['H']];old=json.loads((OLD/'rayleigh_four.json').read_text())
for i in range(9):
 for j in range(9):
  if i<4 and j<4:gg=F(old['Gram'][i][j]);hh=F(old['H'][i][j])
  elif i>=4 and j>=4:gg=dot(b[i-4],b[j-4]);hh=dot(b[i-4],images[j-4])/d
  else:
   a,z=(i-4,j) if i>=4 else (j-4,i);gg=dot(b[a],large[z]);hh=dot(images[a],large[z])/d
  assert G[i][j]==gg and H[i][j]==hh
assert G==list(map(list,zip(*G))) and H==list(map(list,zip(*H)))
def pivots(M):
 M=[row[:] for row in M];p=[]
 for i in range(len(M)):
  x=M[i][i];assert x>0;p.append(x)
  for j in range(i+1,len(M)):
   for k in range(i+1,len(M)):M[j][k]-=M[j][i]*M[i][k]/x
 return p
assert pivots(G)==list(map(F,r['Gram_LDL_pivots']))
ix=[0,1,4,5,6,7,8];assert pivots([[G[i][j] for j in ix] for i in ix])==list(map(F,r['old_two_union_Gram_LDL_pivots']))
c=list(map(F,r['coefficients']));bil=lambda M:sum(c[i]*M[i][j]*c[j] for i in range(9) for j in range(9));q=bil(H)/bil(G);assert q==F(r['exact_rayleigh'])
rec=json.loads((P.parent/'chain_frontier_rank195/expanded_inputs.json').read_text())[0];rho=F(rec['large']['exact_rayleigh']);rho4=F(rec['small']['exact_rayleigh']);target=2*rho4+F(19,1250)
assert q-2*rho4==F(r['new_delta']) and rho-q==F(r['improvement_from_original']) and F(old['exact_rayleigh'])-q==F(r['increment_over_four_span'])
assert target==F(r['necessary_target_rayleigh']) and q>target
assert pivots([[H[i][j]-target*G[i][j] for j in range(9)] for i in range(9)])==list(map(F,r['span_target_LDL_pivots']))
print(json.dumps(dict(status='PASS',exact_checks='Five orbit symmetries and full Hamiltonian actions; streamed physical overlaps; complete 9D Gram/H; ranks; rational quotient; whole-span target exclusion',cpu_seconds=time.process_time()-t,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2))
