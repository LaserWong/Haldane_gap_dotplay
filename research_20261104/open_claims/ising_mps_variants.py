# Sensitivity scan (A3): how much do the purification-MPS lower bounds depend on Trotter/truncation conventions?
# Same rigorous eta/Z/recursion pipeline as ising_mps.py; only the way Y is produced changes.
import sys, numpy as np
sys.argv=['x','8']
src=open('ising_mps.py').read().split("if __name__=='__main__':")[0]; exec(src)
from flint import arb
def run_variant(L,tau,chi,steps,scheme,trunc_each_gate):
    Y=np.eye(2**L).reshape([2]*(2*L)); dt=tau/steps
    zz=-J*np.kron(Z,Z); 
    def g2(Hb,t): return expm_sym(Hb,-t)
    def apply2(Y,i,j,G):
        Y=np.tensordot(G.reshape(2,2,2,2),Y,axes=([2,3],[i,j])); return np.moveaxis(Y,[0,1],[i,j])
    def apply1(Y,i,G):
        Y=np.tensordot(G,Y,axes=([1],[i])); return np.moveaxis(Y,0,i)
    fx=lambda t: expm_sym(-h*X,-t)
    bl=bonds(L)
    if scheme=='strang_field':   # e^{-dt Hx/2} e^{-dt Hzz} e^{-dt Hx/2}
        seq=[('1',i,fx(dt/2)) for i in range(L)]+[('2',i,j,g2(zz,dt)) for (i,j) in bl]+[('1',i,fx(dt/2)) for i in range(L)]
    elif scheme=='strang_zz':    # e^{-dt Hzz/2} e^{-dt Hx} e^{-dt Hzz/2}
        seq=[('2',i,j,g2(zz,dt/2)) for (i,j) in bl]+[('1',i,fx(dt)) for i in range(L)]+[('2',i,j,g2(zz,dt/2)) for (i,j) in bl]
    elif scheme=='first_split':  # e^{-dt Hzz} e^{-dt Hx}
        seq=[('2',i,j,g2(zz,dt)) for (i,j) in bl]+[('1',i,fx(dt)) for i in range(L)]
    # truncation helper from ising_mps.run_mps
    def truncate(Y):
        T=np.transpose(Y,[x for k in range(L) for x in (k,L+k)]).reshape([4]*L)
        cores=[];rest=T.reshape(1,-1);r=1
        for k in range(L-1):
            rest=rest.reshape(r*4,-1);U,S,Vt=np.linalg.svd(rest,full_matrices=False)
            kk=min(chi,len(S));cores.append(U[:,:kk].reshape(r,4,kk));rest=S[:kk,None]*Vt[:kk];r=kk
        cores.append(rest.reshape(r,4,1)); T=cores[0]
        for c in cores[1:]: T=np.tensordot(T,c,axes=([-1],[0]))
        return np.transpose(T.reshape([2]*(2*L)),[2*k for k in range(L)]+[2*k+1 for k in range(L)])
    for _ in range(steps):
        for g in seq:
            Y=apply2(Y,g[1],g[2],g[3]) if g[0]=='2' else apply1(Y,g[1],g[2])
            if trunc_each_gate and g[0]=='2': Y=truncate(Y)
        Y=truncate(Y)
    return Y.reshape(2**L,2**L)
import ising_mps as M
beta=arb(1)/2
for scheme in ('split_bond_2nd','strang_field','strang_zz','first_split'):
  for teg in (False,True):
    if scheme=='split_bond_2nd' and teg: continue
    row=[]
    for chi in (6,9,16):
        def Zb(L,b):
            if scheme=='split_bond_2nd': M.run_mps_override=None; Y=run_mps(L,float(b.mid())/2,chi,32,2)
            else: Y=run_variant(L,float(b.mid())/2,chi,32,scheme,teg)
            Ex=(arb_mat(Hexact(L))*(-b)/2).exp(); n=2**L
            Ya=arb_mat([[arb(float(x)) for x in r] for r in Y]); D=Ya-Ex
            eta=arb(sum((D[i,k]**2 for i in range(n) for k in range(n)),arb(0)).sqrt().upper())
            nY=sum((Ya[i,k]**2 for i in range(n) for k in range(n)),arb(0)).sqrt()
            lo=arb(nY.lower())-eta; lo=arb((lo*lo).lower()) if lo>0 else arb(0)
            return lo,arb(((arb(nY.upper())+eta)**2).upper())
        A=Zb(2,beta);B=Zb(4,beta);D=Zb(4,2*beta)
        s=arb((B[0]/A[1]**2).lower());t=arb((D[0]/B[1]**2).lower());row.append(best(s,t,beta,8))
    print(f'{scheme:15s} trunc_each_gate={teg}: chi=6,9,16 ->',['%.6f'%g if g else None for g in row],flush=True)
print('claimed                       : chi=6,9,16 -> 1.492020 1.714857 1.931304 ; ideal 1.973380')
