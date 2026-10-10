"""Replace only the ground trial using exact scalar moments of the saved
symmetry-compressed block-Krylov trial. Its source remains separately auditable.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import numpy as np
from low_band_certificate import OUT,upper_round,finish_block
from number_sector_tail import update_certificate
ROOT=OUT.parent

def replace(rec,source):
    r=json.loads(source.read_text());c=np.array([int(v) for v in r['coefficients']],dtype=object)
    mat=lambda key:np.array([[int(v) for v in row] for row in r[key]],dtype=object)
    n=int(c@mat('gram')@c);ha=int(c@mat('shifted_hamiltonian_numerator')@c);hb=int(c@mat('shifted_H2_numerator')@c)
    den=r['integer_matrix_denominator'];rho=F(ha,den*n);r2=F(hb,den*den*n)-rho*rho
    assert rho==F(r['exact_rayleigh'])-F(r['E00']) and r2==F(r['exact_residual_squared'])
    E=n*hb-ha*ha;eden=den*den*n;assert E>=0
    b=dict(parity=0,M=0,multiplicity=1,k=1,qmax=r['trial_max_excited_dimers'],
       trial_dimension=r['trial_subspace_dimension'],expanded_trial_dimension=r['actual_trial_support_dimension'],
       reached_dimension=r['reached_support_dimension'],matrix_denominator=den,residual_denominator=eden,
       G=[[str(n)]],A=[[str(ha)]],B=[[str(hb)]],E=[[str(E)]],diagonal_proposal=[str(rho)],
       residual_squared_bound=str(upper_round(float(r2),digits=12)),ritz_lower=[str(rho)],ritz_upper=[str(rho)],
       peak_rss_kib=r['peak_process_rss_kib'],source_file=str(source.relative_to(ROOT)),
       source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
       proof='Scalar moments formed by exact coefficient contraction of saved G,K,J, entire leaked H support retained.')
    rec=json.loads(json.dumps(rec));rec['blocks'][0]=b
    rec['residual_squared_bound']=str(max(F(x['residual_squared_bound']) for x in rec['blocks']))
    rec['ritz_max_upper']=str(max(F(v) for x in rec['blocks'] for v in x['ritz_upper']))
    rec=update_certificate(rec,rec['number_sector_bins'])
    rec['ground_source_variant']='symmetry_block_krylov_depth1'
    return rec

if __name__=='__main__':
    for nx,ny in [(2,2),(4,2),(4,4)]:
        source=ROOT/'symmetry'/f'symmetry_{nx}x{ny}_g3d100_block1.json'
        rec=json.loads((OUT/f'bilayer_{nx}x{ny}_g3d100_number_low_band.json').read_text())
        rec=replace(rec,source)
        (OUT/f'bilayer_{nx}x{ny}_g3d100_symmetric_number_low_band.json').write_text(json.dumps(rec,indent=2))
        b=rec['blocks'][0];print(nx,ny,'rho',float(F(b['ritz_upper'][0])),'residual',float(F(b['residual_squared_bound'])),'width',float(F(b['eigen_upper'][0])-F(b['eigen_lower'][0])),flush=True)
