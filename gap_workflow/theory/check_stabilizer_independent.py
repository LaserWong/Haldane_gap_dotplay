"""Independent small-matrix diagnostic, separate from analytic proof."""
import json
from math import comb
from pathlib import Path
import numpy as np


def check(name, n, edges):
    edges=sorted(set(tuple(sorted(e)) for e in edges))
    assert all(i!=j for i,j in edges)
    neighbors=[[] for _ in range(n)]
    for i,j in edges:
        neighbors[i].append(j)
        neighbors[j].append(i)
    size=2**n
    h=np.eye(size)*n/2
    independent=h.copy()
    phase=np.ones(size)
    for x in range(size):
        phase[x]=(-1)**sum(((x>>i)&1)*((x>>j)&1) for i,j in edges)
        for i in range(n):
            h[x^(1<<i),x]-=0.5*(-1)**sum((x>>j)&1 for j in neighbors[i])
            independent[x^(1<<i),x]-=0.5
    transformed=phase[:,None]*h*phase[None,:]
    exact_conjugation=np.array_equal(transformed,independent)
    eig=np.linalg.eigvalsh(h)
    expected=np.concatenate([np.full(comb(n,k),k) for k in range(n+1)])
    error=float(np.max(np.abs(eig-expected)))
    assert exact_conjugation
    assert error<1e-11
    return dict(name=name,vertices=n,edges=edges,exact_binary_matrix_conjugation=exact_conjugation,
                floating_eigenvalue_max_error=error,expected_gap=1,expected_ground_multiplicity=1)

cases=[check('single_vertex',1,[]),check('periodic_simple_L2',2,[(0,1)]),
       check('odd_cycle_L3',3,[(0,1),(1,2),(2,0)]),
       check('periodic_simple_2x2',4,[(0,1),(0,2),(1,3),(2,3)]),
       check('periodic_simple_2x3',6,[(x*3+y,x*3+(y+1)%3) for x in range(2) for y in range(3)]+[(y,3+y) for y in range(3)]),
       check('even_cycle_L8',8,[(i,(i+1)%8) for i in range(8)])]
result={'status':'PASS','evidence':'Independent finite-matrix diagnostic only. The analytic CZ proof establishes all sizes.', 'cases':cases}
path=Path(__file__).with_name('stabilizer_independent_checks.json')
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
