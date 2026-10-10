"""Independent exact audit. No variational-filter producer code is imported.
Reuses hash-frozen, previously independent G/K/J reconstruction and geometry.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'): os.environ[key]='1'
import sys, resource
sys.dont_write_bytecode=True
resource.setrlimit(resource.RLIMIT_AS,(1536*1024**2,1536*1024**2))
if hasattr(os,'sched_setaffinity'): os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import math,json,hashlib,importlib.util,itertools,time
import numpy as np
OUT=Path(__file__).resolve().parent
SNAP=OUT/'snapshot'
BASE=SNAP/'research_20261010/large_seed_review'
FILTER=SNAP/'reviewed_filter_final'
sys.path.insert(0,str(BASE))
spec=importlib.util.spec_from_file_location('previous_independent_ground',BASE/'audit_large.py')
previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path): return json.loads(path.read_text())
def save(name,obj): (OUT/'results'/name).write_text(json.dumps(obj,indent=2)+'\n')
def dot(a,b): return sum(x*b.get(k,0) for k,x in a.items())
def bil(a,M,b=None):
 if b is None:b=a
 return sum(x*F(M[i][j])*y for i,x in enumerate(a) for j,y in enumerate(b))
def graph(nx,ny):
 edges=Counter()
 for x,y in itertools.product(range(nx),range(ny)):
  i=x*ny+y
  for j in (((x+1)%nx)*ny+y,x*ny+(y+1)%ny): edges[tuple(sorted((i,j)))]+=1
 assert all(sum(w for e,w in edges.items() if i in e)==4 for i in range(nx*ny))
 return edges

def verify_snapshot():
 manifest=load(OUT/'INPUT_SHA256.json')
 assert sha(FILTER/'FROZEN_MANIFEST.json')=='6b520dfee4a083c1f9d98561b859ce8a56790a83ad9f1091107d333e3ff11f3e'
 assert all(sha(FILTER/name)==h for name,h in load(FILTER/'FROZEN_MANIFEST.json')['files'].items())
 assert all(sha(SNAP/p)==h for p,h in manifest.items())
 prior=load(BASE/'MANIFEST_SHA256.json')
 for name in ('audit_large.py','rebuild_geometry.py','snapshot/research_20261010/low_band_review/independent_review.py'):
  assert sha(BASE/name)==prior[name]
 previous_inputs=load(BASE/'INPUT_SHA256.json')
 for shape in ('4x4','8x4','8x8'):
  p=f'research_20261010/large_seed_moments/geometry_{shape}.json'
  assert sha(SNAP/p)==previous_inputs[p]
  priorgeom=load(BASE/'results'/f'geometry_{shape}.json')
  assert sha(BASE/'results'/f'geometry_{shape}.json')==prior[f'results/geometry_{shape}.json']
  original=load(SNAP/p)
  assert all(priorgeom[k]==original[k] for k in ('F','S','V','W'))
 save('input_provenance.json',dict(files=len(manifest),all_snapshot_hashes_match=True,prior_independent_code_hashes_match=True,prior_independent_geometry_hashes_match=True,geometry_F_S_V_W_identical=True))

def upper_data(nx,ny,g):
 q=list(range(0,min(6,nx*ny)+1,2)); edges=graph(nx,ny)
 v=F(3,4)*g*g*sum(w*w for w in edges.values());k2=4*g*g
 diag=[(1+2*g)*z for z in q]
 off=[(z//2+1)*v+k2*((z+1)**2//4) for z in q[:-1]]
 return q,diag,off,v,k2

def pivots(diag,off,R):
 p=[]
 for i,d in enumerate(diag):
  v=R-d-(off[i-1]/p[-1] if i else 0)
  if v<=0:return None
  p.append(v)
 return p

def replay_upper(c,nx,ny,g):
 q,d,b,v,k2=upper_data(nx,ny,g)
 assert c['number_indices']==q
 assert list(map(F,c['diagonal']))==d and list(map(F,c['offdiagonal_squared']))==b
 assert F(c['vacuum_creation_norm_squared'])==v and F(c['creation_matrix_norm_squared_upper'])==k2
 assert c['weighted_edge_square_sum']==sum(w*w for w in graph(nx,ny).values())
 R=F(c['compressed_H_upper']);p=pivots(d,b,R)
 assert p and p==list(map(F,c['upper_LDL_positive_pivots']))
 # Verify the stated upward decimal lattice endpoint and its immediately preceding point.
 unit=F(1,10**c['rounding_digits']); assert (R/unit).denominator==1
 assert pivots(d,b,R-unit) is None
 # Independent positive row-sum initial bracket, with sqrt(x)<=1+x.
 rowbound=max(d[i]+sum(1+b[j] for j in (i-1,i) if 0<=j<len(b)) for i in range(len(d)))+1
 assert pivots(d,b,rowbound)
 original_bracket=max(d[i]+sum(max(F(1),b[j]) for j in (i-1,i) if 0<=j<len(b)) for i in range(len(d)))+1
 assert all(max(F(1),z)**2>=z for z in b) and pivots(d,b,original_bracket)
 return R,d,b

def replay_filter(f,rho,var,R):
 C=R-rho;delta=F(f['improvement']);t=F(f['t']);assert C>0 and var>0 and delta>0
 assert F(f['C'])==C and F(f['variance'])==var and t==delta/var
 slack=var-delta*(C+delta)
 assert slack>=0 and F(f['quadratic_slack'])==slack
 norm=1+t*t*var; assert F(f['normalization_squared'])==norm
 achieved=rho+var*(-2*t+C*t*t)/norm
 assert F(f['achieved_bound'])==achieved<=rho-delta<rho
 assert F(f['shifted_rayleigh_upper'])==rho-delta
 # Root is rounded down, which rounds the promised improvement down.
 scale=10**f['rounding_digits'];D=C*C+4*var
 k=math.isqrt(D.numerator*scale*scale//D.denominator)
 assert F(k,scale)**2<=D<F(k+1,scale)**2
 elementary=var*C/(C*C+var);assert elementary*(C+elementary)<=var
 assert F(f['elementary_t_one_over_C_gain'])==elementary
 assert delta==max(F(0),(F(k,scale)-C)/2,elementary)
 return delta

def sector_masses(rec,geom,G,K,norm,rho):
 n=geom['pair_orbits'];d=n+1;sel=rec['selected_basis_indices'];small=list(map(F,rec['coefficients']))
 full=[F(0)]*(2*n+1)
 for i,c in zip(sel,small): full[i]=c
 den=rec['integer_matrix_denominator'];Hc=[sum(F(K[i,j])*c for j,c in enumerate(full))/den for i in range(d)]
 low=[Hc[i]/G[i,i]-rho*full[i] for i in range(d)]
 masses=[G[0,0]*low[0]**2/norm,sum(G[i,i]*low[i]**2 for i in range(1,d))/norm]
 b,l=full[1:d],full[d:];g=F(rec['coupling']);h=[g*x/2+(4-rho)*y for x,y in zip(b,l)]
 masses += [(bil(h,geom['F'])+g*bil(h,geom['S'],l)+g*g*bil(l,geom['V'])/4)/norm,g*g*bil(l,geom['W'])/(4*norm)]
 return masses

def audit_points():
 out=[]
 for p in sorted(FILTER.glob('filtered*.json')):
  c=load(p);rec=load(SNAP/c['source']);geom=load(SNAP/c['geometry_source'])
  assert sha(SNAP/c['source'])==c['source_sha256'] and sha(SNAP/c['geometry_source'])==c['geometry_source_sha256']
  nx,ny,g=rec['nx'],rec['ny'],F(rec['coupling']);N=nx*ny
  G,K,J,_=previous.ground_matrices(nx,ny,g,geom)
  selected=previous.independent_columns(G);assert selected==rec['selected_basis_indices']
  for M,key in zip((G,K,J),('gram','shifted_hamiltonian_numerator','shifted_H2_numerator')):
   assert M[np.ix_(selected,selected)].tolist()==rec[key]
  coeff=list(map(F,rec['coefficients']));GG=G[np.ix_(selected,selected)];KK=K[np.ix_(selected,selected)];JJ=J[np.ix_(selected,selected)]
  den=rec['integer_matrix_denominator'];assert den==4*g.denominator
  norm=bil(coeff,GG);rho=bil(coeff,KK)/(den*norm);var=bil(coeff,JJ)/(den*den*norm)-rho*rho
  assert var>0 and norm==F(c['original_squared_norm_reduced'])
  assert rho==F(c['exact_original_shifted_rayleigh'])==F(rec['exact_rayleigh'])+F(3*N,4)
  assert var==F(c['exact_original_variance'])==F(rec['exact_residual_squared'])
  assert F(rec['gram_common_factor_removed'])==2**N==F(c['original_gram_common_factor_removed'])
  assert rec['s']=='1/2' and rec['block_krylov_depth']==1
  assert c['local_filter_plane_dimension_upper']==2 and c['original_space_plus_residual_dimension_upper']==len(selected)+1 and c['filtered_trial_max_triplet_number']==6
  assert c['physical_spins']==2*N and c['full_dimension']==4**N and c['original_trial_dimension']==len(selected)
  assert c['original_trial_max_triplet_number']==4 and c['residual_max_triplet_number']==6 and c['residual_parity']=='even'
  assert c['new_residual_claim'] is False and c['reads_higher_moments'] is False
  R,diagonal,off=replay_upper(c['compressed_upper_certificate'],nx,ny,g)
  global_gain=replay_filter(c.get('global_upper_filter',c['filter']),rho,var,R)
  masses=sector_masses(rec,geom,G,K,norm,rho);assert min(masses)>=0 and sum(masses)==var
  s=c['residual_sector_certificate'];assert list(map(F,s['residual_norm_squared_by_number']))==masses
  assert F(s['variance_sum_exact'])==var and s['number_indices']==[0,2,4,6]
  products=[off[i]*masses[i]*masses[i+1] for i in range(3)]
  assert list(map(F,s['cross_term_squared']))==products
  roots=list(map(F,s['cross_term_sqrt_upper']));unit=F(1,10**36)
  for root,z in zip(roots,products):
   assert root>=0 and root*root>=z and (root==0 or (root-unit)**2<z)
   assert (root/unit).denominator==1
  numerator=sum(a*b for a,b in zip(diagonal,masses))+2*sum(roots)
  sectorR=numerator/var
  assert numerator==F(s['residual_H_expectation_numerator_upper']) and sectorR==F(s['residual_normalized_H_expectation_upper'])
  gain=replay_filter(c['filter'],rho,var,min(R,sectorR));assert gain>=global_gain
  assert F(c['shifted_rayleigh_upper'])==rho-gain and F(c['energy_rayleigh_upper'])==rho-gain-F(3*N,4)
  assert c['energy_shift']==str(-F(3*N,4))
  out.append(dict(shape=[nx,ny],g=str(g),source=p.name,global_improvement=str(global_gain),global_improvement_display=float(global_gain),sector_improvement=str(gain),sector_improvement_display=float(gain),old_shifted_rayleigh=str(rho),shifted_rayleigh_upper=str(rho-gain),residual_q6_fraction_display=float(masses[-1]/var),G_K_J_rebuilt=True,LDL_strictly_positive=True,all_rounding_verified=True,exact_sector_mass_sum=True))
  print('POINT PASS',nx,ny,g,float(global_gain),float(gain),flush=True)
 assert len(out)==21
 summary=load(FILTER/'summary.json')
 assert len(summary)==21
 byfile={x['source']:x for x in out}
 for row in summary:
  r=byfile[row['file']]
  assert row['geometry']==r['shape'] and row['g']==r['g']
  assert row['old_shifted_rayleigh']==r['old_shifted_rayleigh'] and row['shifted_rayleigh_upper']==r['shifted_rayleigh_upper'] and row['improvement']==r['sector_improvement']
 save('point_replay.json',out)
 return out

def local_kernel():
 # Rebuild orthonormal dimer coordinates directly from four physical spins.
 import sympy as S
 T=S.Matrix([[0,1,0,0],[-1/S.sqrt(2),0,1/S.sqrt(2),0],[1/S.sqrt(2),0,1/S.sqrt(2),0],[0,0,0,1]])
 assert T.T*T==S.eye(4);U=S.kronecker_product(T,T);V=S.zeros(16)
 for c in range(16):
  for i,j in ((0,2),(1,3)):
   a=(c>>(3-i))&1;b=(c>>(3-j))&1;V[c,c]+=S.Rational((2*a-1)*(2*b-1),4)
   if a!=b:V[c^(1<<(3-i))^(1<<(3-j)),c]+=S.Rational(1,2)
 H=(U.T*V*U).applyfunc(S.simplify);assert H==H.T
 K=[[F(str(x)) for x in row] for row in H.tolist()]
 q=[int(i//4!=0)+int(i%4!=0) for i in range(16)]
 assert all(K[i][j]==0 or abs(q[i]-q[j]) in (0,2) for i in range(16) for j in range(16))
 preserve=[[K[i][j] if q[i]==q[j] else F(0) for j in range(16)] for i in range(16)]
 upper=[[F(q[i],2)*(i==j)-preserve[i][j] for j in range(16)] for i in range(16)]
 inert=previous.inertia(upper);assert inert[0]==0
 creation={(i//4,i%4):K[i][0] for i in range(16) if q[i]==2 and K[i][0]}
 assert creation=={(1,3):-F(1,2),(2,2):F(1,2),(3,1):-F(1,2)}
 blocks={}
 for z in range(3):
  ids=[i for i,x in enumerate(q) if x==z];B=S.Matrix([[H[i,j] for j in ids] for i in ids]);blocks[z]={str(e):int(m) for e,m in B.eigenvals().items()}
 save('local_upper.json',dict(orthonormal_transform=True,upper_difference_inertia=list(inert),number_preserving_spectra=blocks,creation=[[a,b,str(x)] for (a,b),x in creation.items()],parity_and_max_two_change_exact=True,normalized_kernel=[[str(x) for x in row] for row in K]))
 return K

def small_models(K):
 results=[]
 for nx,ny in ((2,2),(3,2),(4,2)):
  N=nx*ny;edges=graph(nx,ny);_,orbits,_=previous.graph(nx,ny);q=lambda s:sum(bool((s>>(2*i))&3) for i in range(N))
  kernel=[[(r//4,r%4,K[r][c]) for r in range(16) if K[r][c]] for c in range(16)]
  def apply(v,g,number=True):
   out=defaultdict(F)
   for s,c in v.items():
    if number:out[s]+=q(s)*c
    for (i,j),w in edges.items():
     a=(s>>(2*i))&3;b=(s>>(2*j))&3
     for u,z,val in kernel[4*a+b]:out[s^((a^u)<<(2*i))^((b^z)<<(2*j))]+=c*w*g*val
   return {s:x for s,x in out.items() if x}
  B=[{0:F(1)}]
  for orb in orbits:
   v={}
   for i,j in orb:
    for a,b,z in ((1,3,-1),(2,2,1),(3,1,-1)):v[(a<<(2*i))|(b<<(2*j))]=F(z)
   B.append(v)
  L=[{s:z for s,z in apply(b,F(2),False).items() if q(s)==4} for b in B[1:]]
  A44=[{s:z for s,z in apply(l,F(2),False).items() if q(s)==4} for l in L]
  A64=[{s:z for s,z in apply(l,F(2),False).items() if q(s)==6} for l in L]
  geo={k:[[dot(a,b) for b in right] for a in left] for k,left,right in (('F',L,L),('S',L,A44),('V',A44,A44),('W',A64,A64))};geo['pair_orbits']=len(orbits)
  if ny==2 and nx in (2,4):
   old=load(BASE/'results'/f'geometry_{nx}x{ny}.json');assert all(geo[k]==old[k] for k in ('F','S','V','W'))
  # Two non-eigenvector probes stress nonzero low-shell residuals and mixed signs.
  for trial in (0,1):
   basis=B+L;c=[F(30 if i==0 else ((-1)**(i+trial))*(i+1+trial),1 if i<len(B) else 17) for i in range(len(basis))]
   psi=defaultdict(F)
   for x,v in zip(c,basis):
    for s,z in v.items():psi[s]+=x*z
   psi={s:z for s,z in psi.items() if z};g=F(1+trial,25)
   hp=apply(psi,g);norm=dot(psi,psi);rho=dot(psi,hp)/norm
   r={s:hp.get(s,0)-rho*psi.get(s,0) for s in hp.keys()|psi.keys()};r={s:z for s,z in r.items() if z}
   assert dot(psi,r)==0 and all(q(s) in (0,2,4) for s in psi) and all(q(s) in (0,2,4,6) for s in r)
   var=dot(r,r)/norm;actual_m=[sum(z*z for s,z in r.items() if q(s)==i)/norm for i in (0,2,4,6)]
   G,A,J,_=previous.ground_matrices(nx,ny,g,geo);den=4*g.denominator
   assert bil(c,G)==norm and bil(c,A)/den==dot(psi,hp) and bil(c,J)/(den*den)==dot(hp,hp)
   rec=dict(selected_basis_indices=list(range(len(c))),coefficients=c,integer_matrix_denominator=den,coupling=str(g))
   masses=sector_masses(rec,geo,G,A,norm,rho);assert actual_m==masses and sum(masses)==var
   qids,d,b,_,_=upper_data(nx,ny,g);R=max(d[i]+sum(1+b[j] for j in (i-1,i) if 0<=j<len(b)) for i in range(len(d)))+1
   assert pivots(d,b,R);hr=apply(r,g);rhr=dot(r,hr)/norm;assert rhr<=R*var
   products=[b[i]*masses[i]*masses[i+1] for i in range(len(b))];root=[]
   for z in products:
    scale=10**24;k=math.isqrt(z.numerator*scale*scale//z.denominator);root.append(F(k if F(k,scale)**2==z else k+1,scale))
   sectorNum=sum(x*y for x,y in zip(d,masses))+2*sum(root);assert rhr<=sectorNum
   C=min(R,sectorNum/var)-rho;assert C>0
   scale=10**24;D=C*C+4*var;k=math.isqrt(D.numerator*scale*scale//D.denominator)
   delta=max(F(0),(F(k,scale)-C)/2,var*C/(C*C+var));assert delta*(C+delta)<=var;t=delta/var
   phi={s:psi.get(s,0)-t*r.get(s,0) for s in psi.keys()|r.keys()};hphi=apply(phi,g);actual=dot(phi,hphi)/dot(phi,phi)
   bound=rho-delta
   assert dot(phi,phi)/norm==1+t*t*var and actual<=bound<rho
   results.append(dict(shape=[nx,ny],trial=trial,g=str(g),psi_support=len(psi),residual_support=len(r),physical_G_K_J_match=True,physical_sector_masses_match=True,orthogonality_exact=True,physical_rHr_below_both_bounds=True,physical_filtered_rayleigh=str(actual),certified_filtered_upper=str(bound)))
   print('SMALL PASS',nx,ny,trial,len(psi),len(r),flush=True)
 save('small_physical_crosschecks.json',results);return results

def algebra_edgecases():
 rows=[]
 for rho,var,R in ((F(-3),F(1,100),F(7)),(F(0),F(4),F(3)),(F(-1,8),F(1,10**60),F(4)),(F(1),F(0),F(2))):
  C=R-rho
  if not var:
   rows.append(dict(rho=str(rho),variance='0',unchanged_exact_eigenvector=True));continue
  scale=10**24;D=C*C+4*var;k=math.isqrt(D.numerator*scale*scale//D.denominator)
  fallback=var*C/(C*C+var);assert var-fallback*(C+fallback)==var**3/(C*C+var)**2
  delta=max(F(0),(F(k,scale)-C)/2,fallback);t=delta/var
  assert 0<delta and delta*(C+delta)<=var
  assert rho+var*(-2*t+C*t*t)/(1+t*t*var)<=rho-delta<rho
  rows.append(dict(rho=str(rho),variance=str(var),improvement=str(delta),fallback_used=delta==fallback,all_exact=True))
 save('algebra_edgecases.json',rows)

if __name__=='__main__':
 start=time.monotonic();verify_snapshot();K=local_kernel();points=audit_points();small=small_models(K);algebra_edgecases()
 save('summary.json',dict(verdict='PASS',global_R_points=21,sector_resolved_points=21,small_physical_probes=len(small),new_ground_residual_certified=False,new_complete_gap_certified=False,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,CPU_limit=1,BLAS_threads=1,address_space_bytes=resource.getrlimit(resource.RLIMIT_AS)[0]))
 print('ALL PASS',time.monotonic()-start,flush=True)
