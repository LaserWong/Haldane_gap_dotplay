from fractions import Fraction as F
def inertia(A):
 """Exact rational congruence, diagonal pivots plus nonsingular 2x2 fallback."""
 A=[[F(x) for x in r] for r in A];neg=zero=0;piv=[]
 assert all(A[i][j]==A[j][i] for i in range(len(A)) for j in range(len(A)))
 while A:
  n=len(A);ix=next((i for i in range(n) if A[i][i]),None)
  if ix is not None:
   order=[ix]+[i for i in range(n) if i!=ix];A=[[A[i][j] for j in order] for i in order];d=A[0][0]
   neg+=d<0;piv.append(str(d));A=[[A[i][j]-A[i][0]*A[0][j]/d for j in range(1,n)] for i in range(1,n)]
  else:
   pair=next(((i,j) for i in range(n) for j in range(i+1,n) if A[i][j]),None)
   if pair is None:zero+=n;break
   i,j=pair;order=[i,j]+[k for k in range(n) if k not in pair];A=[[A[i][j] for j in order] for i in order];b=A[0][1]
   neg+=1;piv.append('2x2 offdiagonal '+str(b));A=[[A[i][j]-(A[i][0]*A[1][j]+A[i][1]*A[0][j])/b for j in range(2,n)] for i in range(2,n)]
 return neg,zero,piv

