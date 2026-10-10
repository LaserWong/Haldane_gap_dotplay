"""Canonical finite-window and exact small-size bridges for transported seeds."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RESEARCH=BAND.parent
sys.path.insert(0,str(BAND/'translation_band'));sys.path.insert(0,str(RESEARCH/'root_review'))
import large_refined_pipeline as P
import number_sector_tail as NT
from finite_window_2d import interpolate_2d,gap


def main():
    small=HERE/'small_sizes';small.mkdir(exist_ok=True);NT.OUT=small;NT.occupation_counts=P.iso_counts
    small_bounds=[]
    for side in range(2,8):
        number=NT.certify_bins(side,side,F(3,50));a1=F(number['bins'][1]['lower']);assert a1>0
        small_bounds.append(dict(side=side,gap_lower=str(a1),method='lambda2>=a1, product trial gives lambda1<=0',
                                 number_file=f'small_sizes/number_bins_{side}x{side}_g3d50.json'))
    rows=[]
    for order in ('xty','txy'):
        source=HERE/f'transported_{order}_g006.json';record=json.loads(source.read_text())
        boot=record['bootstrap'];n=record['canonical_base']['n'];beta=F(record['canonical_base']['beta'])
        states=[list(map(F,record['canonical_first_purities']))]+[[1-F(x) for x in r['defects']] for r in boot['updates']]
        windows=[]
        for j,state in enumerate(states):
            thermal,details=interpolate_2d(*state);gg=gap(thermal,beta*2**j);assert gg is not None
            windows.append(dict(n=n*2**j,through=2*n*2**j,beta=str(beta*2**j),thermal_lower=str(thermal),
                                gap_lower=str(gg),details=details))
        target=F(boot['uniform_square_gap_lower'])
        needed=[F(w['gap_lower']) for w in windows if w['n']<boot['n']]
        allgap=min([target]+needed+[F(x['gap_lower']) for x in small_bounds])
        rows.append(dict(order=order,status='all_size_candidate_pending_independent_review',
            source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),small_sizes=small_bounds,
            windows=windows,asymptotic_gap=str(target),all_integer_L_ge2_gap=str(allgap),all_integer_gap_display=float(allgap)))
    (HERE/'all_size_bridges.json').write_text(json.dumps(rows,indent=2))
    print([(r['order'],r['all_integer_gap_display'],[(w['n'],float(F(w['gap_lower']))) for w in r['windows']]) for r in rows])


if __name__=='__main__':main()
