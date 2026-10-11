import json,time,math
from pathlib import Path
p=Path(__file__).resolve().parent;t=time.process_time();l=json.loads((p/'BUDGET_LEDGER.json').read_text());assert l['charged_cpu_seconds']+1<=270
l['charged_cpu_seconds']+=1;l['attempts'].append({'name':'metadata_summary','reserved_cpu_seconds':1,'charged_cpu_seconds':1,'state':'reserved_before_launch'});(p/'BUDGET_LEDGER.json').write_text(json.dumps(l,indent=2)+'\n')
runs=[p/'runs'/('sample_offset0_fixed' if i==0 else f'sample_offset{i}') for i in range(8)]
s={'sample_q6':512,'sample_q4':128,'sample_q2':64,'sample_q0':1,'phases':{},'field_names':['psi0','psi2','psi4','m','Cm','Edm','chi0','chi2','chi4','chi6','v_uncached']}
for phase in ['cold','warm']:
 rows=[json.loads(x) for r in runs for x in (r/'targets.jsonl').read_text().splitlines() if json.loads(x)['phase']==phase]
 results=[json.loads((r/('cold_result.json' if phase=='cold' else 'result.json')).read_text()) for r in runs]
 totals={}
 for q,N in [(6,169911),(4,4495)]:
  times=[x['seconds'] for x in rows if x['q']==q];assert len(times)==(512 if q==6 else 128);assert len(set(x['sample'] for x in rows if x['q']==q))==len(times)
  totals[f'q{q}']={'count':len(times),'sum_cpu':sum(times),'mean_cpu':sum(times)/len(times),'max_cpu':max(times),'projection_cpu':N*sum(times)/len(times)}
 totals['phase_cpu']=sum(r['phase_cpu_seconds'] for r in results);totals['unprofiled_low_and_checkpoint_cpu']=totals['phase_cpu']-totals['q6']['sum_cpu']-totals['q4']['sum_cpu']
 keys=['lookup_hits','lookup_misses','cache_evictions','operator_calls','diagram_hits','matching_hits','source_requests','GMP_cpu_seconds','GMP_products','GMP_imports']
 for k in keys:totals[k]=sum(r[k] for r in results)
 totals['field_misses']=[sum(r['field_misses'][i] for r in results) for i in range(11)];totals['field_build_inclusive_cpu_seconds']=[sum(r['field_build_inclusive_cpu_seconds'][i] for r in results) for i in range(11)]
 totals['m_zero_targets']=sum(r['m_zero_targets'] for r in results);totals['m_zero_z_nonzero']=sum(r['m_zero_z_nonzero'] for r in results);totals['m_zero_Kv_nonzero']=sum(r['m_zero_Kv_nonzero'] for r in results);totals['cache_peak_entries']=max(r['cache_peak_entries'] for r in results)
 s['phases'][phase]=totals
cold=s['phases']['cold'];warm=s['phases']['warm'];s['warm_counters_are_cumulative']=True
s['total_wait4_cpu']=sum(a.get('wait4_cpu_seconds',0) for a in l['attempts']);s['total_wall']=sum(a.get('wall_seconds',0) for a in l['attempts']);s['peak_rss_kib']=max(a.get('peak_rss_kib',0) for a in l['attempts']);s['charged_cpu_seconds']=l['charged_cpu_seconds']
s['cold_projection_q4_q6']=cold['q4']['projection_cpu']+cold['q6']['projection_cpu'];s['warm_projection_q4_q6']=warm['q4']['projection_cpu']+warm['q6']['projection_cpu']
(p/'SUMMARY.json').write_text(json.dumps(s,indent=2)+'\n');l['attempts'][-1].update(state='complete',process_cpu_seconds=time.process_time()-t);(p/'BUDGET_LEDGER.json').write_text(json.dumps(l,indent=2)+'\n');print(json.dumps(s,indent=2))
