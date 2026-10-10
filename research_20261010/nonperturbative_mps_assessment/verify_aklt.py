#!/usr/bin/env python3
"""Exact rational AKLT local gap/count certificate; no numerical eigenvalues."""
import os, resource, itertools, json, time
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent;t0=time.time()
def mm(A,B):
 return [[sum((a*b for a,b in zip(row,col)),F(0)) for col in zip(*B)] for row in A]
def local():
 # Cartesian spin-1 basis. P2=(I+swap)/2-|Omega><Omega|/3.
 h=[[F(0) for j in range(9)] for i in range(9)]
 for a,b in itertools.product(range(3),repeat=2):
  k=3*a+b;h[k][k]+=F(1,2);h[3*b+a][k]+=F(1,2)
  if a==b:
   for c in range(3):h[3*c+c][k]-=F(1,3)
 assert mm(h,h)==h and sum(h[i][i] for i in range(9))==5
 return h
h=local()
def blocks(n):
 states=list(itertools.product(range(3),repeat=n));groups={}
 for v in states:
  par=tuple(v.count(c)%2 for c in range(3));groups.setdefault(par,[]).append(v)
 out=[]
 for key,ss in sorted(groups.items()):
  idx={v:i for i,v in enumerate(ss)};H=[[F(0) for _ in ss] for _ in ss]
  for j,s in enumerate(ss):
   for a in range(n-1):
    old=3*s[a]+s[a+1]
    for new in range(9):
     val=h[new][old]
     if val:
      v=list(s);v[a],v[a+1]=divmod(new,3);H[idx[tuple(v)]][j]+=val
  out.append((key,H))
 return out
def psd_pivots(A):
 A=[r.copy() for r in A];p=[]
 for k in range(len(A)):
  d=A[k][k];assert d>=0,(k,d)
  p.append(d)
  if d==0:
   assert all(A[k][j]==0 for j in range(k+1,len(A)));continue
  for i in range(k+1,len(A)):
   for j in range(i,len(A)):
    A[j][i]=A[i][j]=A[i][j]-A[i][k]*A[k][j]/d
 return p
rows=[]
for n in (2,3,4):
 rank=0;null=0;details=[]
 for par,H in blocks(n):
  p=psd_pivots(H);rank+=sum(x>0 for x in p);null+=sum(x==0 for x in p)
  if n==4:
   square=mm(H,H);K=[[square[i][j]-F(2,5)*H[i][j] for j in range(len(H))] for i in range(len(H))]
   p_gap=psd_pivots(K)
   assert sum(x==0 for x in p_gap)==sum(x==0 for x in p)
  else:p_gap=[]
  details.append({'parity':par,'dimension':len(H),'H_pivots':[str(x) for x in p],'H2_minus_two_fifths_H_pivots':[str(x) for x in p_gap]})
 assert null==4 and rank+null==3**n
 rows.append({'n':n,'rank':rank,'nullity':null,'blocks':details})
# Product Pauli words span Mat_2 at length 2: XX=I, YZ=iX, ZX=iY, XY=iZ.
# Exact complex arithmetic is only needed for this 9x9 parent check.
import sympy as s
paulis=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
W=s.Matrix([[s.trace(paulis[a]*paulis[b]*B) for B in [s.eye(2),*paulis]] for a,b in itertools.product(range(3),repeat=2)])
assert W.rank()==4 and s.Matrix(h)*W==s.zeros(9,4)
W3=s.Matrix([[s.trace(paulis[a]*paulis[b]*paulis[c]*B) for B in [s.eye(2),*paulis]] for a,b,c in itertools.product(range(3),repeat=3)])
assert W3.rank()==4
H3=s.kronecker_product(s.Matrix(h),s.eye(3))+s.kronecker_product(s.eye(3),s.Matrix(h))
assert H3*W3==s.zeros(27,4)
E=sum((s.kronecker_product(A,A.conjugate()) for A in paulis),s.zeros(4))
z=s.symbols('lambda');assert s.factor(E.charpoly(z).as_expr())==(z-3)*(z+1)**3
# Exact negative realignment direction: Q=diag(1,-1,0), trace Q=0.
Q=s.diag(1,-1,0);coeff=sum(-s.Matrix(h)[3*a+c,3*b+d]*Q[a,b]*Q[c,d] for a,b,c,d in itertools.product(range(3),repeat=4))
assert coeff==s.Rational(-1,3)
# Knabe n=4 open gap >=2/5 -> periodic gap >=(3/2)(2/5-1/3)=1/10 for L>4.
gap=F(3,2)*(F(2,5)-F(1,3));assert gap==F(1,10)
# All omitted states (not Ritz values): unique zero state, exactly 3^L-1 states >=gap.
examples=[]
for L,beta in ((8,160),(16,240)):
 # rigorous exp(-beta/10)<= (1+beta/(10*k))^-k for k=4096, by exp(x)>=1+x.
 x=F(beta,10);k=4096;eupper=(1+x/k)**(-k)
 tail=(3**L-1)*eupper
 assert tail<F(1,100)
 examples.append({'L':L,'beta':beta,'hilbert_dimension':3**L,'MPS_bond_dimension':2,'retained_states':1,'linear_trial_span':1,'count_omitted':3**L-1,'omitted_energy_lower':'1/10','trace_lower':'1','trace_upper_less_than':'101/100','tail_upper_display':float(tail),'MPS_norm_exact':str(3**L+3*(-1)**L)})
result={'status':'PASS exact local AKLT gap and full omitted-state count certificate','normalization':'H_L=sum nearest-neighbor P(total spin=2), periodic L>=5','local_open_gap':'2/5','Knabe_periodic_gap':'1/10','uniqueness':'Pauli MPS injectivity length 2; exact Int(2,3) nullity=4, parent intersection theorem yields unique periodic state for L>=3','thermal_transfer_status':'Existing same-real-factor sufficient condition fails: realignment quadratic on traceless Q is -1/3; no impossibility for every other transfer construction is asserted.','rows':rows,'thermal_examples':examples,'seconds':time.time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'aklt_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
