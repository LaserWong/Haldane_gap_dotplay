#!/usr/bin/env python3
"""Exact pi-only2x2 Gram/H and rational optimized orthogonal trial states."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,time,os,resource
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
P=Path(__file__).resolve().parent;BASE=P.parents[1]/'mps_excited_seed_witnesses';t0=time.process_time()
state=json.loads((P/'n24_checkpoint.json').read_text());assert state['status']=='complete' and len(state['completed'])==37
raw={k:int(v) for k,v in state['exact'].items()};n=24
def vals(prefix,family):return [raw[f'{prefix}_{family}_24_{r if family=="mix" else min(r,n-r)}'] for r in range(n)]
Cmix,Kmix,Cjj,Kjj=[vals(p,f) for p,f in [('C','mix'),('K','mix'),('C','jj'),('K','jj')]]
old={k:int(v) for k,v in (line.strip().split('=') for line in (BASE/'contractions_n24.out').read_text().splitlines())}
summed=lambda xs:sum((-1)**r*x for r,x in enumerate(xs))
G=[[old['N1_24'],2*n*summed(Cmix)],[2*n*summed(Cmix),4*n*summed(Cjj)]]
H=[[old['H1_24'],2*n*summed(Kmix)],[2*n*summed(Kmix),4*n*summed(Kjj)]]
assert 3*G[0][1]==-4*old['H0_24']
detG=G[0][0]*G[1][1]-G[0][1]**2;assert G[0][0]>0 and detG>0
linear=H[0][0]*G[1][1]+H[1][1]*G[0][0]-2*H[0][1]*G[0][1]
detH=H[0][0]*H[1][1]-H[0][1]**2;disc=linear*linear-4*detG*detH;assert disc>0
GRID=1<<160;root=isqrt(disc*GRID*GRID);sl,su=F(root,GRID),F(root+1,GRID);assert sl*sl<=disc<=su*su
lo,hi=(linear-su)/(2*detG),(linear-sl)/(2*detG);mid=(lo+hi)/2
# Use a fully rational fixed vector close to the lower generalized Ritz mode.
c=[-(H[0][1]-mid*G[0][1]),H[0][0]-mid*G[0][0]];scale=max(abs(x) for x in c);assert scale>0
u=[round(x/scale*10**12) for x in c];assert any(u)
a=G[0][0]*u[0]+G[0][1]*u[1];b=G[0][1]*u[0]+G[1][1]*u[1];v=[b,-a]
def bilinear(x,y,A):return sum(x[i]*A[i][j]*y[j] for i in range(2) for j in range(2))
assert bilinear(u,v,G)==0
norms=[bilinear(x,x,G) for x in [u,v]];energies=[bilinear(x,x,H) for x in [u,v]];assert min(norms)>0
rays=[F(e,z) for e,z in zip(energies,norms)];initial=F(H[0][0],G[0][0]);assert lo<=rays[0]<=initial and rays[0]-hi<F(1,10**10)
prior=json.loads((BASE/'singlet_completion/fourier_witness_data.json').read_text());alpha0=F(prior['ground_Rayleigh']);assert min(rays)>alpha0
out={'status':'PASS exact pi2x2 forms and two rational orthogonal trial states; independent review pending','n':24,'momentum':'pi only','basis':['v=A_pi psi, A_pi=sum(-1)^j S_j+/sqrt2','w=[H,A_pi]psi=2sum(-1)^j(R_j M_(j+1)-M_j R_(j+1))psi'],'Gram':[[str(x) for x in r] for r in G],'H_form':[[str(x) for x in r] for r in H],'Gram_determinant':str(detG),'cross_Gram_sum_rule':'3 G01=-4 <psi,Hpsi>, checked exactly against ordinary ground contraction','lower_generalized_Ritz_interval':[str(lo),str(hi)],'initial_pi_Rayleigh':str(initial),'ground_trial_Rayleigh':str(alpha0),'initial_pi_energy_difference_display':float(initial-alpha0),'rational_states':[{'coefficients':list(map(str,x)),'norm':str(z),'H_numerator':str(e),'Rayleigh':str(r),'energy_difference_from_psi':str(r-alpha0),'energy_difference_display':float(r-alpha0)} for x,z,e,r in zip([u,v],norms,energies,rays)],'exact_cross_Gram':'0','pi_Rayleigh_improvement':str(initial-rays[0]),'pi_Rayleigh_improvement_display':float(initial-rays[0]),'physical_search_dimension_at_pi':2,'single_state_MPS_bond_upper':156,'full_Hilbert_dimension':3**24,'symmetry_completion':'The verified n24 singlet and [R_total,[H,A_pi]]=0 make both basis vectors highest-weight Sz1 states. Every rational combination has identical normalized-lowered and spin-flipped Rayleigh partners. Two G-orthogonal combinations produce two mutually orthogonal spin1 triplets.','scope':'These are trial-state energies and compressed2x2 Rayleigh data, not exact physical eigenvalues.','cpu_seconds':time.process_time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'pi_two_vector_results.json').write_text(json.dumps(out,indent=2)+'\n')
groups=[r for r in prior['trace_groups'] if r['k_representative']!=12]
cases=[]
for count in [1,2]:
    casegroups=[{'multiplicity':r['multiplicity'],'gap_upper':r['energy_difference_upper'],'origin':f'momentum representative k{r["k_representative"]}'} for r in groups]
    casegroups += [{'multiplicity':3,'gap_upper':str(rays[i]-alpha0),'origin':f'rational pi triplet {i}'} for i in range(count)]
    cases.append({'retained_denominator_states':67+3*count,'groups':casegroups})
(P/'pi_trace_cases.json').write_text(json.dumps({'n':24,'delta':prior['delta'],'numerator_Rayleigh':prior['numerator_Rayleigh'],'cases':cases},indent=2)+'\n')
print('Original pi trial gap',float(initial-alpha0));print('New rational pi trial gaps',[float(r-alpha0) for r in rays]);print('Improvement',float(initial-rays[0]));print('Search dimension2; MPS bound156; trace spans70 or73')
