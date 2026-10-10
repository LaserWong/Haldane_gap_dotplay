"""Weighted-energy reference E<4, with exact full-action Gram and block inertia."""
exec(open(__file__.replace('build_reference.py','common.py')).read())
import itertools,math,numpy as np
from collections import defaultdict
from scipy.linalg import eigvalsh,eigh
from inertia_trace import inertia
C=p.C
START=time.process_time();WALL=time.monotonic()
def budget():
 assert time.process_time()-START<600,'BENCHMARK STOP: exceeded ten CPU minutes'
states=[s for s in itertools.product(range(9),repeat=4) if sum(C.EX[x] for x in s)<4]
d=len(states);assert d==195
assert sum(any(x>=4 for x in s) for s in states)==20
weights=[math.prod(C.W[x] for x in s) for s in states];index=dict(zip(states,range(d)));acts=[];rows=defaultdict(list)
for j,state in enumerate(states):
 out=defaultdict(F)
 for right in range(4):
  left=(right-1)%4
  for a,b,v in C.K[state[left],state[right]]:
   ss=list(state);ss[left]=a;ss[right]=b;out[tuple(ss)]+=v
 out={ss:v for ss,v in out.items() if v};acts.append(out)
 for ss,v in out.items():rows[ss].append((j,v))
K=[[weights[i]*acts[j].get(states[i],F(0)) for j in range(d)] for i in range(d)]
J=[[F(0) for j in range(d)] for i in range(d)]
for ss,row in rows.items():
 w=math.prod(C.W[x] for x in ss)
 for i,x in row:
  for j,y in row:J[i][j]+=w*x*y
R=[r[:] for r in J]
for k in range(d):
 ids=[i for i in range(d) if K[i][k]]
 for i in ids:
  for j in ids:R[i][j]-=K[i][k]*K[k][j]/weights[k]
assert K==list(map(list,zip(*K))) and R==list(map(list,zip(*R)))
mags=[sum(C.MAG[x] for x in s) for s in states];blocks=[[i for i,x in enumerate(mags) if x==m] for m in sorted(set(mags))]
assert all(K[i][j]==R[i][j]==0 for i in range(d) for j in range(d) if mags[i]!=mags[j])
data=dict(dimension=d,full_dimension=6561,basis=states,Gram_diagonal=list(map(str,weights)),unit_K=[[str(x) for x in r] for r in K],unit_J=[[str(x) for x in r] for r in J],unit_residual_Gram=[[str(x) for x in r] for r in R],full_action_union=len(rows),residual_union=len(set(rows)-set(states)),magnetic_blocks=blocks,single_quintet_count=20,contract='P: weighted dimer energy E<4. Twenty single quintets have E=3 and belong to P. Q has weighted energy >=4.')
(HERE/'expanded_moments.json').write_text(json.dumps(data,indent=2));construction=time.process_time()-START;print('CONSTRUCTION',construction,'dimension',d,'blocks',list(map(len,blocks)),flush=True);budget()
sq=np.sqrt(weights);Kn=np.array(K,dtype=float)/np.outer(sq,sq);Rn=np.array(R,dtype=float)/np.outer(sq,sq);ev,U=eigh(Rn);assert ev.min()>-1e-10;root=U@np.diag(np.sqrt(np.maximum(ev,0)))@U.T
labels,lw,kernels=ds.dimer_local(F(1));n=len(labels);G=np.array([lw[i]*lw[j] for i in range(n) for j in range(n)]);diag=np.array([float(labels[i][2]+labels[j][2]) for i in range(n) for j in range(n)]);v=np.zeros((81,81))
for c in range(81):
 for x,y,z in kernels[1,0][c]:v[x*n+y,c]+=float(z)*math.sqrt(G[x*n+y]/G[c])
def counted(rec):
 g=F(rec['g']);props=[]
 for ai in range(1,490):
  a=ai/1000;b=max(0,-eigvalsh(float(g)*v+a*np.diag(diag),subset_by_index=[0,0],check_finite=False)[0]);props.append((4-8*a-4*b,ai))
 _,ai=max(props);local=lb.local_bound(F(1),g,F(ai,1000),'single');alpha=1-2*F(local['a']);B=4*F(local['b']);A=4*alpha-B
 E=np.diag([sum(C.EX[x] for x in ss) for ss in states]).astype(float);D=E+float(g)*Kn
 vals=eigvalsh(np.block([[D,float(g)*root],[float(g)*root,float(A)*np.eye(d)]]))[:d];groups=[]
 for val in vals:
  if not groups or val-groups[-1][0]>1e-7:groups.append([val,1])
  else:groups[-1][1]+=1
 endpoints=[];count=0
 for val,mult in groups:
  budget();t=F(math.floor((val-1e-7)*10**9),10**9);assert t<A;neg=zero=0;bcounts=[]
  for ids in blocks:
   mat=[[(A-t)*((F(sum(C.EX[x] for x in states[i]))-t)*weights[i]*(i==j)+g*K[i][j])-g*g*R[i][j] for j in ids] for i in ids]
   den=math.lcm(*(x.denominator for rr in mat for x in rr));nn,zz=inertia(np.array([[int(x*den) for x in rr] for rr in mat],dtype=object));neg+=nn;zero+=zz;bcounts.append([len(ids),nn,zz])
  assert zero==0 and neg==count,(g,t,neg,count)
  endpoints.append(dict(lower=str(t),multiplicity=mult,negative_inertia=neg,zero_inertia=zero,magnetic_block_counts=bcounts));count+=mult
 assert count==d
 assert endpoints[0]['multiplicity']==1 and F(rec['small']['ground_lower'])+8>F(endpoints[0]['lower']) and F(rec['small']['ground_lower'])+8<F(endpoints[1]['lower'])
 info=dict(dimension=d,local_comparison=local,local_exact_PSD=C.local_psd(local),alpha=str(alpha),B=str(B),omitted_cutoff=str(A),omitted_reference_excitation=4,comparison_endpoints=endpoints,complete_reference_bins=rec['small']['low_band']['complete_reference_bins'],remaining_count=6561-d)
 rec['small']['expanded_band']=info;return rec

def trace(s,beta):
 info=s['expanded_band'];rho=float(F(s['exact_rayleigh']));lo=float(F(s['ground_lower']));alpha=float(F(info['alpha']));B=float(F(info['B']))
 return math.exp(beta*(rho-lo))+sum(m['multiplicity']*math.exp(-beta*(-8+float(F(m['lower']))-rho)) for m in info['comparison_endpoints'][1:])+sum(mult*math.exp(-beta*(-8+alpha*e-B-rho)) for e,mult in info['complete_reference_bins'] if e>=4)
scan.trace=trace
recs=[];results=[]
for rec in json.loads((HERE.parent/'chain_frontier_above_02/expanded_inputs.json').read_text()):
 if rec['g']!='1/4':continue
 rec=counted(rec);recs.append(rec);print('COUNTED',rec['g'],'cpu',time.process_time()-START,'groups',len(rec['small']['expanded_band']['comparison_endpoints']),flush=True);budget()
 hits=[];maxjoint=(0,0)
 for j in range(40,1601):
  beta=j/20;shift=float(F(rec['large']['exact_rayleigh'])-2*F(rec['small']['exact_rayleigh']));J=math.exp(-2*beta*shift)/trace(rec['small'],beta)**4
  if J>maxjoint[0]:maxjoint=(J,beta)
  r=scan.run(rec['small'],float(F(rec['large']['exact_rayleigh'])),beta)
  if r:
   w=scan.interpolate(math.sqrt(J),J,beta,J);r['initial_window_gap']=w;r['all_size_gap']=min(w,r['all_M_ge8_gap']);hits.append(r)
 result=dict(g=rec['g'],maxjoint=maxjoint,passes=len(hits),best=max(hits,key=lambda r:r['all_size_gap']) if hits else None);results.append(result);print('RESULT',result,flush=True)
(HERE/'expanded_inputs.json').write_text(json.dumps(recs,indent=2));(HERE/'expanded_scan.json').write_text(json.dumps(results,indent=2));(HERE/'benchmark.json').write_text(json.dumps(dict(construction_cpu_seconds=construction,total_cpu_seconds=time.process_time()-START,wall_seconds=time.monotonic()-WALL,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)),AS_limit=resource.getrlimit(resource.RLIMIT_AS)[0]),indent=2))
