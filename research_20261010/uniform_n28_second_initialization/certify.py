#!/usr/bin/env python3
import os,resource,time,json,hashlib,sys
from fractions import Fraction as F
from pathlib import Path
os.sched_setaffinity(0,{2});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));sys.set_int_max_str_digits(100000)
P=Path(__file__).resolve().parent;ROOT=P.parents[1];B=10**100;start=time.process_time();inputs={}
def read(p):
 b=p.read_bytes();inputs[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return b
C=json.loads(read(P.parent/'uniform_second_moment_optimization/certificate.json'));L=json.loads(read(P.parent/'uniform_smaller_second_initialization/long_certificate.json'))
for name,h in [('uniform_second_moment_optimization','dc81945f85281a33df1b272a7a054b6f5d9b5fa32e8c7a1868c26e07bc97ec85'),('uniform_second_moment_review','dbdea168300fa8a014c4a1fcbb72a6f64d1f8ddb3250949eeeed067d55c329de'),('uniform_second_thermal_full_review','792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94')]:
 assert hashlib.sha256(read(P.parent/name/'MANIFEST_SHA256.json')).hexdigest()==h
for dep in [ROOT/'audit/mps/mps_blocks.txt',P/'contract_ground.cpp',ROOT/'audit/mps/build_mps.py',P.parent/'uniform_cooled_seed_optimization/PROOF.md',P.parent/'integer_window_refinement_review/PROOF.md']:
 read(dep)
ints={k:int(v) for line in read(P/'anchor56.out').decode().splitlines() for k,v in [line.split('=')]}
if (P/'anchor60.out').exists():ints.update({k:int(v) for line in read(P/'anchor60.out').decode().splitlines() for k,v in [line.split('=')]})
def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return F(-(-x.numerator*B//x.denominator),B)
def root(x,q):
 assert x>=0
 if q==1:return down(x),up(x)
 lo=0;hi=B
 while F(hi,B)**q<x:hi*=2
 while hi-lo>1:
  m=(lo+hi)//2
  if F(m,B)**q<=x:lo=m
  else:hi=m
 l,u=F(lo,B),F(hi,B);assert l**q<=x<=u**q;return l,u
def power(x,r):
 r=F(r);return root(x**r.numerator,r.denominator)
def expi(x):
 if x<0:
  l,u=expi(-x);return down(1/u),up(1/l)
 ct=0
 while x>F(1,16):x/=2;ct+=1
 term=s=F(1)
 for k in range(1,121):term=term*x/k;s+=term
 nxt=term*x/121;l=down(s);u=up(s+nxt/(1-x/122))
 for _ in range(ct):l=down(l*l);u=up(u*u)
 return l,u
def pack(m,h,r):
 q=m//h;return up(q*power(h,r)[1]+power(m-q*h,r)[1])
U=F(C['filters']['J+']['cap']);V=F(C['filters']['N-']['cap']);mj=F(C['moment_intervals']['J'][-1][1]);mn=F(C['moment_intervals']['N'][-1][1])
def sector(s,n):
 m,h=(mj,U**12) if s=='J' else (mn,V**12);v=pack(m,h,F(n,12));key=f'{s}{n}'
 return min(v,F(L[key]['bound'])) if key in L else v
G=lambda x:1-(1-x)**2/(2*x*x)
def certify(n,gap):
 norm=ints[f'N0_{2*n}'];energy=ints[f'H0_{2*n}'];assert norm>0;R=F(energy,norm)+2*n*F(700741,500000);assert R<0
 # Only use anchor sign: Z_(2n)(beta0)>1 and Z_(2n)(2beta0)>1.
 lo,hi=9900000000,10000000000
 while hi-lo>1:
  k=(lo+hi)//2;e=F(k,10**10)
  if pack(mj,e**12,F(2*n,12))+3*sector('N',2*n)<1:lo=k
  else:hi=k
 ell=F(lo,10**10);forcing=1-pack(mj,ell**12,F(2*n,12))-3*sector('N',2*n);assert forcing>0 and ell>F(C['filters']['J-']['cap'])
 tail=up(power(mj-ell**12,F(n,12))[1]+3*sector('N',n));S=down((1+tail/ell**n)**-2);Q=sector('J',2*n)+3*sector('N',2*n);T=down(Q**-2)
 s,t=S,T;beta=F(49,4);nn=n;states=[];windows=[];asym=None
 for j in range(14):
  K=down(s*s*t)
  if K<=F(1,2):return {'n':n,'status':'FAIL_joint','round':j,'S':str(s),'T':str(t)}
  w=(1+root(2*K-1,2)[0])/2;rho=(1-w)/w;d=down(t/(1+rho*rho));cc=down((1-rho)*min(s*root(d,2)[0],d));e=expi(beta*gap)[1];margin=cc-e*(1-cc)
  if margin<=0:return {'n':n,'status':'FAIL_window','round':j,'gap':str(gap),'purity':str(cc),'states':states,'windows':windows,'S':str(S),'T':str(T),'ell':str(ell),'forcing_margin':str(forcing),'anchor_shifted_Rayleigh':str(R)}
  states.append({'n':nn,'beta':str(beta),'S':str(s),'T':str(t)});windows.append({'from':nn,'to':2*nn,'purity':str(cc),'margin':str(margin)})
  defect=max(1-s,1-t);amargin=1-5*defect*e
  if defect<=F(1,100) and amargin>0:
   asym={'from':nn,'beta':str(beta),'defect':str(defect),'margin':str(amargin)};break
  s=down(G(K));assert s>0;t=down(G(down(t*t*s)));assert t>0;nn*=2;beta*=2
 if asym is None:return {'n':n,'status':'FAIL_asymptotic','gap':str(gap)}
 return {'n':n,'status':'PASS_PRODUCER','gap':str(gap),'beta':'49/4','anchor_length':2*n,'shifted_Rayleigh':str(R),'ell':str(ell),'forcing_margin':str(forcing),'tail':str(tail),'Q':str(Q),'S':str(S),'T':str(T),'states':states,'windows':windows,'asymptotic':asym,'all_integer_L_at_least':n,'unique_ground_state':True}
if __name__=='__main__':
 zero=certify(28,F(0));direct=certify(28,F(179,10000));assert direct['windows'][0]['from']==28 and direct['windows'][0]['to']==56
 old=P.parent/'uniform_smaller_second_initialization';assert hashlib.sha256(read(old/'MANIFEST_SHA256.json')).hexdigest()=='fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84'
 accepted=json.loads(read(old/'certificate.json'));row=next(v for v in accepted['rows'] if v['n']==30);assert F(row['gap'])==F(179,10000) and row['status']=='PASS_PRODUCER'
 out={'status':'Exact producer finite-window coverage extension; not n28 bootstrap initialization','n28_zero_gap_continuation_test':zero,'n28_gap_0179_test':direct,'direct_window':direct['windows'][0],'combined_claim':{'gap':'179/10000','all_integer_L_at_least':28,'unique_ground_state':True,'bootstrap_initialization':30,'coverage_onset':28,'union':['28..56 direct window','30..infinity inherited smaller initialization']},'resources':{'cpu_seconds':time.process_time()-start,'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
 (P/'certificate.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n');print(json.dumps(out['combined_claim']));print('zero-gap first failing window',zero['round'],float(F(zero['purity'])));print(out['resources'])
