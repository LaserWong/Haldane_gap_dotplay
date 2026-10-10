#!/usr/bin/env python3
"""Independent verification of certificate inequalities, not producer execution."""
from fractions import Fraction as Q
from pathlib import Path
import os,sys,resource,json,hashlib,time,itertools
sys.set_int_max_str_digits(100000)
P=Path(__file__).resolve().parent;R=P.parents[1];A=P.with_name('uniform_cooled_seed_optimization');M=P.with_name('uniform_transfer_moment_assessment');V=P.with_name('uniform_transfer_moment_review')
aff=os.sched_getaffinity(0);os.sched_setaffinity(0,{5 if 5 in aff else min(aff)});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600));start=time.process_time();inputs={}
def read(p):
 b=p.read_bytes();inputs[str(p.relative_to(R))]=hashlib.sha256(b).hexdigest();return b
def js(p):return json.loads(read(p))
def exact(v):return Q(v['exact'])
def floor(v,b=10**36):return Q(v.numerator*b//v.denominator,b)
def ceil(v,b=10**36):return Q(-((-v.numerator*b)//v.denominator),b)
def roots(v,k):
 assert v>=0 and k>=1
 if k==1:return v,v
 if not v:return Q(0),Q(0)
 scale=10**36;target=v.numerator*scale**k;den=v.denominator;lo=0;hi=scale
 while hi**k*den<target:hi*=2
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**k*den<=target:lo=mid
  else:hi=mid
 low,high=Q(lo,scale),Q(hi,scale);assert low**k<=v<=high**k
 return low,high
def power(v,p):
 p=Q(p);assert p>=0
 return roots(v**p.numerator,p.denominator)
def exp_upper(x):
 assert x>=0;k=0
 while x>Q(1,8):x/=2;k+=1
 term=total=Q(1)
 for j in range(1,71):term*=x/j;total+=term
 high=ceil(total+(term*x/71)/(1-x/72))
 for j in range(k):high=ceil(high*high)
 return high
sealcounts={}
for folder in (A,M,V):
 manifest=js(folder/'MANIFEST_SHA256.json')
 for f,h in manifest.items():assert hashlib.sha256(read(folder/f)).hexdigest()==h
 sealcounts[folder.name]=len(manifest)
assert inputs[str((A/'MANIFEST_SHA256.json').relative_to(R))]=='13c41cfac38c43a6199bfceebc98be4379773c733d1c59dfdb93af03881a037c'
for f,h in js(A/'INPUT_SHA256.json').items():assert hashlib.sha256(read(R/f)).hexdigest()==h
for f,h in js(M/'INPUT_SHA256.json').items():assert hashlib.sha256(read(R/f)).hexdigest()==h
for doc in ('audit/APPENDIX_A_BRIDGE.md','audit/AUDIT_REPORT.md','research_20261010/root_review/FINITE_WINDOW_INTERPOLATION.md','research_20261010/root_review/INTERPOLATION_DOMAIN.md','heat_trace/PROOF.md','research_20261010/nonperturbative_mps_review/d26_rebuild_results.json','research_20261010/uniform_seed_size_review/independent_d26.py'):
 read(R/doc)
d=js(M/'results.json');caps={s:exact(v['x_cap']) for s,v in d['hankel_caps'].items()};m5={s:exact(v['moment_intervals']['5'][1]) for s,v in d['hankel_caps'].items()}
def sectors(L):
 assert L>=10 and L%2==0
 out=[]
 for s in ('trivial','complex','vector'):
  cap=caps[s];h=cap**5;mass=m5[s];q=int(mass/h);rem=mass-q*h
  assert 0<=rem<h
  out.append(q*cap**(L//2)+power(rem,Q(L,10))[1])
 return out
def bounds(L):
 a,b,c=sectors(L);return a+2*b+3*c,a+2*b
# Fresh contraction outputs must match producer, and rebuilt blocks must match audited blocks.
assert read(P/'d26_blocks.txt')==read(R/'audit/mps/mps_blocks.txt')
assert read(P/'benchmark48.out')==read(A/'benchmark48.out')
assert read(P/'new_lengths.out')==read(A/'new_lengths.out')
def ints(p):return {k:int(v) for line in read(p).decode().splitlines() for k,v in [line.split('=')]}
new=ints(P/'new_lengths.out');arch=ints(R/'audit/mps/contraction.out')
assert new['H0_120']==120*arch['U120'] and new['N0_120']==arch['V120']
anchor={}
for n in (104,108,112,120):
 assert new['N0_'+str(n)]>0
 num=500000*new['H0_'+str(n)]+700741*n*new['N0_'+str(n)]
 assert num<0
 anchor[n]={'shifted_Rayleigh':str(Q(num,500000*new['N0_'+str(n)])),'negative_numerator':str(num)}
G=lambda z:1-(1-z)**2/(2*z*z)
rows=[]
for cert in js(A/'certificates.json')['rows']:
 n=cert['seed_n'];ell=cert['base_moment_length'];r=exact(cert['cooling_ratio']);beta=exact(cert['beta']);gap=exact(cert['gap']);p=Q(2*n,ell);q=p/2
 assert n%2==ell%2==0 and q>=1 and r>=1 and beta==Q(21,2)*r
 assert cert['anchor_length']==2*n and exact(cert['anchor_shifted_Rayleigh'])==Q(anchor[2*n]['shifted_Rayleigh'])
 z,other=bounds(ell);D,E=exact(cert['D']),exact(cert['E'])
 assert D>=power(z,r)[1] and E>=power(other,r)[1]
 tau=(D+11*E)/12;tau0=(D+3*E)/4
 assert tau==exact(cert['tau']) and tau0==exact(cert['tau0']) and D>=tau0>=tau
 def tail(t,exponent):
  assert 0<=t<=tau
  # Enumerate active-constraint intersections, independently of producer vertex list.
  corners=[]
  lines=[(1,0,Q(0)),(0,1,Q(0)),(1,0,tau-t),(1,1,tau0-t)]
  for (a,b,c),(d,e,f) in itertools.combinations(lines,2):
   det=a*e-b*d
   if not det:continue
   x=Q(c*e-b*f,det);y=Q(a*f-c*d,det)
   if x>=0 and y>=0 and x<=tau-t and x+y<=tau0-t:
    zz=D-t-x-y;assert zz>=0
    corners.append(power(x,exponent)[1]+2*power(y/2,exponent)[1]+3*power(zz/3,exponent)[1])
  assert len(corners)>=4
  return max(corners)
 hist=cert['dominant_mass_steps'];t=exact(hist[0]['t_lower'])
 assert t==Q(4,5) and D*power(t,p-1)[1]<1 and 2*t>D
 history_margins=[]
 for step in hist[1:]:
  nxt=exact(step['t_lower']);assert t<nxt<tau
  if cert['mode']=='original_squared_tail':assert p==4;rest=tail(t,2)**2
  else:assert cert['mode']=='direct_sector_power';rest=tail(t,p)
  contradiction=power(nxt,p)[1]+rest
  assert contradiction<1 and contradiction<=exact(step['contradiction_upper'])
  history_margins.append(str(1-contradiction));t=nxt
 S=exact(cert['S_seed']);T=exact(cert['T_seed']);Qanchor=exact(cert['Z_anchor_beta0_upper'])
 assert Qanchor>=bounds(2*n)[0]>1
 Sbound=1/(1+tail(t,q)/power(t,q)[0])**2
 Tbound=1/(1+power(Qanchor-1,r)[1])**2
 assert 0<S<=Sbound<=1 and 0<T<=Tbound<=1
 assert exact(cert['states'][0]['S'])==S and exact(cert['states'][0]['T'])==T
 states=cert['states'];window_results=[]
 for i,state in enumerate(states):
  sn,tn=exact(state['S']),exact(state['T']);nn=state['n'];bt=exact(state['beta'])
  assert 0<sn<=1 and 0<tn<=1 and nn==n*2**i and bt==beta*2**i and state['round']==i
  if i:
   prev=states[i-1];sp,tp=exact(prev['S']),exact(prev['T'])
   assert sn==floor(G(sp*sp*tp),10**24)
   assert tn==floor(G(tp*tp*sn),10**24) # newly updated S, staggered thermal length4n
  pure=sn*sn*tn;assert pure>Q(1,2)
  w=(1+roots(2*pure-1,2)[0])/2;rho=(1-w)/w;dd=tn/(1+rho*rho)
  Cbound=(1-rho)*min(sn*roots(dd,2)[0],dd)
  win=cert['finite_integer_windows'][i];C=exact(win['thermal_purity_lower'])
  assert win['from']==nn and win['to']==2*nn and exact(win['beta'])==bt and exact(win['gap'])==gap
  assert Q(1,2)<C<=Cbound<=1
  margin=C-exp_upper(bt*gap)*(1-C);assert margin>0 and margin>=exact(win['exponential_margin'])
  window_results.append({'from':nn,'to':2*nn,'C':str(C),'margin_lower':str(margin)})
 asym=cert['asymptotic'];last=states[-1];u=max(1-exact(last['S']),1-exact(last['T']))
 assert 0<u<=Q(1,100) and u==exact(asym['common_defect']) and asym['from']==last['n']
 assert exact(asym['beta'])==exact(last['beta']) and exact(asym['gap'])==gap
 margin=1-5*u*exp_upper(exact(last['beta'])*gap)
 assert margin>0 and margin>=exact(asym['exponential_margin'])
 rows.append({'seed_n':n,'gap':str(gap),'beta':str(beta),'mode':cert['mode'],'S_lower':str(S),'T_2n_lower':str(T),'dominant_mass_final':str(t),'dominant_contradiction_margins':history_margins,'windows':window_results,'asymptotic_from':asym['from'],'asymptotic_margin_lower':str(margin),'accepted_scope':f'all integer periodic L >= {n}'})
# Check endpoint constants for the continuous analytic small-defect theorem.
u=Q(1,100)
constants={'spatial_contraction':(3-3*u+u*u)**2/(2*(1-u)**6),'thermal_contraction':(2+5*u)**2/(2*(1-2*u-5*u*u)**2),'interpolation_coefficient':Q(3,2)+5*u+2/(1-2*u),'gap_coefficient':4/(1-4*u)}
assert constants['spatial_contraction']<5 and constants['thermal_contraction']<5 and constants['interpolation_coefficient']<4 and constants['gap_coefficient']<5 and u-5*u*u-u**3>0
out={'status':'PASS independent physical contractions and scalar inequalities; see analytic proof','producer_manifest_sha256':inputs[str((A/'MANIFEST_SHA256.json').relative_to(R))],'seals_verified':sealcounts,'anchors':anchor,'rows':rows,'small_defect_endpoint_constants':{k:str(v) for k,v in constants.items()},'resources':{'cpu_seconds':time.process_time()-start,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'scalar_results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n')
print(json.dumps({'status':out['status'],'rows':[{k:r[k] for k in ('seed_n','gap','beta','asymptotic_from','accepted_scope')} for r in rows],'resources':out['resources']},indent=2))
