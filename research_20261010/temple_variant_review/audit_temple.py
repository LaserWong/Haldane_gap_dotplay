"""Independent sector-Temple endpoint, heat trace and all-size audit.
Physical inputs are inherited by exact hashes from the sealed large_seed_review.
No producer code is imported and no producer or sealed review file is changed.
"""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;PRIOR=HERE.parent/'large_seed_review'
sys.path.insert(0,str(PRIOR))
from audit_tail_trace import *
SRC=HERE/'snapshot'

def output(name,data):(HERE/'results'/name).write_text(json.dumps(data,indent=2)+'\n')

def check_input_hashes():
 for name,h in load(HERE/'INPUT_SHA256.json').items():assert hashlib.sha256((SRC/name).read_bytes()).hexdigest()==h,name
 for name,h in load(PRIOR/'INPUT_SHA256.json').items():assert hashlib.sha256((PRIOR/'snapshot'/name).read_bytes()).hexdigest()==h,name
 prior=load(PRIOR/'REVIEW_STATUS.json');assert prior['status'].startswith('PASS')
 return hashlib.sha256((PRIOR/'MANIFEST_SHA256.json').read_bytes()).hexdigest()

def audit_patches():
 results=[]
 for nx,ny in [(4,4),(8,4),(8,8)]:
  for g in map(F,['3/100','1/25','1/20']):
   tag=f'translated_{nx}x{ny}_g{g}'.replace('/','d');r=load(SRC/f'{tag}_temple_low_band.json');old=load(REF/f'{tag}_block1_low_band.json');fr=load(BAND/f'{tag}_fourier.json');gr=load(RESEARCH/old['ground_source'])
   for name,h in r['source_sha256'].items():assert hashlib.sha256((RESEARCH/name).read_bytes()).hexdigest()==h
   for key in ['nx','ny','N','g','energy_shift','full_hilbert_dimension','retained_full_band_dimension','relative_form_bound','number_sector_bins','global_lambda_kplus1_lower','global_ground_lower','all_excited_global_lower']:assert r[key]==old[key]
   a=F(r['global_lambda_kplus1_lower']);rho=F(gr['exact_rayleigh'])-F(gr['E00']);r2=F(gr['exact_residual_squared']);assert rho<F(r['all_excited_global_lower'])<a
   endpoint=rho-r2/(a-rho);bl=r['blocks'][0];assert F(bl['eigen_lower'][0])==endpoint and F(bl['eigen_upper'][0])==rho
   assert bl['k']==bl['multiplicity']==1 and bl['trial_dimension']==gr['trial_subspace_dimension']
   assert endpoint>=F(old['blocks'][0]['eigen_lower'][0]);assert F(r['ground_width'])==rho-endpoint
   trip=r['blocks'][1];assert trip['k']==nx*ny and trip['multiplicity']==3
   assert len(trip['eigen_lower'])==len(trip['eigen_upper'])==len(trip['exact_Qsqrt2_Temple_endpoints'])==len(trip['exact_Qsqrt2_Temple_margins'])==nx*ny
   for m,l,u,saved_endpoint,saved_margin,old_l in zip(fr['modes'],trip['eigen_lower'],trip['eigen_upper'],trip['exact_Qsqrt2_Temple_endpoints'],trip['exact_Qsqrt2_Temple_margins'],old['blocks'][1]['eigen_lower']):
    theta=qload(m['theta']);variance=qload(m['residual_squared']);distance=qs((a,F(0)),theta);assert qsign(distance)>0 and qsign(variance)>=0
    endpoint=qs(theta,qd(variance,distance));assert endpoint==qload(saved_endpoint)
    l=F(l);assert l<=F(u)<a and qsign(qs(endpoint,(l,F(0))))>=0 and l>=F(old_l)
    margin=qs(qm(distance,qs(theta,(l,F(0)))),variance);assert qsign(margin)>=0 and margin==qload(saved_margin)
    assert u==m['theta_upper']
   results.append(dict(shape=f'{nx}x{ny}',g=str(g),inherited_physical_hashes_verified=True,exact_ground_and_all_Qsqrt2_Temple_endpoints_verified=True,all_endpoints_improve_frozen_angle_endpoints=True))
   print('TEMPLE PATCH PASS',nx,ny,g,flush=True)
 output('patch_review.json',results)

def audit_trace():
 result=[]
 prior_bridge=load(PRIOR/'snapshot/research_20261010/root_review/large_seed_bridges/large_seed_bridge_results.json')
 for g in map(F,['3/100','1/25','1/20']):
  saved=load(SRC/(f'temple_seed_g{g}.json'.replace('/','d')));row=saved['exact'];beta=F(row['beta_initial']);assert row['order']=='xyt'
  recs=[load(SRC/(f'translated_{nx}x{ny}_g{g}_temple_low_band.json'.replace('/','d'))) for nx,ny in [(4,4),(8,4),(8,8)]]
  e=[F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs];q0,q1,q2=[trace(r,beta) for r in recs];q3=trace(recs[-1],2*beta)
  J1=floor_grid(exp_independent(-2*beta*e[2]+8*beta*e[0])[0]*q3[0]/q0[1]**8,10**16)
  J2=floor_grid(exp_independent(-4*beta*e[2]+8*beta*e[1])[0]*q3[0]**2/q1[1]**8,10**16);C=floor_grid(q3[0]/q2[1]**2,10**16)
  assert [J1,J2,C]==[F(row[k]) for k in ['J1','J2','C']]
  def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)
  A=floor_grid(G(J1),10**16);B=floor_grid(G(J2*A),10**16);CC=floor_grid(G(C**4*A*A*B),10**16);seed=[A,B,CC]
  assert seed==list(map(F,row['first_purities']));boot=row['bootstrap'];assert boot['input']['n']==boot['input']['m']==8 and F(boot['input']['beta'])==2*beta
  assert seed==[F(boot['input'][k+'_lower']) for k in ['A','B','C']]
  defect=[ceil_grid(1-v,10**18) for v in seed];n=8;b=2*beta
  for i,step in enumerate(boot['updates']):
   for _ in range(3):
    purity=(1-defect[0])**4*(1-defect[1])**2*(1-defect[2]);assert 0<purity<=1
    new=ceil_grid((1-purity)**2/(2*purity*purity),10**18);assert 0<=new<1;defect=defect[1:]+[new]
   assert step['round']==i+1 and list(map(F,step['defects']))==defect;n*=2;b*=2
  assert n==boot['n']==boot['m'] and b==F(boot['beta']) and len(boot['updates'])==boot['rounds'];assert defect==list(map(F,boot['defects']))
  u=max(defect);assert u==F(boot['u']) and 0<u<=F(1,500);gap=floor_grid(log_lower(1/(32*u))/b,10**12)
  assert gap==F(boot['uniform_square_gap_lower']) and exp_independent(b*gap)[1]*32*u<1
  bridge=next(z for z in prior_bridge['records'] if F(z['g'])==g);covered={2,3}
  assert all(F(z['gap_lower'])>gap for z in bridge['local_L2_L3'])
  for window in bridge['finite_windows']:
   assert F(window['gap_lower'])>gap;covered.update(range(window['n'],window['through']+1))
  assert all(L in covered for L in range(2,n))
  result.append(dict(g=str(g),beta_initial=str(beta),asymptotic_L_ge=n,all_integer_L_ge=2,gap=str(gap),gap_display=float(gap),all_exact_ratios_and_updates_equal=True,independent_exponential_gap_acceptance=True,bridge='Previously independently accepted local and finite-window gaps all exceed this new endpoint; their original temperatures may be retained'))
  print('TEMPLE ALL-SIZE PASS',g,float(gap),flush=True)
 output('trace_and_all_size_review.json',result)
 return result

if __name__=='__main__':
 prior=check_input_hashes();audit_patches();rows=audit_trace()
 status=dict(status='PASS independent exact sector-Temple, trace, recurrence, and all-integer-size review',prior_physical_review='research_20261010/large_seed_review/REVIEW_STATUS.json',prior_manifest_sha256=prior,accepted=rows,qualification='Same independently verified physical moments and full-space sector count; previously reviewed transfer/interpolation theorems inherited; no formal proof assistant')
 (HERE/'REVIEW_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
