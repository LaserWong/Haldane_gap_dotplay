#!/usr/bin/env python3
"""Exact n48 direct finite window, with accepted48/96 anchors only."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,os,resource,time,sys
sys.set_int_max_str_digits(100000);P=Path(__file__).resolve().parent;ROOT=P.parents[1];B=10**24;start=time.process_time();os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));hashes={}
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
 for k in range(1,41):term=term*x/k;sm+=term
 nxt=term*x/41;lo=down(sm);hi=up(sm+nxt/(1-x/42))
 for _ in range(ct):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi
val=lambda x:{'exact':str(x),'display':float(x)}
data=json.loads(sealed('uniform_transfer_moment_assessment','results.json'));m={s:{int(j):tuple(F(v['exact']) for v in iv) for j,iv in dd['moment_intervals'].items()} for s,dd in data['hankel_caps'].items()};caps={s:F(dd['x_cap']['exact']) for s,dd in data['hankel_caps'].items()};nodes={};envelopes={}
for s,h in caps.items():
 a,b,c=[sum(m[s][j],F(0))/2 for j in (3,4,5)];raw=(h*b-c)/(h*a-b);nodes[s]=F((raw*10**10).__floor__(),10**10);assert 0<nodes[s]<h

def bounds(L):
 out=[]
 for s,h in caps.items():
  t=nodes[s];k=L//2-3;cc=(h**k-t**k-k*t**(k-1)*(h-t))/(h-t)**2;bb=k*t**(k-1)-2*cc*t;aa=t**k-k*t**k+cc*t*t
  hermite=up(sum(c*m[s][j][1 if c>=0 else 0] for c,j in zip((aa,bb,cc),(3,4,5))))
  M=m[s][5][1];q=M//h**5;packed=up(q*h**(L//2)+power(M-q*h**5,F(L,10))[1]);v=min(hermite,packed);out.append(v)
  envelopes[f'{s}_{L}']={'support_cap':val(h),'node':val(t),'coefficients':[str(x) for x in (aa,bb,cc)],'Hermite_upper':val(hermite),'packing_upper':val(packed),'chosen_upper':val(v)}
 a,b,c=out;return a+2*b+3*c,a+2*b

def ints(raw):return {k:int(v) for line in raw.decode().splitlines() for k,v in [line.split('=')]}
g48=ints(sealed('mps_excited_seed_review','independent_ground.out'));g96=ints(sealed('uniform_anchor96_100_review','anchors.out'));anchor_verdict=json.loads(sealed('uniform_anchor96_100_review','CLAIM_VERDICTS.json'));assert anchor_verdict['status']=='ACCEPTED independent physical anchors only'
R48=F(g48['H0_48'],g48['N0_48'])+48*F(700741,500000);R96=F(g96['H0_96'],g96['N0_96'])+96*F(700741,500000);assert g48['N0_48']>0 and g96['N0_96']>0 and max(R48,R96)<0
# Accepted tail theorem and direct-window lemma are dependencies; no provisional50 input.
prior=json.loads(sealed('uniform_seed_frontier_review','CLAIM_VERDICTS.json'));assert prior['status'].startswith('ACCEPTED') and prior['gap']=='19/5000' and prior['all_integer_L_at_least']==52
window_accept=json.loads(sealed('integer_window_refinement_review','ACCEPTANCE.json'));assert window_accept['status']=='ACCEPTED_INDEPENDENT_ANALYTIC_AND_EXACT_SCALAR_REVIEW'
sealed('integer_window_refinement_review','PROOF.md')
# A=T48(beta0), based on the48-site ground weight and trace cap.
beta0=F(21,2);Q48=bounds(48)[0];v48=expi(-beta0*R48)[0];assert 1<v48<Q48
A=down((v48/Q48)**2)
# B=S48(2beta0) from base ell26 and96-site anchor, all at beta21.
ell=26;n=48;r=F(2);q=F(n,ell);p=2*q;z,e=bounds(ell);D=up(z*z);E=up(e*e);tau=(D+11*E)/12;tau0=(D+3*E)/4;W=expi(-2*beta0*R96)[0]
def tail(t,degree):
 assert 0<t<tau<=tau0<=D
 vals=[]
 for x,y in [(F(0),F(0)),(tau-t,F(0)),(tau-t,tau0-tau),(F(0),tau0-t)]:
  zz=D-t-x-y;assert min(x,y,zz)>=0;vals.append(up(power(x,degree)[1]+2*power(y/2,degree)[1]+3*power(zz/3,degree)[1]))
 return max(vals)
t=power(W/D,1/(p-1))[0]-F(1,B);assert D*power(t,p-1)[1]<W and 2*t>D
steps=[{'t_lower':val(t),'initial_contradiction_upper':val(D*power(t,p-1)[1])}]
for _ in range(20):
 rem=tail(t,p);assert rem<W
 nt=power(W-rem,1/p)[0]-F(1,B)
 if nt<=t:break
 check=power(nt,p)[1]+rem;assert check<W;t=nt;steps.append({'t_lower':val(t),'contradiction_upper':val(check)})
Bsp=down(1/(1+tail(t,q)/power(t,q)[0])**2);assert Bsp>F(1,2)
C=down(A*A*root(2*Bsp-1,2)[0]);assert C>F(1,2)
finite_gap=F(53,10000);combined_gap=F(19,5000);margin=C-expi(beta0*finite_gap)[1]*(1-C);assert margin>0 and finite_gap>combined_gap
out={'status':'PRODUCER exact finite-window and coverage-extension candidate; independent new review pending','model':'uniform periodic spin-1 Heisenberg, unit bilinear coupling','n':48,'beta':val(beta0),'A_geometry':'T(48,21/2)','B_geometry':'S(48,21)','A_lower':val(A),'B_lower':val(Bsp),'Q48_beta0_upper':val(Q48),'v48_beta0_lower':val(v48),'R48_shifted':val(R48),'R96_shifted':val(R96),'spatial_construction':{'ell':ell,'beta':'21','q':str(q),'p':str(p),'D':val(D),'E':val(E),'tau':val(tau),'tau0':val(tau0),'W96_lower':val(W),'leading_steps':steps},'moment_envelopes':envelopes,'window':{'all_integer_lengths':[48,96],'thermal_purity_lower':val(C),'gap_lower':val(finite_gap),'exponential_margin':val(margin),'unique_ground_state':True},'combined_coverage':{'gap_lower':val(combined_gap),'all_integer_L_at_least':48,'prior_tail_from':52,'overlap':[52,96],'bootstrap_initialization_remains':52,'unique_ground_state':True,'not_claimed':'No48 bootstrap initialization, no below48, no minimality, no adaptive all-r exclusion'},'dependencies':{'n48_anchor':'mps_excited_seed_review independent_ground.out','n96_anchor':'uniform_anchor96_100_review','prior_gap':'uniform_seed_frontier_review','window_lemma':'integer_window_refinement_review'},'resources':{'cpu_seconds':time.process_time()-start,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'certificate.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('status','A_lower','B_lower','window','combined_coverage','resources')},indent=2))
