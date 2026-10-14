"""Independent small numerical crosschecks; numerical agreement is not a proof."""
import json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from gapflow.certify import inertia, thermal_tail_certificate, schur_certificate
from gapflow.model import Model
rng=np.random.default_rng(981)
counts={'inertia_cases':0,'tail_cases':0,'schur_cases':0,'kronecker_models':0}
for n in range(1,10):
    for r in range(100):
        A=rng.integers(-5,6,(n,n)); A=A+A.T
        w=np.linalg.eigvalsh(A)
        c=inertia(A.tolist())
        assert (c.negative,c.zero,c.positive)==(sum(w < -1e-8),sum(abs(w)<1e-8),sum(w>1e-8))
        counts['inertia_cases']+=1
for n in range(2,9):
    for r in range(50):
        A=rng.integers(-2,3,(n,n)); A=A+A.T+np.diag(np.arange(n)*8)
        k=int(rng.integers(1,n)); beta=F(1,3)
        c=thermal_tail_certificate(A.tolist(),list(range(k)),beta)
        if c['tail_upper_rational'] is not None:
            w=np.linalg.eigvalsh(A)
            actual=sum(np.exp(-float(beta)*(w[k:]-w[0])))
            assert actual<=float(c['tail_upper_rational'])+1e-12
            counts['tail_cases']+=1
        try:
            c=schur_certificate(A.tolist(),list(range(k)),0)
        except ValueError:
            continue
        assert c['inertia']==inertia(A.tolist())
        counts['schur_cases']+=1
for s in [.5,1]:
    spec={'spin':s,'geometry':{'type':'graph','n_sites':3,'edges':[[0,1],[1,2],[0,2]]},'terms':[{'type':'xxz','Jxy':'3/7','Jz':'-2/5'},{'type':'field_z','h':'1/9'},{'type':'onsite_d','D':'2/11'}]}
    m=Model.from_dict(spec); d=int(2*s+1); z=np.diag(np.arange(-s,s+1)); p=np.diag([np.sqrt(s*(s+1)-a*(a+1)) for a in np.arange(-s,s)],-1)
    def site(A,i):
        result=np.ones((1,1))
        for j in range(3): result=np.kron(result,A if i==j else np.eye(d))
        return result
    Z=[site(z,i) for i in range(3)]; P=[site(p,i) for i in range(3)]
    independent=sum((3/14*(P[i]@P[j].T+P[i].T@P[j])-2/5*Z[i]@Z[j]) for i,j in [(0,1),(1,2),(0,2)])+sum((1/9*z+2/11*z@z) for z in Z)
    assert np.max(abs(independent-np.array(m.exact_hamiltonian(),dtype=float)))<1e-12
    counts['kronecker_models']+=1
print(json.dumps({'status':'passed','counts':counts,'scope':'Independent numerical diagnostics, not independent exact proof'},indent=2))
