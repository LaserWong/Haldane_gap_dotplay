"""Exactly solvable product-cell diagnostic, not an interacting model certificate."""
from fractions import Fraction as F
from math import comb,log10
from pathlib import Path
import json
rows=[]
eps=F(1,10**8)
for n in [16,64,256]:
 for g in [F(1,20),F(3,20),F(3,10),F(1)]:
  p=g*g/(1+g*g); mass=F(0); dim=0
  for q in range(n+1):
   mass+=comb(n,q)*p**q*(1-p)**(n-q);dim+=comb(n,q)
   if mass>=1-eps:break
  rows.append({'N_cells':n,'g':str(g),'p':str(p),'mean_excitation_count':float(n*p),'minimum_shell_cutoff_q':q,'linear_trial_dimension':str(dim),'log10_dimension':log10(dim),'exact_discarded_weight':str(1-mass),'discarded_weight_display':float(1-mass),'exact_binomial_quantile_verified':True,'compressed_product_state_bond_dimension':1})
out={'model':'H=sum_i [[g^2,-g],[-g,1]]_i; exact ground product of (|0>+g|1>)/sqrt(1+g^2)','purpose':'Quantify excitation-shell truncation cost and distinguish linear support dimension from tensor representation complexity; this is a solvable diagnostic, not evidence for an interacting model.','infidelity_tolerance':str(eps),'rows':rows}
(Path(__file__).parent/'trial_dimension_toy.json').write_text(json.dumps(out,indent=2)+'\n')
for r in rows:print(r['N_cells'],r['g'],r['minimum_shell_cutoff_q'],r['linear_trial_dimension'],r['discarded_weight_display'])
