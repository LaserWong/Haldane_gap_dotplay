# UNTRUSTED producer (push_bound). Same certificate as watertight/auditor/produce_patchedprefix.py, but:
#  (1) the leader ell is bisected on a coarse 10^-140 grid (then the forcing margin is recomputed and asserted at the full grid),
#  (2) the largest passing gap on a 1/RES grid in [GAP_LO, GAP_HI] is located with the exact chain, and that row is written.
# Nothing here is trusted: acceptance comes only from the checkers (original audit_scalar.py / patched FULL one, and original audit.py).
import os,sys,json,time,math
os.environ.setdefault('AUDIT_DIGITS','700'); sys.argv=['x']; t00=time.time()
A='/workspace/haldane_chat_bundle/runs/watertight/auditor/orig_audit/research_20261010/uniform_smaller_second_initialization'
src=open('/workspace/haldane_chat_bundle/audit_copy/research_20261010/uniform_smaller_second_initialization_review/audit_scalar.py').read()
exec(src.split("producer_hash=")[0].replace("os.sched_setaffinity(0,{0});","").replace("P=Path(__file__).resolve().parent","P=Path('"+A+"_review')"))
from fractions import Fraction as F
# Producer-side speedup only: same floor-root result as the checker's binary search (Newton integer q-th root),
# with the checker's own self-check assert l**q<=z<=u**q kept.
def _iroot(N,q):
 if N<2:return N
 x=1<<((N.bit_length()+q-1)//q)
 while True:
  y=((q-1)*x+N//x**(q-1))//q
  if y>=x:break
  x=y
 while x**q>N:x-=1
 while (x+1)**q<=N:x+=1
 return x
@lru_cache(None)
def power(x,r):
 r=F(r);assert x>=0 and r>0;p,q=r.numerator,r.denominator;z=x**p;scaled=z.numerator*B**q//z.denominator
 k=scaled if q==1 else (math.isqrt(scaled) if q==2 else _iroot(scaled,q))
 l,u=F(k,B),F(k+1,B);assert l**q<=z<=u**q;return l,u
full=os.environ.get('AUDIT_FULL_R68')=='1';W=int(os.environ['W']);glo=F(os.environ['GAP_LO']);ghi=F(os.environ['GAP_HI']);res=F(os.environ['RES'])
C=js(R/'uniform_second_moment_optimization/certificate.json');L=js(A/'long_certificate.json');cert=js(A/'certificate.json');M={k:[tuple(map(F,v)) for v in rows] for k,rows in C['moment_intervals'].items()}
U=max(F(C['filters']['J+']['cap']),F(C['filters']['J-']['cap']));V=max(F(C['filters']['N+']['cap']),F(C['filters']['N-']['cap']));mj=M['J'][-1][1];mn=M['N'][-1][1]
def sector(s,n):
 m,h=(mj,U**12) if s=='J' else (mn,V**12);v=pack(m,h,F(n,12));key=f'{s}{n}'
 return min(v,F(L[key]['bound'])) if key in L else v
ours=ints(A/'anchors.out');n=34
ray=F(ours['H0_68'],ours['N0_68'])+68*F(700741,500000)
BIG=B
def forcing_ok(mid,Z1,N2):return Z1-pack(mj,mid**12,F(68,12))-N2>0 and mj-mid**12>0
B=10**140;power.cache_clear();pack.cache_clear();exp_upper.cache_clear()
Z1=exp_lower(-F(49,4)*ray) if full else 1;N2=3*sector('N',68)
lo,hi=F(9,10),F(1)
for _ in range(40):
 mid=F(int((lo+hi)/2*10**10),10**10)
 if forcing_ok(mid,Z1,N2):lo=mid
 else:hi=mid
ell=lo
B=BIG;power.cache_clear();pack.cache_clear();exp_upper.cache_clear()
Z1=exp_lower(-F(49,4)*ray) if full else 1;Z2=exp_lower(-2*F(49,4)*ray) if full else 1;N2=3*sector('N',68)
force=Z1-pack(mj,ell**12,F(68,12))-N2;assert force>0 and 0<mj-ell**12<ell**12
tail=power(mj-ell**12,F(n,12))[1]+3*sector('N',n);Q=sector('J',68)+3*sector('N',68)
S=down((1+tail/ell**n)**-2);T=down(Z2*Q**-2)
states=[];owns=[];s,t=S,T
for j in range(W):
 size=n*2**j;beta=F(49,4)*2**j
 if j: s=down(G(prev[0]**2*prev[1]));t=down(G(prev[1]**2*s))
 states.append({'n':size,'beta':str(beta),'S':str(s),'T':str(t)})
 K=s*s*t;root=power(2*K-1,F(1,2))[0];rho=(1-root)/(1+root);d=t/(1+rho*rho);own=down((1-rho)*min(s*power(d,F(1,2))[0],d))
 owns.append(own);prev=s,t
u=max(1-s,1-t);print('setup+states %.1fs'%(time.time()-t00),flush=True)
def chain(gap):
 ws=[]
 for j,own in enumerate(owns):
  beta=F(49,4)*2**j;m=down(own-exp_upper(beta*gap)*(1-own))
  if not m>0:return None,('window',j)
  ws.append({'from':n*2**j,'to':n*2**(j+1),'purity':str(own),'margin':str(m)})
 beta=F(49,4)*2**(W-1);am=down(1-5*u*exp_upper(beta*gap))
 if not(u<=F(1,100) and am>0):return None,('asym',)
 return (ws,am),None
assert chain(glo)[0] is not None,('GAP_LO fails',chain(glo)[1])
a,b=glo,ghi
while b-a>res:
 m=F(math.floor(((a+b)/2)/res))*res
 if m<=a:m=a+res
 ok,why=chain(m);print(' gap',m,float(m),'PASS' if ok else why,flush=True)
 if ok:a=m
 else:b=m
gap=a;(ws,am),_=chain(gap);size=n*2**(W-1);beta=F(49,4)*2**(W-1)
row=dict(next(r for r in cert['rows'] if r['n']==34))
row.update({'gap':str(gap),'ell':str(ell),'forcing_margin':str(down(force)),'tail':str(up(tail)),'Q':str(up(Q)),'S':str(S),'T':str(T),'states':states,'windows':ws,
 'asymptotic':{**row['asymptotic'],'from':size,'beta':str(beta),'defect':str(u),'margin':str(am)},'full_R68_forcing':full,'closure_factor':str(1-am)})
out=dict(cert);out['rows']=[r for r in cert['rows'] if r['n']!=34]+[row]
name=os.environ['AUDIT_CERT'];open(str(A)+'/'+name,'w').write(json.dumps(out,indent=1))
print(json.dumps({'wrote':name,'gap':str(gap),'gap_float':float(gap),'first_fail':str(b),'ell':str(ell),'closure_factor':float(1-am),'from':size,'W':W,'digits':os.environ['AUDIT_DIGITS'],'producer_s':round(time.time()-t00,1)}))
