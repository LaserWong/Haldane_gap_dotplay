"""Small noncommuting spin-model pilots; floating diagnostics, not gap certificates."""
import json,time,sys
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import eigsh
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from gapflow.model import Model
from gapflow.resources import plan_resources

cases=[]
for spin,sizes in [(0.5,[4,6,8,10]),(1,[2,4,6])]:
 for n in sizes:cases.append({'name':f'spin{spin}_chain_{n}','spin':spin,'geometry':{'type':'lattice','shape':[n],'periodic':True},'terms':[{'type':'heisenberg','J':'1'}]})
for shape in [[2,2],[2,3],[3,3],[2,2,2]]:
 cases.append({'name':'half_lattice_'+'x'.join(map(str,shape)),'spin':0.5,'geometry':{'type':'lattice','shape':shape,'periodic':True},'terms':[{'type':'heisenberg','J':'1'}]})
rows=[]
for spec in cases:
 model=Model.from_dict(spec);start=time.perf_counter();H=model.hamiltonian(matrix_free=True);build=time.perf_counter()-start
 x=np.linspace(1,2,H.shape[0]);start=time.perf_counter();H@x;mv=time.perf_counter()-start
 start=time.perf_counter();vals,vecs=eigsh(H,k=min(4,H.shape[0]-1),which='SA',tol=1e-10,maxiter=2000,v0=x);elapsed=time.perf_counter()-start
 order=np.argsort(vals);vals=vals[order];vecs=vecs[:,order];res=[float(np.linalg.norm(H@v-e*v)) for e,v in zip(vals,vecs.T)]
 cal={'dimension':H.shape[0],'expanded_term_count':len(model.terms),'matvec_seconds':mv,'provenance':'Measured in this pilot, same Python matrix-free backend; one matvec measurement.'}
 plan=plan_resources(model,trial_rank=4,calibration=cal,memory_budget_bytes=512*2**20,time_budget_seconds=60)
 row={'model':spec,'dimension':H.shape[0],'computed_low_eigenpairs':len(vals),'build_seconds':build,'matvec_seconds':mv,'partial_solve_seconds':elapsed,'eigenvalues':vals.tolist(),'ritz_residual_norms':res,'lowest_ritz_spacing':float(vals[1]-vals[0]),'evidence':'FLOATING_PARTIAL_SPECTRUM_ONLY','uniform_gap_claim':False,'plan':plan}
 rows.append(row);print(spec['name'],H.shape[0],elapsed,res,flush=True)
 Path(__file__).with_name('partial_spectrum_pilots.json').write_text(json.dumps(rows,indent=2)+'\n')
