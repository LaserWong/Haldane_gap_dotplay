import numpy as np, json, time, os, sys
from flint import arb, acb, fmpq
from common import certify, arbs
L=12; N=3**L; p3=3**np.arange(L)
allst=np.arange(N); dig=(allst[:,None]//p3)%3; Sz=(1-dig).sum(1)
def rot(s): d=(s[...,None]//p3)%3; return (np.roll(d,1,axis=-1)*p3).sum(-1)
OUT='enclosures12.json'; out=json.load(open(OUT)) if os.path.exists(OUT) else {}
order=[int(x) for x in sys.argv[1:]] if len(sys.argv)>1 else list(range(L-1,-1,-1))
t0=time.time()
for sz in order:
    sec=allst[Sz==sz]
    rorb=[sec]; c=sec
    for _ in range(L-1): c=rot(c); rorb.append(c)
    reps=np.unique(np.array(rorb).min(0))
    rorb=[reps]; c=reps
    for _ in range(L-1): c=rot(c); rorb.append(c)
    rorb=np.array(rorb); period=np.array([(rorb[1:,j]==reps[j]).argmax()+1 if (rorb[1:,j]==reps[j]).any() else L for j in range(len(reps))])
    idx={int(r):j for j,r in enumerate(reps)}
    d=(reps[:,None]//p3)%3; mm=1-d; diag=(mm*np.roll(mm,-1,axis=1)).sum(1)
    rows=[];cols=[];shifts=[]
    for i in range(L):
        j=(i+1)%L
        for (di,dj) in [(-1,1),(1,-1)]:
            ok=(d[:,i]+di>=0)&(d[:,i]+di<=2)&(d[:,j]+dj>=0)&(d[:,j]+dj<=2); a=np.nonzero(ok)[0]
            new=reps[a]+di*p3[i]+dj*p3[j]; o=[new]; c=new
            for _ in range(L-1): c=rot(c); o.append(c)
            o=np.array(o); rows+=list(a); cols+=[idx[int(x)] for x in o.min(0)]; shifts+=list(o.argmin(0))
    rows=np.array(rows,int);cols=np.array(cols,int);shifts=np.array(shifts,int); n=len(reps)
    for k in range(L//2+1):
        key=f'{sz},{k}'
        if key in out: continue
        okk=(period*k)%L==0; sel=np.nonzero(okk)[0]; m=len(sel)
        if m==0: continue
        pos=-np.ones(n,int); pos[sel]=np.arange(m)
        g=okk[rows]&okk[cols]; r_,c_,s_=pos[rows[g]],pos[cols[g]],shifts[g]; pr,pc=period[rows[g]],period[cols[g]]
        # exact entries H[c,r] += exp(-2 pi i k s/L) sqrt(p_r/p_c)  (balls)
        cache={}; ent={}
        for a_,b_,s0,x,y in zip(c_,r_,s_,pr,pc):
            kk=(int(s0)*k)%L,int(x),int(y)
            if kk not in cache: cache[kk]=acb(arb(fmpq(-2*kk[0],L))).exp_pi_i()*(arb(kk[1])/kk[2]).sqrt()
            ent[(int(a_),int(b_))]=ent.get((int(a_),int(b_)),acb(0))+cache[kk]
        for q in range(m): ent[(q,q)]=ent.get((q,q),acb(0))+int(diag[sel[q]])
        Hf=np.zeros((m,m),complex)
        for (a_,b_),v in ent.items(): Hf[a_,b_]=float(v.real.mid())+1j*float(v.imag.mid())
        for (a_,b_),v in ent.items():   # exact Hermiticity of the ball entries
            w=ent.get((b_,a_)); assert w is not None and (v-w.conjugate()).contains(0)
        real=(k==0 or 2*k==L)
        if real:
            assert all(v.imag.contains(0) and v.imag.rad()<1e-30 for v in ent.values())
            ent={kk:acb(v.real) for kk,v in ent.items()}   # imag part exactly 0 (phase = +-1)
            Hf=Hf.real.copy()
        Hf=(Hf+Hf.conj().T)/2
        frob=sum((abs(v)**2 for v in ent.values()),arb(0)); tr=sum((ent[(q,q)].real for q in range(m)),arb(0))
        lt,eta,delta=certify(Hf,ent,arb(24))
        rec=dict(lam_t=lt,eta=arbs(eta),delta=arbs(delta),mult=(1 if sz==0 else 2)*(1 if real else 2),
                 conj_pair=None if real else L-k, trace=arbs(tr), frob2=arbs(frob))
        out[key]=rec; json.dump(out,open(OUT+'.tmp','w')); os.replace(OUT+'.tmp',OUT)
        print(sz,k,m,'eta',eta.mid(),'delta',delta.mid(),round(time.time()-t0),flush=True)
print('done',flush=True)
