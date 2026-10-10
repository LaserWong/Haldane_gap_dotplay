#!/usr/bin/env python3
"""Exact Q(sqrt2,sqrt3) coefficient collection before interval evaluation."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,os,resource,time
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
P=Path(__file__).resolve().parent;t0=time.process_time();D=10**60
m=json.loads((P/'inputs/exact_matrices_n24.json').read_text());C=list(map(int,m['C_displacements']));K=list(map(int,m['K_displacements']));n=24
assert len(C)==len(K)==n and C==[C[-r%n] for r in range(n)] and K==[K[-r%n] for r in range(n)]
for i in range(n):
 for j in range(n):assert int(m['Gram_matrix'][i][j])==C[(j-i)%n] and int(m['H_quadratic_form_matrix'][i][j])==K[(j-i)%n]
assert sum(C)==sum(K)==0 and C[0]>0
root_intervals=[(F(1),F(1))]
for rad in [2,3,6]:
 r=isqrt(rad*D*D);lo,hi=F(r,D),F(r+1,D);assert lo*lo<rad<hi*hi;root_intervals.append((lo,hi))
# Four coordinates denote 1,sqrt2,sqrt3,sqrt6.
cos_base=[(1,0,0,0),(0,F(1,4),0,F(1,4)),(0,0,F(1,2),0),(0,F(1,2),0,0),(F(1,2),0,0,0),(0,-F(1,4),0,F(1,4)),(0,0,0,0)]
def cos_coeff(k):
 k%=24
 if k>12:k=24-k
 if k>6:return tuple(-x for x in cos_base[12-k])
 return cos_base[k]
def coefficients(values,k):return tuple(sum(F(v)*cos_coeff(k*r)[i] for r,v in enumerate(values)) for i in range(4))
def interval(coeff):
 lo=hi=F(0)
 for a,(x,y) in zip(coeff,root_intervals):
  lo+=a*(x if a>=0 else y);hi+=a*(y if a>=0 else x)
 return lo,hi
# Exact ring multiplication checks the trigonometric addition recurrence.
def mul(a,b):
 out=[F(0)]*4
 # sqrt2^2=2, sqrt3^2=3, sqrt6=sqrt2 sqrt3.
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i^j]+=x*y*(2 if i&j&1 else 1)*(3 if i&j&2 else 1)
 return tuple(out)
for k in range(24):assert tuple(cos_coeff(k+1)[i]+cos_coeff(k-1)[i] for i in range(4))==tuple(2*x for x in mul(cos_coeff(1),cos_coeff(k)))
prior=json.loads((P/'inputs/fourier_witness_data.json').read_text());alpha0=F(prior['ground_Rayleigh']);rows=[]
for k in range(n):
 nc,hc=coefficients(C,k),coefficients(K,k);N,H=interval(nc),interval(hc)
 if k==0:
  assert nc==hc==(0,0,0,0);rows.append({'k':0,'status':'exact zero vector; omitted'});continue
 assert N[0]>0
 endpoints=[x/y for x in H for y in N];a,b=min(endpoints),max(endpoints)
 pn=list(map(F,prior['rows'][k]['norm_eigenvalue_interval']));ph=list(map(F,prior['rows'][k]['H_eigenvalue_interval']));pa=list(map(F,prior['rows'][k]['Rayleigh_interval']))
 assert pn[0]<=N[0]<=N[1]<=pn[1] and ph[0]<=H[0]<=H[1]<=ph[1] and pa[0]<=a<=b<=pa[1]
 rows.append({'k':k,'norm_algebraic_coefficients':list(map(str,nc)),'energy_algebraic_coefficients':list(map(str,hc)),'Gram_eigenvalue_interval':list(map(str,N)),'unnormalized_fourier_norm_interval':list(map(str,[n*N[0],n*N[1]])),'Rayleigh_interval':[str(a),str(b)],'gap_upper':str(b-alpha0),'gap_display':float((a+b)/2-alpha0)})
for k in range(1,12):assert rows[k]['Rayleigh_interval']==rows[n-k]['Rayleigh_interval']
base=json.loads((P.parent/'inputs/exact_witness_data.json').read_text())['rows'][-1]
assert 24*sum((-1)**r*C[r] for r in range(n))==int(base['norm_phi_plus_and_minus'])
assert 24*sum((-1)**r*K[r] for r in range(n))==int(base['H_numerator_phi_plus_and_minus'])
assert F(rows[12]['Rayleigh_interval'][0])==F(rows[12]['Rayleigh_interval'][1])==F(base['alpha1'])
out={'status':'PASS independent Fourier algebra and directed radical intervals; displacement replay required separately','n':24,'rows':rows,'zero_global_raising_norm':True,'Gram_rank':23,'ground_Rayleigh':str(alpha0),'numerator_Rayleigh':prior['numerator_Rayleigh'],'delta':prior['delta'],'groups48':[{'k':k,'multiplicity':4 if k<12 else 3,'gap_upper':rows[k]['gap_upper']} for k in range(1,13)],'groups70':[{'k':k,'multiplicity':6 if k<12 else 3,'gap_upper':rows[k]['gap_upper']} for k in range(1,13)],'root_intervals':[[str(a),str(b)] for a,b in root_intervals],'CPU_seconds':time.process_time()-t0,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'independent_fourier.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'Gram_rank':23,'counts':[1+sum(x['multiplicity'] for x in out[g]) for g in ['groups48','groups70']],'CPU_seconds':out['CPU_seconds']}))
