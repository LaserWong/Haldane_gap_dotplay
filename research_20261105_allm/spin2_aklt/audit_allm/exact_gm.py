# Auditor-independent exact recomputation of GM' hypothesis + constants.
from fractions import Fraction as Fr
import json
def analyze(c,n,ms=range(8,40)):
    c=[Fr(x) for x in c]; assert len(c)==n-1
    q=lambda x: sum(c[j]*c[j+x] for j in range(len(c)-x)) if 0<=x<len(c) else Fr(0)
    S=sum(c); S2=q(0); a=1/q(1); beta=a*S2-1
    res={}
    for m in ms:
        # all unordered pairs of distinct nonadjacent bonds on Z_m: separation e in 2..floor(m/2)
        ok=True; worst=None
        for e in range(2,m//2+1):
            Ce=q(e)+q(m-e) if 2*e!=m else q(e)+q(m-e)   # ordered-window count; both orientations
            # coefficient of h_a h_b + h_b h_a for separation e: windows containing both: q(e)+q(m-e) (wrap) 
            val=1-a*Ce
            if worst is None or val<worst: worst=val
            if val<0: ok=False
        res[m]=(ok,worst)
    F=a*S*S/(n-1)/(1+beta)  # eps^2+beta eps >= a eps_n S^2/(n-1) eps  =>  eps >= a S^2/(n-1) eps_n - beta
    # bound = a S^2/(n-1) * eps_n - beta = F*(eps_n - G)
    Fp=a*S*S/(n-1); G=beta/Fp
    return dict(q1=q(1),S=S,S2=S2,alpha=a,beta=beta,Fp=Fp,G=G,res=res)
c=[465,771,944,1000,944,771,465]; n=8
A=analyze(c,n)
eps8=Fr(6261,50000)
bnd=A['Fp']*(eps8-A['G'])
print('Fp',A['Fp'],float(A['Fp']),'G',A['G'],float(A['G']))
print('bound',bnd,float(bnd), 'claimed', Fr(74814907,1776546625), bnd==Fr(74814907,1776546625))
for m,(ok,w) in A['res'].items(): print(m,ok,w if m<14 else float(w))
