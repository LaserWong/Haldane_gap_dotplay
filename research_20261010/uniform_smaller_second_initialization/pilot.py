from pathlib import Path
from fractions import Fraction as F
import json,math,resource,os,time
os.sched_setaffinity(0,{2});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
P=Path(__file__).resolve().parent;C=json.loads((P.parent/'uniform_second_moment_optimization/certificate.json').read_text());L=json.loads((P/'long_certificate.json').read_text());U=float(F(C['filters']['J+']['cap']));V=float(F(C['filters']['N-']['cap']));mj=float(F(C['moment_intervals']['J'][-1][1]));mn=float(F(C['moment_intervals']['N'][-1][1]));pack=lambda m,h,r:math.floor(m/h)*h**r+(m-math.floor(m/h)*h)**r
Q=lambda n:min(float(F(L[f'J{n}']['bound'])),pack(mj,U**12,n/12))+3*min(float(F(L[f'N{n}']['bound'])),pack(mn,V**12,n/12))
G=lambda x:1-(1-x)**2/(2*x*x)
def run(s,t,beta):
 best=1e9;rows=[]
 for j in range(32):
  k=s*s*t
  if k<=.5:return False,best,rows,'joint <= .5'
  w=(1+math.sqrt(2*k-1))/2;rho=(1-w)/w;d=t/(1+rho*rho);cc=(1-rho)*min(s*math.sqrt(d),d)
  if cc<=.5:return False,best,rows,'window <= .5'
  
  if cc>=1-1e-14:return True,best,rows,'floating saturation; exact checker required'
  best=min(best,math.log(cc/(1-cc))/beta);rows.append([s,t,cc,best])
  u=max(1-s,1-t)
  if u<=1e-12:return True,min(best,-math.log(5*u)/beta),rows,'entry'
  s=G(k)
  if s<=0:return False,best,rows,'S <= 0'
  t=G(t*t*s)
  if t<=0:return False,best,rows,'T <= 0'
  beta*=2
 return False,best,rows,'round limit'
for n in [34,32]:
 lo,hi=.99,1.
 for _ in range(60):
  e=(lo+hi)/2
  if pack(mj,e**12,2*n/12)+3*pack(mn,V**12,2*n/12)<1:lo=e
  else:hi=e
 ell=lo;tail=(mj-ell**12)**(n/12)+3*float(F(L[f'N{n}']['bound']));s=(1+tail/ell**n)**-2;t=Q(2*n)**-2
 print(n,'ell',ell,'Q',Q(2*n),'S,T',s,t,'run',run(s,t,12.25),flush=True)
