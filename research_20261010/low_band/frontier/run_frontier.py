"""Fresh coupling-specific frontier, without altering the audited g=.03 files."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,math,time,argparse
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RESEARCH=BAND.parent
sys.path.insert(0,str(BAND))
import low_band_certificate as L
import number_sector_tail as N
import correlated_low_band as C
import integrate_symmetric_ground as S
L.OUT=N.OUT=C.OUT=HERE
SHAPES=[(2,2),(4,2),(4,4)]

def create_patch(nx,ny,g):
    name=f'{nx}x{ny}_g{g}'.replace('/','d');target=HERE/f'bilayer_{name}_number_low_band.json'
    if target.exists():return json.loads(target.read_text())
    nd=nx*ny;blocks=[]
    for parity,M,q,k in [(0,0,2,1),(1,0,3,nd),(1,1,3,nd)]:
        path=HERE/f'bilayer_{name}_p{parity}_M{M}_q{q}_gram.json'
        block=json.loads(path.read_text()) if path.exists() else L.certify_block(nx,ny,g,parity,M,q,k,bits=34)
        blocks.append(block)
    bound=L.optimize_tail_bound(g,nd)
    number=N.certify_bins(nx,ny,g)
    rec=dict(status='coupling_frontier_exact_candidate_pending_independent_review',model='ordinary spin-1/2 square bilayer',
       nx=nx,ny=ny,N=nd,g=str(g),energy_shift=str(-F(3*nd,4)),boundary='periodic positive-direction edge multiset, length-2 multiplicity retained',
       full_hilbert_dimension=4**nd,retained_full_band_dimension=1+3*nd,relative_form_bound=bound,
       ritz_max_upper=str(max(F(x) for b in blocks for x in b['ritz_upper'])),
       residual_squared_bound=str(max(F(b['residual_squared_bound']) for b in blocks)),blocks=blocks)
    rec=N.update_certificate(rec,number);target.write_text(json.dumps(rec,indent=2));return rec

def ablation(recs):
    original=C.traces_float
    variants={}
    for mode in ['certified_inputs_float_replay','remove_only_omitted_tail','zero_all_low_band_widths_and_tail']:
        def trace(rec,beta):
            lo,hi,tail=original(rec,beta)
            if mode=='remove_only_omitted_tail':return lo,hi-tail,0
            if mode=='zero_all_low_band_widths_and_tail':return lo,lo,0
            return lo,hi,tail
        C.traces_float=trace
        rows=[]
        for order in ['xyt','xty','txy']:
            grid=[(C.float_score(recs,b/20,order),F(b,20)) for b in range(80,401)]
            good=sorted((score,beta) for score,beta in grid if score<0)
            valid=[(max(1-x for x in abc),F(b,20)) for b in range(80,401) if (abc:=C.float_initial(recs,b/20,order)) is not None]
            rows.append(dict(order=order,grid_beta_start='4',grid_beta_end='20',step='1/20',
              accepted_float=len(good),best_float=([float(good[0][0]),str(good[0][1])] if good else None),
              smallest_first_cycle_defect=(min(valid)[0] if valid else None)))
        variants[mode]=rows
    C.traces_float=original
    return variants

def main():
    p=argparse.ArgumentParser();p.add_argument('--couplings',default='1/25,1/20');p.add_argument('--scan-only',action='store_true');a=p.parse_args()
    summary=[]
    for g in map(F,a.couplings.split(',')):
        start=time.monotonic();recs=[create_patch(nx,ny,g) for nx,ny in SHAPES]
        sources=[HERE/'symmetry'/f'symmetry_{nx}x{ny}_g{g}_block1.json'.replace('/','d') for nx,ny in SHAPES]
        if all(p.exists() for p in sources):
            recs=[S.replace(rec,src) for rec,src in zip(recs,sources)]
            for rec,src in zip(recs,sources):
                assert F(rec['blocks'][0]['residual_squared_bound']) >= F(json.loads(src.read_text())['exact_residual_squared'])
            for (nx,ny),rec in zip(SHAPES,recs):
                (HERE/f'bilayer_{nx}x{ny}_g{g}_symmetric_number_low_band.json'.replace('/','d')).write_text(json.dumps(rec,indent=2))
            variant='symmetry_block1_ground'
        else:variant='q2_ground_waiting_for_symmetry_source'
        info=ablation(recs)
        row=dict(g=str(g),variant=variant,status='float_parameter_and_ablation_scan_of_exact_patch_inputs_not_an_all_beta_exclusion',
            ablations=info,seconds=time.monotonic()-start,
            patch_cutoffs=[str(r['global_lambda_kplus1_lower']) for r in recs],
            residual_bounds=[r['residual_squared_bound'] for r in recs],
            ground_widths=[float(F(r['blocks'][0]['eigen_upper'][0])-F(r['blocks'][0]['eigen_lower'][0])) for r in recs])
        summary.append(row);(HERE/f'frontier_g{g}.json'.replace('/','d')).write_text(json.dumps(row,indent=2));print('FRONTIER',json.dumps(row),flush=True)
    (HERE/'frontier_summary.json').write_text(json.dumps(summary,indent=2))
if __name__=='__main__':main()
