# A3 follow-up: chi=9 convention scan with the strang_field Trotter scheme (which reproduces chi=6 and chi=16).
import sys, numpy as np
exec(open('ising_mps.py').read().split("if __name__=='__main__':")[0])
from flint import arb
def run(L,tau,chi,steps,when,order_bonds):
    Y=np.eye(2**L).reshape([2]*(2*L)); dt=tau/steps; zz=-J*np.kron(Z,Z)
    def a2(Y,i,j,G): Y=np.tensordot(G.reshape(2,2,2,2),Y,axes=([2,3],[i,j])); return np.moveaxis(Y,[0,1],[i,j])
    def a1(Y,i,G): Y=np.tensordot(G,Y,axes=([1],[i])); return np.moveaxis(Y,0,i)
    fx=expm_sym(-h*X,-dt/2); gz=expm_sym(zz,-dt); bl=bonds(L)
    if order_bonds=='periodic_first' and L>2: bl=[bl[-1]]+bl[:-1]
    if order_bonds=='even_odd' and L==4: bl=[(0,1),(2,3),(1,2),(3,0)]
    def tr(Y):
        T=np.transpose(Y,[x for k in range(L) for x in (k,L+k)]).reshape([4]*L);cores=[];rest=T.reshape(1,-1);r=1
        for k in range(L-1):
            rest=rest.reshape(r*4,-1);U,S,Vt=np.linalg.svd(rest,full_matrices=False);kk=min(chi,len(S))
            cores.append(U[:,:kk].reshape(r,4,kk));rest=S[:kk,None]*Vt[:kk];r=kk
        cores.append(rest.reshape(r,4,1));T=cores[0]
        for c in cores[1:]:T=np.tensordot(T,c,axes=([-1],[0]))
        return np.transpose(T.reshape([2]*(2*L)),[2*k for k in range(L)]+[2*k+1 for k in range(L)])
    for st in range(steps):
        for i in range(L): Y=a1(Y,i,fx)
        if when=='after_field1': Y=tr(Y)
        for (i,j) in bl: Y=a2(Y,i,j,gz)
        if when=='after_zz': Y=tr(Y)
        for i in range(L): Y=a1(Y,i,fx)
        if when in ('step','after_field1'): Y=tr(Y)
    if when=='end': Y=tr(Y)
    return Y.reshape(2**L,2**L)
def Zb(L,b,chi,when,ob):
    Y=run(L,float(b.mid())/2,chi,32,when,ob); Ex=(arb_mat(Hexact(L))*(-b)/2).exp(); n=2**L
    Ya=arb_mat([[arb(float(x)) for x in r] for r in Y]); D=Ya-Ex
    eta=arb(sum((D[i,k]**2 for i in range(n) for k in range(n)),arb(0)).sqrt().upper())
    nY=sum((Ya[i,k]**2 for i in range(n) for k in range(n)),arb(0)).sqrt(); lo=arb(nY.lower())-eta
    return (arb((lo*lo).lower()) if lo>0 else arb(0)),arb(((arb(nY.upper())+eta)**2).upper())
beta=arb(1)/2
for ob in ('ring','periodic_first','even_odd'):
  for when in ('step','after_zz','after_field1','end'):
    row=[]
    for chi in (6,9,16):
        A=Zb(2,beta,chi,when,ob);B=Zb(4,beta,chi,when,ob);D=Zb(4,2*beta,chi,when,ob)
        s=arb((B[0]/A[1]**2).lower());t=arb((D[0]/B[1]**2).lower());row.append(best(s,t,beta,8))
    print(f'bonds={ob:14s} truncate={when:12s}: chi=6,9,16 ->',['%.7f'%g if g else None for g in row],flush=True)
print('claimed: 1.492020 1.714857 1.931304')
