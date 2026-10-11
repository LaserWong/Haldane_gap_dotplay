#!/usr/bin/env python3
"""Rebuild D26 T/O directly entrywise, without importing the producer."""
import os,resource,time,json,hashlib,itertools
from pathlib import Path
os.sched_setaffinity(0,{5 if 5 in os.sched_getaffinity(0) else min(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2))
resource.setrlimit(resource.RLIMIT_CPU,(30,30))
P=Path(__file__).resolve().parent;ROOT=P.parents[1];start=time.time()
ells=[1,1,1,1,3,3,3,5];diag=[-289,-84,-9,33,-22,27,71,-11]
pair={(0,4):-11,(0,5):-35,(0,6):-28,(1,4):-23,(1,5):16,(1,6):-49,(2,4):-6,(2,5):-25,(2,6):-20,(3,4):-34,(3,5):9,(3,6):-32,(4,7):1,(5,7):2,(6,7):-16}
labels=[(a,m) for a,l in enumerate(ells) for m in range(-l,l+1,2)]
A={s:[[0]*26 for _ in range(26)] for s in (-1,0,1)}
for i,(a,m) in enumerate(labels):
    ell=ells[a];r=(ell+m)//2
    for j,(b,k) in enumerate(labels):
        s=(k-m)//2
        if s not in A or k-m!=2*s:continue
        if a==b:val=diag[a]*({-1:2*(ell-r+1),0:m,1:-(r+1)}[s])
        elif (a,b) in pair:val=pair[a,b]*({-1:2*(ell+1-r)*(ell+2-r),0:2*(r+1)*(ell-r+1),1:(r+1)*(r+2)}[s])
        elif (b,a) in pair:val=-pair[b,a]*({-1:2,0:-2,1:1}[s])
        else:continue
        A[s][i][j]=val

def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(26)) for j in range(26)] for i in range(26)]
B={(s,t):mul(A[s],A[t]) for s in A for t in A}
h={(s,t,u,v):(s*t if (s,t)==(u,v) else int(s+t==u+v and abs(s-u)==1)) for s,t,u,v in itertools.product(A,repeat=4)}
assert sum(h[s,t,s,t] for s,t in itertools.product(A,repeat=2))==0
assert all(h[s,t,u,v]==h[u,v,s,t] for s,t,u,v in h)
groups={}
for i in range(26):
    for j in range(26):groups.setdefault(labels[i][1]-labels[j][1],[]).append((i,j))
# Difference conservation follows termwise from the physical magnetization rule.
assert all(not A[s][i][j] or labels[j][1]-labels[i][1]==2*s for s in A for i in range(26) for j in range(26))
with (P/'d26_blocks.txt').open('w') as out:
    out.write(str(len(groups))+'\n')
    for q,ids in sorted(groups.items()):
        out.write(f'{q} {len(ids)}\n')
        for insertion in (False,True):
            for i,j in ids:
                row=[]
                for k,l in ids:
                    value=(sum(h[s,t,u,v]*B[s,t][i][k]*B[u,v][j][l] for s,t,u,v in h if h[s,t,u,v]) if insertion else sum(A[s][i][k]*A[s][j][l] for s in A))
                    row.append(str(value))
                out.write(' '.join(row)+'\n')
assert (P/'d26_blocks.txt').read_bytes()==(ROOT/'audit/mps/mps_blocks.txt').read_bytes()
# Independent direct physical amplitudes, no transfer representation here.
checks=[]
for n in (2,3):
    vectors={}
    for config in itertools.product(A,repeat=n):
        prod=A[config[0]]
        for s in config[1:]:prod=mul(prod,A[s])
        vectors[config]=sum(prod[i][i] for i in range(26))
    norm=sum(c*c for c in vectors.values());energy=0
    for conf,c in vectors.items():
        for site in range(n):
            nxt=(site+1)%n
            for s,t in itertools.product(A,repeat=2):
                factor=h[s,t,conf[site],conf[nxt]]
                if factor:
                    target=list(conf);target[site]=s;target[nxt]=t
                    energy+=c*factor*vectors[tuple(target)]
    checks.append({'n':n,'norm':str(norm),'total_H_numerator':str(energy)})
old=json.loads((P.parent/'nonperturbative_mps_review/d26_rebuild_results.json').read_text())
for a,b in zip(checks,old['direct_amplitude_checks']):assert a['norm']==b['norm'] and a['total_H_numerator']==b['total_H_numerator']
result={'status':'PASS','D':26,'transfer_dimension':676,'block_dimensions':[len(ids) for q,ids in sorted(groups.items())],'direct_amplitude_checks':checks,'rebuilt_blocks_sha256':hashlib.sha256((P/'d26_blocks.txt').read_bytes()).hexdigest(),'seconds':time.time()-start,'cpu_seconds':time.process_time(),'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'independent_d26.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
