"""Store the exact local comparison used at every staircase node, including 2beta."""
from fractions import Fraction as Q
import json
from pathlib import Path
from optimize_bilayer_tail import q_cached,g_for
from axis_order_search import ROOT,OUT,nodes,record_for
p=OUT/'optimized_bilayer_tail_results.json';rows=json.loads(p.read_text())
for row in rows:
 best=row['best_grid_gap']
 if not best:continue
 records=[json.loads(Path(path).read_text()) for path in row['sources']]
 best.pop('thermal_tail_local_bounds',None);best['thermal_tail_nodes']=[]
 for i,v in enumerate(nodes(row['order'],Q(best['beta_initial']))):
  r=record_for(records,v);par=q_cached(g_for(r),r['N_dimers'],r['ground_lower'],r['ground_upper'],r['E00'],v[2])[1]
  best['thermal_tail_nodes'].append({'node_index':i,'nx':v[0],'ny':v[1],'beta':str(v[2]),'N_dimers':r['N_dimers'],'g':g_for(r),'ground_lower':r['ground_lower'],'ground_upper':r['ground_upper'],'E00':r['E00'],'parameters':par})
 best['ground_certificate_records']=records
p.write_text(json.dumps(rows,indent=2))
print('Saved actual local bounds at all used beta/2beta nodes')
