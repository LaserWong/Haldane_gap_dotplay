#!/usr/bin/env python3
"""Independent standard-library rational review; no producer modules imported."""
import ast, copy, hashlib, json, math, os, re, resource, sys, time
from pathlib import Path
from fractions import Fraction as F
os.sched_setaffinity(0,{2})
resource.setrlimit(resource.RLIMIT_CPU,(600,600))
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
sys.set_int_max_str_digits(100000)
P=Path(__file__).resolve().parent; R=P.parents[1]; A=P/'snapshot/producer'; start=time.process_time(); hashes={}
GRID=10**200

def read(p):
 b=p.read_bytes();hashes[str(p.relative_to(R))]=hashlib.sha256(b).hexdigest();return b

def js(p):return json.loads(read(p))
def seal(p,want=None):
 h=hashlib.sha256(read(p/'MANIFEST_SHA256.json')).hexdigest()
 if want:assert h==want
 d=js(p/'MANIFEST_SHA256.json');d=d.get('files',d)
 for name,digest in d.items():assert hashlib.sha256(read(p/name)).hexdigest()==digest,(p,name)
 return h

def down(x):return F(x.numerator*GRID//x.denominator,GRID)
def up(x):return -down(-x)
def roots(x):
 assert x>=0
 k=math.isqrt(x.numerator*GRID**2//x.denominator);l,u=F(k,GRID),F(k+1,GRID)
 assert l*l<=x<=u*u
 return l,u

def exponential(x):
 assert x>=0
 n=0
 while x>F(1,4):x/=2;n+=1
 lo=hi=tl=th=F(1)
 for k in range(1,221):
  tl=down(tl*x/k);th=up(th*x/k);lo+=tl;hi+=th
 hi=up(hi+up(th*x/221)/(1-x/222))
 for _ in range(n):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi

def dot_upper(co,ivs):return sum((c*(b if c>=0 else a) for c,(a,b) in zip(co,ivs)),F())
def polyval(co,x):
 z=F()
 for c in reversed(co):z=z*x+c
 return z

def square(co):
 return [sum(co[j]*co[k-j] for j in range(len(co)) if 0<=k-j<len(co)) for k in range(2*len(co)-1)]

def shift(co,a,b):
 return [sum(co[j]*math.comb(j,k)*a**(j-k)*b**k for j in range(k,len(co))) for k in range(len(co))]

def positive_definite(A):
 # Separate explicit LDL factorization, not in-place Schur code from producer.
 n=len(A);L=[[F(i==j) for j in range(n)] for i in range(n)];D=[]
 for i in range(n):
  d=A[i][i]-sum(L[i][k]**2*D[k] for k in range(i));assert d>0;D.append(d)
  for j in range(i+1,n):L[j][i]=(A[j][i]-sum(L[j][k]*L[i][k]*D[k] for k in range(i)))/d
 return D

def bernstein_positive(co,a,b):
 # Reconstruct full degree, not a sampled grid and not just the endpoints.
 power=shift(co,a,b-a);d=len(co)-1
 bern=[sum(power[k]*F(math.comb(i,k),math.comb(d,k)) for k in range(i+1)) for i in range(d+1)]
 pending=[(bern,0)];leaves=0;depth=0
 while pending:
  row,level=pending.pop()
  if min(row)>=0:leaves+=1;depth=max(depth,level);continue
  assert row[0]>=0 and row[-1]>=0,'negative endpoint or subdivision point'
  assert level<30,'unresolved positivity'
  triangle=[row]
  for j in range(d):triangle.append([(x+y)/2 for x,y in zip(triangle[-1][:-1],triangle[-1][1:])])
  left=[r[0] for r in triangle];right=[r[-1] for r in triangle[::-1]]
  pending.extend([(left,level+1),(right,level+1)])
 return leaves,depth

def packed(m,h,r):
 assert m>=0 and h>0 and r>=1
 q=m//h;return q*h**r+(m-q*h)**r

def G(z):assert 0<z<=1;return 1-(1-z)**2/(2*z*z)

def check_cap(row,sector,sg,M):
 q=list(map(F,row['q']));assert len(q)==5
 r=F(row['cap']);assert r>0
 B=dot_upper(square(q),M[sector]);assert B==F(row['upper_filter_sum'])
 margin=r**4*polyval(q,sg*r)**2-B;assert margin>0 and margin==F(row['exterior_margin'])
 shifted=shift(q,sg*r,F(sg));assert all(x>0 for x in shifted)
 assert shifted==list(map(F,row['positive_shift_coefficients']))
 t=F(row['midpoint_square_method_nonexclusion_at']);assert 0<sg*t<r
 mid=[(x+y)/2 for x,y in M[sector]]
 piv=positive_definite([[mid[i+j]-t**(i+j+4) for j in range(5)] for i in range(5)])
 assert piv==list(map(F,row['residual_ldl_pivots']))
 return r

def check_continuation(c,S0,T0):
 assert c['conditional_conclusion']=={'all_integer_L_at_least':36,'gap':'107/5000','unique_ground_state':True}
 assert c['seed']['n']==36 and F(c['seed']['beta'])==F(49,4)
 assert F(c['seed']['S'])==S0 and F(c['seed']['T72'])==T0
 states=c['states'];windows=c['all_integer_windows'];assert len(states)==len(windows)==11
 last=None;ms=[]
 for j,(st,w) in enumerate(zip(states,windows)):
  n=36*2**j;b=F(49,4)*2**j;s,t=F(st['S']),F(st['T'])
  assert st['round']==j and st['n']==n and F(st['beta'])==b and 0<s<=1 and 0<t<=1
  if last is None:assert s<=S0 and t<=T0
  else:
   old_s,old_t=last;assert s<=G(old_s**2*old_t) and t<=G(old_t**2*s)
  K=s*s*t;assert K>F(1,2)
  r=roots(2*K-1)[0];rho=(1-r)/(1+r);d=t/(1+rho*rho)
  own=(1-rho)*min(s*roots(d)[0],d)
  C=F(w['purity_lower']);assert F(1,2)<C<=own
  assert (w['from'],w['to'])==(n,2*n) and F(w['beta'])==b and F(w['gap'])==F(107,5000)
  margin=C-exponential(b*F(107,5000))[1]*(1-C);assert 0<F(w['margin'])<=margin
  ms.append(str(margin));last=s,t
 a=c['asymptotic'];u=max(1-s,1-t)
 assert a['from']==n==36864 and F(a['beta'])==b==12544 and F(a['gap'])==F(107,5000)
 assert 0<u==F(a['defect'])<=F(1,100)
 margin=1-5*u*exponential(b*F(107,5000))[1];assert 0<F(a['exponential_margin'])<=margin
 return ms,str(margin)

def run():
 producer_seal=seal(A,'dc81945f85281a33df1b272a7a054b6f5d9b5fa32e8c7a1868c26e07bc97ec85')
 baseline=R/'research_20261010/uniform_second_initialization_review'
 baseline_seal=seal(baseline,'3e713b2de14407cca8c14e7236c23077998d29ea13268267626859fc5c23511b')
 for name,h in js(A/'INPUT_SHA256.json').items():assert hashlib.sha256(read(R/name)).hexdigest()==h
 c=js(A/'certificate.json');lc=js(A/'long_certificate.json');cont=js(A/'continuation_certificate.json')
 for name,h in cont['input_sha256'].items():assert hashlib.sha256(read(R/name)).hexdigest()==h
 assert c['conditional_on_published_thermal_totals'] is True and c['physical_thermal_rerun'] is False
 # Official table parsed independently from TeX; archived Python table used only for cross-check.
 tex=read(baseline/'sources/thermal72.tex').decode()
 rows=re.findall(r'^(\d+)&(\d{15,})&(\d{15,})',tex,re.M);assert len(rows)==9
 W={(int(n),s):int(w) for n,z,p in rows for s,w in [('I',z),('P',p)]}
 tree=ast.parse(read(R/'upstream/extracted/cases/haldane_reference_audit/published_scalar_enclosures.py'))
 tab=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='B' for t in n.targets))
 assert len(tab)==18
 for j,(n,center,w) in enumerate(tab):assert w==W[n,'IP'[j%2]]
 endpoints={}
 for (n,s),w in W.items():
  x=F(49*n,4)*(F(3,2)-F(700741,500000));assert 0<x<15
  term=total=F(1)
  for k in range(1,101):term=term*x/k;total+=term
  d=math.isqrt(3**n)+1;err=d*(281*(d+1)+1);r=math.isqrt(w);assert r*r<=w<(r+1)**2
  low=total*max(0,r-err)**2/2**110;high=(total+term)*(r+1+err)**2/2**110
  endpoints[n,s]=(F(low.numerator*10**18//low.denominator,10**18),F(-((-high.numerator*10**18)//high.denominator),10**18))
 M={'J':[],'N':[]}
 for n in range(4,13):
  zl,zu=endpoints[n,'I'];pl,pu=endpoints[n,'P']
  M['J'].append(((zl+3*pl)/4,(zu+3*pu)/4));M['N'].append(((zl-pu)/4,(zu-pl)/4))
 assert {s:[[str(a),str(b)] for a,b in iv] for s,iv in M.items()}==c['moment_intervals']
 assert all(M['N'][n-4][1]<0 for n in [5,7,9,11])
 caps={key:check_cap(row,key[0],1 if key[-1]=='+' else -1,M) for key,row in c['filters'].items()}
 assert set(caps)=={'J+','J-','N+','N-'}
 # Verify all ten majorants over CLOSED signed support, including zero.
 proof_sizes={}
 for key,v in lc.items():
  sec=key[0];k=int(key[1:]);q=list(map(F,v['coeff']));assert len(q)==9 and k>=12 and k%2==0
  co=q+[F()]*(k-3-len(q));co[k-4]-=1
  assert polyval(co,F())>=0
  leaves,depth=bernstein_positive(co,-caps[sec+'-'],caps[sec+'+'])
  assert (leaves,depth)==(v['bernstein_leaf_count'],v['bernstein_max_depth'])
  assert dot_upper(q,M[sec])==F(v['bound'])>0
  proof_sizes[key]={'leaves':leaves,'depth':depth}
 assert set(lc)=={s+str(k) for s in 'JN' for k in [24,36,48,72,120]}
 U=max(caps['J+'],caps['J-']);V=max(caps['N+'],caps['N-']);mj=M['J'][-1][1];mn=M['N'][-1][1]
 for k,v in c['long_even_moments'].items():
  k=int(k);val=packed(mj,U**12,k//12)+3*packed(mn,V**12,k//12)
  assert val==F(v['new'])<=packed(F('1.0657205'),F('1.00139')**12,k//12)+3*packed(F('.2783155'),F('.872')**12,k//12)
 dom=c['dominant'];ell=F(dom['ell']);assert dom['positive'] is True and ell>caps['J-']
 absent=1-packed(mj,ell**12,6)-3*packed(mn,V**12,6);assert absent==F(dom['absence_contradiction_margin'])>0
 residual=mj-ell**12;assert 0<residual<ell**12
 ra=lambda k:residual**(k//12)+3*packed(mn,V**12,k//12)
 assert F(dom['p0'])==1-(1+ra(36)/ell**36)**-2
 T0=(U**72+ra(72))**-2;assert F(dom['q0'])==1-T0
 S0=(1+(residual**3+3*F(lc['N36']['bound']))/ell**36)**-2
 assert S0>1-F(dom['p0'])
 anchor=dict(line.split('=') for line in read(R/'audit/mps/contraction.out').decode().splitlines())
 v,u=int(anchor['V72']),int(anchor['U72']);assert v>0 and -700741*v-500000*u>0
 shifted=72*(F(u,v)+F(700741,500000));assert shifted<0
 margins,am=check_continuation(cont,S0,T0)
 # Independent endpoint safeguards for the inherited small-defect theorem.
 e=F(1,100)
 assert (3-3*e+e*e)**2/(2*(1-e)**6)<=5
 assert (2+5*e)**2/(2*(1-2*e-5*e*e)**2)<=5
 assert e-5*e*e-e**3>0 and 4*e*(1-e)<=(1-2*e)**2 and 4/(1-4*e)<=5
 # Alternative explicit window estimate used in this review's proof.
 assert e<=F(4,49) and e<=F(1,63)
 assert 1+F(81,25)*e<=F(26,25) and F(9,5)+F(51,25)<4
 for name,info in js(baseline/'SOURCE_PROVENANCE.json').items():
  raw=read(baseline/'sources'/name)
  assert hashlib.sha256(raw).hexdigest()==info['sha256']
  assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==info['git_blob_sha1']
 read(R/'research_20261010/root_review/FINITE_WINDOW_INTERPOLATION.md')
 read(R/'audit/APPENDIX_A_BRIDGE.md')
 return {'status':'CONDITIONALLY ACCEPTED','gap':'107/5000','all_integer_L_at_least':36,'unique_ground_state':True,'thermal_premise':'All 18 published beta49/4 integer-total and error certificates; tighter rational enclosures, not just coarse center +/-30e-6','full_local_physical_thermal_rerun':False,'producer_manifest':producer_seal,'baseline_manifest':baseline_seal,'caps':{k:str(v) for k,v in caps.items()},'majorants':proof_sizes,'seed':{'n':36,'beta':'49/4','S':str(S0),'T72':str(T0),'spatial_defect_decimal':float(1-S0),'thermal_defect_decimal':float(1-T0)},'MPS72_shifted_Rayleigh':str(shifted),'window_margins':margins,'asymptotic_margin':am,'asymptotic_from':36864,'asymptotic_beta':12544,'cpu_seconds':time.process_time()-start,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},M,c,lc,cont

if __name__=='__main__':
 out,*_=run();(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ['status','gap','all_integer_L_at_least','cpu_seconds','maxrss_kib']},indent=2))
