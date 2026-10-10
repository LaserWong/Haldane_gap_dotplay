import sympy as s
import json,time
from pathlib import Path
t=time.perf_counter(); D=16

def heis(i,j):
 h=s.zeros(D)
 for c in range(D):
  bi=(c>>i)&1; bj=(c>>j)&1
  h[c,c]+=s.Rational(1 if bi==bj else -1,4)
  if bi!=bj:h[c^((1<<i)|(1<<j)),c]+=s.Rational(1,2)
 return h
h0=heis(0,1)+heis(2,3)+s.Rational(3,2)*s.eye(D)
v=heis(0,2)+heis(1,3)
g=s.Rational(1,50);a=s.Rational(17,400);b=s.Rational(2163649829,500000000000)
A=g*v+a*h0+b*s.eye(D)
assert A==A.T
minors=[A[:k,:k].det(method='domain-ge') for k in range(1,D+1)]
assert all(x>0 for x in minors)
result={'status':'PASS','method':'Independent physical four-spin product basis and exact Sylvester leading-principal-minor criterion','g':str(g),'a':str(a),'b':str(b),'leading_principal_minors':[str(x) for x in minors],'global_degree':4,'edges_for_16_rungs':32,'alpha':str(1-4*a),'B':str(32*b),'first_excited_bin_shift':str(1-4*a-32*b),'seconds':time.perf_counter()-t}
p=Path(__file__).parent/'local_bilayer_g002_exact.json';p.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps({k:v for k,v in result.items() if k!='leading_principal_minors'},indent=2))
