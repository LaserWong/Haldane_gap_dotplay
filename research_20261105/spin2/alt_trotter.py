"""Araki-Lieb-Thirring (symmetric Trotter) UPPER bound check, float64, NONRIGOROUS evaluation:
   Z_L(beta) = Tr e^{-beta(He+Ho)} <= Tr (e^{-tau He/2} e^{-tau Ho} e^{-tau He/2})^m, tau=beta/m  (even L).
Measures the slack eta(m) = ln(Z_trot/Z) and compares with the repo's rigorous spin-1 intervals."""
import numpy as np, json, sys, time
from scipy.linalg import expm, eigvalsh
def spin(S):
    d=int(2*S+1); m=S-np.arange(d); Sz=np.diag(m)
    Sp=np.zeros((d,d)); 
    for k in range(1,d): Sp[k-1,k]=np.sqrt(S*(S+1)-m[k]*(m[k]+1))
    return Sz,Sp
def bond(S):
    Sz,Sp=spin(S); return np.kron(Sz,Sz)+0.5*(np.kron(Sp,Sp.T)+np.kron(Sp.T,Sp))
def layer(g,L,d):
    M=np.array([[1.0]])
    for _ in range(L//2): M=np.kron(M,g)
    return M
def shift_perm(L,d):
    idx=np.arange(d**L).reshape([d]*L); return np.moveaxis(idx,0,-1).ravel()  # cyclic shift of sites
def run(S,L,beta,ms,shift=0.0):
    d=int(2*S+1); h=bond(S); ev,U=np.linalg.eigh(h)
    g=lambda t: (U*np.exp(-t*ev))@U.T
    p=shift_perm(L,d)
    # exact Z via full H
    He_e=layer(np.diag(np.zeros(d*d)),L,d)
    out={}
    H=np.zeros((d**L,d**L)); 
    Hb=sum_layer=None
    def layerH():
        M=np.zeros((d**L,d**L)); I=np.eye(d)
        for b in range(L//2):
            left=np.eye(d**(2*b)); right=np.eye(d**(L-2*b-2))
            M+=np.kron(np.kron(left,h),right)
        return M
    He=layerH(); Ho=He[np.ix_(p,p)]
    E=eigvalsh(He+Ho); lnZ=np.log(np.sum(np.exp(-beta*(E-E[0]))))-beta*E[0]
    out['E0']=E[0]; out['lnZ_exact_float']=lnZ-beta*shift*L
    for m in ms:
        t=beta/m; A=layer(g(t/2),L,d); B=layer(g(t),L,d)[np.ix_(p,p)]
        M=A@B@A; lam=eigvalsh(M); lam=lam[lam>0]
        lt=np.log(np.sum((lam/lam.max())**m))+m*np.log(lam.max())
        out[f'eta_m{m}']=lt-lnZ
    return out
if __name__=='__main__':
    res={}
    a=700741/500000
    rig=json.load(open('../thermal_arb/results.json'))
    for (S,L,beta,ms) in [(1,4,12.25,[8,16,32,64,128]),(1,6,12.25,[8,16,32,64,128]),(1,8,12.25,[16,64,256]),
                          (2,4,20.0,[16,64,256]),(2,4,60.0,[64,256,1024]),(2,6,20.0,[32,128])]:
        t0=time.time(); r=run(S,L,beta,ms,shift=a if S==1 else 0.0)
        if S==1:
            hi=float(rig[f'L{L}_I']['Z_upper']); r['lnZ_rig_upper']=np.log(hi)
            r['ALT_upper_ge_rig_upper_all_m']=bool(all(r['lnZ_exact_float']+r[f'eta_m{m}']>=np.log(hi)-1e-9 for m in ms))
        r['c_fit_per_site']= {m: r[f'eta_m{m}']*m*m/(L*beta**3) for m in ms}
        r['sec']=time.time()-t0; res[f'S{S}_L{L}_b{beta}']=r; print(S,L,beta,json.dumps(r),flush=True)
    json.dump(res,open('alt_trotter.json','w'),indent=1)
