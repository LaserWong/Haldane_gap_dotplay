"""Independent full physical and scalar audit of eight new closed intervals."""
import physical_library as P
from physical_library import F,S,HERE,load,sha
import copy,json,time,resource,os

def run(row,entry):
 inp=row['input'];cert=row['certificate'];lo,hi=map(F,inp['coupling_interval'])
 assert F(1,10)<=lo<hi<=F(51,500)
 assert inp['coupling_interval']==entry['interval']==cert['coupling_interval']
 assert cert['gap']==entry['gap']
 for patch in inp['denominator_patches']:assert F(patch['odd_band']['fixed_center'])==F(1,10)
 physical=P.physical(inp)
 rec=copy.deepcopy(inp);rec['physical_independently_verified']=True
 c=copy.deepcopy(cert);c['source']=entry['file'];result=P.scalar_ns['replay'](c,rec)
 result['physical']=physical;return result

def main():
 start=time.monotonic();P.verify()
 point=load(S/'POINT_REVIEW_MANIFEST_SHA256.json');assert point['audit.py']==sha(HERE/'physical_library.py')
 assert sha(S/'POINT_REVIEW_MANIFEST_SHA256.json')=='d101b554ea00c044e148031ec4d073d10f6f757b78a019e5bc6502a67e086d05'
 assert load(S/'POINT_REVIEW_ACCEPTANCE.json')['new_coupling_physical_cutoffs_recomputed'] is True
 assert sha(S/'INTERVAL_PRODUCER_MANIFEST.json')=='ae11e04adf4aded2a5aebd57bdc3692a0a2c3e6023ed060740bf93e16efa42e6'
 for rel,h in load(S/'INTERVAL_PRODUCER_MANIFEST.json').items():assert sha(S/'interval_producer'/rel)==h
 summary=load(S/'interval_producer/extension_summary.json');assert summary['count']==8==len(summary['intervals'])
 assert summary['coupling_interval']==['1/10','51/500']
 rows=[];results=[];cursor=F(1,10)
 for entry in summary['intervals']:
  assert F(entry['interval'][0])==cursor;cursor=F(entry['interval'][1])
  row=load(S/'interval_producer'/entry['file']);rows.append(row);results.append(run(row,entry));print('PASS',entry['interval'],results[-1]['gap_display'],flush=True)
 assert cursor==F(51,500)
 uniform=min(F(r['gap']) for r in results);assert uniform==F(summary['uniform_gap'])
 old=load(S/'OLD_UNIFORM_ACCEPTANCE.json');old_m=load(S/'OLD_UNIFORM_MANIFEST_SHA256.json')
 assert sha(S/'OLD_UNIFORM_MANIFEST_SHA256.json')=='c9dadb17430a3523cda109599f3025ff62c7b9ebebacc2b9eb48acce2381e977'
 assert sha(S/'OLD_UNIFORM_ACCEPTANCE.json')==old_m['ACCEPTANCE.json'] and old['status']=='PASS' and old['coupling_interval']==['0','1/10']
 combined=min(uniform,F(old['uniform_gap_lower']));assert combined==F(summary['preserved_whole_0_through_0102_gap'])
 bad=[];source=rows[-1]
 mutations=[('wrong_actual_fixed_z',lambda p:p['input']['denominator_patches'][0]['odd_band'].update(fixed_center=p['input']['fixed_vector_center'])),('alter_endpoint_variance',lambda p:p['input']['denominator_patches'][1]['residual_endpoint_values'].__setitem__(1,'0')),('replace_endpoint_margin',lambda p:p['input']['denominator_patches'][0]['reference_minus_rayleigh_endpoint_lowers'][0].__setitem__(1,'1')),('wrong_odd_endpoint',lambda p:p['input']['denominator_patches'][0]['odd_band']['modes'][0]['theta_endpoint_enclosures'][1].__setitem__(0,'0')),('inflate_uniform_energy',lambda p:p['input']['correlated_energy_combinations']['J1'].update(uniform_lower='1')),('wrong_short_upper_endpoint',lambda p:p['input']['short_sizes'][-1].update(gap_lower='1')),('wrong_terminal_beta',lambda p:p['certificate'].update(terminal_beta='1')),('missing_window',lambda p:p['certificate']['windows'].pop(0))]
 for label,mutate in mutations:
  row=copy.deepcopy(source);mutate(row)
  try:run(row,summary['intervals'][-1])
  except AssertionError:bad.append(label)
  else:raise AssertionError('corruption accepted '+label)
 out=dict(status='PASS_FULL_PHYSICAL_AND_ALL_INTEGER_CLOSED_EXTENSION',extension_interval=['1/10','51/500'],extension_uniform_gap=str(uniform),extension_gap_display=float(uniform),combined_interval=['0','51/500'],combined_uniform_gap=str(combined),combined_gap_display=float(combined),intervals=results,closed_interval_count=8,combined_closed_interval_count=old['source_intervals']+8,finite_windows=sum(r['finite_windows'] for r in results),odd_modes=48*8,endpoint_physical_checks=2*8,adversarial_rejections=bad,no_physical_gap_monotonicity_assumed=True,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)))
 (HERE/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS uniform extension',float(uniform),'combined',float(combined),'seconds',out['seconds'],flush=True)
if __name__=='__main__':main()
