from pathlib import Path
import json,math
P=Path(__file__).resolve().parent;d=json.load(open(P.parent/'uniform_transfer_moment_assessment/results.json'));caps={s:float(v['x_cap']['display']) for s,v in d['hankel_caps'].items()};m={s:v['moment_intervals']['5'][1]['display'] for s,v in d['hankel_caps'].items()}
def bounds(L):
 vals=[]
 for s,x in caps.items():
  h=x**5;M=m[s];q=int(M/h);vals.append(q*x**(L/2)+(M-q*h)**(L/10))
 a,b,c=vals;return a+2*b+3*c,a+2*b

def recur(s,t,n,beta):
 for j in range(20):
  if min(s,t)>=.99:return (n,beta, -math.log(5*max(1-s,1-t))/beta,j)
  z=s*s*t
  if z<=0:return
  s=1-(1-z)**2/(2*z*z)
  if s<=0:return
  z=t*t*s;t=1-(1-z)**2/(2*z*z)
  if t<=0:return
  n*=2;beta*=2

def test(l,r,R=0):
 D,E=[u**r for u in bounds(l)];tau=(D+11*E)/12;tau0=(D+3*E)/4;w=math.exp(-10.5*r*R);t=(w/D)**(1/3)
 if 2*t<=D or t>tau:return
 def rr(t):return max(x*x+y*y/2+(D-t-x-y)**2/3 for x,y in [(0,0),(tau-t,0),(tau-t,tau0-tau),(0,tau0-t)])
 for _ in range(100):
  rad=w-rr(t)**2
  if rad<=0:return
  tn=rad**.25
  if tn<=t:break
  t=tn
 S=(1+rr(t)/t**2)**-2
 q=bounds(4*l)[0];v=math.exp(-10.5*R);T=(1+((q-v)/v)**r)**-2
 ans=recur(S,T,2*l,10.5*r)
 if ans:return {'l':l,'n':2*l,'r':r,'S':S,'T':T,'t':t,'D':D,'E':E,'final':ans}
if __name__=='__main__':
 for l in range(10,42,2):
  out=[v for r in range(100,501) if (v:=test(l,r/100))]
  if out:print(l,min(out,key=lambda v:v['final'][0]),'bestgap',max(out,key=lambda v:v['final'][2]))

def general(n,l,r,R=0):
 D,E=[u**r for u in bounds(l)];tau=(D+11*E)/12;tau0=(D+3*E)/4;w=math.exp(-10.5*r*R);p=2*n/l;q=n/l;t=(w/D)**(1/(p-1))
 if n<l or 2*t<=D or t>tau:return
 def rr(t,p):return max(x**p+y**p/2**(p-1)+(D-t-x-y)**p/3**(p-1) for x,y in [(0,0),(tau-t,0),(tau-t,tau0-tau),(0,tau0-t)])
 for _ in range(60):
  rad=w-rr(t,p)
  if rad<=0:return
  tn=rad**(1/p)
  if tn<=t:break
  t=tn
 S=(1+rr(t,q)/t**q)**-2
 z=bounds(2*n)[0];v=math.exp(-10.5*R);T=(1+((z-v)/v)**r)**-2
 ans=recur(S,T,n,10.5*r)
 if ans:return {'l':l,'n':n,'r':r,'S':S,'T':T,'t':t,'D':D,'E':E,'final':ans}
