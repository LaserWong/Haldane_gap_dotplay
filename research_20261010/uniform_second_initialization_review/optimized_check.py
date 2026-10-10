#!/usr/bin/env python3
"""Independent directed audit. No producer code imported or executed."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import hashlib,json,os,resource,time,sys
os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));sys.set_int_max_str_digits(100000);start=time.process_time()
P=Path(__file__).resolve().parent;ROOT=P.parents[1];A=P.with_name('uniform_second_initialization_scalar');GRID=10**110;hashes={};seals={}
def read(p):
 b=p.read_bytes();hashes[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return b
def js(p):return json.loads(read(p))
for folder in [A,P.with_name('uniform_cooled_seed_review'),P.with_name('uniform_seed_frontier_review'),P.with_name('integer_window_refinement_review'),P.with_name('uniform_source_scope_review')]:
 mf=js(folder/'MANIFEST_SHA256.json');mf=mf.get('files',mf)
 for f,h in mf.items():assert hashlib.sha256(read(folder/f)).hexdigest()==h
 seals[folder.name]=hashlib.sha256((folder/'MANIFEST_SHA256.json').read_bytes()).hexdigest()
assert seals[A.name]=='2ee9120d69863ab73babbcc9c07036cabcd787f9d8ad6b61f9f485656ccb1a59'
for f,h in js(A/'INPUT_SHA256.json').items():assert hashlib.sha256(read(ROOT/f)).hexdigest()==h
c=js(A/'certificate.json');orig=js(P/'original_scalar_results.json')
assert F(c['seed']['S'])==1-F(orig['p0']) and F(c['seed']['T72'])==1-F(orig['q0'])
assert c['seed']['n']==36 and F(c['seed']['beta'])==F(49,4)
for name in ['initialization','thermal72','trials']:assert read(P/'sources'/f'{name}.tex')+b'\n'==read(A/f'official_{name}.tex')
# Anchor U is PER BOND. The total shifted Rayleigh is72(U/V+a).
vals={k:int(v) for line in read(ROOT/'audit/mps/contraction.out').decode().splitlines() for k,v in [line.split('=')]};u,v=vals['U72'],vals['V72'];assert v>0 and -700741*v-500000*u>0
assert F(c['anchor']['shifted_Rayleigh'])==72*(F(u,v)+F(700741,500000))<0
for saved,own in zip(c['published_six_rounds'],orig['rounds']):assert saved['round']==own['round'] and F(saved['p'])==F(own['spatial_defect']) and F(saved['q'])==F(own['thermal_defect'])
def down(x):return F(x.numerator*GRID//x.denominator,GRID)
def up(x):return F(-((-x.numerator*GRID)//x.denominator),GRID)
def sqrtiv(x):
 assert x>=0
 n=isqrt(x.numerator*GRID*GRID//x.denominator);a=F(n,GRID);b=F(n+1,GRID);assert a*a<=x<=b*b;return a,b
def expiv(x):
 assert x>=0
 scale=0
 while x>F(1,8):x/=2;scale+=1
 tl=th=sl=sh=F(1)
 for k in range(1,141):tl=down(tl*x/k);th=up(th*x/k);sl+=tl;sh+=th
 lo=sl;hi=up(sh+up(th*x/141)/(1-x/142))
 for _ in range(scale):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi
def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)
last=None;margins=[]
assert len(c['improved_states'])==len(c['all_integer_windows'])==11
for j,(s,w) in enumerate(zip(c['improved_states'],c['all_integer_windows'])):
 n=36*2**j;beta=F(49,4)*2**j;S,T=F(s['S']),F(s['T']);assert s['round']==j and s['n']==n and F(s['beta'])==beta and 0<S<=1 and 0<T<=1
 if last is None:assert S<=F(c['seed']['S']) and T<=F(c['seed']['T72'])
 else:
  a,b=last;assert 0<S<=G(a*a*b) and 0<T<=G(b*b*S)
 K=S*S*T;assert K>F(1,2);r=sqrtiv(2*K-1)[0];rho=(1-r)/(1+r);d=T/(1+rho*rho);C=(1-rho)*min(S*sqrtiv(d)[0],d)
 assert (w['from'],w['to'])==(n,2*n) and F(w['beta'])==beta and F(w['gap'])==F(23,5000)
 saved=F(w['purity_lower']);assert F(1,2)<saved<=C
 margin=saved-expiv(beta*F(23,5000))[1]*(1-saved);assert 0<F(w['margin'])<=margin;margins.append(str(margin));last=S,T
asym=c['asymptotic'];assert asym['from']==n==36864 and F(asym['beta'])==beta==12544 and F(asym['gap'])==F(23,5000)
u=max(1-S,1-T);assert u==F(asym['defect'])<=F(1,100);am=1-5*u*expiv(beta*F(23,5000))[1];assert 0<F(asym['exponential_margin'])<=am
assert c['conditional_conclusion']=={'all_integer_L_at_least':36,'gap':'23/5000','unique_ground_state':True}
# Endpoint exact inequalities for the inherited small-defect recurrence/window.
e=F(1,100);assert (3-3*e+e*e)**2/(2*(1-e)**6)<=5 and (2+5*e)**2/(2*(1-2*e-5*e*e)**2)<=5
assert e-5*e*e-e**3>0 and 4*e*(1-e)<=(1-2*e)**2 and 4/(1-4*e)<=5
out={'status':'CONDITIONALLY ACCEPTED independent scalar theorem','condition':'all18 published beta49/4 physical I/P trace intervals; no full local thermal rerun claimed','gap':'23/5000','all_integer_L_at_least':36,'unique_ground_state':True,'canonical_seed':{'n':36,'beta':'49/4','thermal_coordinate':'T(72,49/4)'},'windows':11,'asymptotic_from':36864,'asymptotic_beta':12544,'window_margins':margins,'asymptotic_margin':str(am),'seals_verified':seals,'CPU_seconds':time.process_time()-start,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'optimized_results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','gap','all_integer_L_at_least','asymptotic_from','CPU_seconds','RSS_KiB']},indent=2))
