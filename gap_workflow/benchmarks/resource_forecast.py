"""Pilot-calibrated estimates for larger finite computations, not seed predictions."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from gapflow.model import Model
from gapflow.resources import plan_resources
p=Path(__file__).parent;pilots=json.loads((p/'partial_spectrum_pilots.json').read_text())
configs=[(1,[n],'spin1_chain_6') for n in [8,10,12,16,20,24]]+[(.5,[l,l],'half_lattice_2x3') for l in [3,4,5,6,8]]+[(.5,[l,l,l],'half_lattice_2x2x2') for l in [2,3,4]]
rows=[]
for spin,shape,ref in configs:
 pilot=next(x for x in pilots if x['model']['name']==ref)
 cal=pilot['plan']['timing']['calibration']
 spec={'name':f'forecast_spin{spin}_'+ 'x'.join(map(str,shape)),'spin':spin,'geometry':{'type':'lattice','shape':shape,'periodic':True},'terms':[{'type':'heisenberg','J':'1'}]}
 model=Model.from_dict(spec)
 for sector in [None,0 if sum(model.spins2)%2==0 else 1]:
  plan=plan_resources(model,total_m2=sector,trial_rank=4,krylov_vectors=24,memory_budget_bytes=512*2**20,time_budget_seconds=60,calibration=cal)
  rows.append(plan)
(p/'resource_forecasts.json').write_text(json.dumps({'status':'HEURISTIC_RESOURCE_FORECAST_ONLY','not_minimal_seed_estimates':True,'assumed_matvec_count':200,'hardware':'Current cloud Python backend; other backends and hardware require calibration','rows':rows},indent=2)+'\n')
lines=['# Measured pilots and resource forecasts','','Eleven noncommuting finite spin models were tested with four low Ritz pairs per model. No full spectrum is required by these pilots. The spectra are floating-point diagnostics and do not certify a thermodynamic gap. The first spacing can vanish because of a ground multiplet.','','The runs used periodic positive-direction multigraph bonds. Length-two directions retain parallel bonds. A single measured matrix-vector operation calibrates each forecast, so timings are approximate. The forecasts assume 200 operations. Solver iteration counts, overheads, and convergence can differ.','','| Pilot | Full dimension | Partial solve (s) | Largest residual |','| --- | ---: | ---: | ---: |']
for x in pilots:lines.append(f"| {x['model']['name']} | {x['dimension']} | {x['partial_solve_seconds']:.5g} | {max(x['ritz_residual_norms']):.3g} |")
lines+=['','The resource forecast file compares full-space and fixed-magnetization calculations at larger sizes. A smaller symmetry sector needs independent coverage of omitted sectors before any full-model gap claim. The Python matrix-free implementation stores a basis and lookup table, so its memory is still exponential. These forecasts do not identify the minimum physical bootstrap seed.','','For comparison, the graph-state benchmark uses an exact combinatorial tail and zero computed eigenpairs. Its retained ground-state rank is one. This illustrates why a Hilbert-space dimension alone cannot predict the difficulty of a proof.']
(p/'PILOT_REPORT.md').write_text('\n'.join(lines)+'\n')
print('forecasts',len(rows),'pilot max seconds',max(x['partial_solve_seconds'] for x in pilots))
