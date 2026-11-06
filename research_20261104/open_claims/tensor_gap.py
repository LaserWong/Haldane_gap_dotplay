# Claim A1 (gap part): rerun the n=34 doubling chain (logic of a_uniform/improve.py = repo audit_scalar.py with
# Z68(b)>=exp(-b R68)) for each tensor variant. Exact rationals, directed rounding grid 1e-600.
# Change vs improve.py: exp(-b0*R) for R>0 is bounded below by 1/exp_upper(b0*R) (rounded down), which is rigorous;
# improve.py's exp_lower (truncated Taylor) is only valid for nonnegative arguments.
import sys,json
WARG=int(sys.argv[1]) if len(sys.argv)>1 else 10;ARGV=list(sys.argv)
from fractions import Fraction as F
sys.argv=['x','none','10']
src=open('/workspace/haldane_chat_bundle/runs/a_uniform/improve.py').read().split("import sys\nmode")[0]
exec(src)
def explow(x):  # rigorous lower bound for e^x, any rational x
    return exp_lower(x) if x>=0 else down(1/exp_upper(-x))
exp_lower_orig=exp_lower
W=WARG;WMAX=W;FREE=False
Rs=json.load(open('tensor_R68.json'))
def seed_full(Rv):
    Z1=explow(-b0*Rv);Z2=explow(-2*b0*Rv);N2=3*sector('N',2*n)
    lo,hi=F(9*10**9,10**10),F(10**10,10**10)
    for _ in range(40):
        mid=down((lo+hi)/2)
        if pack(mj,mid**12,F(2*n,12))+N2<Z1: lo=mid
        else: hi=mid
    ell=F(int(lo*10**10),10**10)
    ok=pack(mj,ell**12,F(2*n,12))+N2<Z1 and 0<mj-ell**12<ell**12 and ell>max(F(C['filters']['J-']['cap']),V)
    if not ok: return None
    tail=power(mj-ell**12,F(n,12))[1]+3*sector('N',n);Q=sector('J',2*n)+3*sector('N',2*n)
    return ell,(1+tail/ell**n)**-2,Z2/Q**2
res={}
for d0 in (ARGV[2].split(',') if len(ARGV)>2 else ['-289','-288','-287','-285']):
    Rv=F(Rs[d0]['R68']);sd=seed_full(Rv)
    if sd is None: print(d0,'R68',float(Rv),'seed: no admissible ell (dominant-eigenvalue step fails)');res[d0]=None;continue
    ell,S,T=sd
    r0=chain(S,T,F(0),W=W)
    if not(r0 and r0[0]):
        print(d0,'R68',float(Rv),'ell',ell,'S',float(S),'T',float(T),'-> chain does not start even at gap 0:',r0[1] if r0 else r0);res[d0]='no start';continue
    lo,hi=F(0),F(1,10)
    for _ in range(34):
        mid=(lo+hi)/2;r=chain(S,T,mid,W=W)
        if r and r[0]: lo=mid
        else: hi=mid
    g=F(int(lo*10**6),10**6);r=chain(S,T,g,W=W);assert r[0]
    rr=chain(S,T,g+F(1,10**6),W=W)
    print(d0,'R68',float(Rv),'ell',ell,'S',float(S),'T',float(T),f'W={W}: certified gap {g} ({r[1]}, factor {float(r[2]):.8f}); {g+F(1,10**6)} ->',(rr[0],rr[1]) if rr else rr,flush=True)
    res[d0]=str(g)
json.dump(res,open(f'tensor_gap_W{W}_'+'_'.join(res)+'.json','w'),indent=1)
