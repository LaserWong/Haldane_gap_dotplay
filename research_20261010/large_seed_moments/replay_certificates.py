"""Exact replay of saved rational candidates; does not regenerate geometry."""
import sys
sys.dont_write_bytecode=True
import json,time
from fractions import Fraction as F
from large_seed_moments import OUT,bilinear,matrices,geometry
from symmetric_ground import independent_indices

def run():
    start=time.monotonic();checks=[]
    for path in sorted(OUT.glob('block1_*.json')):
        r=json.loads(path.read_text());model,G,K,J,mom=matrices(r['nx'],r['ny'],r['coupling'])
        inds=independent_indices(G.tolist())
        assert inds==r['selected_basis_indices']
        for key,A in [('gram',G),('shifted_hamiltonian_numerator',K),('shifted_H2_numerator',J)]:
            assert [[int(A[i,j]) for j in inds] for i in inds]==r[key]
        assert [A.tolist() for A in mom]==r['shifted_integer_moments_M0_to_M4']
        import numpy as np
        G,K,J=[A[np.ix_(inds,inds)] for A in [G,K,J]]
        v=r['coefficients'];norm=bilinear(v,G);e=F(bilinear(v,K),model.den*norm)
        rho=model.E00+e;res=F(bilinear(v,J),model.den**2*norm)-e**2
        assert rho==F(r['exact_rayleigh']) and res==F(r['exact_residual_squared']) and res>=0
        a=F(r['second_eigenvalue_lower'])
        if r['ground_lower'] is not None:assert rho<a and F(r['ground_lower'])==rho-res/(a-rho)
        else:assert rho>=a
        checks.append(dict(file=path.name,trial_dimension=len(inds),affine_Temple=r['ground_lower'] is not None))
    out=dict(status='passed',checks=checks,seconds=time.monotonic()-start)
    (OUT/'exact_replay.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':run()
