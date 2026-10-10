"""Bounded floating scalar diagnostic only; no claimed gap certificate.

Only the largest seed's one ground numerator Rayleigh is replaced. All
denominator lower endpoints, omitted-tail data, and smaller seeds are frozen.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys,json,math,copy,hashlib
from fractions import Fraction as F
from exact_filter import HERE,RES
sys.dont_write_bytecode=True
BAND=HERE.parent
sys.path.insert(0,str(BAND/'frontier_g009'))
from scan_joint import sequence,stages

def screen(recs,new_upper):
    recs=copy.deepcopy(recs);recs[2]['blocks'][0]['eigen_upper']=[new_upper]
    rows=[];best_failure=None
    for bi in range(140,281):
        beta=bi/20;st=stages(recs,beta,'txy');seq,status=sequence(st,beta,'txy',False)
        if status!='accepted_small_defect':continue
        last=seq[-1];u=last['u'];score=math.log(1/(32*u))/last['beta']
        rows.append(dict(beta=beta,asymptotic_score=score,cycle=last['cycle'],u=u,
                         initial_ratios={k:st[k] for k in ('J1','J2','C0')},
                         terminal_canonical=last['canonical']))
    return dict(successful_grid_points=len(rows),best=max(rows,key=lambda x:x['asymptotic_score']) if rows else None,
                limitation='Floating diagnostic; new independent exact scalar replay and all-size proof are required.')

def main():
    paths=[BAND/'frontier_g009'/f'combined_patch_{nx}x{ny}_g9d100.json' for nx,ny in ((4,4),(8,4),(8,8))]
    recs=[json.loads(p.read_text()) for p in paths]
    paths+=[HERE/'filtered_8x8_g9d100.json',HERE/'enlarged_8x8_g9d100.json']
    filtered,enlarged=[json.loads(p.read_text()) for p in paths[-2:]]
    out=dict(status='floating_scalar_diagnostic_only_pending_exact_replay_and_independent_review',
      g='9/100',grid='beta 7..14 step .05, txy joint sequence, at most 10 cycles',
      changed_input='Only 8x8 ground eigen_upper for one retained numerator state',
      smaller_seed_inputs_unchanged=True,all_denominator_ground_lower_bounds_unchanged=True,
      two_vector=screen(recs,filtered['shifted_rayleigh_upper']),
      enlarged_numerator=screen(recs,enlarged['shifted_rayleigh_upper']),
      source_sha256={str(p.relative_to(RES)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    (HERE/'scalar_diagnostic.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
