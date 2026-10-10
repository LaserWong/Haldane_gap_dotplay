import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from fractions import Fraction as Q
from pathlib import Path
import json
from axis_order_search import ordered_bilayer,ROOT,OUT
CASES=[('s_half_g003_depth2',[f'bilayer_s1d2_{x}x{y}_g3d100_depth2_ground.json' for x,y in [(2,2),(4,2),(4,4)]]),
       ('s_one_g001',[f'bilayer_s1_{x}x{y}_g1d100_k1d100_q2_ground.json' for x,y in [(2,2),(4,2),(4,4)]]),
       ('s_one_g0005',[f'bilayer_s1_{x}x{y}_g1d200_k1d200_q2_ground.json' for x,y in [(2,2),(4,2),(4,4)]])]
def main():
 out=[]
 for case,files in CASES:
  paths=[ROOT/'low_energy'/f for f in files]
  if not all(p.exists() for p in paths):print('MISSING',case,flush=True);continue
  records=[json.loads(p.read_text()) for p in paths]
  for order in ['xyt','xty','txy']:
   rows=[ordered_bilayer(records,Q(k,2),order) for k in range(12,81)]
   ok=[r for r in rows if r['accepted']]
   best=max(ok,key=lambda r:Q(r['gap_lower'])) if ok else None
   item={'model_id':'square_af_bilayer_unit_rung_'+case,'hamiltonian':'sum_rung S_L dot S_R + g sum_intralayer_xy S_i dot S_j; periodic multibond convention','case':case,'order':order,'sources':list(map(str,paths)),'accepted_beta_count':len(ok),'best_grid_gap':best}
   out.append(item)
   print(case,order,'best beta',best['beta_initial'] if best else None,'gap',float(Q(best['gap_lower'])) if best else None,'L0',best['n'] if best else None,flush=True)
 (OUT/'extended_bilayer_order_results.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
