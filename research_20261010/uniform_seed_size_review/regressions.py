#!/usr/bin/env python3
"""Cheap exact negative tests and analytic cost-estimate checks."""
import os,resource,json
from pathlib import Path
from fractions import Fraction as F
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
P=Path(__file__).resolve().parent
trials=json.loads((P/'independent_trials.json').read_text());scalar=json.loads((P/'independent_scalar.json').read_text())
tests={}
for row in trials['rows']:
 n=row['n'];states=row['states'];gram=[[int(x) for x in line] for line in row['Gram_matrix']]
 assert all(gram[i][j]==0 for i in range(len(states)) for j in range(len(states)) if i!=j)
 if n>=10:
  duplicate=[line[:] for line in gram];duplicate[0][1]=duplicate[0][0]
  assert not all(duplicate[i][j]==0 for i in range(4) for j in range(4) if i!=j)
  tests[f'n{n}_duplicated_trial_rejected']=True
  assert F(states[1]['Rayleigh'])==F(states[2]['Rayleigh'])
  assert F(states[1]['Rayleigh'])!=F(states[3]['Rayleigh'])
  tests[f'n{n}_lowered_energy_not_assumed_equal']=True
for r in scalar['rows']:
 n=r['n'];R=F(r['large_Rayleigh']);alpha=F(next(x for x in trials['rows'] if x['n']==n)['states'][0]['Rayleigh'])
 assert R-2*alpha==F(r['delta'])
 assert R/F(2*n)-2*alpha!=F(r['delta'])
 tests[f'n{n}_per_site_total_energy_error_rejected']=True
 if n>=10:
  boxes=r['closed_boxes'];assert len(boxes)==38
  broken=boxes[:18]+boxes[19:]
  assert any(broken[i]['upper']!=broken[i+1]['lower'] for i in range(len(broken)-1))
  tests[f'n{n}_missing_closed_box_rejected']=True
# Trinomial recurrence counts only, no next-size basis/vector is constructed.
def counts(n):
 d={0:1}
 for _ in range(n):
  e={}
  for s,c in d.items():
   for m in (-1,0,1):e[s+m]=e.get(s+m,0)+c
  d=e
 return d
C=counts(12);D=counts(14);expected=json.loads((P.parent/'uniform_seed_size_diagnostics/next_size_cost_estimate.json').read_text())
for row in expected['rows']:
 m=row['Sz'];off=14*2*sum(C.get(m-a-b,0) for a in (-1,0) for b in (0,1));nnz=off+D[m]
 assert row['sector_dimension']==D[m]
 assert row['directed_offdiagonal_entries']==off and row['stored_CSR_entry_upper']==nnz
 assert row['CSR_bytes_float64_int32']==nnz*12+(D[m]+1)*4
 assert row['eigsh_20_vector_bytes']==D[m]*20*8
 tests[f'n14_Sz{m}_analytic_count_only']=True
out={'status':'PASS','negative_and_boundary_tests':tests,'resource_estimate_scope':'Only n14 integer sector/entry/storage counts verified. Peak memory and CPU ranges remain unvalidated forecasts. No next-size support or proposal constructed.'}
(P/'regression_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
