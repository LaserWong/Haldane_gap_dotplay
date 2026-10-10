#!/usr/bin/env python3
"""Local double commutator and independently checked tiny f-sum rule."""
import os,resource,json
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1');os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
R=np.array([[0,0,0],[1,0,0],[0,1,0]],dtype=object);L=R.T;M=np.diag([-1,0,1]).astype(object);I=np.eye(3,dtype=object)
h=np.kron(M,M)+np.kron(R,L)+np.kron(L,R);J=h@np.kron(R,I)-np.kron(R,I)@h;diffL=np.kron(L,I)-np.kron(I,L)
assert np.array_equal(2*(diffL@J-J@diffL),-2*(2*np.kron(M,M)+np.kron(L,R)+np.kron(R,L)))
old=json.loads((P.parent/'mps_excited_seed_review/independent_physical.json').read_text());tiny=json.loads((P/'independent_tiny.json').read_text())
for row in tiny['rows']:
 ground=next(r for r in old['direct_fixtures'] if r['n']==row['n'])['states'][0]
 assert 3*int(row['Gram'][0][1])==-4*int(ground['energy_numerator'])
out={'status':'PASS exact local double commutator and all tiny f-sum equalities','tiny_sizes':[2,4,6],'identity':'3 G01=-4 <psi,Hpsi> for the normalized R=S+/sqrt2, w=[H,A_pi]psi convention','assumptions':'Real periodic even-length singlet psi. No H-eigenvector assumption.','n24_large_check':'To be performed against independently assembled mixed correlations.'}
(P/'independent_fsum.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
