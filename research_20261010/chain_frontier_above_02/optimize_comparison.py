exec(open(__file__.replace('optimize_comparison.py','explore.py')).read().split('records=[];results=[]')[0])
import numpy as np,math
from scipy.linalg import eigvalsh
labels,weights,kernels=ds.dimer_local(F(1));n=len(labels);D=n*n
G=np.array([weights[i]*weights[j] for i in range(n) for j in range(n)])
diag=np.array([float(labels[i][2]+labels[j][2]) for i in range(n) for j in range(n)])
v=np.zeros((D,D))
for c in range(D):
 for x,y,z in kernels[1,0][c]:v[x*n+y,c]+=float(z)*math.sqrt(G[x*n+y]/G[c])
results=[];updated=[]
for rec in json.loads((HERE/'inputs.json').read_text()):
 g=F(rec['g']);proposals=[]
 for ai in range(1,490):
  a=ai/1000;b=max(0,-eigvalsh(float(g)*v+a*np.diag(diag),subset_by_index=[0,0],check_finite=False)[0]);A=2-4*a-4*b;proposals.append((A,ai,b))
 A,ai,b=max(proposals);local=lb.local_bound(F(1),g,F(ai,1000),'single');info=rec['small']['low_band'];alpha=1-2*F(local['a']);B=4*F(local['b']);A=2*alpha-B
 info.update(local_comparison=local,local_exact_PSD=p.C.local_psd(local),alpha=str(alpha),B=str(B),omitted_cutoff=str(A))
 info['ground_Schur']=p.lower_root(F(0),g*g*F(16,3),A)
 for m in info['triplet_modes']:m.update(p.lower_root(1+g*F(m['V_expectation']),g*g*F(m['residual_unit_squared']),A))
 hits=[];maxjoint=(0,0)
 for j in range(40,1601):
  beta=j/20;shift=float(F(rec['large']['exact_rayleigh'])-2*F(rec['small']['exact_rayleigh']));J=math.exp(-2*beta*shift)/p.trace_float(rec['small'],beta)**4
  if J>maxjoint[0]:maxjoint=(J,beta)
  r=scan.run(rec['small'],float(F(rec['large']['exact_rayleigh'])),beta)
  if r:
   w=scan.interpolate(math.sqrt(J),J,beta,J);r['initial_window_gap']=w;r['all_size_gap']=min(w,r['all_M_ge8_gap']);hits.append(r)
 result=dict(g=str(g),a=str(local['a']),b=str(local['b']),A=str(A),maxjoint=maxjoint,passes=len(hits),best=max(hits,key=lambda r:r['all_size_gap']) if hits else None);results.append(result);updated.append(rec);print(result,flush=True)
(HERE/'optimized_inputs.json').write_text(json.dumps(updated,indent=2));(HERE/'optimized_scan.json').write_text(json.dumps(results,indent=2))
