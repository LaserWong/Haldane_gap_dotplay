from pathlib import Path
from fractions import Fraction as F
# Rung columns are integer vectors divided by sqrt(2)^r, with r=(1,0,1,0).
R=[[0,1,0,0],[1,0,1,0],[-1,0,1,0],[0,0,0,1]];exps=[1,0,1,0]
# Twice intralayer exchange: antiparallel flip coefficient 1, diagonal +/-1/2 per layer.
H=[[F(0) for _ in range(16)] for _ in range(16)]
for s in range(16):
 for a,b in ((3,1),(2,0)):
  x=(s>>a)&1;y=(s>>b)&1
  H[s][s]+=F(1 if x==y else -1,2)
  if x!=y:H[s^((1<<a)|(1<<b))][s]+=1
T=[[R[i//4][j//4]*R[i%4][j%4] for j in range(16)] for i in range(16)]
M=[[F(0) for _ in range(16)] for _ in range(16)]
for d in range(16):
 for s in range(16):
  raw=sum(T[i][d]*H[i][j]*T[j][s] for i in range(16) for j in range(16))
  e=exps[d//4]+exps[d%4]+exps[s//4]+exps[s%4]
  assert raw==0 or e%2==0
  if raw:M[d][s]=raw/(2**(e//2))
  assert M[d][s].denominator==1
p=Path(__file__).parent;tab=list(map(int,(p/'edge_table.txt').read_text().split()))
for op,delta in enumerate((-2,2,0)):
 for src in range(16):
  a,b=src%4,src//4
  for dst in range(16):
   c,d=dst%4,dst//4
   want=M[4*c+d][4*a+b] if (c!=0)+(d!=0)-(a!=0)-(b!=0)==delta else 0
   assert want==tab[op*256+src*16+dst]
print('Exact rational spin-half derivation certifies every spherical edge-table integer; no floating tolerance in acceptance.')
