import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import ast,json,math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.optimize import minimize,brentq
P=Path(__file__).resolve().parent;R=P.parents[1]
src=R/'upstream/extracted/cases/haldane_reference_audit/published_scalar_enclosures.py'
tree=ast.parse(src.read_text());tab=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='B' for t in n.targets))
D={}
for j,(n,c,W) in enumerate(tab):
 x=F(49,4)*n*(F(3,2)-F(700741,500000));s=sum((x**k/F(math.factorial(k)) for k in range(101)),F());d=math.isqrt(3**n)+1;err=d*(281*(d+1)+1);r=math.isqrt(W)
 lo=s*max(0,r-err)**2/2**110;hi=(s+x**100/F(math.factorial(100)))*(r+1+err)**2/2**110
 grid=10**18;D[n,j%2]=(F(lo.numerator*grid//lo.denominator,grid),F(-((-hi.numerator*grid)//hi.denominator),grid))
M={}
for sector in ['J','N']:
 vals=[]
 for n in range(4,13):
  z,p=D[n,0],D[n,1]
  vals.append(((z[0]+3*p[0])/4,(z[1]+3*p[1])/4) if sector=='J' else ((z[0]-p[1])/4,(z[1]-p[0])/4))
 M[sector]=vals
if __name__=='__main__':
 result={}
 for sector,vals in M.items():
  mid=np.array([float((l+u)/2) for l,u in vals]);err=np.array([float((u-l)/2) for l,u in vals]);H=np.array([[mid[i+j] for j in range(5)] for i in range(5)])
  print(sector,'mid',mid,'err',err,'eig',np.linalg.eigvalsh(H),flush=True)
  for sg in [1,-1]:
   target=(1.00139 if sector=='J' else .872)*sg
   def objective(q):
    c=np.convolve(q,q);return (c@mid+abs(c)@err)/(target**4*np.polyval(q[::-1],target)**2)
   init=np.linalg.solve(H,np.array([target**i for i in range(5)]));init/=np.max(abs(init))
   for iteration in range(8):
    fit=minimize(objective,init,method='BFGS',options={'maxiter':300,'gtol':1e-10});q=fit.x; q/=q[-1];q=np.round(q,9)
    def f(r):return r**4*np.polyval(q[::-1],sg*r)**2-(np.convolve(q,q)@mid+abs(np.convolve(q,q))@err)
    grid=np.linspace(.05,1.1,1000); pairs=[(a,b) for a,b in zip(grid[:-1],grid[1:]) if f(a)<0<f(b)];cap=brentq(f,*pairs[-1])
    target=sg*cap;init=q
   result[sector+('+' if sg==1 else '-') ]={'q':q.tolist(),'cap':cap,'objective':objective(q)}
   print(sector,sg,'q',q,'cap',cap,'objective',objective(q),flush=True)
 (P/'candidates.json').write_text(json.dumps(result,indent=2))
