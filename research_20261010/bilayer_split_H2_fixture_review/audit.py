import os,resource
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(30,30));resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2))
from fractions import Fraction as F
from pathlib import Path
from collections import Counter,defaultdict
import json,hashlib,itertools,time,math
H=Path(__file__).resolve().parent;S=H/'snapshot';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def mat(x):return [[F(v) for v in r] for r in x]
def zero(n,m=None):return [[F(0)]*(n if m is None else m) for _ in range(n)]
def tr(a):return list(map(list,zip(*a)))
def mul(a,b):
 bt=tr(b);return [[sum(x*y for x,y in zip(row,col)) for col in bt] for row in a]
def add(*args):return [[sum(a[i][j] for a in args) for j in range(len(args[0][0]))] for i in range(len(args[0]))]
def scale(a,s):return [[x*s for x in r] for r in a]
def psd(a,strict=False):
 assert a==tr(a);a=mat(a);piv=[]
 for j in range(len(a)):
  p=a[j][j];assert p>0 if strict else p>=0;piv.append(str(p))
  if not p:assert all(a[i][j]==0 for i in range(j+1,len(a)));continue
  for i in range(j+1,len(a)):
   for k in range(i,len(a)):a[k][i]=a[i][k]=a[i][k]-a[i][j]*a[k][j]/p
 return piv

def main():
 t=time.monotonic();pm=S/'PRODUCER_MANIFEST.json';assert sha(pm)=='ac65a7b4eb897e3744fdbd16a0030f00e20da08416dddd746e27c62a9389025d'
 for rel,h in load(pm).items():assert sha(S/'producer'/rel)==h
 prev=S/'PREVIOUS_MANIFEST_SHA256.json';assert sha(prev)=='a77330918068b2fcb60a6bdc11412546a4e3fd909a7b393e46c98b62236b654a';assert sha(S/'PREVIOUS_independent_matrix.cpp')==load(prev)['independent_matrix.cpp']
 fm=S/'MATRIX4_MANIFEST_SHA256.json';assert sha(fm)=='a4eec8140e891b53cc9bd4c237c95236dd32a7069180ed9bc9355df82e4060fb';assert sha(S/'MATRIX4_audit.json')==load(fm)['audit.json'];assert sha(S/'GEOMETRY_4x4.json')==load(fm)['snapshot/GEOMETRY_4x4.json']
 actual=load(H/'independent_result.json');prod=load(S/'producer/matrix_4x4.json');assert actual['partial'] is False and actual['q4_processed']==455 and actual['q6_processed']==3003
 keys=['R4R4','R4CM','R6R6','R6M6','M6M6'];blocks={k:mat(actual[k]) for k in keys}
 for k in keys:assert blocks[k]==mat(prod[k])
 assert blocks['R4CM']!=tr(blocks['R4CM']) and blocks['R6M6']!=tr(blocks['R6M6'])
 old=load(S/'MATRIX4_audit.json');prior={k:mat(v) for k,v in old['blocks'].items()}
 for k in prior:assert mat(actual[k])==prior[k]
 q8=add(prior['CMCM'],prior['COMM']);assert add(blocks['R4R4'],blocks['R4CM'],tr(blocks['R4CM']),prior['CMCM'])==prior['PP'];assert add(blocks['R6R6'],blocks['R6M6'],tr(blocks['R6M6']),blocks['M6M6'])==prior['TT']
 # Independent weighted physical pair graph and orbit basis.
 L=4;N=16;edges=Counter();orbs=[];classes={};ids={}
 for i in range(N):
  x,y=divmod(i,L)
  for j in (((x+1)%L)*L+y,x*L+(y+1)%L):edges[tuple(sorted((i,j)))]+=1
 for a,b in itertools.combinations(range(N),2):
  ax,ay=divmod(a,L);bx,by=divmod(b,L);key=tuple(sorted((min((ax-bx)%L,(bx-ax)%L),min((ay-by)%L,(by-ay)%L))))
  if key not in classes:classes[key]=len(orbs);orbs.append([])
  ids[a,b]=classes[key];orbs[classes[key]].append((a,b))
 n=len(orbs);assert n==5;b=n+1;d=4*n+1;oldsize=3*n+1;initial=2*n+1;D=[F(1)]+[F(3*len(x)) for x in orbs]
 pairA=zero(b)
 for j in range(b):
  coeff=defaultdict(F);vac=F(0)
  if j==0:
   for e,w in edges.items():coeff[e]+=w
  else:
   for a,c in orbs[j-1]:
    w=edges.get((a,c),0);coeff[a,c]-=2*w;vac+=3*w
    for (u,v),w in edges.items():
     if u in (a,c) and v not in (a,c):coeff[tuple(sorted((v,c if u==a else a)))]+=w
     elif v in (a,c) and u not in (a,c):coeff[tuple(sorted((u,c if v==a else a)))]+=w
  pairA[0][j]=vac
  for i,orb in enumerate(orbs,1):vals={coeff[e] for e in orb};assert len(vals)==1;pairA[i][j]=D[i]*vals.pop()
 assert pairA==tr(pairA)
 geo=load(S/'GEOMETRY_4x4.json');ff,ss,vv,ww,xx,yy,zz=[mat(geo[k]) for k in ('F','S','V','W','X','Y','Z')];G=zero(d);A=zero(d)
 for i in range(b):
  G[i][i]=D[i]
  for j in range(b):A[i][j]=pairA[i][j]
 for i in range(n):
  for j in range(n):
   li,ri,mi=b+i,b+n+i,b+2*n+i;lj,rj,mj=b+j,b+n+j,b+2*n+j
   G[li][lj]=ff[i][j];G[li][rj]=G[rj][li]=ss[i][j];G[ri][rj]=vv[i][j];G[mi][mj]=ww[i][j]
   A[1+i][lj]=A[lj][1+i]=ff[i][j];A[1+i][rj]=A[rj][1+i]=ss[i][j];A[li][lj]=ss[i][j];A[li][rj]=A[rj][li]=vv[i][j];A[li][mj]=A[mj][li]=ww[i][j];A[ri][rj]=xx[i][j];A[ri][mj]=A[mj][ri]=yy[i][j];A[mi][mj]=zz[i][j]
 assert G==tr(G) and A==tr(A);gpiv=psd(G,True);q=[0]+[2]*n+[4]*(2*n)+[6]*n
 Q=[[G[i][j]*q[j] for j in range(d)] for i in range(d)];Q2=[[G[i][j]*q[i]*q[j] for j in range(d)] for i in range(d)];QA=[[A[i][j]*(q[i]+q[j]) for j in range(d)] for i in range(d)]
 W=zero(d,initial)
 for i in range(b):
  for j in range(b):W[i][j]=A[i][j]/D[i]
 for j in range(n):
  W[b+j][1+j]=1
  for i in range(n):W[1+i][b+j]=ff[i][j]/D[1+i]
  W[b+n+j][b+j]=W[b+2*n+j][b+j]=1
 assert mul(G,W)==[r[:initial] for r in A]
 rows=mul(tr(W),A);A2=zero(d)
 for i in range(initial):
  for j in range(d):A2[i][j]=A2[j][i]=rows[i][j]
 dinv=[[F(i==j,D[1+i]) for j in range(n)] for i in range(n)];D2=mul(mul(tr(ss),dinv),ss)
 rr=add(D2,blocks['R4R4'],blocks['R6R6']);rm=add(blocks['R4CM'],blocks['R6M6']);mm=add(prior['CMCM'],blocks['M6M6'],q8)
 for i in range(n):
  for j in range(n):A2[initial+i][initial+j]=rr[i][j];A2[initial+i][initial+n+j]=A2[initial+n+j][initial+i]=rm[i][j];A2[initial+n+i][initial+n+j]=mm[i][j]
 assert A2==tr(A2);cs=[Q2,scale(QA,F(1,2)),scale(A2,F(1,4))];ks=[Q,scale(A,F(1,2))]
 embedding=zero(d,oldsize)
 for i in range(oldsize):embedding[i][i]=1
 for i in range(n):embedding[oldsize+i][initial+i]=1
 oldG=zero(oldsize)
 for i in range(b):oldG[i][i]=D[i]
 for i in range(n):
  for j in range(n):oldG[b+i][b+j]=ff[i][j];oldG[b+i][initial+j]=oldG[initial+j][b+i]=ss[i][j];oldG[initial+i][initial+j]=vv[i][j]+ww[i][j]
 assert mul(mul(tr(embedding),G),embedding)==oldG
 oldA=zero(oldsize);oldQ=zero(oldsize)
 for i in range(b):
  oldQ[i][i]=D[i]*(0 if i==0 else 2)
  for j in range(b):oldA[i][j]=pairA[i][j]
 for i in range(n):
  for j in range(n):
   li,ui=b+i,initial+i;lj,uj=b+j,initial+j
   oldQ[li][lj]=4*ff[i][j];oldQ[li][uj]=oldQ[uj][li]=4*ss[i][j];oldQ[ui][uj]=4*vv[i][j]+6*ww[i][j]
   oldA[1+i][lj]=oldA[lj][1+i]=ff[i][j];oldA[1+i][uj]=oldA[uj][1+i]=ss[i][j];oldA[li][lj]=ss[i][j];oldA[li][uj]=oldA[uj][li]=vv[i][j]+ww[i][j];oldA[ui][uj]=xx[i][j]+yy[i][j]+yy[j][i]+zz[i][j]
 assert mul(mul(tr(embedding),Q),embedding)==oldQ and mul(mul(tr(embedding),A),embedding)==oldA
 for a,c in zip(cs,old['complete_H2_coefficients_g0_g1_g2']):assert mul(mul(tr(embedding),a),embedding)==mat(c)
 saved=load(S/'producer/complete_H2_polynomial_4x4.json');assert saved['dimension']==21 and mat(saved['gram'])==G and list(map(mat,saved['H_coefficients']))==ks and list(map(mat,saved['H2_coefficients']))==cs
 g=F(21,200);K=add(ks[0],scale(ks[1],g));J=add(cs[0],scale(cs[1],g),scale(cs[2],g*g));jpiv=psd(J);block=[G[i]+K[i] for i in range(d)]+[K[i]+J[i] for i in range(d)];bpiv=psd(block)
 ps={k:psd(blocks[k]) for k in ('R4R4','R6R6','M6M6')};ps['q8']=psd(q8)
 # Independently check only recombination of the producer's partial8x4 sample.
 sample=load(S/'producer/sample_8x4.json');assert sample['partial'] is True and sample['q4_processed']==2248 and sample['q6_processed']==2023
 assert sha(S/'PRIOR_SAMPLE_MANIFEST.json')=='86b34b8fe80d89fa958b777f7af5fbcf81ce9af588d123e02f4d7c2641fe56e6';assert sha(S/'PRIOR_SAMPLE8.json')==load(S/'PRIOR_SAMPLE_MANIFEST.json')['sample_8x4.json']
 oldsample=load(S/'PRIOR_SAMPLE8.json');assert oldsample['partial'] is True
 assert add(mat(sample['R4R4']),mat(sample['R4CM']),tr(mat(sample['R4CM'])),mat(oldsample['CMCM']))==mat(oldsample['PP'])
 assert add(mat(sample['R6R6']),mat(sample['R6M6']),tr(mat(sample['R6M6'])),mat(sample['M6M6']))==mat(oldsample['TT'])
 out=dict(status='PASS_INDEPENDENT_COMPLETE21D4X4_SPLIT_FIXTURE',dimension=21,full_Hilbert_dimension=str(2**32),individual_split_entries_verified=125,oriented_cross_blocks_nonsymmetric=True,full16D_compression_exact=True,complete_H2_polynomial_entries_verified=3*21*21,full_q8_retained_in_MM=True,residual_block_Gram_PSD=True,Gram_pivots=gpiv,complete_H2_PSD_pivots=jpiv,residual_block_PSD_pivots=bpiv,sector_block_PSD_pivots=ps,blocks={k:[[str(x) for x in r] for r in m] for k,m in blocks.items()},partial8x4_recombination_only=True,full8x4_split_matrix_not_reviewed=True,no_new_endpoint_or_gap=True,producer_manifest_sha256=sha(pm),seconds=time.monotonic()-t,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (H/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['seconds'],out['peak_rss_kib'])
if __name__=='__main__':main()
