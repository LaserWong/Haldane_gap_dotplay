#!/usr/bin/env python3
"""Independent exact direct-window replay from sealed moment and Rayleigh inputs."""
from pathlib import Path
from fractions import Fraction as F
import os,resource,sys,json,hashlib,time,itertools
sys.set_int_max_str_digits(1000000)
P=Path(__file__).resolve().parent;ROOT=P.parents[1];A=P.with_name('uniform_n48_direct_window');M=P.with_name('uniform_transfer_moment_assessment');AR=P.with_name('uniform_anchor96_100_review')
os.sched_setaffinity(0,{5 if 5 in os.sched_getaffinity(0) else min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));start=time.process_time();B=10**40;hashes={}
def read(p):
 b=p.read_bytes();hashes[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return b
def js(p):return json.loads(read(p))
def floor(v,b=B):return F(v.numerator*b//v.denominator,b)
def ceil(v,b=B):return F(-((-v.numerator*b)//v.denominator),b)
def roots(v,k):
 assert v>=0 and k>=1
 if k==1:return v,v
 if not v:return F(0),F(0)
 lo=0;hi=B;n=v.numerator*B**k;d=v.denominator
 while hi**k*d<n:hi*=2
 while hi-lo>1:
  mid=(hi+lo)//2
  if mid**k*d<=n:lo=mid
  else:hi=mid
 a,b=F(lo,B),F(hi,B);assert a**k<=v<=b**k;return a,b
def power(v,q):
 q=F(q);return roots(v**q.numerator,q.denominator)
def expiv(x):
 if x<0:
  a,b=expiv(-x);return floor(1/b),ceil(1/a)
 k=0
 while x>F(1,8):x/=2;k+=1
 termlo=termhi=sumlo=sumhi=F(1)
 for j in range(1,81):
  termlo=floor(termlo*x/j);termhi=ceil(termhi*x/j);sumlo+=termlo;sumhi+=termhi
 rem=ceil(termhi*x/81)/(1-x/82);lo=sumlo;hi=ceil(sumhi+rem)
 for j in range(k):lo=floor(lo*lo);hi=ceil(hi*hi)
 return lo,hi
def logunit(x):
 assert 1<=x<=2
 v=(x-1)/(x+1);lo=floor(v);hi=ceil(v);sl=su=F(0)
 for j in range(96):
  sl+=2*floor(lo/(2*j+1));su+=2*ceil(hi/(2*j+1));lo=floor(lo*v*v);hi=ceil(hi*v*v)
 rem=2*hi/(193*(1-v*v));return sl,ceil(su+rem)
LOG2=logunit(F(2))
def logiv(x):
 assert x>0
 if x<1:
  a,b=logiv(1/x);return -b,-a
 shift=0
 while x>=2:x/=2;shift+=1
 a,b=logunit(x);return a+shift*LOG2[0],b+shift*LOG2[1]
G=lambda z:1-(1-z)**2/(2*z*z)
seals={}
for folder in (A,M,AR,P.with_name('mps_excited_seed_review'),P.with_name('uniform_seed_frontier_review'),P.with_name('integer_window_refinement_review'),P.with_name('uniform_source_scope_review')):
 mf=js(folder/'MANIFEST_SHA256.json');mf=mf.get('files',mf)
 for f,h in mf.items():assert hashlib.sha256(read(folder/f)).hexdigest()==h
 seals[folder.name]=hashlib.sha256((folder/'MANIFEST_SHA256.json').read_bytes()).hexdigest()
assert seals['uniform_n48_direct_window']=='720a4243609cf64f451cd138f5297a110ad2b0d79db57994202e0ef300f3b65e'
for f,h in js(A/'INPUT_SHA256.json').items():assert hashlib.sha256(read(ROOT/f)).hexdigest()==h
cert=js(A/'certificate.json');data=js(M/'results.json');ex=lambda x:F(x['exact']);caps={s:ex(v['x_cap']) for s,v in data['hankel_caps'].items()};mom={s:{int(j):tuple(ex(v) for v in iv) for j,iv in r['moment_intervals'].items()} for s,r in data['hankel_caps'].items()};nodes={}
for s,h in caps.items():
 a,b,c=[sum(mom[s][j])/2 for j in (3,4,5)];nodes[s]=floor((h*b-c)/(h*a-b),10**10);assert 0<nodes[s]<h
checks={}
def envelope(L):
 vals=[]
 for s,h in caps.items():
  t=nodes[s];k=L//2-3;cc=(h**k-t**k-k*t**(k-1)*(h-t))/(h-t)**2;bb=k*t**(k-1)-2*cc*t;aa=(1-k)*t**k+cc*t*t
  rec=cert['moment_envelopes'][f'{s}_{L}'];assert ex(rec['support_cap'])==h and ex(rec['node'])==t and tuple(map(F,rec['coefficients']))==(aa,bb,cc)
  hermite=sum(co*mom[s][j][int(co>=0)] for co,j in zip((aa,bb,cc),(3,4,5)))
  assert ex(rec['Hermite_upper'])==ceil(hermite,10**24)
  M=mom[s][5][1];h5=h**5;n=int(M/h5);rem=M-n*h5;pack=n*h**(L//2)+power(rem,F(L,10))[1]
  assert ex(rec['packing_upper'])>=pack
  chosen=min(ex(rec['Hermite_upper']),ex(rec['packing_upper']));assert chosen==ex(rec['chosen_upper']);vals.append(chosen)
  # Independent nonnegative-factor identity for the specific fixed-node majorant.
  fac=[sum((a+1)*t**a*h**(k-3-j-a) for a in range(k-2-j)) for j in range(k-2)]
  def mul(a,b):
   out=[F(0)]*(len(a)+len(b)-1)
   for i,x in enumerate(a):
    for j,y in enumerate(b):out[i+j]+=x*y
   return out
  assert all(v>0 for v in fac) and mul(mul([h,-F(1)],[t*t,-2*t,F(1)]),fac)==[aa,bb,cc]+[F(0)]*(k-3)+[-F(1)]
  checks[f'{s}_{L}']={'k':k,'majorant_identity':True,'upper':str(chosen)}
 a,b,c=vals;return a+2*b+3*c,a+2*b

def ints(p):return {k:int(v) for line in read(p).decode().splitlines() for k,v in [line.split('=')]}
g48=ints(P.parent/'mps_excited_seed_review/independent_ground.out');g96=ints(AR/'anchors.out');benchmark=ints(AR/'benchmark48.out')
assert g48['H0_48']==benchmark['H0_48'] and g48['N0_48']==benchmark['N0_48']
assert g48['N0_48']>0 and g96['N0_96']>0
R48=F(g48['H0_48'],g48['N0_48'])+48*F(700741,500000);R96=F(g96['H0_96'],g96['N0_96'])+96*F(700741,500000)
assert R48<0 and R96<0 and R48==ex(cert['R48_shifted']) and R96==ex(cert['R96_shifted'])
assert cert['n']==48 and cert['A_geometry']=='T(48,21/2)' and cert['B_geometry']=='S(48,21)' and ex(cert['beta'])==F(21,2)
Q48=envelope(48)[0];v48=ex(cert['v48_beta0_lower']);assert Q48==ex(cert['Q48_beta0_upper']) and 1<v48<=expiv(-F(21,2)*R48)[0]<Q48
Alo=ex(cert['A_lower']);assert 0<Alo<1 and Alo<=F(v48,Q48)**2
r=cert['spatial_construction'];assert (r['ell'],r['beta'],r['q'],r['p'])==(26,'21','24/13','48/13')
z,e=envelope(26);D,E=ex(r['D']),ex(r['E']);assert D>=z*z and E>=e*e
tau,tau0=(D+11*E)/12,(D+3*E)/4;assert tau==ex(r['tau']) and tau0==ex(r['tau0']) and tau<=tau0<=D
W=ex(r['W96_lower']);assert 1<W<=expiv(-21*R96)[0]
q,p=F(24,13),F(48,13)
def tail(t,degree):
 assert 0<t<tau
 lines=[(F(1),F(0),F(0)),(F(0),F(1),F(0)),(F(1),F(0),tau-t),(F(1),F(1),tau0-t)];values=[]
 for (a,b,c),(d,e,f) in itertools.combinations(lines,2):
  det=a*e-b*d
  if not det:continue
  x,y=(c*e-b*f)/det,(a*f-c*d)/det
  if x>=0 and y>=0 and x<=tau-t and x+y<=tau0-t:
   zz=D-t-x-y;assert zz>=0
   values.append(power(x,degree)[1]+2*power(y/2,degree)[1]+3*power(zz/3,degree)[1])
 assert len(values)>=4;return max(values)
steps=r['leading_steps'];t=ex(steps[0]['t_lower']);initial=D*power(t,p-1)[1];assert initial<W and initial<=ex(steps[0]['initial_contradiction_upper']) and 2*t>D
margins=[str(W-initial)]
for step in steps[1:]:
 nt=ex(step['t_lower']);assert nt>t
 contradiction=power(nt,p)[1]+tail(t,p);assert contradiction<W and contradiction<=ex(step['contradiction_upper']);margins.append(str(W-contradiction));t=nt
Blo=ex(cert['B_lower']);assert F(1,2)<Blo<=1/(1+tail(t,q)/power(t,q)[0])**2<=1
win=cert['window'];assert win['all_integer_lengths']==[48,96] and win['unique_ground_state'] is True
C=ex(win['thermal_purity_lower']);assert F(1,2)<C<=Alo*Alo*roots(2*Blo-1,2)[0]
gap=ex(win['gap_lower']);assert gap==F(53,10000);margin=C-expiv(F(21,2)*gap)[1]*(1-C);assert margin>0 and margin>=ex(win['exponential_margin'])
prior=js(P.parent/'uniform_seed_frontier_review/CLAIM_VERDICTS.json');assert prior['status'].startswith('ACCEPTED') and prior['gap']=='19/5000' and prior['all_integer_L_at_least']==52 and prior['unique_ground_state'] is True
scope=cert['combined_coverage'];assert ex(scope['gap_lower'])==F(19,5000)<gap and scope['all_integer_L_at_least']==48 and scope['prior_tail_from']==52 and scope['overlap']==[52,96] and scope['bootstrap_initialization_remains']==52 and scope['unique_ground_state'] is True
assert all(L>=52 or 48<=L<=96 for L in range(48,200))
out={'status':'ACCEPTED finite48–96 window and allinteger coverage extension; bootstrapseed remains52','seals_verified':seals,'A_geometry':'T(48,21/2)','B_geometry':'S(48,21)','A_lower':str(Alo),'B_lower':str(Blo),'thermal_window_lower':str(C),'finite_window':[48,96],'finite_gap':'53/10000','finite_margin_lower':str(margin),'leading_forcing_steps':len(steps),'leading_contradiction_margins':margins,'moment_checks':checks,'combined_gap':'19/5000','all_integer_L_at_least':48,'bootstrap_initialization_remains':52,'source_identity_floor':4,'new50site_anchor_used':False,'resources':{'CPU_seconds':time.process_time()-start,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'CPU':5,'memory_limit_MiB':100}}
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('status','A_lower','B_lower','thermal_window_lower','finite_gap','combined_gap','all_integer_L_at_least','bootstrap_initialization_remains','resources')},indent=2))
