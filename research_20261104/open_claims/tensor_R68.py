# Claim A1: exact R68 for the D=26 tensor with first diagonal parameter d0 in {-289,-288,-287,-285}.
# Independent exact-integer contraction (python-flint fmpz_mat), built from the printed Appendix-C formulas
# (same formulas as repo audit/mps/build_mps.py; diag[0] is the varied parameter).
import sys, itertools, json, time
from fractions import Fraction as F
import flint
sys.set_int_max_str_digits(0)
ells=[1,1,1,1,3,3,3,5]
pair={(0,4):-11,(0,5):-35,(0,6):-28,(1,4):-23,(1,5):16,(1,6):-49,(2,4):-6,(2,5):-25,(2,6):-20,(3,4):-34,(3,5):9,(3,6):-32,(4,7):1,(5,7):2,(6,7):-16}
labels=[(a,m) for a,l in enumerate(ells) for m in range(-l,l+1,2)]
def tensors(d0):
    diag=[d0,-84,-9,33,-22,27,71,-11]
    A={s:[[0]*26 for _ in range(26)] for s in (-1,0,1)}
    for i,(a,m) in enumerate(labels):
        ell=ells[a];r=(ell+m)//2
        for j,(b,k) in enumerate(labels):
            if (k-m)%2: continue
            s=(k-m)//2
            if s not in A: continue
            if a==b: val=diag[a]*({-1:2*(ell-r+1),0:m,1:-(r+1)}[s])
            elif (a,b) in pair: val=pair[a,b]*({-1:2*(ell+1-r)*(ell+2-r),0:2*(r+1)*(ell-r+1),1:(r+1)*(r+2)}[s])
            elif (b,a) in pair: val=-pair[b,a]*({-1:2,0:-2,1:1}[s])
            else: continue
            A[s][i][j]=val
    return {s:flint.fmpz_mat(A[s]) for s in A}
# two-site spin-1 Heisenberg x_{12}=S1.S2 in Sz basis: <s t|h|u v>
h={(s,t,u,v):(s*t if (s,t)==(u,v) else int(s+t==u+v and abs(s-u)==1)) for s,t,u,v in itertools.product((-1,0,1),repeat=4)}
def kron(a,b):
    n=a.nrows();out=[[0]*(n*n) for _ in range(n*n)]
    for i in range(n):
        for k in range(n):
            x=a[i,k]
            if x==0: continue
            for j in range(n):
                for l in range(n):
                    y=b[j,l]
                    if y: out[i*n+j][k*n+l]=int(x*y)
    return out
def tr(M):return sum(int(M[i,i]) for i in range(M.nrows()))
def anchors(d0,L):
    A=tensors(d0);B={(s,t):A[s]*A[t] for s in A for t in A}
    T=[[0]*676 for _ in range(676)]
    for s in A:
        K=kron(A[s],A[s])
        for i in range(676):
            for j in range(676): T[i][j]+=K[i][j]
    O=[[0]*676 for _ in range(676)]
    for (s,t,u,v),c in h.items():
        if c:
            K=kron(B[s,t],B[u,v])
            for i in range(676):
                for j in range(676): O[i][j]+=c*K[i][j]
    diffs=[labels[i][1]-labels[j][1] for i in range(26) for j in range(26)]
    N=0;H=0
    for q in sorted(set(diffs)):
        ids=[i for i in range(676) if diffs[i]==q]
        for i in range(676):
            for j in range(676):
                if diffs[i]!=diffs[j]: assert T[i][j]==0 and O[i][j]==0
        Tb=flint.fmpz_mat([[T[i][j] for j in ids] for i in ids]);Ob=flint.fmpz_mat([[O[i][j] for j in ids] for i in ids])
        P=Tb**(L-2)
        N+=tr(P*(Tb*Tb));H+=tr(Ob*P)
    return L*H,N
if __name__=='__main__':
    a=F(700741,500000);out={}
    ref={k:int(v) for k,v in (l.split('=') for l in open('/workspace/repos/Haldane_gap_dotplay/research_20261010/uniform_smaller_second_initialization_review/anchors.out').read().split())}
    for d0 in [-289,-288,-287,-285]:
        t=time.time();H,N=anchors(d0,68);R=F(H,N)+68*a
        if d0==-289: assert H==ref['H0_68'] and N==ref['N0_68'],'mismatch with repo anchors'
        out[d0]={'H0_68':str(H),'N0_68':str(N),'R68':str(R),'R68_float':float(R)}
        print(d0,'R68 =',float(R),'(exact rational stored)',f'{time.time()-t:.1f}s',flush=True)
    json.dump(out,open('tensor_R68.json','w'),indent=1)
