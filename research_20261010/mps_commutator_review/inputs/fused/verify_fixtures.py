#!/usr/bin/env python3
"""Independent physical correlators, exact periodic source/energy fixtures."""
import os,resource
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
from pathlib import Path
import json,itertools,time
import numpy as np
P=Path(__file__).resolve().parent;t0=time.process_time();base=P.parents[1]/'mps_excited_seed_witnesses'
A=[np.array(m,dtype=object) for m in json.loads((base/'local_tensors.json').read_text())['A']]
def clean(v):return {s:c for s,c in v.items() if c}
def Rsite(psi,j):
    v={}
    for s,c in psi.items():
        if s[j]<2:
            w=list(s);w[j]+=1;v[tuple(w)]=c
    return v
def Jsite(psi,j,n):
    v={};k=(j+1)%n
    for s,c in psi.items():
        for r,m in [(j,s[k]-1),(k,1-s[j])]:
            if s[r]<2:
                w=list(s);w[r]+=1;w=tuple(w);v[w]=v.get(w,0)+m*c
    return clean(v)
def H(v,n):
    out={}
    for s,c in v.items():
        for j in range(n):
            k=(j+1)%n;out[s]=out.get(s,0)+(s[j]-1)*(s[k]-1)*c
            for d in [-1,1]:
                if 0<=s[j]+d<3 and 0<=s[k]-d<3:
                    t=list(s);t[j]+=d;t[k]-=d;t=tuple(t);out[t]=out.get(t,0)+c
    return clean(out)
def inner(v,w):return sum(c*w.get(s,0) for s,c in v.items())
rows=[]
for n in [4,6]:
    psi={}
    for s in itertools.product(range(3),repeat=n):
        if sum(s)!=n:continue
        mat=np.eye(26,dtype=object)
        for x in s:mat=mat@A[x]
        c=int(sum(mat[i,i] for i in range(26)))
        if c:psi[s]=c
    v=Rsite(psi,0);js=[Jsite(psi,r,n) for r in range(n)];hjs=[H(j,n) for j in js]
    expected={}
    for r in range(n):
        expected.update({f'C_mix_{n}_{r}':inner(v,js[r]),f'K_mix_{n}_{r}':inner(v,hjs[r]),f'C_jj_{n}_{r}':inner(js[0],js[r]),f'K_jj_{n}_{r}':inner(js[0],hjs[r])})
    raw={k:int(v) for k,v in (line.strip().split('=') for line in (P/f'fixtures_n{n}.out').read_text().splitlines())}
    assert raw==expected,(n,set(raw)^set(expected),[(k,raw.get(k),v) for k,v in expected.items() if raw.get(k)!=v][:1])
    prior=next(r for r in json.loads((P.parent/'tiny_results.json').read_text())['rows'] if r['n']==n)
    for prefix,key in [('C','Gram'),('K','H_form')]:
        cross=2*n*sum((-1)**r*raw[f'{prefix}_mix_{n}_{r}'] for r in range(n))
        current=4*n*sum((-1)**r*raw[f'{prefix}_jj_{n}_{r}'] for r in range(n))
        assert cross==int(prior[key][0][1]) and current==int(prior[key][1][1])
    rows.append({'n':n,'all_displacements_match_full_physical_actions':True,'summed_pi_Gram_H_match_frozen_two_vector_fixture':True,'raw':{k:str(v) for k,v in raw.items()}})
out={'status':'PASS fused cells, all overlaps, periodic seam, and summed two-vector pi fixtures','rows':rows,'cpu_seconds':time.process_time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'fixture_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
