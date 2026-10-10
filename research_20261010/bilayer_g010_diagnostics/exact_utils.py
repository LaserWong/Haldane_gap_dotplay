from fractions import Fraction as F
from math import lcm
import hashlib,json

def positive_definite(M):
 den=1
 for x in M.flat:den=lcm(den,F(x).denominator)
 z=[[int(F(x)*den) for x in row] for row in M];prev=1;piv=[]
 for k in range(len(z)):
  p=z[k][k];piv.append(p)
  if p<=0:return dict(positive_definite=False,first_nonpositive_pivot=k)
  for i in range(k+1,len(z)):
   for j in range(i,len(z)):
    v=p*z[i][j]-z[i][k]*z[k][j];assert v%prev==0;z[i][j]=z[j][i]=v//prev
  prev=p
 return dict(positive_definite=True,positive_leading_minor_count=len(piv),clearing_denominator=str(den),leading_minor_sha256=hashlib.sha256(json.dumps(list(map(str,piv))).encode()).hexdigest())

