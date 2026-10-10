"""Bounded new-coupling inputs, reusing the audited geometry and first-order band."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RESEARCH=BAND.parent
sys.path.insert(0,str(BAND/'translation_band'));sys.path.insert(0,str(BAND/'quadratic_boson'))
sys.path.insert(0,str(RESEARCH/'large_seed_moments'))
import translated_band as T
import quadratic_bins as Q
import large_seed_moments as GS


def main():
    geometry={};hashes={}
    for nx,ny in ((4,4),(8,4),(8,8)):
        path=RESEARCH/'large_seed_moments'/f'geometry_{nx}x{ny}.json'
        geometry[nx,ny]=json.loads(path.read_text());hashes[str(path.relative_to(RESEARCH))]=hashlib.sha256(path.read_bytes()).hexdigest()
    GS.geometry=lambda nx,ny:geometry[nx,ny]
    allrows=[]
    for g in map(F,('7/100','2/25','1/10')):
        out=HERE/f'g{g}'.replace('/','d');out.mkdir(exist_ok=True);T.HERE=GS.OUT=Q.HERE=out
        rows=[]
        for nx,ny in ((4,4),(8,4),(8,8)):
            gr=GS.certify(nx,ny,g);four=T.fourier_certificate(T.moments(nx,ny,g));bins=Q.certify(nx,ny,g)
            a1=F(bins['bins'][1]['lower']);a2=F(bins['bins'][2]['lower']);rho=F(gr['exact_rayleigh'])-F(gr['E00']);rmax=F(four['ritz_max_upper'])
            row=dict(nx=nx,ny=ny,g=str(g),ground_rayleigh_shifted=str(rho),ground_residual_squared=gr['exact_residual_squared'],
                all_excited_cutoff=str(a1),omitted_band_cutoff=str(a2),ritz_max_upper=str(rmax),
                triplet_residual_squared_max=four['residual_squared_bound'],ground_identified=rho<a1,band_separated=rmax<a2,
                ground_Temple_width=str(F(gr['exact_residual_squared'])/(a2-rho)) if rho<a2 else None)
            rows.append(row);print('FEASIBILITY',nx,ny,g,'a2',float(a2),'rmax',float(rmax),'r2',float(F(four['residual_squared_bound'])),'ground width',float(F(row['ground_Temple_width'])) if row['ground_Temple_width'] else None,flush=True)
        (out/'feasibility.json').write_text(json.dumps(rows,indent=2));allrows.extend(rows)
    (HERE/'feasibility_summary.json').write_text(json.dumps(allrows,indent=2))
    (HERE/'geometry_source_sha256.json').write_text(json.dumps(hashes,indent=2))


if __name__=='__main__':main()
