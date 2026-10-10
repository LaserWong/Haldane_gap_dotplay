exec(open(__file__.replace('expand_reference.py','explore.py')).read().split('records=[];results=[]')[0])
import numpy as np,math,itertools
from collections import defaultdict,Counter
from scipy.linalg import eigvalsh,eigh
from inertia_trace import inertia
C=p.C
states=[s for s in itertools.product(range(4),repeat=4) if sum(x!=0 for x in s)<3]
assert len(states)==67
weights=[math.prod(C.W[x] for x in s) for s in states];index=dict(zip(states,range(len(states))));actions=[]
for state in states:
 out=defaultdict(F)
 for right in range(4):
  left=(right-1)%4
  for a,b,v in C.K[state[left],state[right]]:
   s=list(state);s[left]=a;s[right]=b;out[tuple(s)]+=v
 actions.append({s:v for s,v in out.items() if v})
d=len(states)
K=[[weights[i]*actions[j].get(states[i],F(0)) for j in range(d)] for i in range(d)]
J=[[sum((math.prod(C.W[x] for x in s)*v*actions[j].get(s,F(0)) for s,v in actions[i].items()),F(0)) for j in range(d)] for i in range(d)]
R=[[J[i][j]-sum(K[i][k]*K[k][j]/weights[k] for k in range(d)) for j in range(d)] for i in range(d)]
assert K==list(map(list,zip(*K))) and R==list(map(list,zip(*R)))
data=dict(dimension=d,full_dimension=6561,basis=states,Gram_diagonal=list(map(str,weights)),unit_K=[[str(x) for x in row] for row in K],unit_J=[[str(x) for x in row] for row in J],unit_residual_Gram=[[str(x) for x in row] for row in R],full_action_union=len(set().union(*map(set,actions))),residual_union=len(set().union(*map(set,actions))-set(states)),contract='P: weighted dimer energy E<3. All quintets E=3 remain in Q.')
(HERE/'expanded_moments.json').write_text(json.dumps(data,indent=2))
sq=np.sqrt(weights);Kn=np.array(K,dtype=float)/np.outer(sq,sq);Rn=np.array(R,dtype=float)/np.outer(sq,sq)
ev,U=eigh(Rn);assert ev.min()>-1e-10
root=U@np.diag(np.sqrt(np.maximum(ev,0)))@U.T
labels,lw,kernels=ds.dimer_local(F(1));n=len(labels);G=np.array([lw[i]*lw[j] for i in range(n) for j in range(n)]);diag=np.array([float(labels[i][2]+labels[j][2]) for i in range(n) for j in range(n)]);v=np.zeros((81,81))
for c in range(81):
 for x,y,z in kernels[1,0][c]:v[x*n+y,c]+=float(z)*math.sqrt(G[x*n+y]/G[c])
def counted(rec):
 g=F(rec['g']);props=[]
 for ai in range(1,490):
  a=ai/1000;b=max(0,-eigvalsh(float(g)*v+a*np.diag(diag),subset_by_index=[0,0],check_finite=False)[0]);props.append((3-6*a-4*b,ai))
 _,ai=max(props);local=lb.local_bound(F(1),g,F(ai,1000),'single');alpha=1-2*F(local['a']);B=4*F(local['b']);A=3*alpha-B
 E=np.diag([sum(C.EX[x] for x in s) for s in states]).astype(float);D=E+float(g)*Kn
 vals=eigvalsh(np.block([[D,float(g)*root],[float(g)*root,float(A)*np.eye(d)]]))[:d]
 groups=[]
 for val in vals:
  if not groups or val-groups[-1][0]>1e-7:groups.append([val,1])
  else:groups[-1][1]+=1
 endpoints=[];count=0
 for val,mult in groups:
  t=F(math.floor((val-1e-7)*10**9),10**9);assert t<A
  mat=[[(A-t)*((F(sum(C.EX[x] for x in states[i]))-t)*weights[i]*(i==j)+g*K[i][j])-g*g*R[i][j] for j in range(d)] for i in range(d)]
  den=math.lcm(*(x.denominator for row in mat for x in row));imat=np.array([[int(x*den) for x in row] for row in mat],dtype=object);neg,zero=inertia(imat)
  assert zero==0 and neg==count,(g,t,neg,count)
  endpoints.append(dict(lower=str(t),multiplicity=mult,negative_inertia=neg,zero_inertia=zero));count+=mult
 assert count==67
 assert endpoints[0]['multiplicity']==1 and F(rec['small']['ground_lower'])+8>F(endpoints[0]['lower']) and F(rec['small']['ground_lower'])+8<F(endpoints[1]['lower'])
 info=dict(dimension=d,local_comparison=local,local_exact_PSD=C.local_psd(local),alpha=str(alpha),B=str(B),omitted_cutoff=str(A),omitted_reference_excitation=3,comparison_endpoints=endpoints,complete_reference_bins=rec['small']['low_band']['complete_reference_bins'],remaining_count=6561-67)
 rec['small']['expanded_band']=info
 return rec

def trace(s,beta):
 info=s['expanded_band'];rho=float(F(s['exact_rayleigh']));lo=float(F(s['ground_lower']));alpha=float(F(info['alpha']));B=float(F(info['B']))
 return math.exp(beta*(rho-lo))+sum(m['multiplicity']*math.exp(-beta*(-8+float(F(m['lower']))-rho)) for m in info['comparison_endpoints'][1:])+sum(mult*math.exp(-beta*(-8+alpha*e-B-rho)) for e,mult in info['complete_reference_bins'] if e>=3)
scan.trace=trace
rows=[];recs=[]
for rec in json.loads((HERE/'inputs.json').read_text()):
 rec=counted(rec);recs.append(rec);print('COUNTED',rec['g'],rec['small']['expanded_band']['omitted_cutoff'],rec['small']['expanded_band']['comparison_endpoints'][:3],flush=True)
 hits=[];maxjoint=(0,0)
 for j in range(40,1601):
  beta=j/20;shift=float(F(rec['large']['exact_rayleigh'])-2*F(rec['small']['exact_rayleigh']));J=math.exp(-2*beta*shift)/trace(rec['small'],beta)**4
  if J>maxjoint[0]:maxjoint=(J,beta)
  r=scan.run(rec['small'],float(F(rec['large']['exact_rayleigh'])),beta)
  if r:
   w=scan.interpolate(math.sqrt(J),J,beta,J);r['initial_window_gap']=w;r['all_size_gap']=min(w,r['all_M_ge8_gap']);hits.append(r)
 result=dict(g=rec['g'],maxjoint=maxjoint,passes=len(hits),best=max(hits,key=lambda r:r['all_size_gap']) if hits else None);rows.append(result);print('RESULT',result,flush=True)
 (HERE/'expanded_inputs.json').write_text(json.dumps(recs,indent=2));(HERE/'expanded_scan.json').write_text(json.dumps(rows,indent=2))
