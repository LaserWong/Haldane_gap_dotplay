# Task B scanner (exact rationals, same arithmetic as the producer produce_w12.py / produce_patchedprefix.py).
# try_gap(gap,W) runs the exact producer chain (no file output) and reports pass/fail + failing stage.
# This is only used to LOCATE candidates; every reported bound is then re-checked by the checker (run via
# watertight/auditor/run_orig_logic.py for ORIGINAL logic, run_patched.py for FULL).
import os,sys,time,math,json
from fractions import Fraction as F
mode=sys.argv[1]; W=int(sys.argv[2]); digits=int(sys.argv[3]); lo_g=F(sys.argv[4]); hi_g=F(sys.argv[5]); res=F(sys.argv[6])
os.environ['AUDIT_DIGITS']=str(digits); os.environ['AUDIT_FULL_R68']='1' if mode=='FULL' else '0'
sys.argv=['x']
A='/workspace/haldane_chat_bundle/runs/watertight/auditor/orig_audit/research_20261010/uniform_smaller_second_initialization'
src=open('/workspace/haldane_chat_bundle/audit_copy/research_20261010/uniform_smaller_second_initialization_review/audit_scalar.py').read()
exec(src.split("producer_hash=")[0].replace("os.sched_setaffinity(0,{0});","").replace("P=Path(__file__).resolve().parent","P=Path('"+A+"_review')"))
full=mode=='FULL'
C=js(R/'uniform_second_moment_optimization/certificate.json');L=js(A/'long_certificate.json');M={k:[tuple(map(F,v)) for v in rows] for k,rows in C['moment_intervals'].items()}
U=max(F(C['filters']['J+']['cap']),F(C['filters']['J-']['cap']));V=max(F(C['filters']['N+']['cap']),F(C['filters']['N-']['cap']));mj=M['J'][-1][1];mn=M['N'][-1][1]
def sector(s,n):
 m,h=(mj,U**12) if s=='J' else (mn,V**12);v=pack(m,h,F(n,12));key=f'{s}{n}'
 return min(v,F(L[key]['bound'])) if key in L else v
ours=ints(A/'anchors.out');n=34
ray=F(ours['H0_68'],ours['N0_68'])+68*F(700741,500000)
Z1=exp_lower(-F(49,4)*ray) if full else 1;Z2=exp_lower(-2*F(49,4)*ray) if full else 1
N2=3*sector('N',68)
lo,hi=F(9,10),F(1)
for _ in range(40):
 mid=F(int((lo+hi)/2*10**10),10**10)
 if Z1-pack(mj,mid**12,F(68,12))-N2>0 and mj-mid**12>0:lo=mid
 else:hi=mid
ell=lo;tail=power(mj-ell**12,F(n,12))[1]+3*sector('N',n);Q=sector('J',68)+3*sector('N',68)
S=down((1+tail/ell**n)**-2);T=down(Z2*Q**-2)
# precompute states / purities once (independent of gap)
t0=time.time();st=[];s,t=S,T
for j in range(W):
 if j: s=down(G(prev[0]**2*prev[1]));t=down(G(prev[1]**2*s))
 K=s*s*t;root=power(2*K-1,F(1,2))[0];rho=(1-root)/(1+root);d=t/(1+rho*rho);own=down((1-rho)*min(s*power(d,F(1,2))[0],d))
 st.append(own);prev=s,t
u=max(1-s,1-t);print('states built',round(time.time()-t0,1),'s; u_final ~ 10^%.1f'%(math.log10(u.numerator)-math.log10(u.denominator) if u>0 else -1e9),flush=True)
def try_gap(gap):
 for j,own in enumerate(st):
  beta=F(49,4)*2**j
  if not down(own-exp_upper(beta*gap)*(1-own))>0: return ('window',j)
 beta=F(49,4)*2**(W-1)
 if not (u<=F(1,100) and down(1-5*u*exp_upper(beta*gap))>0): return ('asym',)
 return None
assert try_gap(lo_g) is None,('lower end fails',try_gap(lo_g))
a,b=lo_g,hi_g
while b-a>res:
 m=(a+b)/2; m=F(math.floor(m/res))*res
 if m<=a: m=a+res
 r=try_gap(m); print(' gap',m,float(m),'->','PASS' if r is None else r,flush=True)
 if r is None:a=m
 else:b=m
print(json.dumps({'mode':mode,'W':W,'digits':digits,'max_pass':str(a),'max_pass_float':float(a),'first_fail':str(b),'elapsed_s':round(time.time()-t0,1)}))
