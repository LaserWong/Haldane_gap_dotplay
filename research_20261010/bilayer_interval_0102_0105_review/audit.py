import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
os.sched_setaffinity(0,{4});import resource
resource.setrlimit(resource.RLIMIT_CPU,(600,600));resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
import physical_library as P
from physical_library import F,HERE,S,load,sha,poly,eqseq,contract,reference
import copy,json,time
POLYS={N:load(S/f'PHYSICAL_{N}_audit.json')['polynomial'] for N in (16,32)}
NUM=next(x['data']['largest_base_trial'] for x in load(S/'budget_producer/reoptimized_saved.json')['results'] if F(x['g'])==F(21,200))

def trial(t,index,lo,hi):
 if index==2:
  assert t==NUM and t['geometry']==[8,8] and t['N']==64 and t['trial_dimension']==43
  c=t['integer_coefficients'];norm=contract(c,P.m8['gram']);assert norm==F(t['integer_metric_norm'])>0
  rho=[contract(c,m)/norm for m in P.m8['affine_A']];eqseq(rho,t['rayleigh_coefficients']);return rho,None
 N=(16,32)[index];v=POLYS[N];assert t['N']==N and t['geometry']==([4,4],[8,4])[index] and t['trial_dimension']==(16,43)[index]
 assert t['integer_coefficients']==v['coefficients'] and F(t['integer_metric_norm'])==F(v['norm'])
 rho=list(map(F,v['rayleigh_coefficients']));second=list(map(F,v['full_second_moment_coefficients']));var=list(map(F,v['complete_variance_coefficients']))
 for a,k in [(rho,'rayleigh_coefficients'),(second,'full_second_moment_coefficients'),(var,'full_residual_squared_coefficients')]:eqseq(a,t[k])
 norm=F(v['norm']);assert {k:F(x) for k,x in t['unnormalized_expectations'].items()}==dict(Q=norm*rho[0],A=2*norm*rho[1],Q2=norm*second[0],QA_plus_AQ=2*norm*second[1],A2=4*norm*second[2])
 assert var==[second[0]-rho[0]**2,second[1]-2*rho[0]*rho[1],second[2]-rho[1]**2]
 assert var[0]>=0 and var[2]>=0 and 4*var[0]*var[2]>=var[1]**2
 values=[poly(var,g) for g in (lo,hi)];eqseq(values,t['residual_endpoint_values']);vmax=max(values);assert vmax==F(t['residual_squared_max'])
 ends=[[reference(N,g,q)-poly(rho,g) for g in (lo,hi)] for q in range(1,N+1)]
 assert len(ends)==len(t['reference_minus_rayleigh_endpoint_lowers'])
 for a,b in zip(ends,t['reference_minus_rayleigh_endpoint_lowers']):eqseq(a,b)
 lower=[min(x) for x in ends];eqseq(lower,t['reference_minus_rayleigh_uniform_lowers']);assert lower[0]==F(t['ground_identification_margin'])>0 and lower[1]==F(t['even_Temple_denominator'])>0
 width=vmax/lower[1];assert width==F(t['uniform_Temple_width']) and F(t['odd_band']['fixed_center'])==F(1,10)
 odd=P.ns['check_odd'](t,rho,lo,hi)
 return rho,dict(N=N,width=width,lower=lower,odd=odd,ground_margin=lower[0],even_margin=lower[1],odd_margin=min(F(x['uniform_Temple_denominator']) for x in t['odd_band']['modes']))
P.physical_trial=trial
P.extract(HERE/'physical_library.py',['physical'],vars(P),{'physical':[("assert F(record['fixed_vector_center'])==(lo+hi)/2","assert F(record['fixed_vector_center'])==F(21,200)")]})
def run(row,entry):
 inp=row['input'];cert=row['certificate'];lo,hi=map(F,inp['coupling_interval']);assert F(51,500)<=lo<hi<=F(21,200)
 assert inp['coupling_interval']==entry['interval']==cert['coupling_interval'] and cert['gap']==entry['gap']
 checked=copy.deepcopy(inp);checked.setdefault('largest_numerator',dict(retained_states=1,search_dimension=43,max_triplet_number=6,residual_required=False,physical_spins=128,full_dimension=4**64));physical=P.physical(checked);raw=list(map(F,inp['permuted_first_purities']));assert all(F(x)<=y for x,y in zip(inp['canonical_first_purities'],P.scalar_ns['convert'](raw)));assert F(inp.get('initial_joint_product','0'))<=max(P.full(raw),P.full(list(map(F,inp['canonical_first_purities']))));rec=copy.deepcopy(inp);rec['physical_independently_verified']=True;c=copy.deepcopy(cert);c['source']=entry['file'];out=P.scalar_ns['replay'](c,rec);out['physical']=physical;return out

def main():
 start=time.monotonic();P.verify()
 seals={16:'928f1e61cee6a273c7d3af70d3caed60628373435b3b0985ae3005e9de70ac90',32:'6c19485312d08ad0cca2fc76367d5c9172d3aab8ea843d0a740324b69837b331'}
 for N,h in seals.items():
  mf=S/f'PHYSICAL_{N}_MANIFEST_SHA256.json';assert sha(mf)==h;m=load(mf);assert sha(S/f'PHYSICAL_{N}_audit.json')==m['audit.json'];assert POLYS[N]['operator_identity_for_all_real_g'] is True
 mf=S/'NEW_INTERVAL_PRODUCER_MANIFEST.json';assert sha(mf)=='4b883b9ec2af7fc652f8309a4650257cd023ddea38a517266dc673bfc6b7476f'
 for rel,h in load(mf).items():assert sha(S/'new_interval_producer'/rel)==h
 summary=load(S/'new_interval_producer/summary.json');assert summary['count']==len(summary['intervals'])==6
 rows=[];results=[];cursor=F(51,500)
 for e in summary['intervals']:
  assert F(e['interval'][0])==cursor;cursor=F(e['interval'][1]);row=load(S/'new_interval_producer'/e['file']);rows.append(row);results.append(run(row,e));print('PASS',e['interval'],results[-1]['gap_display'],flush=True)
 assert cursor==F(21,200);uniform=min(F(r['gap']) for r in results);assert uniform==F(summary['uniform_gap'])
 oldmf=S/'PREVIOUS_MANIFEST_SHA256.json';assert sha(oldmf)=='45d651b0f68b840ed2c7a42978acd975d7789b69ad75acd3b4c21a9b74d2a7ed'
 assert sha(S/'PREVIOUS_ACCEPTANCE.json')==load(oldmf)['ACCEPTANCE.json'];old=load(S/'PREVIOUS_ACCEPTANCE.json');assert old['status']=='PASS' and old['combined_interval']==['0','51/500']
 combined=min(uniform,F(old['combined_uniform_gap_lower']));assert combined==F(summary['candidate_joined_0_through_0105_gap'])
 bad=[]
 for label,mut in [('wrong_variance_polynomial',lambda r:r['input']['denominator_patches'][0]['full_residual_squared_coefficients'].__setitem__(2,'0')),('alter_endpoint_variance',lambda r:r['input']['denominator_patches'][1]['residual_endpoint_values'].__setitem__(1,'0')),('wrong_cutoff_endpoint',lambda r:r['input']['denominator_patches'][0]['reference_minus_rayleigh_endpoint_lowers'][0].__setitem__(1,'1')),('wrong_odd_center',lambda r:r['input']['denominator_patches'][0]['odd_band'].update(fixed_center='21/200')),('inflate_energy',lambda r:r['input']['correlated_energy_combinations']['J1'].update(uniform_lower='1')),('wrong_short_bound',lambda r:r['input']['short_sizes'][-1].update(gap_lower='1')),('wrong_terminal_beta',lambda r:r['certificate'].update(terminal_beta='1')),('missing_window',lambda r:r['certificate']['windows'].pop(0))]:
  row=copy.deepcopy(rows[-1]);mut(row)
  try:run(row,summary['intervals'][-1])
  except AssertionError:bad.append(label)
  else:raise AssertionError('accepted corruption '+label)
 out=dict(status='PASS_COMPLETE_PHYSICAL_POLYNOMIAL_AND_ALL_INTEGER_CLOSED_EXTENSION',extension_interval=['51/500','21/200'],extension_uniform_gap=str(uniform),extension_gap_display=float(uniform),combined_interval=['0','21/200'],combined_uniform_gap=str(combined),combined_gap_display=float(combined),closed_interval_count=6,combined_closed_interval_count=old['combined_closed_intervals']+6,finite_windows=sum(r['finite_windows'] for r in results),odd_mode_interval_checks=48*6,physical_endpoint_checks=12,results=results,adversarial_rejections=bad,no_gap_monotonicity_assumed=True,complete_variance_polynomials_independently_reconstructed=True,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (HERE/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',out['extension_gap_display'],out['combined_gap_display'],out['seconds'])
if __name__=='__main__':main()
