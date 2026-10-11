import certify as c
import math,json,time
P=c.P;start=time.process_time();n=24;Q=float(c.sector('J',48)+3*c.sector('N',48));R=float(c.F(c.ints['H0_48'],c.ints['N0_48'])+48*c.F(700741,500000));v=math.exp(-12.25*R)
G=lambda x:1-(1-x)**2/(2*x*x)
def run(s,t,b):
 K=s*s*t
 if K<=.5:return False,0,0,'joint',0.
 w=(1+math.sqrt(2*K-1))/2;rho=(1-w)/w;d=t/(1+rho*rho);p=25/24;C=s**(2-p)*d**(p/2)*(1-rho**p)
 return C>.5,(math.log(C/(1-C))/b if C>.5 else 0.),0,'odd25',C
rows=[]
for ell in [12]+list(range(16,25,2)):
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
  s=(1+tail(t0,q)/t0**q)**-2;t=(1+(Q/v-1)**r)**-2;ok,g,j,gate,C25=run(s,t,12.25*r)
  rows.append({'ell':ell,'r':r,'S':s,'T':t,'pass':ok,'gap':g,'round':j,'gate':gate,'C25':C25})
out={'status':'FLOATING_FINITE_GRID_ONLY','tested_n':n,'Q48':Q,'R48':R,'rows':rows,'cpu_seconds':time.process_time()-start}
(P/'cooling_pilot.json').write_text(json.dumps(out,indent=2)+'\n');print('rows',len(rows),'passes',sum(x['pass'] for x in rows));print(sorted(rows,key=lambda x:x['C25'],reverse=True)[:5])
