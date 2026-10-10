"""Independent exact small-column and aggregate-interval audit of streamed thermal inputs."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
from collections import Counter
import subprocess,math,json,hashlib
BASE=Path(__file__).resolve().parents[2];HEAT=BASE/'heat_trace';OUT=BASE/'audit/independent'
Q=2**56;mu=84;J=256
terms=[F(1)]
for j in range(1,J+1):terms.append(terms[-1]*mu/j)
sumterms=sum(terms);coeff=[int(Q*x//sumterms) for x in terms]
assert coeff==list(map(int,(HEAT/'coefficients_A.txt').read_text().split()))
kmax=max(i for i,c in enumerate(coeff) if c)
assert kmax==172

def encode(w):
 c=0
 for x in w:c=3*c+x+1
 return c

def small(twist,L=4):
 total=0;checked=0;words=list(product((-1,0,1),repeat=L))
 for M in range(-L,L+1):
  basis=[w for w in words if sum(w)==M];lookup={w:i for i,w in enumerate(basis)};d=len(basis)
  A=[[(0,0) for _ in range(d)] for _ in range(d)]
  for c,w in enumerate(basis):
   diag=16-3*L//2-sum(w[j]*w[(j+1)%L] for j in range(L));A[c][c]=(diag,0)
   for j in range(L):
    k=(j+1)%L
    for dx in (-1,1):
     v=list(w);v[j]+=dx;v[k]-=dx
     if max(v)>1 or min(v)<-1:continue
     r=lookup[tuple(v)];p=w[0]-v[0] if k==0 else 0
     if twist=='I':a,b=-1,0
     elif twist=='P':a,b=(-1 if p%2==0 else 1),0
     else:a,b=[(-1,0),(0,-1),(1,1)][p%3]
     x,y=A[r][c];A[r][c]=(x+a,y+b)
  output=subprocess.check_output([str(HEAT/'stream_horner'),str(L),twist,'none',str(M),'0',str(d),str(HEAT/'coefficients_A.txt'),'compute'],text=True,stderr=subprocess.DEVNULL)
  observed={int(line.split()[0]):int(line.split()[2]) for line in output.splitlines()}
  for c,w in enumerate(basis):
   u=[0]*d;v=[0]*d
   for j in range(kmax,-1,-1):
    un=[];vn=[]
    for row in A:
     un.append(sum(a*x-b*y for (a,b),x,y in zip(row,u,v))//16)
     vn.append(sum(b*x+(a-b)*y for (a,b),x,y in zip(row,u,v))//16)
    un[c]+=coeff[j];u,v=un,vn
   norm=sum(x*x-x*y+y*y for x,y in zip(u,v))
   assert norm==observed[encode(w)]
   checked+=1;total+=norm
 return {'L':L,'twist':twist,'independent_columns_matching_binary':checked,'integer_total':str(total)}

def ceilroot(x):return math.isqrt(x)+(math.isqrt(x)**2<x)
def frac(d):return F(int(d['numerator']),int(d['denominator']))
def aggregate(path):
 c=json.loads(path.read_text());L=c['L'];records=[]
 for p in path.parent.glob('M*.json'):records.extend(json.loads(p.read_text())['records'])
 assert len(records)==c['representatives'];assert len({r['code'] for r in records})==len(records)
 assert sum(r['multiplicity'] for r in records)==3**L
 dims=Counter(map(sum,product((-1,0,1),repeat=L)))
 for r in records:assert r['block_dimension']==dims[r['M']]
 N=sum(r['multiplicity']*int(r['norm_squared']) for r in records)
 assert N==int(c['total_squared_integer_norm'])
 err2=sum(r['multiplicity']*((kmax+1)*ceilroot(r['block_dimension'])+258)**2 for r in records)
 e=ceilroot(err2);assert e==int(c['frobenius_error_numerator'])
 tail=terms[-1]*mu/(J+1)/(1-F(mu,J+2));assert 2*tail/sumterms<1/F(Q)
 x=F(21,2)*L*(F(3,2)-F(700741,500000))
 tt=[F(1)]
 for j in range(1,101):tt.append(tt[-1]*x/j)
 loexp=sum(tt);hiexp=loexp+tt[-1]*x/101/(1-x/102)
 r=math.isqrt(N);lo=loexp*F(max(0,r-e)**2,Q*Q);hi=hiexp*F((r+1+e)**2,Q*Q)
 assert lo==frac(c['interval']['lower']) and hi==frac(c['interval']['upper'])
 center=F(c['published_center']);assert center-F(1,100000)<lo<=hi<center+F(1,100000)
 return {'certificate':str(path.relative_to(BASE)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'all_record_dimensions_and_multiplicities_valid':True,'independent_interval_exact_match':True,'lower_display':float(lo),'upper_display':float(hi)}

if __name__=='__main__':
 smalls=[small(t) for t in ('I','P','C')]
 aggregates=[aggregate(p) for p in sorted((HEAT/'results').glob('A_L[68]_*/certificate.json'))]
 result={'status':'PASS','independent_L4_full_column_tests':smalls,'independent_aggregate_intervals':aggregates,'cpp_sha256':hashlib.sha256((HEAT/'stream_horner.cpp').read_bytes()).hexdigest(),'binary_sha256':hashlib.sha256((HEAT/'stream_horner').read_bytes()).hexdigest(),'coefficient_sha256':hashlib.sha256((HEAT/'coefficients_A.txt').read_bytes()).hexdigest()}
 (OUT/'streamed_heat_audit.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
