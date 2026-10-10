"""Checkpointed diagnostic sweep. No floating data in this file are certificates."""
from pathlib import Path
import json,time,resource
import numpy as np
from scipy.special import logsumexp
from threadpoolctl import threadpool_limits
from models import *
OUT=Path(__file__).resolve().parent/'results'

def cache_full(m):
    p=OUT/(m.fingerprint+'.npz');meta=OUT/(m.fingerprint+'.json')
    if p.exists():return np.load(p)['energies']
    t=time.monotonic();e,sec=full_spectrum(m)
    record=dict(model=m.metadata(),fingerprint=m.fingerprint,method='all nonnegative Sz dense blocks, negative Sz by spin reversal',certified=False,sectors=sec,seconds=time.monotonic()-t,E0=float(e[0]),gap=float(e[np.searchsorted(e,e[0]+1e-8)]-e[0]),ground_degeneracy=int(np.sum(abs(e-e[0])<1e-8)),dimension=len(e),max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    np.savez_compressed(p,energies=e);meta.write_text(json.dumps(record,indent=2))
    print('FULL',json.dumps(record),flush=True)
    return e

def cache_low(m,ms=(0,2,4),k=12):
    p=OUT/(m.fingerprint+'_low.json')
    if p.exists():return json.loads(p.read_text())
    t=time.monotonic();rec=dict(model=m.metadata(),fingerprint=m.fingerprint,certified=False,sectors=[])
    for m2 in ms:
        rec['sectors'].append(low_sector(m,m2,k=k));rec['seconds']=time.monotonic()-t
        p.write_text(json.dumps(rec,indent=2))
        a=rec['sectors'][-1];print('LOW',m.label,m2,a['dimension'],a['eigenvalues'][:4],max(a['residuals']),rec['seconds'],flush=True)
    return rec

def pair(e,f,b):
    le=logsumexp(-b*e);lf=logsumexp(-b*f)
    return np.exp(lf-2*le),np.exp(logsumexp(-2*b*f)-2*lf)

def accepted(S,T):
    if not 0<S<=1+1e-10 or not 0<T<=1+1e-10:return False
    p,q=max(0,1-S),max(0,1-T)
    for _ in range(32):
        if max(p,q)<=.01:return True
        a=(1-p)**2*(1-q)
        if a<=0:return False
        p=(1-a)**2/(2*a*a)
        if p>=1:return False
        a=(1-q)**2*(1-p)
        if a<=0:return False
        q=(1-a)**2/(2*a*a)
        if q>=1:return False
    return False

def run():
    # Basic square controls include nonzero transverse coupling, both spin values.
    for s in [.5,1.]:
        for nx in [2,3,4]:cache_full(square(s,nx,2))
    pairrows=[]
    for g in [.00025,.005,.02,.05,.1]:
        e=cache_full(large_d_square(2,2,g,g));f=cache_full(large_d_square(4,2,g,g))
        rows=[dict(beta=float(b),S=float(pair(e,f,b)[0]),T=float(pair(e,f,b)[1]),accepted=accepted(*pair(e,f,b))) for b in np.arange(1,20.25,.25)]
        pairrows.append(dict(family='large_D_spin1',g=g,n=2,width=2,periodic_both=True,energy_defect=float(f[0]-2*e[0]),values=rows,claim_scope='floating fixed-width diagnostic; no growing-width conclusion'))
        (OUT/'purity_scans.json').write_text(json.dumps(pairrows,indent=2))
    for g in [.00025,.005,.02]:
        cache_full(bilayer(.5,2,2,g,g,True,True))
        cache_low(bilayer(.5,4,2,g,g,True,True))
    # Strongly coupled square AFM finite-size control is not a gapped 2D certificate.
    for s in [.5,1.]:
        e=cache_full(square(s,2,2,periodic_x=True,periodic_y=True))
        f=cache_full(square(s,4,2,periodic_x=True,periodic_y=True))
        vals=[dict(beta=float(b),S=float(pair(e,f,b)[0]),T=float(pair(e,f,b)[1]),accepted=accepted(*pair(e,f,b))) for b in np.arange(.25,20.25,.25)]
        pairrows.append(dict(family='square_isotropic',spin=s,n=2,width=2,periodic_both=True,energy_defect=float(f[0]-2*e[0]),values=vals,claim_scope='negative/control finite-width diagnostic'))
    (OUT/'purity_scans.json').write_text(json.dumps(pairrows,indent=2))
if __name__=='__main__':
    with threadpool_limits(limits=1):run()
