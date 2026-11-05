import numpy as np
from scipy.linalg import expm
from jsearch import x, G, v, P
ms=[2,1,0,-1,-2]; Sp=np.zeros((5,5))
for i in range(1,5): m=ms[i]; Sp[i-1,i]=np.sqrt(6-m*(m+1))
Sy=(Sp-Sp.T)/(2j)
U=expm(-1j*np.pi*Sy); print('U real?',np.abs(U.imag).max(),'sym?',np.abs(U-U.T).max())
w,O=np.linalg.eigh(U.real); V=O@np.diag(np.sqrt(w.astype(complex)))
print('VV^T=U?',np.abs(V@V.T-U).max())
def test(h,name):
    VV=np.kron(V,V); hp=VV.conj().T@h@VV; g=G(hp)
    print(name,'imag',np.abs(g.imag).max().round(12),'asym',np.abs(g-g.T).max().round(12))
    gs=g.real
    for t in [0,10,100,1000]:
        print('  t',t,'lmin',np.linalg.eigvalsh(gs+t*np.outer(v,v)).min().round(6), 'eigs', np.round(sorted(np.linalg.eigvalsh(gs+t*np.outer(v,v))),4)[:4])
test(x,'Heis'); test(x+(2/9)*x@x+(1/63)*x@x@x,'KHH1'); test(P['P3']+35/9*P['P4'],'P3+35/9P4')
