"""Independent counted low-band audit. Exact proof checks, optional floating diagnostic."""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'): os.environ[name]='1'
if hasattr(os,'sched_getaffinity'): os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import itertools,json,math,time,resource,hashlib
from fractions import Fraction as F
from collections import Counter,defaultdict
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
HERE=Path(__file__).resolve().parent
# Independently specified integer Clebsch-Gordan columns in |m_left,m_right>, m=-1,0,1.
CG=[[0,0,1,0,-1,0,1,0,0],[0,-1,0,1,0,0,0,0,0],[0,0,-1,0,0,0,1,0,0],[0,0,0,0,0,-1,0,1,0],[1,0,0,0,0,0,0,0,0],[0,1,0,1,0,0,0,0,0],[0,0,1,0,2,0,1,0,0],[0,0,0,0,0,1,0,1,0],[0,0,0,0,0,0,0,0,1]]
W=[sum(x*x for x in v) for v in CG]
EX=[0,1,1,1,3,3,3,3,3]; MAG=[0,-1,0,1,-2,-1,0,1,2]
assert W==[3,2,2,2,1,2,6,2,1]
assert all(sum(x*y for x,y in zip(CG[i],CG[j]))==(W[i] if i==j else 0) for i in range(9) for j in range(9))
def dimer_action(v):
 out=[0]*9
 for c,vv in enumerate(v):
  i,j=divmod(c,3);out[c]+=(i-1)*(j-1)*vv
  if i<2 and j>0:out[c+2]+=vv
  if i>0 and j<2:out[c-2]+=vv
 return out
assert all(dimer_action(v)==[(e-2)*x for x in v] for v,e in zip(CG,EX))
def op(site,kind):
 A=[[0]*9 for _ in range(9)]
 for c in range(9):
  x=list(divmod(c,3));m=x[site]
  if kind=='z':A[c][c]=m-1
  elif kind=='+' and m<2:x[site]+=1;A[3*x[0]+x[1]][c]=1
  elif kind=='-' and m>0:x[site]-=1;A[3*x[0]+x[1]][c]=1
 return [[F(sum(CG[r][i]*A[i][j]*CG[c][j] for i in range(9) for j in range(9)),W[r]) for c in range(9)] for r in range(9)]
O={(s,k):op(s,k) for s in [0,1] for k in ['z','+','-']}
K={}
for c,d in itertools.product(range(9),repeat=2):
 row=[]
 for r,s in itertools.product(range(9),repeat=2):
  z=O[1,'z'][r][c]*O[0,'z'][s][d]+O[1,'+'][r][c]*O[0,'-'][s][d]+O[1,'-'][r][c]*O[0,'+'][s][d]
  if z:row.append((r,s,z))
 K[c,d]=row
# Physical spin-one ladder sqrt(2) factors cancel the conventional 1/2.
def metric(st):return math.prod(W[i] for i in st)
def action(st):
 out=defaultdict(F)
 for j in range(4):
  i=(j-1)%4
  for a,b,v in K[st[i],st[j]]:
   s=list(st);s[i]=a;s[j]=b;out[tuple(s)]+=v
 return {s:v for s,v in out.items() if v}
def psd(A):
 A=[[F(x) for x in r] for r in A];n=len(A);p=[]
 assert all(A[i][j]==A[j][i] for i in range(n) for j in range(n))
 for k in range(n):
  x=A[k][k];assert x>=0,(k,x)
  p.append(x)
  if not x:assert all(A[j][k]==0 for j in range(k+1,n));continue
  for i in range(k+1,n):
   for j in range(i,n):A[i][j]=A[j][i]=A[i][j]-A[i][k]*A[j][k]/x
 return p

def main():
 start=time.monotonic()
 # Unit-coupling local inequality V + (h_i+h_j)/2 + I >=0.
 A=[[F(0) for _ in range(81)] for _ in range(81)]
 for c,d in itertools.product(range(9),repeat=2):
  col=9*c+d;A[col][col]=(F(EX[c]+EX[d],2)+1)*W[c]*W[d]
  for r,s,v in K[c,d]:A[9*r+s][col]+=v*W[r]*W[s]
 blocks=[]
 for m in range(-4,5):
  ids=[i for i in range(81) if MAG[i//9]+MAG[i%9]==m]
  assert all(A[i][j]==0 for i in ids for j in range(81) if j not in ids)
  p=psd([[A[i][j] for j in ids] for i in ids]);blocks.append(dict(m=m,pivots=list(map(str,p))))
 P=[(0,0,0,0)]
 for m in [1,2,3]:
  for i in range(4):s=[0]*4;s[i]=m;P.append(tuple(s))
 ind={s:i for i,s in enumerate(P)};cols=[action(s) for s in P];G=[metric(s) for s in P]
 V=[[cols[c].get(P[r],F(0)) for c in range(13)] for r in range(13)]
 R=[{s:v for s,v in col.items() if s not in ind} for col in cols]
 # Within each nonzero block all P norms agree; mixed vacuum-triplet entries vanish.
 R2=[[sum(metric(s)*v*R[j].get(s,F(0)) for s,v in R[i].items()) for j in range(13)] for i in range(13)]
 assert all(R2[i][j]==0 or G[i]==G[j] for i in range(13) for j in range(13))
 S=[[R2[i][j]/G[i] for j in range(13)] for i in range(13)]
 assert all(G[i]*V[i][j]==G[j]*V[j][i] for i in range(13) for j in range(13))
 assert all(V[0][j]==V[j][0]==S[0][j]==S[j][0]==0 for j in range(1,13))
 eigen=[]
 for m in range(3):
  ids=range(1+4*m,5+4*m)
  B=[[V[i][j] for j in ids] for i in ids];D=[[S[i][j] for j in ids] for i in ids]
  assert all(V[i][j]==S[i][j]==0 for i in ids for j in range(1,13) if j not in ids)
  for tag,f in [('0',[1,1,1,1]),('pi',[1,-1,1,-1]),('pi/2_cos',[1,0,-1,0]),('pi/2_sin',[0,1,0,-1])]:
   n=sum(x*x for x in f);vb=sum(f[i]*B[i][j]*f[j] for i in range(4) for j in range(4))/n;rb=sum(f[i]*D[i][j]*f[j] for i in range(4) for j in range(4))/n
   assert all(sum(B[i][j]*f[j] for j in range(4))==vb*f[i] for i in range(4))
   assert all(sum(D[i][j]*f[j] for j in range(4))==rb*f[i] for i in range(4))
   eigen.append(dict(magnetic=m-1,momentum=tag,V=str(vb),residual_unit_squared=str(rb)))
 bins=Counter();qcomp=Counter();single_quintets=0
 for s in itertools.product(range(9),repeat=4):
  E=sum(EX[i] for i in s);bins[E]+=1
  if s not in ind:
   assert E>=2;qcomp[E]+=1
   if sum(i!=0 for i in s)==1:assert E==3;single_quintets+=1
 assert len(P)==13 and sum(bins.values())==6561 and sum(qcomp.values())==6548 and single_quintets==20
 result=dict(status='EXACT_BLOCK_PREMISES_VERIFIED',normalization='H_shift=H+8; weighted strong-dimer excitation h has eigenvalues0,1,3 with multiplicities1,3,5',P_dimension=13,Q_dimension=6548,full_dimension=6561,single_quintets_in_Q=single_quintets,reference_bins=dict(sorted(bins.items())),complement_bins=dict(sorted(qcomp.items())),local_psd=dict(inequality='V+(h_i+h_j)/2+I>=0',blocks=blocks,positive_pivots=sum(F(x)>0 for b in blocks for x in b['pivots']),zero_pivots=sum(F(x)==0 for b in blocks for x in b['pivots'])),vacuum_residual_unit_squared=str(S[0][0]),triplet_eigenchannels=eigen,P_norms=G,V_P=[[str(v) for v in r] for r in V],residual_Gram_normalized=[[str(v) for v in r] for r in S],P_action_support=len(set().union(*(set(c) for c in cols))),residual_support=len(set().union(*(set(c) for c in R))),seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (HERE/'block_premises.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','vacuum_residual_unit_squared','triplet_eigenchannels','seconds','peak_rss_kib']},indent=2))
if __name__=='__main__':main()
