#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
from math import factorial,isqrt,comb
import ast,hashlib,json,os,resource,time
os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));st=time.process_time()
P=Path(__file__).resolve().parent;R=P.parents[1];src=R/'upstream/extracted/cases/haldane_reference_audit/published_scalar_enclosures.py'
tree=ast.parse(src.read_text());tab=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='B' for t in n.targets))
# Parse literal data only, never execute the imported source.
cent={};enc={};eps=F(30,10**6)
for j,(n,c,W) in enumerate(tab):
 seam='I' if j%2==0 else 'P';cent[n,seam]=F(c,10**6);x=F(49,4)*n*(F(3,2)-F(700741,500000));assert 0<x<15
 term=F(1);s=term
 for k in range(1,101):term*=x/k;s+=term
 d=isqrt(3**n)+1;err=d*(281*(d+1)+1);r=isqrt(W);assert r*r<=W<(r+1)**2
 lo=s*max(0,r-err)**2/2**110;hi=(s+term)*(r+1+err)**2/2**110
 assert lo-(cent[n,seam]-eps)>F(13,10**6) and cent[n,seam]+eps-hi>F(13,10**6)
 enc[f'{n}_{seam}']={'lower':str(lo),'upper':str(hi),'printed_total':str(W),'rerun':False}
J={n:(cent[n,'I']+3*cent[n,'P'])/4 for n in range(4,13)};N={n:(cent[n,'I']-cent[n,'P'])/4 for n in range(4,13)}
def mult(a,b):
 z=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):z[i+j]+=x*y
 return z
def evalp(p,x):return sum(c*x**j for j,c in enumerate(p))
QJ=[7,17,-280,-185,1000];QN=[12,0,-394,0,1000]
filters={};caps=[F(100139,100000),F(872,1000)]
for name,M,Q,v,target in [('J',J,QJ,caps[0],F('318604.54848175')),('N',N,QN,caps[1],F('48169.880699'))]:
 co=[F(0)]*4+mult(Q,Q);B=sum(c*M[j] for j,c in enumerate(co) if c)+eps*sum(abs(c) for c in co);assert B==target
 pos=evalp(co,v)-B;neg=evalp(co,-v)-B;assert pos>0 and neg>0
 filters[name]={'coefficients':list(map(str,co)),'summed_upper':str(B),'positive_ray_margin':str(pos),'negative_ray_margin':str(neg)}
# Both signed exterior rays checked symbolically, not a finite root scan.
plus=[sum(QJ[j]*comb(j,k) for j in range(k,5)) for k in range(5)]
minus=[sum(QJ[j]*(-1)**j*comb(j,k) for j in range(k,5)) for k in range(5)]
assert plus==[559,2902,5165,3815,1000] and minus==[895,3978,6275,4185,1000]
assert evalp(QN,caps[1])>0 and 1000*caps[1]**2>197
mJ,mN=F('1.0657205'),F('.2783155');assert J[12]+eps==mJ and N[12]+eps==mN
ell=F(999,1000)
def cap(m,h,r):
 q=m//h;return q*h**r+(m-q*h)**r
def BN(k):return 3*cap(mN,caps[1]**12,k//12)
def RA(k):return BN(k)+(mJ-ell**12)**(k//12)
contr=1-cap(mJ,ell**12,6)-BN(72);assert contr>F('.0693')
p=1-(1+RA(36)/ell**36)**-2;q=1-(caps[0]**72+RA(72))**-2;assert p<F('.047916') and q<F('.181521')
p0,q0=p,q
expected=[(F(151249,2500000),F(433453,2500000)),(F(343303,5000000),F(1632381,10**7)),(F(44601,625000),F(361773,2500000)),(F(632939,10**7),F(1055161,10**7)),(F(375793,10**7),F(445941,10**7)),(F(84513,10**7),F(27493,5*10**6))]
def up(x):return F(-((-x.numerator*10**7)//x.denominator),10**7)
def upd(u):assert 0<=u<1;return u*u/(2*(1-u)**2)
rows=[]
for j,want in enumerate(expected,1):
 p=up(upd(1-(1-p)**2*(1-q)));q=up(upd(1-(1-q)**2*(1-p)));assert (p,q)==want
 rows.append({'round':j,'n':36*2**j,'beta':str(F(49,4)*2**j),'spatial_defect':str(p),'thermal_length':72*2**j,'thermal_defect':str(q)})
assert p<F(1,100) and q<F(1,100)
# Changing odd moments to absolute values does not preserve the given filter sums.
wrong=sum(c*abs(N[j]) for j,c in enumerate([0]*4+mult(QN,QN)) if c)
assert all(N[j]<0 for j in (5,7,9,11))
out={'status':'PASS conditional scalar reconstruction; no physical thermal rerun','18_enclosures':enc,'filters':filters,'J_positive_shift_coefficients':plus,'J_negative_shift_coefficients':minus,'dominant_mass_contradiction_margin':str(contr),'p0':str(p0),'q0':str(q0),'rounds':rows,'original_even_length_threshold':2304,'original_gap':'log(20)/784','inherited_thermal_intervals':18,'physical_second_temperature_totals_locally_verified':False,'resource_cpu_seconds':time.process_time()-st}
(P/'original_scalar_results.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS18 enclosures, signed filters, exterior domains, six staggered updates; CPU',time.process_time()-st)
