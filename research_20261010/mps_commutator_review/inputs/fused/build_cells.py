#!/usr/bin/env python3
"""Range-two current source cells with exact internal and edge-H transfers."""
import os,resource
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(2400,2400))
from pathlib import Path
import itertools,json,time
import numpy as np
P=Path(__file__).resolve().parent;t0=time.process_time();base=P.parents[1]/'mps_excited_seed_witnesses'
d=json.loads((base/'local_tensors.json').read_text());A=[np.array(m,dtype=object) for m in d['A']];labels=d['labels']
B=[np.zeros((26,26),dtype=object),A[0],A[1]];Z=[(s-1)*A[s] for s in range(3)]
R=np.array([[0,0,0],[1,0,0],[0,1,0]],dtype=object);L=R.T;M=np.diag([-1,0,1]).astype(object);I=np.eye(3,dtype=object)
q=[labels[i][1]-labels[j][1] for i in range(26) for j in range(26)]
specs=[('normal',1,None,None),('plus_bra',1,('R',0),None),('current_bra',2,('J',0),None),('current_ket',2,None,('J',0)),('current_both',2,('J',0),('J',0)),('plus_first_current',2,('R',0),('J',0)),('plus_second_current',2,('R',1),('J',0)),('current_overlap_right',3,('J',0),('J',1)),('current_overlap_left',3,('J',1),('J',0))]
def word(s,op):
    terms=[({},1)] if op is None else ([({op[1]:'R'},1)] if op[0]=='R' else [({op[1]:'R',op[1]+1:'M'},1),({op[1]:'M',op[1]+1:'R'},-1)])
    out=np.zeros((26,26),dtype=object)
    for mods,c in terms:
        mat=np.eye(26,dtype=object)
        for j,x in enumerate(s):mat=mat@({'R':B,'M':Z}.get(mods.get(j),A)[x])
        out+=c*mat
    return out
def onsite(X,j,n):
    mat=np.array([[1]],dtype=object)
    for k in range(n):mat=np.kron(mat,X if k==j else I)
    return mat
rows=[]
with (P/'cells.txt').open('w') as f:
    f.write(' '.join(map(str,q))+'\n');f.write(str(len(specs))+'\n')
    for ix,(name,n,bra,ket) in enumerate(specs):
        states=list(itertools.product(range(3),repeat=n));wb=[word(s,bra) for s in states];wk=[word(s,ket) for s in states]
        H=np.zeros((3**n,3**n),dtype=object)
        for j in range(n-1):
            H+=onsite(M,j,n)@onsite(M,j+1,n)+onsite(R,j,n)@onsite(L,j+1,n)+onsite(L,j,n)@onsite(R,j+1,n)
        obs=[np.eye(3**n,dtype=object),H]+[onsite(X,0,n) for X in [M,R,L]]+[onsite(X,n-1,n) for X in [M,R,L]]
        base_shift=int(ket is not None)-int(bra is not None);shifts=[base_shift,base_shift,base_shift,base_shift+1,base_shift-1,base_shift,base_shift+1,base_shift-1]
        f.write(f'{ix} {n}\n');counts=[];maxentry=0
        for observable,shift in zip(obs,shifts):
            mat=np.zeros((676,676),dtype=object)
            for i in range(3**n):
                for j in range(3**n):
                    if observable[i,j]:mat+=observable[i,j]*np.kron(wb[i],wk[j])
            entries=[(i,j,int(mat[i,j])) for i in range(676) for j in range(676) if mat[i,j]]
            assert all(q[j]-q[i]==2*shift for i,j,v in entries)
            maxentry=max(maxentry,max((abs(v) for i,j,v in entries),default=0));counts.append(len(entries));f.write(f'{shift} {len(entries)}\n')
            for i,j,v in entries:f.write(f'{i} {j} {v}\n')
        rows.append({'id':ix,'name':name,'length':n,'bra':bra,'ket':ket,'nonzero_counts':counts,'max_abs_entry':str(maxentry)})
        print(name,'CPU',time.process_time()-t0,'maxentry',maxentry,flush=True)
out={'status':'PASS source/observable charge checks','cells':rows,'observable_order':['identity','open internal H','first M','first R','first L','last M','last R','last L'],'cpu_seconds':time.process_time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'cell_metadata.json').write_text(json.dumps(out,indent=2)+'\n');print('DONE',out['cpu_seconds'],out['peak_kb'])
