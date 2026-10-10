#!/usr/bin/env python3
"""Integer spin-z reconstruction. No numpy, scipy, producer code, or eigensolver."""
import os,resource,time,json,gzip,hashlib,struct
from pathlib import Path
from fractions import Fraction as F
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
resource.setrlimit(resource.RLIMIT_CPU,(300,300))
P=Path(__file__).resolve().parent;SRC=P.parent/'uniform_seed_size_diagnostics';OLD=P.parent/'nonperturbative_mps_assessment';start=time.time()

def digits(c,n):
    ds=[]
    for _ in range(n):c,d=divmod(c,3);ds.append(d-1)
    return ds

def basis(n,sz):
    # Build by appending the most significant site; ascending integer code order.
    def rec(k,target):
        if k==0:return [0] if target==0 else []
        if abs(target)>k:return []
        return [a*3**(k-1)+c for a in range(3) for c in rec(k-1,target-(a-1))]
    return rec(n,sz)

def hamiltonian(v,n):
    w={};pw=[3**a for a in range(n)]
    for code,c in v.items():
        if c==0:continue
        m=digits(code,n)
        diagonal=sum(m[a]*m[(a+1)%n] for a in range(n))
        w[code]=w.get(code,0)+diagonal*c
        for a in range(n):
            b=(a+1)%n
            # 1/2 times the two sqrt(2) ladder coefficients equals 1.
            if m[a]<1 and m[b]>-1:
                dest=code+pw[a]-pw[b];w[dest]=w.get(dest,0)+c
            if m[a]>-1 and m[b]<1:
                dest=code-pw[a]+pw[b];w[dest]=w.get(dest,0)+c
    return {k:v for k,v in w.items() if v}

def lower(v,n):
    w={}
    for code,c in v.items():
        for a,m in enumerate(digits(code,n)):
            if m>-1:
                dest=code-3**a;w[dest]=w.get(dest,0)+c
    return {k:v for k,v in w.items() if v}
def spinflip(v,n):return {3**n-1-k:c for k,c in v.items() if c}
def dot(v,w):return sum(c*w.get(k,0) for k,c in v.items())
def digest(values):return hashlib.sha256(b''.join(struct.pack('<q',v) for v in values)).hexdigest()
def load(n,sz):
    if n in (6,8):obj=json.loads((OLD/f'trial_n{n}.json').read_text())
    else:
        with gzip.open(SRC/f'trial_n{n}_sz{sz}.json.gz','rt') as f:obj=json.load(f)
    codes=basis(n,sz);assert len(codes)==len(obj['coefficients'])
    return dict(zip(codes,obj['coefficients']))

def report(v,n,sz,sign):
    codes=basis(n,sz);assert set(v)<=set(codes)
    if sign is not None:
        for code in codes:
            rotated=code//3+(code%3)*3**(n-1)
            assert v.get(rotated,0)==sign*v.get(code,0)
    hv=hamiltonian(v,n);assert set(hv)<=set(codes)
    nn=dot(v,v);en=dot(v,hv);assert nn>0
    return {'Sz':sz,'momentum_sign':sign,'sector_dimension':len(codes),'nonzero_support':sum(c!=0 for c in v.values()),'full_H_action_support':len(hv),'norm_square':str(nn),'energy_form':str(en),'Rayleigh':str(F(en,nn)),'coefficient_sha256':digest(v.get(c,0) for c in codes),'H_action_sha256':digest(hv.get(c,0) for c in codes)}

rows=[];claimed={r['n']:r for r in json.loads((SRC/'exact_trial_data.json').read_text())['rows']}
for n in (6,8,10,12):
    v0=load(n,0);trials=[(v0,0,None if n<10 else 1)]
    if n>=10:
        v1=load(n,1);vm=spinflip(v1,n);vl=lower(v1,n)
        assert spinflip(hamiltonian(v1,n),n)==hamiltonian(vm,n)
        assert lower(hamiltonian(v1,n),n)==hamiltonian(vl,n)
        trials += [(v1,1,-1),(vm,-1,-1),(vl,0,-1)]
    gram=[[str(dot(v,w)) for w,_,_ in trials] for v,_,_ in trials]
    assert all(gram[i][j]=='0' for i in range(len(trials)) for j in range(len(trials)) if i!=j)
    states=[report(v,n,sz,sgn) for v,sz,sgn in trials]
    for new,old in zip(states,claimed[n]['states']):
        for key,value in new.items():assert value==old[key],(n,key,value,old[key])
    # Trace test in the entire physical space, independent of trial sectors.
    trace=sum(sum(m[a]*m[(a+1)%n] for a in range(n)) for m in (digits(c,n) for c in range(3**n)))
    assert trace==0
    rows.append({'n':n,'full_dimension':3**n,'trace_H':trace,'states':states,'Gram_matrix':gram,'lowering_H_commutator_checked':n>=10,'spinflip_H_commutator_checked':n>=10})
    print('PASS exact physical trials n',n,flush=True)
result={'status':'PASS','implementation':'Python arbitrary-precision integer action in independent sparse product-basis dictionaries; no producer functions imported','rows':rows,'seconds':time.time()-start,'cpu_seconds':time.process_time(),'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'independent_trials.json').write_text(json.dumps(result,indent=2)+'\n')
print({k:v for k,v in result.items() if k!='rows'})
