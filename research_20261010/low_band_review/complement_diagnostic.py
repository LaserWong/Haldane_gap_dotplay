"""Floating diagnostics of the physical 2x2 complement and principal angle.
Not part of exact proof; imports only the independent review's model builder.
"""
from independent_review import *
import scipy.linalg as la
rec=json.loads((SRC/'bilayer_2x2_g3d100_low_band.json').read_text());n=rec['N'];k=1+3*n
h=physical_matrix(2,2).toarray();ev,uv=la.eigh(h)
p=np.array([[0,1,0,0],[1,0,1,0],[-1,0,1,0],[0,0,0,1]],dtype=float)
blocks=[]
for bl in rec['blocks']:
    ar=np.load(SRC/bl['trial_file']);basis=ar['basis'];v=ar['vectors'].astype(float)
    transform=[]
    for st in basis:
        vec=np.array([1.])
        for s in reversed(st):vec=np.kron(vec,p[:,s])
        transform.append(vec)
    w=np.array(transform).T@v
    q,_=la.qr(w,mode='economic');blocks.append(q)
    if bl['multiplicity']==2:blocks.append(q[::-1])
q=np.column_stack(blocks)
assert np.linalg.norm(q.T@q-np.eye(k))<1e-12
T=q.T@h@q;R=h@q-q@T
complement=la.null_space(q.T);C=complement.T@h@complement
residual_squared=float(la.eigvalsh(R.T@R)[-1])
angle_squared=float(la.svdvals((np.eye(4**n)-uv[:,:k]@uv[:,:k].T)@q)[0]**2)
comp_min=float(la.eigvalsh(C,subset_by_index=[0,0])[0])
b=float(F(rec['orthogonal_complement_lower']));eta2=float(F(rec['residual_squared_bound']));s2=float(F(rec['sin_angle_squared_upper']))
assert residual_squared<=eta2 and angle_squared<=s2 and comp_min>=b
result=dict(status='passed_floating_diagnostic_only',dimension=4**n,band_dimension=k,
    physical_trial_orthogonality_error=float(np.linalg.norm(q.T@q-np.eye(k))),
    physical_residual_squared_norm=residual_squared,certified_residual_squared_upper=eta2,
    physical_sin_angle_squared=angle_squared,certified_sin_angle_squared_upper=s2,
    physical_complement_minimum=comp_min,certified_complement_lower=b,
    physical_lambda_kplus1=float(ev[k]),certified_lambda_kplus1_lower=float(F(rec['global_lambda_kplus1_lower'])))
(OUT/'complement_diagnostic.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
