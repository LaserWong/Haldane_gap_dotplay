"""Extract exact parameter-polynomial trial matrices from audited fixed bases.
The polynomial degree follows analytically from H'(g)=Q+gV. Interpolation here
recovers matrix coefficients, not eigenvalues or certificates between points.
The 8x8 model deliberately contains Gram/first moments only.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys;sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;R=HERE.parent;ROOT=R.parent
READS={}
def read(p):
 b=p.read_bytes();READS[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return json.loads(b)
def scaled(r,k):
 d=r['integer_matrix_denominator']**(2 if k=='shifted_H2_numerator' else 1)
 return [[F(x,d) for x in row] for row in r[k]]
def fit(nodes,matrices):
 d=len(matrices[0]);degree=len(nodes)-1;out=[[[F(0) for _ in range(d)] for _ in range(d)] for _ in nodes]
 for k,x in enumerate(nodes):
  cs=[F(1)];den=F(1)
  for j,y in enumerate(nodes):
   if j==k:continue
   new=[F(0)]*(len(cs)+1)
   for i,c in enumerate(cs):new[i]-=y*c;new[i+1]+=c
   cs=new;den*=x-y
  for n,c in enumerate(cs):
   for i in range(d):
    for j in range(d):out[n][i][j]+=c/den*matrices[k][i][j]
 return out
def evaluate(cs,g):return [[sum(g**k*M[i][j] for k,M in enumerate(cs)) for j in range(len(cs[0]))] for i in range(len(cs[0]))]
def serialize(cs):return [[[str(x) for x in row] for row in M] for M in cs]
def main():
 for nx,ny in [(4,4),(8,4),(8,8)]:
  small=nx*ny<64
  nodes=list(map(F,['3/100','1/25','1/20'])) if small else list(map(F,['3/100','1/25']))
  paths=[R/'large_seed_moments'/f'block1_{nx}x{ny}_g{g}.json'.replace('/','d') for g in nodes] if small else [R/'low_band/reduced_input'/f'largest_ground_g{g}.json'.replace('/','d') for g in nodes]
  records=[read(p) for p in paths];base=records[0]
  for r in records:
   for key in ('gram','selected_basis_indices','basis','trial_subspace_dimension','gram_common_factor_removed'):assert r[key]==base[key]
  Ks=fit(nodes[:2],[scaled(r,'shifted_hamiltonian_numerator') for r in records[:2]])
  Js=fit(nodes,[scaled(r,'shifted_H2_numerator') for r in records]) if small else None
  checks=[]
  for g in map(F,['1/100','1/50','3/100','1/25','1/20','3/50','7/100','2/25','1/10']):
   if small:
    folder=R/'large_seed_moments' if g<F(3,50) else R/'low_band/frontier_g006' if g==F(3,50) else R/'low_band/frontier_g007_g010'/f'g{g}'.replace('/','d')
    path=folder/f'block1_{nx}x{ny}_g{g}.json'.replace('/','d')
   else:
    path=R/'low_band/reduced_input'/f'largest_ground_g{g}.json'.replace('/','d')
   if not path.exists():continue
   r=read(path)
   for key in ('gram','selected_basis_indices','basis','trial_subspace_dimension','gram_common_factor_removed'):assert r[key]==base[key]
   assert evaluate(Ks,g)==scaled(r,'shifted_hamiltonian_numerator')
   if small:assert evaluate(Js,g)==scaled(r,'shifted_H2_numerator')
   checks.append(str(g))
  rec=dict(status='exact_polynomial_model_candidate_pending_independent_review',geometry=[nx,ny],N=nx*ny,physical_spins=2*nx*ny,full_hilbert_dimension=4**(nx*ny),basis=base['basis'],selected_basis_indices=base['selected_basis_indices'],trial_dimension=base['trial_subspace_dimension'],gram_common_factor_removed=base['gram_common_factor_removed'],G=base['gram'],first_moment_coefficients=serialize(Ks),source_parameter_points=list(map(str,nodes)),exact_reproduction_parameter_points=checks)
  if small:rec['full_second_moment_coefficients']=serialize(Js)
  (HERE/f'model_{nx}x{ny}.json').write_text(json.dumps(rec,indent=2)+'\n')
 (HERE/'MODEL_INPUT_SHA256.json').write_text(json.dumps(READS,indent=2)+'\n')
 print('Extracted 11/29/29-dimensional fixed models; exact coupling polynomial checks passed. Largest model has no H2.',flush=True)
if __name__=='__main__':main()
