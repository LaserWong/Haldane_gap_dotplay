# Claim A2 side remark (NUMERICAL ONLY, float64 Lanczos): periodic 3x3 spin-1/2 bilayer, rung J=1.
# gap(gx=gy=0.1) claimed 0.915256 ; gap(gx=0.1, gy=0) claimed 0.958627.
# E0 and E1 both have Sz=0 members (any SU(2) multiplet does), so the Sz=0 block (dim C(18,9)=48620) suffices.
import numpy as np, itertools, scipy.sparse as sp, scipy.sparse.linalg as sl
Lx=Ly=3; site=lambda x,y,l:2*(x+Lx*y)+l; N=18
states=[s for s in range(1<<N) if bin(s).count('1')==9]; idx={s:i for i,s in enumerate(states)}
def H(gx,gy):
    b=[(site(x,y,0),site(x,y,1),1.0) for x in range(Lx) for y in range(Ly)]
    for x in range(Lx):
        for y in range(Ly):
            for l in (0,1):
                b.append((site(x,y,l),site((x+1)%Lx,y,l),gx)); b.append((site(x,y,l),site(x,(y+1)%Ly,l),gy))
    r=[];c=[];v=[]
    for s in states:
        i=idx[s];d=0.0
        for (p,q,J) in b:
            if J==0:continue
            if ((s>>p)&1)==((s>>q)&1): d+=J/4
            else:
                d-=J/4; r.append(idx[s^(1<<p)^(1<<q)]); c.append(i); v.append(J/2)
        r.append(i);c.append(i);v.append(d)
    return sp.csr_matrix((v,(r,c)),shape=(len(states),)*2)
for gx,gy,claim in [(0.1,0.1,0.915256),(0.1,0.0,0.958627)]:
    ev=np.sort(sl.eigsh(H(gx,gy),k=6,which='SA',tol=1e-12)[0])
    print(f'gx={gx} gy={gy}: E0={ev[0]:.10f} E1={ev[1]:.10f} gap={ev[1]-ev[0]:.6f} (claim {claim})',flush=True)
