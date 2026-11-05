"""TESTED only: truncated low-energy float estimates, no rigorous tail."""
from ed_helpers import *
from pathlib import Path
import scipy, platform
from scipy.special import logsumexp
beta=64.0; shift=4.761248
out={"status":"TESTED","beta":beta,"shift":shift,"k_eigs":8,"max_Sz":4,"numpy":np.__version__,"scipy":scipy.__version__,"python":platform.python_version(),"data":{}}
for L in range(4,9):
    row={}
    for twist in (False,True):
        es=[]; blocks=[]; t=time.time()
        for M in range(5):
            st=sector(2,L,M); H=ham(2,L,st,twist)
            assert abs(H-H.T).max()<1e-12
            ev,vec=sla.eigsh(H,k=8,which='SA',tol=1e-12,v0=np.sin(np.arange(len(st))+0.123)+np.cos(np.arange(len(st))*1.4142135623730951)) if len(st)>50 else np.linalg.eigh(H.toarray())
            order=np.argsort(ev); ev=ev[order][:8]; vec=vec[:,order][:,:8]
            residual=max(np.linalg.norm(H@vec[:,i]-ev[i]*vec[:,i]) for i in range(len(ev)))
            assert residual<1e-7
            blocks.append({"M":M,"dim":len(st),"energies":ev.tolist(),"max_residual":residual})
            es.extend([(float(e),1 if M==0 else 2) for e in ev])
        val=float(logsumexp([-beta*(e+shift*L)+np.log(w) for e,w in es]))
        key='P' if twist else 'Z'; row[key]={"log":val,"blocks":blocks,"seconds":time.time()-t}
        print(L,key,'log=',val,'seconds=',time.time()-t,flush=True)
    out['data'][str(L)]=row
    Path('ed_estimates.json').write_text(json.dumps(out,indent=2))
assert abs(out['data']['4']['Z']['blocks'][0]['energies'][0]+20)<1e-9
print('Smoke check L4 E0=-20 passed; NOT full traces or rigorous intervals.',flush=True)
