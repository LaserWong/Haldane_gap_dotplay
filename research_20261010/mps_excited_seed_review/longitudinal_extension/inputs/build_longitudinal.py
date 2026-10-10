#!/usr/bin/env python3
"""A fourth compact witness: staggered total Sz applied to the fixed MPS."""
import os,resource
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(300,300))
from pathlib import Path
import json,itertools,time
import numpy as np
P=Path(__file__).resolve().parent;t0=time.process_time()
data=json.loads((P.parent/'local_tensors.json').read_text());labels=data['labels']
A=[np.array(m,dtype=object) for m in data['A']]
B=[(s-1)*A[s] for s in range(3)]
q=[labels[i][1]-labels[j][1] for i in range(26) for j in range(26)]
W=[[A[s]@A[t],B[s]@A[t]-A[s]@B[t]] for s,t in itertools.product(range(3),repeat=2)]
h=np.zeros((9,9),dtype=object)
for s,t in itertools.product(range(3),repeat=2):
    h[3*s+t,3*s+t]=(s-1)*(t-1)
    for d in [-1,1]:
        if 0<=s+d<3 and 0<=t-d<3:h[3*(s+d)+t-d,3*s+t]=1
transfers=[]
for family in ['norm','H']:
    for p in range(4):
        u,v=p&1,(p>>1)&1;M=np.zeros((676,676),dtype=object)
        if family=='norm':
            for a,b in zip(B if u else A,B if v else A):M+=np.kron(a,b)
        else:
            for x,y in itertools.product(range(9),repeat=2):
                if h[x,y]:M+=h[x,y]*np.kron(W[x][u],W[y][v])
        assert max(abs(x) for x in M.flat)<2**63
        assert all(not M[i,j] or q[i]==q[j] for i in range(676) for j in range(676))
        transfers.append(M)
with (P/'sources.txt').open('w') as f:
    f.write(' '.join(map(str,q))+'\n')
    for M in transfers:
        entries=[(i,j,int(M[i,j])) for i in range(676) for j in range(676) if M[i,j]]
        f.write(str(len(entries))+'\n')
        for i,j,v in entries:f.write(f'{i} {j} {v}\n')
fixtures=[]
for n in [2,4,6]:
    psi={}
    for state in itertools.product(range(3),repeat=n):
        if sum(state)!=n:continue
        M=np.eye(26,dtype=object)
        for s in state:M=M@A[s]
        value=int(sum(M[i,i] for i in range(26)))
        if value:psi[state]=value
    phi={s:sum((-1)**j*(x-1) for j,x in enumerate(s))*v for s,v in psi.items()}
    phi={s:v for s,v in phi.items() if v}
    assert phi and sum(phi.get(s,0)*v for s,v in psi.items())==0
    for s,v in psi.items():assert psi.get(s[1:]+s[:1],0)==v
    for s,v in phi.items():assert phi.get(s[1:]+s[:1],0)==-v
    Hphi={}
    for s,v in phi.items():
        for j in range(n):
            k=(j+1)%n;Hphi[s]=Hphi.get(s,0)+(s[j]-1)*(s[k]-1)*v
            for d in [-1,1]:
                if 0<=s[j]+d<3 and 0<=s[k]-d<3:
                    w=list(s);w[j]+=d;w[k]-=d;w=tuple(w);Hphi[w]=Hphi.get(w,0)+v
    fixtures.append({'n':n,'norm':str(sum(v*v for v in phi.values())),'H_numerator':str(sum(v*Hphi.get(s,0) for s,v in phi.items())),'psi_cross_inner_product':'0','translation_eigenvalue':-1,'physical_support':len(phi)})
out={'status':'PASS construction and direct fixtures','fixtures':fixtures,'cpu_seconds':time.process_time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'source_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
