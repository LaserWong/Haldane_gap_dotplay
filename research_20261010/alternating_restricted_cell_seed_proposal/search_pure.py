import json,math
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
C=json.loads((P.parent/'uniform_second_moment_optimization/certificate.json').read_text())
M={s:[[F(v) for v in row] for row in C['moment_intervals'][s][::2]] for s in ['J','N']}
def solve(A,b):
 A=[list(a)+[v] for a,v in zip(A,b)];n=len(b)
 for j in range(n):
  p=max(range(j,n),key=lambda i:abs(A[i][j]));A[j],A[p]=A[p],A[j]
  z=A[j][j];A[j]=[x/z for x in A[j]]
  for i in range(n):
   if i!=j:
    z=A[i][j];A[i]=[x-z*y for x,y in zip(A[i],A[j])]
 return [a[-1] for a in A]
def conv(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
out={'moments':{s:[[str(v) for v in row] for row in a] for s,a in M.items()},'support':{},'nodes':{}}
for s in ['J','N']:
 mid=[float((l+u)/2) for l,u in M[s]];err=[float((u-l)/2) for l,u in M[s]]
 H=[[mid[i+j] for j in range(3)] for i in range(3)];target=1.005 if s=='J' else .78
 for k in range(6):
  q=solve(H,[target**i for i in range(3)]);q=[round(x/q[-1],10) for x in q];cc=conv(q,q);B=sum(c*m+abs(c)*e for c,m,e in zip(cc,mid,err));lo=target-.05;hi=target+.05
  for _ in range(60):
   x=(lo+hi)/2;y=x*x*sum(c*x**i for i,c in enumerate(q))**2
   if y>B:hi=x
   else:lo=x
  target=hi
 U=math.ceil(target*10**9+1)/10**9;out['support'][s]={'coeff':[str(F(str(x))) for x in q],'cap':str(F(str(U)))}
 w=[U*mid[i]-mid[i+1] for i in range(4)];d,c=solve([[w[0],w[1]],[w[1],w[2]]],[-w[2],-w[3]])
 a=(-c-math.sqrt(c*c-4*d))/2;b=(-c+math.sqrt(c*c-4*d))/2
 out['nodes'][s]=[str(F(round(x*10**9),10**9)) for x in [a,b]]
 print('moments',s,mid,err,'support',U,'q',q,'hermite_nodes',[a,b],flush=True)
(P/'candidates.json').write_text(json.dumps(out,indent=2)+'\n')
