"""Bounded first-order g=.06 test, reusing independently audited geometry.
All output is confined to this new directory. Existing source files are read.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent
BAND=HERE.parent
RESEARCH=BAND.parent
sys.path.insert(0,str(BAND/'translation_band'))
sys.path.insert(0,str(RESEARCH/'large_seed_moments'))
import translated_band as T
import large_refined_pipeline as P
import number_sector_tail as NT
import large_seed_moments as GS


def main():
    T.HERE=HERE;NT.OUT=HERE;NT.occupation_counts=P.iso_counts
    geom={};hashes={}
    for nx,ny in [(4,4),(8,4),(8,8)]:
        path=RESEARCH/'large_seed_moments'/f'geometry_{nx}x{ny}.json'
        geom[nx,ny]=json.loads(path.read_text())
        hashes[str(path.relative_to(RESEARCH))]=hashlib.sha256(path.read_bytes()).hexdigest()
    GS.OUT=HERE
    GS.geometry=lambda nx,ny:geom[nx,ny]
    rows=[]
    for nx,ny in [(4,4),(8,4),(8,8)]:
        g=F(3,50);tag=f'translated_{nx}x{ny}_g3d50'
        # Preserve already prepared records and avoid repeating sparse work.
        fp=HERE/f'{tag}_fourier.json';bp=HERE/f'number_bins_{nx}x{ny}_g3d50.json'
        four=json.loads(fp.read_text()) if fp.exists() else T.fourier_certificate(T.moments(nx,ny,g))
        bins=json.loads(bp.read_text()) if bp.exists() else NT.certify_bins(nx,ny,g)
        ground=GS.certify(nx,ny,g)
        a=F(bins['bins'][2]['lower']);r=F(four['ritz_max_upper'])
        rows.append(dict(nx=nx,ny=ny,a2=str(a),ritz_max_upper=str(r),separated=r<a,
            residual_squared_bound=four['residual_squared_bound'],
            ground_residual_squared=ground['exact_residual_squared']))
    (HERE/'first_order_count_diagnostics.json').write_text(json.dumps(rows,indent=2))
    (HERE/'geometry_source_sha256.json').write_text(json.dumps(hashes,indent=2))
    print(rows)


if __name__=='__main__':main()
