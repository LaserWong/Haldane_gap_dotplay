"""Two Ritz states propose finite gaps. Exact rational inertia certifies completeness."""
import json,time,sys
from pathlib import Path
from dataclasses import asdict,is_dataclass
from fractions import Fraction
import numpy as np
from scipy.sparse.linalg import eigsh
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from gapflow.model import Model
from gapflow.certify import certify_gap_from_vector
cases=[(.5,[4]),(.5,[6]),(.5,[2,2]),(.5,[2,3]),(1,[2]),(1,[3])]
rows=[]
for spin,shape in cases:
 spec={'name':f'exact_spin{spin}_'+ 'x'.join(map(str,shape)),'spin':spin,'geometry':{'type':'lattice','shape':shape,'periodic':True},'terms':[{'type':'heisenberg','J':'1'}]}
 model=Model.from_dict(spec);H=model.hamiltonian(matrix_free=True)
 vals,vecs=eigsh(H,k=2,which='SA',tol=1e-11,v0=np.linspace(1,2,H.shape[0]));o=np.argsort(vals);vals=vals[o];vec=vecs[:,o[0]]
 vector=[int(round(x*10**8)) for x in vec];threshold=Fraction(int(np.floor((vals[0]+.9*(vals[1]-vals[0]))*10**8)),10**8)
 start=time.perf_counter();matrix=model.exact_hamiltonian(max_dimension=64);cert=certify_gap_from_vector(matrix,vector,threshold,max_dimension=64);elapsed=time.perf_counter()-start
 row={'model':spec,'computed_ritz_pairs':2,'full_matrix_inertia_used':True,'dimension':H.shape[0],'rational_trial_vector':vector,'threshold':str(threshold),'certificate':cert,'certificate_seconds':elapsed,'scope':'FINITE_SIZE_FULL_HILBERT_SPACE_ONLY','uniform_gap_claim':False}
 rows.append(row);print(spec['name'],H.shape[0],cert['certified'],str(cert.get('gap_lower')),elapsed,flush=True)
 Path(__file__).with_name('exact_finite_certificates.json').write_text(json.dumps(rows,indent=2,default=lambda x:asdict(x) if is_dataclass(x) else str(x))+'\n')
