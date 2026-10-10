"""Continuous extension with two fixed-center odd-band denominator families.
Every interval uses exact full G/H/H²; no new sparse support is constructed.
"""
import certify_range as C
import odd_polynomials as O
from fractions import Fraction as F
import numpy as np,json,math
from scipy.linalg import eigh
RAW={(nx,ny):O.extract(nx,ny) for nx,ny in ((4,4),(8,4))}

def optimized_auxiliary(model,g):
 G=model['G'];A=sum(g**k*M for k,M in enumerate(model['first_moment_coefficients']));B=sum(g**k*M for k,M in enumerate(model['full_second_moment_coefficients']))
 a=C.reference(g,model['N'],2);K=A-a*G;S=B-2*a*A+a*a*G
 sc=np.sqrt(np.diag(np.asarray(S,float)));ks=np.asarray(K,float)/sc[:,None]/sc[None,:];ss=np.asarray(S,float)/sc[:,None]/sc[None,:]
 vals,U=eigh(ks,ss);assert vals[0]<0
 v=U[:,0]/sc;v/=max(abs(v));return [int(round(x*2**48)) for x in v]

base_interval_data=C.interval_data
base_upper_float=C.upper_float
base_upper_exact=C.upper_exact

def interval_data(lo,hi,vectors=None):
 center=(lo+hi)/2
 if vectors is None:vectors=[optimized_auxiliary(m,center) for m in C.MODELS[:2]]+[C.optimized_vector(C.MODELS[2],center)]
 data=base_interval_data(lo,hi,vectors)
 for p in data['denominator_patches']:
  nx,ny=p['geometry'];N=p['N'];modes=O.fixed_modes(RAW[nx,ny],center)
  ground=list(map(F,p['rayleigh_coefficients']));rows=[]
  for row in modes['modes']:
   theta=[O.Quad(*map(F,x)) for x in row['theta_coefficients']]
   var=[O.Quad(*map(F,x)) for x in row['residual_squared_coefficients']]
   ths=[O.evaluate(theta,g) for g in (lo,hi)];vs=[O.evaluate(var,g) for g in (lo,hi)]
   assert all(x.sign()>=0 for x in vs)
   vhigh=max(x.bounds(160)[1] for x in vs)
   margins=[(O.Quad(C.reference(g,N,2))-th).bounds(160)[0] for g,th in zip((lo,hi),ths)]
   denom=min(margins);assert denom>0
   width=vhigh/denom
   rel_ends=[(th-O.Quad(C.poly(ground,g))).bounds(160)[0] for g,th in zip((lo,hi),ths)]
   rel=min(rel_ends)-width
   rows.append(dict(**row,theta_endpoint_enclosures=[[str(x) for x in th.bounds(160)] for th in ths],
    residual_squared_endpoint_enclosures=[[str(x) for x in v.bounds(160)] for v in vs],
    residual_squared_max=str(vhigh),cutoff_minus_theta_endpoint_lowers=list(map(str,margins)),
    uniform_Temple_denominator=str(denom),uniform_Temple_width=str(width),
    theta_minus_ground_rayleigh_endpoint_lowers=list(map(str,rel_ends)),
    eigen_lower_minus_ground_rayleigh_uniform_lower=str(rel)))
  p['odd_band']=dict(fixed_center=str(center),trial_family='w_r(z)=|t+_r>−z C_create(1)|t+_r>/2',
   q_components=[1,3],per_spin_projection_dimension=N,spin_multiplicity=3,retained_odd_dimension=3*N,
   all_modes_below_global_q2_cutoff=True,modes=rows)
 return data

def upper_float(p,b):
 N=p['N'];d=float(F(p['uniform_Temple_width']));band=p['odd_band']
 return math.exp(b*d)+3*sum(math.exp(-b*float(F(row['eigen_lower_minus_ground_rayleigh_uniform_lower']))) for row in band['modes'])+sum(math.comb(3*N+q-1,q)*math.exp(-b*float(F(en))) for q,en in enumerate(p['reference_minus_rayleigh_uniform_lowers'],1) if q>=2)

def upper_exact(p,b):
 N=p['N'];ground=C.exp_interval(b*F(p['uniform_Temple_width']))[1]
 terms=[3*C.exp_interval(-b*F(row['eigen_lower_minus_ground_rayleigh_uniform_lower']))[1] for row in p['odd_band']['modes']]
 tail=[math.comb(3*N+q-1,q)*C.exp_interval(-b*F(e))[1] for q,e in enumerate(p['reference_minus_rayleigh_uniform_lowers'],1) if q>=2]
 total=ground+sum(terms)+sum(tail)
 return total,dict(beta=str(b),normalized_ground_upper=str(ground),normalized_odd_band_upper=str(sum(terms)),normalized_tail_upper=str(sum(tail)),normalized_trace_upper=str(total),retained_states=1+3*N,reference_q_range=[2,N],odd_mode_count=N,spin_multiplicity=3)
C.interval_data=interval_data;C.upper_float=upper_float;C.upper_exact=upper_exact

if __name__=='__main__':
 for (nx,ny),raw in RAW.items():(C.HERE/f'odd_polynomial_{nx}x{ny}.json').write_text(json.dumps(raw,indent=2)+'\n')
 C.main()
