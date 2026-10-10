"""Saved-moment residual filter diagnostic; no new large H action."""
import json,math
from fractions import Fraction as Q
from pathlib import Path
from scan_orders import run
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'chain_frontier'
rows=[]
for tag in ['7d40','1d5']:
 saved=json.loads((OLD/f'chain_sparse_s1_g{tag}_n4_depth4.json').read_text());s,l=saved['ground_certificates'];g=Q(saved['g']);rho=Q(l['exact_rayleigh']);v=Q(l['exact_residual_squared']);R=8*(1+g);C=R-rho
 D=10**30;rad=C*C+4*v;root=Q(math.isqrt(rad.numerator*D*D//rad.denominator),D);gain=(root-C)/2
 assert gain>0 and gain*(C+gain)<=v
 hits=[r for j in range(40,1601) if (r:=run(s,float(rho-gain),j/20))]
 best=max(hits,key=lambda r:r['all_M_ge8_gap']) if hits else None
 rows.append(dict(g=str(g),rho=str(rho),saved_full_residual_squared=str(v),global_H_upper=str(R),gain_lower=str(gain),gain_display=float(gain),quadratic_slack=str(v-gain*(C+gain)),small_ground_width=str(Q(s['ground_upper'])-Q(s['ground_lower'])),unfiltered_curvature=str(rho-2*Q(s['ground_upper'])),bounded_beta_grid='2,2.05,...,80',filtered_float_passes=len(hits),best_float=best,scope='Conditional on saved complete variance; .2 variance is not newly independently reconstructed. Bounded-grid diagnostic, not all-temperature exclusion.'))
(HERE/'filter_diagnostic.json').write_text(json.dumps(rows,indent=2)+'\n')
