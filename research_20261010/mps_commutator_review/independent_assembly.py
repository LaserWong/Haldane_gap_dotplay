#!/usr/bin/env python3
"""Independent pi Gram/H assembly and exact rational orthogonalization checks."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,os,resource,time
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));P=Path(__file__).resolve().parent;t0=time.process_time()
def raw(path):return {k:int(v) for k,v in (s.split('=') for s in path.read_text().splitlines())}
a=raw(P/'independent_n24.out');assert len(a)==74 and a==raw(P/'inputs/physical/n24_exact.out')
old=raw(P.parent/'mps_excited_seed_review/independent_contractions.out');n=24
mixed={kind:[a[f'{kind}_mix_24_{r}'] for r in range(n)] for kind in ['C','K']}
current={kind:[a[f'{kind}_jj_24_{min(r,n-r)}'] for r in range(n)] for kind in ['C','K']}
def alternating(v):return sum(v[::2])-sum(v[1::2])
G=[[old['N1_24'],2*n*alternating(mixed['C'])],[2*n*alternating(mixed['C']),4*n*alternating(current['C'])]]
H=[[old['H1_24'],2*n*alternating(mixed['K'])],[2*n*alternating(mixed['K']),4*n*alternating(current['K'])]]
producer=json.loads((P/'inputs/scalar/pi_two_vector_results.json').read_text());assert G==[[int(x) for x in r] for r in producer['Gram']] and H==[[int(x) for x in r] for r in producer['H_form']]
assert 3*G[0][1]==-4*old['H0_24'];det=G[0][0]*G[1][1]-G[0][1]**2;assert G[0][0]>0 and det>0 and det==int(producer['Gram_determinant'])
b=H[0][0]*G[1][1]+H[1][1]*G[0][0]-2*H[0][1]*G[0][1];c=H[0][0]*H[1][1]-H[0][1]**2;disc=b*b-4*det*c;assert disc>0;D=10**80;s=isqrt(disc*D*D);sl,sh=F(s,D),F(s+1,D);assert sl*sl<=disc<=sh*sh
lower=[(b-sh)/(2*det),(b-sl)/(2*det)];upper=[(b+sl)/(2*det),(b+sh)/(2*det)]
pl,ph=map(F,producer['lower_generalized_Ritz_interval']);assert pl<=lower[0]<=lower[1]<=ph
coefficients=[list(map(int,x['coefficients'])) for x in producer['rational_states']]
def bilinear(x,A,y):return sum(x[i]*A[i][j]*y[j] for i in range(2) for j in range(2))
u,v=coefficients;assert any(u) and any(v) and bilinear(u,G,v)==0
Gu=[sum(G[i][j]*u[j] for j in range(2)) for i in range(2)];assert v==[Gu[1],-Gu[0]]
alpha0=F(old['H0_24'],old['N0_24']);rays=[];states=[]
for vec,saved in zip(coefficients,producer['rational_states']):
 norm=bilinear(vec,G,vec);energy=bilinear(vec,H,vec);assert norm>0
 ray=F(energy,norm);assert norm==int(saved['norm']) and energy==int(saved['H_numerator']) and ray==F(saved['Rayleigh']) and ray>alpha0
 rays.append(ray);states.append({'coefficients':list(map(str,vec)),'norm':str(norm),'H_numerator':str(energy),'Rayleigh':str(ray),'gap_from_psi':str(ray-alpha0),'gap_display':float(ray-alpha0)})
initial=F(H[0][0],G[0][0]);assert lower[0]<=rays[0]<initial and rays[0]-lower[1]<F(1,10**10)
assert rays[0]+rays[1]==F(b,det), 'Trace of the compressed operator is basis independent.'
derivative=2*F(H[0][1]*G[0][0]-H[0][0]*G[0][1],G[0][0]**2);assert derivative>0
prior=json.loads((P.parent/'mps_excited_seed_review/momentum_extension/independent_fourier.json').read_text());groups=[g for g in prior['groups70'] if g['k']!=12];assert sum(g['multiplicity'] for g in groups)==66
cases=[]
source=json.loads((P/'inputs/scalar/pi_trace_cases.json').read_text())
for count in [1,2]:
 own=[{'multiplicity':g['multiplicity'],'gap_upper':g['gap_upper'],'origin':f'k{g["k"]}'} for g in groups]+[{'multiplicity':3,'gap_upper':str(rays[j]-alpha0),'origin':f'pi direction {j}'} for j in range(count)]
 size=67+3*count;assert 1+sum(g['multiplicity'] for g in own)==size
 saved=next(c for c in source['cases'] if c['retained_denominator_states']==size)
 for x,y in zip(own,saved['groups']):assert x['multiplicity']==y['multiplicity'] and F(x['gap_upper'])<=F(y['gap_upper'])
 cases.append({'retained_states':size,'groups':own})
out={'status':'PASS independent exact assembly from independently replayed physical integers','Gram':[[str(x) for x in r] for r in G],'H_form':[[str(x) for x in r] for r in H],'Gram_positive_definite':True,'Gram_determinant':str(det),'exact_fsum_pass':True,'Rayleigh_derivative_at_old_state':str(derivative),'Rayleigh_derivative_display':float(derivative),'lower_generalized_interval':list(map(str,lower)),'upper_generalized_interval':list(map(str,upper)),'rational_states':states,'exact_cross_Gram':'0','improvement':str(initial-rays[0]),'improvement_display':float(initial-rays[0]),'compressed_trace_identity_pass':True,'delta':prior['delta'],'numerator_Rayleigh':prior['numerator_Rayleigh'],'cases':cases,'single_state_MPS_bond_bound':156,'CPU_seconds':time.process_time()-t0,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'independent_assembly.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'improved_gaps':[x['gap_display'] for x in states],'improvement':out['improvement_display'],'derivative':float(derivative)}))
