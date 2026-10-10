#!/usr/bin/env python3
"""Exact n48 direct finite window, with accepted48/96 anchors only."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,os,resource,time,sys
sys.set_int_max_str_digits(100000);P=Path(__file__).resolve().parent;ROOT=P.parents[1];B=10**80;start=time.process_time();os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));hashes={}
def read(p):
 raw=p.read_bytes();hashes[str(p.relative_to(ROOT))]=hashlib.sha256(raw).hexdigest();return raw
def sealed(folder,file):
 p=P.parent/folder;mf=json.loads(read(p/'MANIFEST_SHA256.json'));mf=mf.get('files',mf);raw=read(p/file);assert hashlib.sha256(raw).hexdigest()==mf[file];return raw

def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return F(-(-x.numerator*B//x.denominator),B)
def root(x,q):
 assert x>=0
 if q==1:return down(x),up(x)
 lo=0;hi=B
 while F(hi,B)**q<x:hi*=2
 while hi-lo>1:
  mid=(lo+hi)//2
  if F(mid,B)**q<=x:lo=mid
  else:hi=mid
 l,u=F(lo,B),F(hi,B);assert l**q<=x<=u**q;return l,u

def power(x,r):
 r=F(r);return root(x**r.numerator,r.denominator)
def expi(x):
 if x<0:
  lo,hi=expi(-x);return down(1/hi),up(1/lo)
 ct=0
 while x>F(1,16):x/=2;ct+=1
 term=sm=F(1)
 for k in range(1,121):term=term*x/k;sm+=term
 nxt=term*x/121;lo=down(sm);hi=up(sm+nxt/(1-x/122))
 for _ in range(ct):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi
val=lambda x:{'exact':str(x),'display':float(x)}
# Published table is an inherited premise, not a locally rerun thermal certificate.
centers={4:(124885379,65757),5:(2925,2960742),6:(12870614,286599),7:(54069,1920414),8:(4639283,510140),9:(195455,1514846),10:(2654823,675419),11:(377629,1314544),12:(1900547,787405)}
eps=F(30,10**6);J={n:F(z+3*p,4*10**6) for n,(z,p) in centers.items()};N={n:F(z-p,4*10**6) for n,(z,p) in centers.items()}
def square_filter(coeff):
 result={}
 for i,a in enumerate(coeff):
  for j,b in enumerate(coeff):result[4+i+j]=result.get(4+i+j,F(0))+a*b
 return {k:v for k,v in result.items() if v}
filters={};U=F(100139,100000);V=F(872,1000)
for name,M,c,cap,expected in [('J',J,[7,17,-280,-185,1000],U,F('318604.54848175')),('N',N,[12,0,-394,0,1000],V,F('48169.880699'))]:
 f=square_filter(c);bound=sum(v*M[k] for k,v in f.items())+eps*sum(abs(v) for v in f.values());assert bound==expected
 values=[sum(v*x**k for k,v in f.items()) for x in [cap,-cap]];assert min(values)>bound
 filters[name]={'coefficients':{k:str(v) for k,v in f.items()},'sum_upper':str(bound),'cap':str(cap),'endpoint_margins':[str(v-bound) for v in values]}
# Exterior-ray monotonicity is audited symbolically in PROOF.md.
mJ=F('1.0657205');mN=F('.2783155');assert J[12]+eps==mJ and N[12]+eps<=mN
ell=F(999,1000)
def capped(m,h,k):
 assert k.denominator==1;q=m//h;return q*h**int(k)+(m-q*h)**int(k)
def ntail(k):return 3*capped(mN,V**12,F(k,12))
def tail(k):return ntail(k)+(mJ-ell**12)**(k//12)
assert capped(mJ,ell**12,F(6))+ntail(72)<1
# Existing independently reconstructed 72-site physical anchor; ordinary per-bond U/V.
raw=read(ROOT/'audit/mps/contraction.out');ints={k:int(v) for line in raw.decode().splitlines() for k,v in [line.split('=')]};u,v=ints['U72'],ints['V72'];assert v>0 and -700741*v-500000*u>0
read(ROOT/'audit/APPENDIX_A_BRIDGE.md');read(ROOT/'audit/mps/build_mps.py');read(ROOT/'audit/mps/mps_exact.cpp')
S=(1+tail(36)/ell**36)**-2;T=(U**72+tail(72))**-2
assert 1-S<F('.047916') and 1-T<F('.181521')
def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)
# Reproduce every published rounded defect exactly.
p,q=1-S,1-T;official=[]
expected=[(F(151249,2500000),F(433453,2500000)),(F(343303,5000000),F(1632381,10000000)),(F(44601,625000),F(361773,2500000)),(F(632939,10000000),F(1055161,10000000)),(F(375793,10000000),F(445941,10000000)),(F(84513,10000000),F(27493,5000000))]
for i,(pe,qe) in enumerate(expected):
 pp=1-G((1-p)**2*(1-q));p=F(-(-pp.numerator*10**7//pp.denominator),10**7);qq=1-G((1-q)**2*(1-p));q=F(-(-qq.numerator*10**7//qq.denominator),10**7);assert (p,q)==(pe,qe);official.append({'round':i+1,'p':str(p),'q':str(q)})
assert max(p,q)<F(1,100)
# Stronger high-precision continuation and signed all-integer windows.
gap=F(46,10000);s,t=down(S),down(T);n=36;beta=F(49,4);states=[];windows=[]
for j in range(16):
 K=down(s*s*t);assert K>F(1,2);w=(1+root(2*K-1,2)[0])/2;rho=(1-w)/w;di=down(t/(1+rho*rho));C=down((1-rho)*min(s*root(di,2)[0],di));assert C>F(1,2)
 e=expi(beta*gap)[1];margin=C-e*(1-C);assert margin>0
 states.append({'round':j,'n':n,'beta':str(beta),'S':str(s),'T':str(t)})
 windows.append({'from':n,'to':2*n,'beta':str(beta),'purity_lower':str(C),'gap':str(gap),'margin':str(margin)})
 defect=max(1-s,1-t);amargin=1-5*defect*e
 if defect<=F(1,100) and amargin>0:
  asym={'from':n,'beta':str(beta),'defect':str(defect),'gap':str(gap),'exponential_margin':str(amargin)};break
 s=down(G(K));assert s>0;t=down(G(down(t*t*s)));assert t>0;n*=2;beta*=2
else:raise AssertionError('no asymptotic entry')
# General all-integer interpolation and bootstrap dependencies.
for folder,file in [('uniform_seed_frontier_review','CLAIM_VERDICTS.json'),('uniform_seed_frontier_optimization','PROOF.md'),('integer_window_refinement_review','PROOF.md')]:sealed(folder,file)
out={'status':'CONDITIONAL PRODUCER scalar certificate; inherits all18 published beta49/4 thermal intervals, not locally reconstructed full physical certificate','model':'periodic uniform spin1 Heisenberg, unit bilinear exchange, physical lengths at least4','thermal_premise':{'beta':'49/4','centers_in_units_1e-6':centers,'absolute_error':'3/100000','seams':['I','P']},'filters':filters,'anchor':{'length':72,'shifted_Rayleigh':str(72*F(u,v)+72*F(700741,500000)),'source':'audit/mps/contraction.out'},'seed':{'n':36,'beta':'49/4','S':str(S),'T72':str(T)},'published_six_rounds':official,'improved_states':states,'all_integer_windows':windows,'asymptotic':asym,'conditional_conclusion':{'all_integer_L_at_least':36,'gap':str(gap),'unique_ground_state':True},'resources':{'cpu_seconds':time.process_time()-start,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'certificate.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n');print(json.dumps({'status':out['status'],'S36':float(S),'T72':float(T),'conditional_conclusion':out['conditional_conclusion'],'asymptotic':asym,'resources':out['resources']},indent=2))
