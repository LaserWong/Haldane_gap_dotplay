import certify as c
import math,json,time
P=c.P;start=time.process_time();n=28;Q=float(c.sector('J',56)+3*c.sector('N',56));R=float(c.F(c.ints['H0_56'],c.ints['N0_56'])+56*c.F(700741,500000));v=math.exp(-12.25*R)
G=lambda x:1-(1-x)**2/(2*x*x)
def run(s,t,b):
 best=100;states=[]
 for j in range(16):
  K=s*s*t
  if K<=.5:return False,0,j,'joint'
  w=(1+math.sqrt(2*K-1))/2;rho=(1-w)/w;d=t/(1+rho*rho);C=(1-rho)*min(s*math.sqrt(d),d)
  if C<=.5:return False,0,j,'window'
  if C>=1-1e-12:return True,best,j,'float_saturation'
  best=min(best,math.log(C/(1-C))/b)
  u=max(1-s,1-t)
  if u<=1e-8:return True,min(best,-math.log(5*u)/b),j,'small_defect'
  s=G(K)
  if s<=0:return False,0,j,'S'
  t=G(t*t*s)
  if t<=0:return False,0,j,'T'
  b*=2
 return False,0,16,'limit'
rows=[]
for ell in [12]+list(range(16,29,2)):
 a=float(c.sector('J',ell));b=float(c.sector('N',ell));q=n/ell;p=2*q
 for k in range(100,301):
  r=k/100;D=(a+3*b)**r;E=a**r;tau=(D+3*E)/4;W=v**r;t0=(W/D)**(1/(p-1))*(1-1e-13)
  if 2*t0<=D or t0>=tau:continue
  def tail(t,e):return max(3*((D-t)/3)**e,(tau-t)**e+3*((D-tau)/3)**e)
  legal=True
  for _ in range(20):
   rem=tail(t0,p)
   if rem>=W:legal=False;break
   new=(W-rem)**(1/p)*(1-1e-13)
   if new<=t0:break
   t0=new
  if not legal:continue
  s=(1+tail(t0,q)/t0**q)**-2;t=(1+(Q/v-1)**r)**-2;ok,g,j,gate=run(s,t,12.25*r)
  rows.append({'ell':ell,'r':r,'S':s,'T':t,'pass':ok,'gap':g,'round':j,'gate':gate})
out={'status':'FLOATING_FINITE_GRID_ONLY','tested_n':n,'Q56':Q,'R56':R,'rows':rows,'cpu_seconds':time.process_time()-start}
(P/'cooling_pilot.json').write_text(json.dumps(out,indent=2)+'\n');print('rows',len(rows),'passes',sum(x['pass'] for x in rows));print(sorted(rows,key=lambda x:x['gap'],reverse=True)[:5])
