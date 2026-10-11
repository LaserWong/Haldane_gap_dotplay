import os,resource
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(600,600));resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
import physical_library as P
from physical_library import F,HERE as H,S,load,sha
import matrix_math as M
import numpy as np,json,math,itertools,copy,time
mat=M.mat;bil=M.contract

def mode_count(shape,g):
 nx,ny=shape;N=nx*ny;ns=P.ns;arr=ns['fixed_arrays'](nx,ny,F(1,10));margins=[];modes=[];a=P.reference(N,g,2)
 for kx,ky in itertools.product(range(nx),range(ny)):
  mom={k:ns['symbol'](v,nx,ny,kx,ky) for k,v in arr.items()};G=mom['G'];assert ns['sign'](G)>0
  theta=[ns['qd'](mom[k],G) for k in ('Q','V')];mean=ns['qpoly'](theta,g);gap=ns['bounds'](ns['qs'](ns['q'](a),mean))[0];assert gap>0;margins.append(gap)
  modes.append(dict(momentum=[kx,ky],gram=list(map(str,G)),mean=list(map(str,mean)),cutoff_margin=str(gap)))
 assert len(modes)==N and 1+3*N<4**N and sum(math.comb(3*N+q-1,q) for q in range(N+1))>=4**N
 return dict(fixed_z='1/10',modes=modes,odd_trial_dimension=3*N,reference_levels_below_q2=1+3*N,minimum_margin=str(min(margins)))

def main():
 t=time.monotonic();P.verify();assert sha(H/'physical_library.py')==load(S/'LIBRARY_REVIEW_MANIFEST.json')['physical_library.py']
 seals={'OPTIMIZATION':'b7182fdbe901f78e7f1efbfc1456153ba9948debaf8e0d6aa8fe93614e743046','ASSESSMENT':'0ffd7b5d40738c7c22772bd5d72584eadb9b0c963f5746b660c4ecbafcc3030f','SPLIT':'0ec374aa4eb61acbe1740549096a06f0ef916050ec092238488318a294a7211b','MATRIX4':'a4eec8140e891b53cc9bd4c237c95236dd32a7069180ed9bc9355df82e4060fb','MATRIX8':'a77330918068b2fcb60a6bdc11412546a4e3fd909a7b393e46c98b62236b654a'}
 for tag,h in seals.items():
  mf=S/(tag+('_MANIFEST_SHA256.json' if tag.startswith('MATRIX') else '_MANIFEST.json'));assert sha(mf)==h;m=load(mf)
  if tag.startswith('MATRIX'):
   for f in ('audit.json','PROOF.md'):assert sha(S/(tag+'_'+f))==m[f]
  else:
   for rel,h in m.items():assert sha(S/tag.lower()/rel)==h
 assert sha(H/'matrix_math.py')==load(S/'MATRIX8_MANIFEST_SHA256.json')['audit.py']
 assert sha(S/'GEOMETRY_4x4.json')==load(S/'MATRIX4_MANIFEST_SHA256.json')['snapshot/GEOMETRY_4x4.json'] and sha(S/'GEOMETRY_8x4.json')==load(S/'MATRIX8_MANIFEST_SHA256.json')['snapshot/GEOMETRY_8x4.json']
 data={16:load(S/'MATRIX4_audit.json'),32:load(S/'MATRIX8_audit.json')};energy=load(S/'split/reoptimization.json')['results'];deficits=load(S/'split/deficit.json')['results'];saved=load(S/'optimization/result.json')['results'];assert len(saved)==4 and {(tuple(r['shape']),F(r['g'])) for r in saved}=={(sh,g) for sh in ((4,4),(8,4)) for g in (F(11,100),F(3,25))}
 matrices={};out=[];odd={}
 for row in saved:
  shape=tuple(row['shape']);N=math.prod(shape);g=F(row['g']);assert shape in ((4,4),(8,4)) and g in (F(11,100),F(3,25))
  geo=load(S/('GEOMETRY_8x4.json' if N==32 else 'GEOMETRY_4x4.json'));base=M.ns['rebuild'](*shape,g,geo);G=mat(base['G']);K=mat(base['A']);cs=list(map(mat,data[N]['complete_H2_coefficients_g0_g1_g2']));J=sum((cs[i]*g**i for i in range(3)),np.zeros(G.shape,dtype=object));assert len(G)==row['dimension']==(16 if N==16 else 43)
  c=list(map(F,row['integer_coefficients']));assert len(c)==len(G) and all(x.denominator==1 for x in c);norm=bil(c,G);rho=bil(c,K)/norm;second=bil(c,J)/norm;var=second-rho*rho
  a=P.reference(N,g,2);r1=P.reference(N,g,1);ell=F(row['strict_pencil_endpoint']);w=bil(c,J-(a+ell)*K+a*ell*G)/norm
  assert norm>0 and var>=0 and rho<r1<a and ell<a and w<0;lower=rho-var/(a-rho);assert lower>ell
  expected=dict(norm=norm,rayleigh=rho,variance=var,cutoff=a,global_r1=r1,normalized_pencil_witness=w,Temple_lower=lower)
  for k,v in expected.items():assert F(row[k])==v,k
  old=next(x['old'] for x in energy if tuple(x['shape'])==shape and F(x['g'])==g);c0=list(map(F,old['integer_coefficients']));n0=bil(c0,G);rho0=bil(c0,K)/n0;var0=bil(c0,J)/n0-rho0*rho0;low0=rho0-var0/(a-rho0)
  assert n0==F(old['norm']) and rho0==F(old['rayleigh']) and rho0<r1 and var0>=0
  assert F(row['energy_optimized_lower'])==low0 and F(row['energy_optimized_variance'])==var0 and F(row['endpoint_improvement'])==lower-low0>0
  count=mode_count(shape,g);priorcut=next(x for x in next(x for x in deficits if F(x['g'])==g)['physical_cutoffs'] if x['N']==N);assert F(count['minimum_margin'])==F(priorcut['odd_min_cutoff_margin'])
  odd[N,g]=count;matrices[N,g]=(G,K,J,a,rho,var);out.append(dict(shape=list(shape),g=str(g),dimension=len(G),norm=str(norm),rayleigh=str(rho),variance=str(var),strict_pencil_endpoint=str(ell),normalized_negative_witness=str(w),ground_lower=str(lower),ground_lower_display=float(lower),improvement_over_energy_only_trial=str(lower-low0),global_r1_margin=str(r1-rho),odd_count=count,unique_global_ground_identified=True,full_even_singlet_sector_cutoff=str(a)))
 targets=load(S/'assessment/target_limit.json')['results'];assert len(targets)==2 and {F(t['beta']) for t in targets}=={F(47,5),F(10)};assess=load(S/'assessment/result.json')['results'];chosen=next(x['hypothetical_ground32_targets'] for x in assess if F(x['g'])==F(11,100));assert len(chosen)==2
 G,K,J,a,rho,var=matrices[32,F(11,100)];limits=[]
 for row in targets:
  target=next(x for x in chosen if x['beta']==row['beta']);ell=F(row['target_lower']);assert ell==F(target['target_ground32_lower'])<a;pm=J-(a+ell)*K+a*ell*G;piv=M.psd(pm,True);assert piv==row['positive_LDL_pivots'] and len(piv)==43 and row['positive_definite'] is True
  assert F(row['variance_budget_for_saved_endpoint_vector'])==(rho-ell)*(a-rho) and F(row['current_variance'])==var
  current=next(x for x in out if x['shape']==[8,4] and F(x['g'])==F(11,100));assert F(target['current_ground32_lower'])==F(current['ground_lower']);assert F(target['required_lower_improvement'])==ell-F(current['ground_lower'])>0
  limits.append(dict(beta=row['beta'],target_lower=str(ell),positive_LDL_pivots=piv,dimension=43,fixed_sector_cutoff=str(a),excluded_scope='No current43D vector has a negative complete Temple pencil at this specified target and cutoff; not a universal bootstrap obstruction',target_sufficiency_scalar_certificate_not_promoted_here=True))
 # Negative control: replacing a complete squared moment by projected H² changes the certified forms.
 omitted=J-K@M.inverse(G)@K;assert any(v>0 for v in omitted.diagonal())
 result=dict(status='PASS_FOUR_PHYSICAL_SECTOR_PENCIL_ENDPOINTS_AND_TWO_SCOPED_LDL_EXCLUSIONS',physical_endpoints=out,scoped_target_exclusions=limits,all_size_gap_claim=False,global_cutoffs_and_odd_counts_recomputed=True,complete_matrices_independently_accepted=True,float_optimization_used_as_proposal_only=True,scalar_temperature_diagnostics_not_certificates=True,seconds=time.monotonic()-t,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (H/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['seconds'],result['peak_rss_kib'])
if __name__=='__main__':main()
