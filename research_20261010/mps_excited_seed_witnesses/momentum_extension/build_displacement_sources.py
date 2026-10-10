#!/usr/bin/env python3
"""Local source tensors for exact C(r)=<v0,vr>, K(r)=<v0,Hvr>."""
import os,resource
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
import numpy as np
import json,itertools,time,sys
from pathlib import Path
P=Path(__file__).resolve().parent;t0=time.process_time();mode=sys.argv[1] if len(sys.argv)>1 else 'plus'
assert mode in ['plus','z']
d=json.loads((P.parent/'local_tensors.json').read_text());A=[np.array(m,dtype=object) for m in d['A']];labels=d['labels']
B=[np.zeros((26,26),dtype=object),A[0],A[1]] if mode=='plus' else [-A[0],np.zeros((26,26),dtype=object),A[2]]
q=[labels[i][1]-labels[j][1] for i in range(26) for j in range(26)]
h=np.zeros((9,9),dtype=object)
for s,t in itertools.product(range(3),repeat=2):
    h[3*s+t,3*s+t]=(s-1)*(t-1)
    for v in [-1,1]:
        if 0<=s+v<3 and 0<=t-v<3:h[3*(s+v)+t-v,3*s+t]=1
W=[[A[s]@A[t],B[s]@A[t],A[s]@B[t]] for s,t in itertools.product(range(3),repeat=2)]
sizes=[]
with (P/f'sources_{mode}.txt').open('w') as f:
    f.write(('1' if mode=='plus' else '0')+'\n')
    f.write(' '.join(map(str,q))+'\n')
    for bra,ket in itertools.product(range(2),repeat=2):
        M=sum((np.kron(a,b) for a,b in zip(B if bra else A,B if ket else A)),np.zeros((676,676),dtype=object))
        entries=[(i,j,int(M[i,j])) for i in range(676) for j in range(676) if M[i,j]];sizes.append(len(entries));f.write(str(len(entries))+'\n')
        for i,j,v in entries:assert abs(v)<2**63;f.write(f'{i} {j} {v}\n')
    for bra,ket in itertools.product(range(3),repeat=2):
        M=np.zeros((676,676),dtype=object)
        for x,y in itertools.product(range(9),repeat=2):
            if h[x,y]:M+=h[x,y]*np.kron(W[x][bra],W[y][ket])
        entries=[(i,j,int(M[i,j])) for i in range(676) for j in range(676) if M[i,j]];sizes.append(len(entries));f.write(str(len(entries))+'\n')
        for i,j,v in entries:assert abs(v)<2**63;f.write(f'{i} {j} {v}\n')
fixtures=[]
for n in [2,4,6]:
    psi={}
    for s in itertools.product(range(3),repeat=n):
        if sum(s)!=n:continue
        M=np.eye(26,dtype=object)
        for x in s:M=M@A[x]
        v=int(sum(M[i,i] for i in range(26)))
        if v:psi[s]=v
    vecs=[]
    for r in range(n):
        v={}
        for s,c in psi.items():
            if mode=='plus':
                if s[r]==2:continue
                w=list(s);w[r]+=1;v[tuple(w)]=c
            elif s[r]!=1:v[s]=(s[r]-1)*c
        vecs.append(v)
    hv=[]
    for v in vecs:
        w={}
        for s,c in v.items():
            for j in range(n):
                k=(j+1)%n;w[s]=w.get(s,0)+(s[j]-1)*(s[k]-1)*c
                for a in [-1,1]:
                    if 0<=s[j]+a<3 and 0<=s[k]-a<3:
                        t=list(s);t[j]+=a;t[k]-=a;t=tuple(t);w[t]=w.get(t,0)+c
        hv.append(w)
    C=[sum(v*vecs[r].get(s,0) for s,v in vecs[0].items()) for r in range(n)]
    K=[sum(v*hv[r].get(s,0) for s,v in vecs[0].items()) for r in range(n)]
    assert C==[C[-r%n] for r in range(n)] and K==[K[-r%n] for r in range(n)]
    fixtures.append({'n':n,'C':list(map(str,C)),'K':list(map(str,K))})
out={'mode':mode,'status':'PASS local construction and full tiny physical fixtures','fixtures':fixtures,'nonzero_counts':sizes,'cpu_seconds':time.process_time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/f'source_checks_{mode}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
