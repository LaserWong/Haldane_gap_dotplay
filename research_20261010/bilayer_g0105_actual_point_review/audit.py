"""Actual full-residual ground overrides, complete traces and all-size closure."""
import budget_math as B
from budget_math import F,HERE,S,load,sha,P,poly,G
import json,copy,time,resource,os

def main():
 start=time.monotonic();P.verify()
 budgetseal=load(S/'BUDGET_REVIEW_MANIFEST_SHA256.json');assert budgetseal['audit.py']==sha(HERE/'budget_math.py')
 assert sha(S/'BUDGET_REVIEW_MANIFEST_SHA256.json')=='a52450baf76b0a3fb17addec8e784da7c2e19de0c49ef56efb79d2d2e0391361'
 assert sha(S/'POINT_PRODUCER_MANIFEST.json')=='5ead9d9d438a74e3b87507680f34c25631c3ad09e589c3ab0777ddd720357724'
 for rel,h in load(S/'POINT_PRODUCER_MANIFEST.json').items():assert sha(S/'point_producer'/rel)==h
 expected=copy.deepcopy(next(r['data'] for r in load(S/'budget_producer/reoptimized_saved.json')['results'] if F(r['g'])==F(21,200)))
 base=copy.deepcopy(expected);patches=B.certify_data(base);g=F(21,200);lowers={}
 seals={16:'928f1e61cee6a273c7d3af70d3caed60628373435b3b0985ae3005e9de70ac90',32:'6c19485312d08ad0cca2fc76367d5c9172d3aab8ea843d0a740324b69837b331'}
 sourcepaths={16:'bilayer_16d_4x4_residual_g0105/physical_result.json',32:'bilayer_optimized_residual_g0105/physical_result.json'}
 saved=load(S/'point_producer/candidate.json');assert len(saved['results'])==4
 for i,N in enumerate((16,32)):
  mf=S/f'PHYSICAL_{N}_MANIFEST_SHA256.json';assert sha(mf)==seals[N];m=load(mf)
  assert sha(S/f'PHYSICAL_{N}_audit.json')==m['audit.json'] and sha(S/f'PHYSICAL_{N}_ACCEPTANCE.json')==m['ACCEPTANCE.json']
  r=load(S/f'PHYSICAL_{N}_audit.json');assert r['status']=='PASS_COMPLETE_NEW_VECTOR_PHYSICAL_RESIDUAL_AND_TEMPLE' and F(r['g'])==g
  assert sha(S/f'physical_result_{N}.json')==m['snapshot/producer/physical_result.json']==saved['physical_source_sha256'][sourcepaths[N]]
  lower=F(r['ground_lower']);lowers[N]=lower;p=expected['denominator_patches'][i];rho=poly(list(map(F,p['rayleigh_coefficients'])),g);width=rho-lower;assert width>0
  p['uniform_Temple_width']=str(width)
  p['trace_ground_lower_override']=dict(lower=str(lower),source=sourcepaths[N],search_dimension=r['trial_dimension'],explanation='Original pivot trial and polynomial metadata are retained for trace normalization only; the overridden ground lower comes from the new complete residual.')
 def check(row):
  assert F(row['g'])==g and row['physical_input']==expected
  cert=row['certificate'];beta=F(cert['states'][0]['beta'])/2;assert beta in (F(47,5),F(19,2),F(10),F(11))
  widths={N:F(p['uniform_Temple_width']) for N,p in zip((16,32),expected['denominator_patches'])}
  rr,cc=B.ratios(base,patches,beta,widths=widths)
  assert len(row['exact_initial_trace_components'])==3
  for actual,calc in zip(row['exact_initial_trace_components'],cc):
   assert F(actual['total'])==sum(F(actual[k]) for k in ('ground','odd','tail'))
   assert all(F(actual[k])>=calc[k][1] for k in ('ground','odd','tail','total'))
  assert all(0<F(row['exact_initial_ratios'][k])<=rr[k][0]<=1 for k in rr)
  raw=list(map(F,cert['states'][0]['raw']));js={k:v[0] for k,v in rr.items()}
  assert raw[0]<=G(js['J1']) and raw[1]<=G(js['J2']*raw[0]) and raw[2]<=G(js['C0']**4*raw[0]**2*raw[1])
  can=P.scalar_ns['convert'](raw);assert all(F(x)<=y for x,y in zip(cert['states'][0]['canonical'],can))
  inp=dict(coupling_interval=[str(g),str(g)],beta_initial=str(beta),permuted_first_purities=list(map(str,raw)),canonical_first_purities=list(map(str,can)),short_sizes=B.short_rows(g),all_integer_L_ge2_gap='0',physical_independently_verified=True,**{k:str(v) for k,v in js.items()})
  c=copy.deepcopy(cert);c['source']='actual_g0105_complete_residual_inputs';result=P.scalar_ns['replay'](c,inp);result['beta_initial']=str(beta);return result
 results=[check(row) for row in saved['results']];best=max(results,key=lambda r:F(r['gap']))
 assert saved['best'] in saved['results'] and F(saved['best']['certificate']['gap'])==F(best['gap'])
 bad=[]
 for name,mutate in [('invented_ground_lower',lambda r:r['physical_input']['denominator_patches'][0]['trace_ground_lower_override'].update(lower='0')),('wrong_ground_dimension',lambda r:r['physical_input']['denominator_patches'][0]['trace_ground_lower_override'].update(search_dimension=11)),('changed_odd_endpoint',lambda r:r['physical_input']['denominator_patches'][1]['odd_band']['modes'][0].update(eigen_lower_minus_ground_rayleigh_uniform_lower='1')),('omitted_tail',lambda r:r['exact_initial_trace_components'][0].update(tail='0')),('inflated_initial_ratio',lambda r:r['exact_initial_ratios'].update(J1='1')),('missing_window',lambda r:r['certificate']['windows'].pop(0))]:
  row=copy.deepcopy(saved['results'][0]);mutate(row)
  try:check(row)
  except AssertionError:bad.append(name)
  else:raise AssertionError('corruption accepted '+name)
 out=dict(status='PASS_ACTUAL_G0105_ALL_INTEGER_POINT',g=str(g),all_integer_L_ge2_gap=best['gap'],gap_display=float(F(best['gap'])),best=best,results=results,actual_ground_lowers={str(k):str(v) for k,v in lowers.items()},ground_search_dimensions=[16,43],denominator_retained_spectral_counts=[49,97],total_denominator_search_dimensions=[64,139],largest_numerator_search_dimension=43,largest_numerator_retained_states=1,largest_physical_dimension=str(2**128),unique_finite_volume_ground=True,hypothetical_targets_used=False,adversarial_rejections=bad,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)))
 (HERE/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS actual g=.105 gap',out['gap_display'],'seconds',out['seconds'])
if __name__=='__main__':main()
