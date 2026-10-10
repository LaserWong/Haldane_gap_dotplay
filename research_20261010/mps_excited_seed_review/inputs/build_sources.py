#!/usr/bin/env python3
"""Rebuild integer local tensors and two-source norm/H insertions.

Only even-chain fixtures of length <= 6 are physically expanded. All longer
chains use charge-block auxiliary contractions. No eigensolver is used.
"""
import os, resource
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
os.sched_setaffinity(0, {max(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
resource.setrlimit(resource.RLIMIT_CPU, (300, 300))
from pathlib import Path
import itertools, json, hashlib, time
import numpy as np
P = Path(__file__).resolve().parent
ROOT = P.parents[1]
t0 = time.process_time()
ell = [1,1,1,1,3,3,3,5]
diag = [-289,-84,-9,33,-22,27,71,-11]
cross = [[-11,-35,-28],[-23,16,-49],[-6,-25,-20],[-34,9,-32]]
edge = {(a,b):cross[a][b-4] for a in range(4) for b in range(4,7)}
edge.update({(4,7):1,(5,7):2,(6,7):-16})
labels = [(a,m) for a,l in enumerate(ell) for m in range(-l,l+1,2)]
A = []
for s in [-1,0,1]:
    M = np.zeros((26,26), dtype=object)
    for i,(a,m) in enumerate(labels):
        for j,(b,k) in enumerate(labels):
            if k-m != 2*s: continue
            la,lb = ell[a],ell[b]; r = (la+m)//2
            if a==b:
                v = {-1:2*(la-r+1),0:m,1:-r-1}[s]*diag[a]
            elif (a,b) in edge:
                v = {-1:2*(la+1-r)*(la+2-r),0:2*(r+1)*(la-r+1),1:(r+1)*(r+2)}[s]*edge[a,b]
            elif (b,a) in edge:
                v = {-1:2,0:-2,1:1}[s]*(-edge[b,a])
            else: continue
            M[i,j] = v
    A.append(M)
B = [np.zeros((26,26),dtype=object),A[0],A[1]]
q = [labels[i][1]-labels[j][1] for i in range(26) for j in range(26)]
shifts = [0,-2,2,0]
E = []
O = []
W = [[A[s]@A[t], B[s]@A[t]-A[s]@B[t]] for s,t in itertools.product(range(3), repeat=2)]
h = np.zeros((9,9),dtype=object)
for s,t in itertools.product(range(3),repeat=2):
    h[3*s+t,3*s+t]=(s-1)*(t-1)
    for d in [-1,1]:
        if 0<=s+d<3 and 0<=t-d<3: h[3*(s+d)+t-d,3*s+t]=1
for p in range(4):
    u,v = p&1, (p>>1)&1
    ea,eb = (B if u else A),(B if v else A)
    E.append(sum((np.kron(a,b) for a,b in zip(ea,eb)),np.zeros((676,676),dtype=object)))
    o = np.zeros((676,676),dtype=object)
    for x,y in itertools.product(range(9),repeat=2):
        if h[x,y]: o += h[x,y]*np.kron(W[x][u],W[y][v])
    O.append(o)
    for M in [E[-1],O[-1]]:
        assert all(not M[i,j] or q[j]-q[i]==shifts[p] for i in range(676) for j in range(676))
        assert max(abs(x) for x in M.flat) < 2**63
# Byte-exact match to the already audited ground-state transfer blocks.
lines = [str(len(set(q)))]
for d in sorted(set(q)):
    ids = [i for i,x in enumerate(q) if x==d]
    lines.append(f'{d} {len(ids)}')
    for M in [E[0],O[0]]:
        lines.extend(' '.join(map(str,row)) for row in M[np.ix_(ids,ids)])
rebuilt = ('\n'.join(lines)+'\n').encode()
assert rebuilt == (ROOT/'audit/mps/mps_blocks.txt').read_bytes()
with (P/'sources.txt').open('w') as f:
    f.write(' '.join(map(str,q))+'\n')
    for family in [E,O]:
        for M in family:
            entries = [(i,j,int(M[i,j])) for i in range(676) for j in range(676) if M[i,j]]
            f.write(str(len(entries))+'\n')
            for i,j,value in entries: f.write(f'{i} {j} {value}\n')

# Independent direct physical amplitudes and complete H actions at tiny sizes.
fixtures = []
for n in [2,4,6]:
    ground = {}
    for state in itertools.product(range(3),repeat=n):
        if sum(state)!=n: continue
        mat = np.eye(26,dtype=object)
        for s in state: mat=mat@A[s]
        value = sum(mat[i,i] for i in range(26))
        if value: ground[state]=int(value)
    raised = {}
    for state,value in ground.items():
        for j,s in enumerate(state):
            if s==2: continue
            w=list(state);w[j]+=1;w=tuple(w)
            raised[w]=raised.get(w,0)+(-1)**j*value
    raised={s:v for s,v in raised.items() if v}
    flipped={tuple(2-x for x in s):v for s,v in raised.items()}
    assert ground and raised and flipped
    assert all(sum(s)==n for s in ground)
    assert all(sum(s)==n+1 for s in raised)
    assert all(sum(s)==n-1 for s in flipped)
    row={'n':n,'states':[]}
    for name,vec in [('psi',ground),('phi_plus',raised),('phi_minus',flipped)]:
        norm=sum(v*v for v in vec.values()); hv={}
        for s,v in vec.items():
            for j in range(n):
                k=(j+1)%n
                hv[s]=hv.get(s,0)+(s[j]-1)*(s[k]-1)*v
                for d in [-1,1]:
                    if 0<=s[j]+d<3 and 0<=s[k]-d<3:
                        w=list(s);w[j]+=d;w[k]-=d;w=tuple(w)
                        hv[w]=hv.get(w,0)+v
        energy=sum(v*hv.get(s,0) for s,v in vec.items())
        row['states'].append({'name':name,'norm':str(norm),'energy_numerator':str(energy),'nonzero_support':len(vec),'H_action_support':sum(v!=0 for v in hv.values())})
    assert row['states'][1]['norm']==row['states'][2]['norm']
    assert row['states'][1]['energy_numerator']==row['states'][2]['energy_numerator']
    fixtures.append(row)
out={'status':'PASS','direct_fixtures':fixtures,'source_shifts':shifts,'E_nonzero':[sum(x!=0 for x in m.flat) for m in E],'O_nonzero':[sum(x!=0 for x in m.flat) for m in O],'maximum_entry':str(max(abs(x) for m in E+O for x in m.flat)),'ground_blocks_sha256':hashlib.sha256(rebuilt).hexdigest(),'cpu_seconds':time.process_time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'source_checks.json').write_text(json.dumps(out,indent=2)+'\n')
(P/'local_tensors.json').write_text(json.dumps({'labels':labels,'physical_order':[-1,0,1],'A':[m.tolist() for m in A]},indent=2)+'\n')
print(json.dumps(out,indent=2))
