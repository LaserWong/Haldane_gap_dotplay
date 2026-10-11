import os,resource
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2))
import json,math,time
from pathlib import Path
from fractions import Fraction as F
p=Path(__file__).resolve().parent;r=p.parent;start=time.time()
w=next(x for x in json.loads((r/'bilayer_split_pencil_optimization/result.json').read_text())['results'] if F(x['g'])==F(11,100));rho=F(w['rayleigh']);v=F(w['variance']);m2=rho*rho+v;ell=F(w['Temple_lower']);a=F(w['cutoff']);U=F(888,25);cap=F(73,5);eup=F(next(x for x in json.loads((r/'bilayer_split_basis_plan/reoptimization.json').read_text())['results'] if x['shape']==[8,4] and F(x['g'])==F(11,100))['split']['rayleigh'])
Rmin=a+ell-rho;Rmax=U-v/(U-rho);b0=(U+ell)*rho-ell*U-m2;assert b0>0 and ell==rho-v/(a-rho)
def x(R):return rho**3+2*rho*v+v*R
def M4(R):return (U+ell)*x(R)-ell*U*m2
def M4sharp(R):
 b1=-x(R)+(U+ell)*m2-ell*U*rho
 return M4(R)-b1*b1/b0
def M4low(R):return m2*m2+(x(R)-rho*m2)**2/v
assert x(Rmin)==ell*m2+(m2-ell*rho)**2/(rho-ell)
assert x(Rmax)==U*m2-(U*rho-m2)**2/(U-rho)
# Conservative q<=8 compression: ||Dq||<=8q; ||C_(q-2,q)||²<=3E*(2q), E=64.
g=F(11,100);t=g/2;roots={2:28,4:40,6:48,8:56};assert all(F(z*z)>=384*q for q,z in roots.items())
rows=[]
for q in (0,2,4,6,8):
 diag=q*(1+4*g);off=t*(roots.get(q,0)+roots.get(q+2,0));rows.append(dict(q=q,diagonal_upper=str(diag),off_diagonal_sum_upper=str(off),row_upper=str(diag+off)))
assert max(F(z['row_upper']) for z in rows)==cap and Rmin<cap<Rmax
out=[]
for target in json.loads((r/'bilayer_pencil_scalar_assessment/result.json').read_text())['results'][0]['hypothetical_ground32_targets']:
 L=F(target['target_ground32_lower']);P=m2-(a+L)*rho+a*L;B=(a+L)*m2-a*L*rho;assert P>0
 def threshold(R):return (a+L)*x(R)-a*L*m2+(x(R)-B)**2/P
 def det(R,sharp=False):return P*((M4sharp(R) if sharp else M4(R))-threshold(R))
 coefficients=[]
 for sharp in (False,True):
  c=det(F(0),sharp);d1=det(F(1),sharp);d2=det(F(2),sharp);aa=(d2-2*d1+c)/2;bb=d1-c-aa;assert aa<0
  left=det(Rmin,sharp);right=det(cap,sharp);assert left>=0 and right>0
  if sharp:assert left==0
  else:assert left>0
  assert det(Rmax,sharp)<0
  lo,hi=cap,Rmax
  for _ in range(72):
   mid=(lo+hi)/2
   if det(mid,sharp)>=0:lo=mid
   else:hi=mid
  assert det(lo,sharp)>=0 and det(hi,sharp)<0
  coefficients.append(dict(bound='interval_localizing_PSD_upper' if sharp else 'generic_global_U_upper',determinant_coefficients=list(map(str,[c,bb,aa])),concave=True,at_Rmin=str(left),at_support_cap=str(right),large_root_bracket=list(map(str,[lo,hi])),large_root_display=[float(lo),float(hi)],m3_root_bracket=list(map(str,[x(lo),x(hi)])),strict_negative_only_above_large_root_in_global_moment_range=True,no_negative_witness_on_actual_support_range=True))
 # A rational two-atom moment model shows the generic-bound obstruction is not a Krylov no-go.
 R=F(9,2);m3=x(R);m4=M4low(R);th=threshold(R);assert m4<th and m4<=M4sharp(R)
 poly=lambda z:(z-rho)*(z-R)-v
 assert ell<rho and poly(ell)>0 and poly(eup)<0 and poly(a)<0 and U>R and poly(U)>0
 assert L<rho and poly(L)>0
 # Moment Hankel PSD lower saturated; all stated support and gap constraints hold in this model.
 out.append(dict(beta=target['beta'],target_lower=str(L),P00=str(P),B=str(B),threshold_formula='m4 < (a+L)*m3-a*L*m2+(m3-B)^2/P00',bounds=coefficients,admissible_two_atom_example=dict(residual_R=str(R),m3=str(m3),m4=str(m4),required_m4_threshold=str(th),generic_m4_upper=str(M4(R)),PSD_sharp_m4_upper=str(M4sharp(R)),generic_excess_over_required=str(M4(R)-th),PSD_sharp_excess_over_required=str(M4sharp(R)-th),exact_actual_pencil_determinant=str(P*(m4-th)),spectral_characteristic_coefficients=list(map(str,[rho*R-v,-rho-R,F(1)])),polynomial_signs_at_ell_ground_upper_a_U_target={key:str(poly(z)) for key,z in [('ell',ell),('ground_upper',eup),('a',a),('U',U),('target',L)]},scope='Selected target and this fixed psi only; generic-bound obstruction, not a physical or exact-Krylov impossibility')))
result=dict(status='EXACT_CACHED_MOMENT_BARRIER_NO_PHYSICAL_CONTRACTIONS',g='11/100',rho=str(rho),variance=str(v),m2=str(m2),global_lower=str(ell),global_upper=str(U),ground_upper=str(eup),even_cutoff=str(a),moment_PSD_R_range=list(map(str,[Rmin,Rmax])),moment_PSD_m3_range=list(map(str,[x(Rmin),x(Rmax)])),actual_residual_support_q_max=8,support_R_cap=str(cap),occupation_compression_rows=rows,results=out,seconds=time.time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(p/'result.json').write_text(json.dumps(result,indent=2)+'\n');print([(t['beta'],[(b['bound'],b['large_root_display']) for b in t['bounds']]) for t in out]);print('R range',float(Rmin),float(Rmax),'actual cap',float(cap),'runtime',result['seconds'])
