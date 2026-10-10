"""Independent finite-chain calculations. Floating diagnostics, not interval certificates."""
from pathlib import Path
import json
import argparse
import time
from math import sqrt
import numpy as np
import scipy.sparse as sp
import scipy.linalg as la
from scipy.sparse.linalg import eigsh
from scipy.special import logsumexp
from scipy.optimize import minimize_scalar
from threadpoolctl import threadpool_limits
BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'results'

def local(s,xy=1.,z=1.,kind='heis'):
    d=int(2*s+1)
    m=np.arange(d)-s
    plus=np.zeros((d,d))
    for a in range(d-1):
        plus[a+1,a]=sqrt(s*(s+1)-m[a]*(m[a]+1))
    sz=np.diag(m)
    x=(np.kron(plus,plus.T)+np.kron(plus.T,plus))/2+np.kron(sz,sz)
    if kind=='aklt':
        vals=[(j*(j+1)-2*s*(s+1))/2 for j in range(int(2*s)+1)]
        h=np.zeros_like(x)
        for j in range(int(s)+1,int(2*s)+1):
            p=np.eye(d*d)
            for k,a in enumerate(vals):
                if k!=j:
                    p=p@(x-a*np.eye(d*d))/(vals[j]-a)
            h+=p
        h=(h+h.T)/2
        h[abs(h)<1.e-12]=0
        return h
    return xy*(np.kron(plus,plus.T)+np.kron(plus.T,plus))/2+z*np.kron(sz,sz)

def sectors(s,L):
    d=int(2*s+1)
    if abs(s*L-round(s*L))>1e-12:
        raise ValueError('This diagnostic implementation requires integer total-spin sectors.')
    ids=np.arange(d**L,dtype=np.int64)
    pw=d**np.arange(L,dtype=np.int64)
    digits=(ids[:,None]//pw)%d
    sums=digits.sum(axis=1)
    for q in range(int(s*L),int(2*s*L)+1):
        mask=sums==q
        yield q-int(s*L),ids[mask],digits[mask],pw

def block(s,L,ids,digits,pw,h,bonds=None,onsite=None):
    d=int(2*s+1)
    if bonds is None:
        bonds=np.ones(L)
    lookup=np.full(d**L,-1,dtype=np.int64)
    lookup[ids]=np.arange(len(ids))
    rr=[]
    cc=[]
    vv=[]
    if onsite is not None:
        diag=np.sum(np.asarray(onsite)[digits],axis=1)
        rr.extend(np.arange(len(ids)))
        cc.extend(np.arange(len(ids)))
        vv.extend(diag)
    trans=[]
    for ab in range(d*d):
        aa=np.flatnonzero(abs(h[:,ab])>1.e-13)
        trans.append([(int(t//d),int(t%d),float(h[t,ab])) for t in aa])
    for j in range(L):
        k=(j+1)%L
        if bonds[j]==0:
            continue
        for ab in range(d*d):
            a,b=divmod(ab,d)
            cols=np.flatnonzero((digits[:,j]==a)&(digits[:,k]==b))
            for c,e,v in trans[ab]:
                rows=lookup[ids[cols]+(c-a)*pw[j]+(e-b)*pw[k]]
                assert np.all(rows>=0)
                rr.extend(rows)
                cc.extend(cols)
                vv.extend(np.full(len(cols),v*bonds[j]))
    H=sp.coo_matrix((vv,(rr,cc)),shape=(len(ids),len(ids))).tocsr()
    H.sum_duplicates()
    assert np.max(abs((H-H.T).data),initial=0)<2.e-11
    return H

def spectrum(s,L,tag,xy=1.,z=1.,kind='heis',g=None,U=0.):
    path=OUT/f'spec_{tag}_s{s:g}_L{L}.npz'
    if path.exists():
        return np.load(path)['energies']
    h=local(s,xy,z,kind)
    m=np.arange(int(2*s+1))-s
    onsite=U*m*m*(m*m-1)/12 if U else None
    bonds=None if g is None else np.array([g if j%2==0 else 1 for j in range(L)])
    all_e=[]
    dims=[]
    t=time.time()
    for M,ids,digits,pw in sectors(s,L):
        H=block(s,L,ids,digits,pw,h,bonds,onsite)
        e=la.eigvalsh(H.toarray(),overwrite_a=True,check_finite=False,driver='evr')
        mult=1 if M==0 else 2
        all_e.extend([e]*mult)
        dims.append((M,len(e),mult))
    energies=np.sort(np.concatenate(all_e))
    assert len(energies)==int(2*s+1)**L
    np.savez_compressed(path,energies=energies,dims=np.array(dims),seconds=time.time()-t)
    print(tag,s,L,'D',len(energies),'E0',energies[0],'gap',energies[1]-energies[0],
          'seconds',time.time()-t,flush=True)
    return energies

def archived_spin2(L):
    cached=OUT/f'archived_spin2_L{L}.npz'
    if cached.exists():
        return np.load(cached)['energies']
    import os
    root=Path(os.environ.get('HALDANE_PROJECT', '/mnt/data/haldane_project'))/'cases/spin2_followup/inputs/verified_real'
    meta=json.loads((root/f'n{L}_I.json').read_text())
    es=[]
    for b in meta['blocks']:
        e=np.load(root/f'n{L}_I_m{b["m"]}_k{b["k"]}.npz')['energies']
        es.extend([e]*b['multiplicity'])
    out=np.sort(np.concatenate(es))
    assert len(out)==5**L
    return out

def pairs(e,f,beta):
    ndef=f[0]-2*e[0]
    zn=logsumexp(-beta*(e-e[0]))
    z2=logsumexp(-beta*(f-f[0]))
    z22=logsumexp(-2*beta*(f-f[0]))
    S=np.exp(-beta*ndef+z2-2*zn)
    T=np.exp(z22-2*z2)
    W=np.exp(-2*beta*ndef+z22-4*zn)
    return float(S),float(T),float(W)

def scalar_float(S,T):
    p,q=1-S,1-T
    for j in range(40):
        if max(p,q)<=.01:
            return True,j
        a=(1-p)**2*(1-q)
        p=(1-a)**2/(2*a*a)
        if p>=1:
            return False,j+1
        a=(1-q)**2*(1-p)
        q=(1-a)**2/(2*a*a)
        if q>=1:
            return False,j+1
    return False,40

def bench():
    rows=[]
    for s,L in [(1,2),(1,4),(1,6),(1,8),(2,2),(2,4),(2,6),(3,2),(3,4)]:
        e=spectrum(s,L,'heis')
        rows.append(dict(s=s,L=L,E0=float(e[0]),gap=float(e[1]-e[0]),dimension=len(e)))
    for U in [8,32,128]:
        for L in [4,6]:
            e=spectrum(2,L,f'penU{U}',xy=1/3,z=1,U=U)
            rows.append(dict(s=2,L=L,U=U,E0=float(e[0]),gap=float(e[1]-e[0]),dimension=len(e),model='penalty'))
    for s in [1.5,2.5]:
        g=.03/(s*(2*s+1))
        for L in ([4,6] if s==1.5 else [4]):
            e=spectrum(s,L,'dimer',g=g)
            rows.append(dict(s=s,L=L,g=g,E0=float(e[0]),gap=float(e[1]-e[0]),dimension=len(e),model='dimer'))
    (OUT/'finite_chain_diagnostics.json').write_text(json.dumps(rows,indent=2))

def purity_scan():
    rows=[]
    curves={}
    for s,n in [(1,2),(1,4),(2,2),(2,4),(3,2)]:
        e=spectrum(s,n,'heis')
        f=archived_spin2(8) if (s,n)==(2,4) else spectrum(s,2*n,'heis')
        C=float(f[0]-2*e[0])
        hi=max(4.,(2*n*np.log(2*s+1)-np.log(np.sqrt(2)-1))/(2*C))
        res=minimize_scalar(lambda b:-pairs(e,f,b)[2],bounds=(0,hi),method='bounded',options={'xatol':1e-11})
        bs=np.linspace(0,hi,401)
        vals=np.array([pairs(e,f,b) for b in bs])
        curves[f's{s}_n{n}']=np.column_stack([bs,vals])
        S,T,W=pairs(e,f,res.x)
        row=dict(s=s,n=n,beta_at_Wmax=float(res.x),Wmax=W,S=S,T=T,
                 E0n=float(e[0]),E02n=float(f[0]),energy_defect=C,
                 gap_n=float(e[1]-e[0]),gap_2n=float(f[1]-f[0]),
                 thermal_scan_end=hi,seed_success_on_grid=any(scalar_float(a,b)[0] for a,b,c in vals),
                 source='independent ED except archived spin-2 L=8')
        print('PURITY',row,flush=True)
        rows.append(row)
    np.savez_compressed(OUT/'purity_curves.npz',**curves)
    (OUT/'purity_scan.json').write_text(json.dumps(rows,indent=2))
    comparisons=[]
    for L in [4,6]:
        e=spectrum(2,L,'heis')
        a=archived_spin2(L)
        comparisons.append(dict(L=L,max_abs_difference=float(np.max(abs(e-a)))))
    (OUT/'independent_archive_crosscheck.json').write_text(json.dumps(comparisons,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('task',choices=['bench','purity'])
    args=ap.parse_args()
    with threadpool_limits(limits=1):
        bench() if args.task=='bench' else purity_scan()
