"""Exact SU(2) x translation dimensions, using only integer word counting.
A period-p orbit contributes momentum k precisely when n divides k*p.
"""
from pathlib import Path
import json

def sector_coefficient(length,m):
 p=[1]
 for _ in range(length):
  out=[0]*(len(p)+4)
  for i,x in enumerate(p):
   for j in range(5):out[i+j]+=x
  p=out
 pos=2*length+m
 return p[pos] if 0<=pos<len(p) else 0

def dimensions(n,m):
 divs=[p for p in range(1,n+1) if n%p==0];exact={}
 for p in divs:
  num=sector_coefficient(p,m*p//n) if (m*p)%n==0 else 0
  num-=sum(exact[q] for q in exact if p%q==0)
  assert num>=0 and num%p==0;exact[p]=num
 d=[sum(num//p for p,num in exact.items() if (k*p)%n==0) for k in range(n)]
 assert sum(d)==sector_coefficient(n,m)
 return d
n=10;dims=[dimensions(n,m) for m in range(21)]
su2=[[dims[j][k]-(dims[j+1][k] if j<20 else 0) for k in range(n)] for j in range(21)]
assert all(x>=0 for row in su2 for x in row)
assert sum((2*j+1)*sum(row) for j,row in enumerate(su2))==5**n
out={'n':n,'magnetization_momentum_dimensions':dims,'spin_momentum_multiplicity_dimensions':su2,'max_magnetization_block':max(map(max,dims)),'max_su2_block':max(map(max,su2)),'max_su2_J_le_4':max(max(r) for r in su2[:5]),'status':'Exact dimensions only; no Hamiltonian construction or diagonalization'}
p=Path(__file__).resolve().parent/'exact_block_dimensions.json'
if p.exists():assert json.loads(p.read_text())['magnetization_momentum_dimensions']==dims
p.write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if 'dimensions' not in k},indent=2));print('J0',su2[0]);print('J4',su2[4])
