#!/usr/bin/env python3
"""Independent all-r interval replay, strengthened to ideal unrounded fixed envelopes."""
from pathlib import Path
from fractions import Fraction as F
import os,resource,sys,json,hashlib,time,itertools
sys.set_int_max_str_digits(1000000)
P=Path(__file__).resolve().parent;ROOT=P.parents[1];A=P.with_name('uniform_seed_recipe_minimum');M=P.with_name('uniform_transfer_moment_assessment');AR=P.with_name('uniform_anchor96_100_review')
os.sched_setaffinity(0,{5 if 5 in os.sched_getaffinity(0) else min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600));start=time.process_time();B=10**40;hashes={}
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
for folder in (A,M,AR,P.with_name('uniform_seed_frontier_review')):
 manifest=js(folder/'MANIFEST_SHA256.json')
 for f,h in manifest.items():assert hashlib.sha256(read(folder/f)).hexdigest()==h
 seals[folder.name]=hashlib.sha256((folder/'MANIFEST_SHA256.json').read_bytes()).hexdigest()
assert seals['uniform_seed_recipe_minimum']=='94b7c842440d46fdb77f197a92e2096313f34afcc975bf0846e8c4b4414d5900'
assert seals['uniform_anchor96_100_review']=='99317ea99db7892f33852e6a0b12b9aa4d3825527852ff605d7d86f22d3f22d7'
for name,h in js(A/'INPUT_SHA256.json').items():assert hashlib.sha256(read(ROOT/name)).hexdigest()==h
d=js(M/'results.json');caps={s:F(v['x_cap']['exact']) for s,v in d['hankel_caps'].items()};mom={s:{int(j):tuple(F(x['exact']) for x in iv) for j,iv in v['moment_intervals'].items()} for s,v in d['hankel_caps'].items()};nodes={}
for s,h in caps.items():
 a,b,c=[sum(mom[s][j])/2 for j in (3,4,5)];nodes[s]=floor((h*b-c)/(h*a-b),10**10);assert 0<nodes[s]<h
CACHE={}
def envelope_lower(L):
 # These are lower bounds on prescribed upper-envelope FORMULAS, not on physical traces.
 if L in CACHE:return CACHE[L]
 vals=[]
 for s,h in caps.items():
  t=nodes[s];k=L//2-3;c=(h**k-t**k-k*t**(k-1)*(h-t))/(h-t)**2;b=k*t**(k-1)-2*c*t;a=(1-k)*t**k+c*t*t
  hermite=sum(co*mom[s][j][int(co>=0)] for co,j in zip((a,b,c),(3,4,5)))
  mass=mom[s][5][1];unit=h**5;count=int(mass/unit);rem=mass-count*unit
  packlo=count*h**(L//2)+power(rem,F(L,10))[0]
  value=floor(min(hermite,packlo));assert value>0;vals.append(value)
 a,b,c=vals;CACHE[L]=(a+2*b+3*c,a+2*b);return CACHE[L]
anchor=js(AR/'results.json');R={v['L']//2:F(v['total_shifted_Rayleigh_exact']) for v in anchor['rows']};assert set(R)=={48,50} and all(v<0 for v in R.values())
producer=js(A/'results.json');expected={(n,ell) for n in (48,50) for ell in range(10,n+1,2)}
assert len(producer['families'])==len(expected)==41 and {(r['n'],r['ell']) for r in producer['families']}==expected
assert producer['selected_n']==[48,50] and producer['selected_ell'] is None
# First inspect every original saved failure, including all intermediate states and domains.
saved_types={};saved_round=0;leaf_total=0
for rec in producer['families']:
 leaves=rec['closed_interval_leaves'];ends=[(F(v['r_lower']),F(v['r_upper'])) for v in leaves]
 assert ends[0][0]==1 and ends[-1][1]==16 and all(a<b for a,b in ends) and all(a[1]==b[0] for a,b in zip(ends,ends[1:]))
 for leaf in leaves:
  s,t=F(leaf['S_upper']),F(leaf['T_upper']);assert 0<s<=1 and 0<t<=1
  hist=leaf['failure']['history'];assert hist
  for j,h in enumerate(hist):
   if not j%2:
    assert min(s,t)<F(99,100);arg=s*s*t;kind='spatial';value=ceil(G(arg),10**24);s=value
   else:arg=t*t*s;kind='thermal';value=ceil(G(arg),10**24);t=value
   assert 0<arg<=1 and h['kind']==kind and F(h['argument_upper'])==arg and F(h['output_upper'])==value
   assert (value<=0)==(j==len(hist)-1)
  assert leaf['failure']['kind']==kind and leaf['failure']['round']==(len(hist)+1)//2
  saved_types[kind]=saved_types.get(kind,0)+1;saved_round=max(saved_round,(len(hist)+1)//2);leaf_total+=1
assert leaf_total==producer['leaf_count']==332
# New all-r interval bounds based on a lower enclosure of the ideal unrounded envelope.
thermal={}
for n in (48,50):
 Qlo=envelope_lower(2*n)[0];vhi=expiv(-F(21,2)*R[n])[1];base=Qlo/vhi-1;assert 0<base<1
 thermal[n]=(Qlo,vhi,base,logiv(base)[0])
rows=[];failure_types={};maxround=0
for rec in producer['families']:
 n,ell=rec['n'],rec['ell'];assert F(rec['anchor_shifted_R'])==R[n]
 q=F(n,ell);p=2*q;z,e=envelope_lower(ell);Qlo,vhi,base,logbase=thermal[n]
 assert z>=e>1 and z<=F(rec['z']) and e<=F(rec['e']) and Qlo<=F(rec['Q'])
 lz,le=logiv(z)[0],logiv(e)[0];coef=-F(21,2)*R[n]/p;cold=lz-coef
 assert cold>0;ratio=expiv(16*cold)[0];assert ratio>4 and G(F(1,256))<0
 output=[];dcache={};tcache={};Tcache={}
 for leaf in rec['closed_interval_leaves']:
  a,b=F(leaf['r_lower']),F(leaf['r_upper'])
  if a not in dcache:dcache[a]=(expiv(a*lz)[0],expiv(a*le)[0])
  if b not in tcache:tcache[b]=expiv(b*coef)[1]
  D,E=dcache[a];tstar=tcache[b];tau=(D+11*E)/12;tau0=(D+3*E)/4;assert 0<tstar<tau<=tau0<=D
  # Independently enumerate vertices from active constraints.
  lines=[(F(1),F(0),F(0)),(F(0),F(1),F(0)),(F(1),F(0),tau-tstar),(F(1),F(1),tau0-tstar)];values=[]
  for (aa,bb,cc),(dd,ee,ff) in itertools.combinations(lines,2):
   det=aa*ee-bb*dd
   if not det:continue
   x,y=(cc*ee-bb*ff)/det,(aa*ff-cc*dd)/det
   if x>=0 and y>=0 and x<=tau-tstar and x+y<=tau0-tstar:
    zz=D-tstar-x-y;assert zz>=0
    values.append(power(x,q)[0]+2*power(y/2,q)[0]+3*power(zz/3,q)[0])
  assert len(values)>=4
  tail=max(values);den=power(tstar,q)[1];s=ceil(1/(1+tail/den)**2)
  if b not in Tcache:Tcache[b]=ceil(1/(1+expiv(b*logbase)[0])**2)
  t=Tcache[b];assert 0<s<=1 and 0<t<=1;s0,t0=s,t;hist=[]
  for iteration in range(1,101):
   if min(s,t)>=F(99,100):raise AssertionError(('Optimistic target reached',n,ell,a,b))
   arg=s*s*t;assert 0<arg<=1;s=ceil(G(arg));hist.append({'kind':'spatial','argument':str(arg),'upper_output':str(s)})
   if s<=0:kind='spatial';break
   arg=t*t*s;assert 0<arg<=1;t=ceil(G(arg));hist.append({'kind':'thermal','argument':str(arg),'upper_output':str(t)})
   if t<=0:kind='thermal';break
  else:raise AssertionError(('Unresolved optimistic path, not an exclusion',n,ell,a,b))
  assert F(hist[-1]['upper_output'])<=0
  failure_types[kind]=failure_types.get(kind,0)+1;maxround=max(maxround,iteration)
  output.append({'r_lower':str(a),'r_upper':str(b),'S_optimistic_upper':str(s0),'T_optimistic_upper':str(t0),'failure_round':iteration,'failure_kind':kind,'history':hist})
 rows.append({'n':n,'ell':ell,'ideal_envelope_z_lower':str(z),'ideal_envelope_e_lower':str(e),'ideal_envelope_Q_lower':str(Qlo),'cold_log_ratio_lower':str(cold),'cold_ratio_at16_lower':str(ratio),'cold_ray':'all r>=16, certificateS<=1/16, first spatial G nonpositive','leaves':output})
 print(json.dumps({'n':n,'ell':ell,'leaves':len(output),'max_round':max(x['failure_round'] for x in output),'elapsed_CPU':time.process_time()-start}),flush=True)
out={'status':'PASS exclusion only n48/n50 in specified fixed-node canonical cooled grammar; includes ideal unrounded envelope evaluation','producer_manifest_sha256':seals['uniform_seed_recipe_minimum'],'verified_seals':seals,'families':rows,'scope':{'n':[48,50],'bases':'every even ell10..n','r':'all real r>=1','finite_boxes':332,'family_count':41,'envelope':'fixed inherited caps/moment intervals and floor1e-10Radau nodes; min(Hermite,packing), ideal exact or arbitrary conservative numerical evaluation','continuation':'canonical sequentialG only; finite bridges granted free','not_claimed':['minimumseed52','n<48exclusion','allmethodno-go','physicalpurityupperbound','physicalleadingeigenvaluecap','alternateupdateorders','newnodeorintegermomentcorrections']},'original_history_summary':{'failure_types':saved_types,'max_round':saved_round,'roundcap_only_failures':0},'independent_ideal_history_summary':{'failure_types':failure_types,'max_round':maxround,'roundcap_only_failures':0},'resources':{'CPU_seconds':time.process_time()-start,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'CPU':5,'memory_limit_MiB':700}}
(P/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('status','original_history_summary','independent_ideal_history_summary','resources')},indent=2))
