#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,os,resource,time,sys
sys.set_int_max_str_digits(100000);P=Path(__file__).resolve().parent;ROOT=P.parents[1];B=10**160;start=time.process_time();os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return F(-(-x.numerator*B//x.denominator),B)
def root(x,q):
 assert x>=0
 lo=0;hi=B
 while F(hi,B)**q<x:hi*=2
 while hi-lo>1:
  mid=(lo+hi)//2
  if F(mid,B)**q<=x:lo=mid
  else:hi=mid
 l,u=F(lo,B),F(hi,B);assert l**q<=x<=u**q;return l,u
def expi(x):
 if x<0:
  lo,hi=expi(-x);return down(1/hi),up(1/lo)
 ct=0
 while x>F(1,16):x/=2;ct+=1
 term=sm=F(1)
 for k in range(1,181):term=term*x/k;sm+=term
 nxt=term*x/181;lo=down(sm);hi=up(sm+nxt/(1-x/182))
 for _ in range(ct):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi
def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)
c=json.loads((P/'certificate.json').read_text());l=json.loads((P/'long_certificate.json').read_text());ell=F(c['dominant']['ell']);mj=F(c['moment_intervals']['J'][-1][1]);ra=(mj-ell**12)**3+3*F(l['N36']['bound']);S=(1+ra/ell**36)**-2;T=1-F(c['dominant']['q0'])
# Confirm the unchanged physical variational premise, with exact archived integers.
ints={k:int(v) for line in (ROOT/'audit/mps/contraction.out').read_text().splitlines() for k,v in [line.split('=')]};assert -700741*ints['V72']-500000*ints['U72']>0
s,t=down(S),down(T);n=36;beta=F(49,4);states=[];windows=[];gap=F('0.0214')
for j in range(14):
 K=down(s*s*t);assert K>F(1,2);w=(1+root(2*K-1,2)[0])/2;rho=(1-w)/w;di=down(t/(1+rho*rho));C=down((1-rho)*min(s*root(di,2)[0],di));assert C>F(1,2)
 e=expi(beta*gap)[1];margin=C-e*(1-C);assert margin>0,('window',j,float(margin))
 states.append({'round':j,'n':n,'beta':str(beta),'S':str(s),'T':str(t)})
 windows.append({'from':n,'to':2*n,'beta':str(beta),'purity_lower':str(C),'gap':str(gap),'margin':str(margin)})
 defect=max(1-s,1-t);amargin=1-5*defect*e
 if defect<=F(1,100) and amargin>0:
  asym={'from':n,'beta':str(beta),'defect':str(defect),'gap':str(gap),'exponential_margin':str(amargin)};break
 s=down(G(K));assert s>0;t=down(G(down(t*t*s)));assert t>0;n*=2;beta*=2
else:raise AssertionError('no asymptotic entry')
inputs=[P/'certificate.json',P/'long_certificate.json',ROOT/'audit/mps/contraction.out',P.parent/'uniform_seed_frontier_optimization/PROOF.md',P.parent/'integer_window_refinement_review/PROOF.md']
out={'status':'CONDITIONAL PRODUCER: not independent review and all18 published thermal inputs inherited','conditional_conclusion':{'all_integer_L_at_least':36,'gap':str(gap),'unique_ground_state':True},'seed':{'n':36,'beta':'49/4','S':str(S),'T72':str(T),'spatial_defect_decimal':float(1-S),'thermal_defect_decimal':float(1-T)},'states':states,'all_integer_windows':windows,'asymptotic':asym,'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'resources':{'cpu_seconds':time.process_time()-start,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'continuation_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',out['conditional_conclusion'],'asymptotic n',n,'beta',beta,'CPU',out['resources']['cpu_seconds'])
