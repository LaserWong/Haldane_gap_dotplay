import json,resource,os
from pathlib import Path
os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_CPU,(2,2));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
p=Path(__file__).parent;r=p/'run';cart=p.parent/'bilayer_cartesian_indexed_sample/run'
for name in ['fixture_4x2.json','fixture_5x2.json','terms_4x2.json','terms_5x2.json']:
 assert json.loads((r/name).read_text())==json.loads((cart/name).read_text()),name
s=json.loads((r/'summary.json').read_text());old=json.loads((cart/'summary.json').read_text());samples=[json.loads(line) for line in (r/'samples.jsonl').read_text().splitlines()]
assert len(samples)==1536 and all(x['all_15_channels_equal'] for x in samples)
for fam in ['N','F','L']:
 rows=[x for x in samples if x['family']==fam];assert [x['sample'] for x in rows]==list(range(512))
comparisons=sum(json.loads((r/f'compiler_{f}.json').read_text())['exact_local_matrix_entries_compared'] for f in ['N','F','L'])
result={'all_local_Cartesian_matrix_entries_equal':True,'implicit_local_matrix_entry_comparisons':comparisons,'all_15_fixture_terms_m3_m4_equal':True,'sampled_per_channel_equalities':1536*15,'target_supports':512,'source':'analytic m=M cM, same source as Cartesian fixture','families':[],'timing_caveat':'Brauer and Cartesian actions alternate and share the capped lazy source cache; timings are not independent cold-cache speedup measurements.'}
for a,b in zip(s['families'],old['families']):
 assert a['name']==b['name'] and a['samples']==512
 result['families'].append({'name':a['name'],'diagrams':a['diagrams'],'Cartesian_records':b['rules'],'record_count_reduction':b['rules']/a['diagrams'],'brauer_sample_seconds':a['brauer_cpu_seconds'],'Cartesian_same_run_reference_seconds':a['cartesian_reference_cpu_seconds'],'Cartesian_previous_run_sample_seconds':b['sample_cpu_seconds'],'empirical_all_origin_action_seconds':a['brauer_cpu_seconds']/512*169911,'diagram_hits':a['diagram_hits'],'matching_hits':a['matching_hits'],'active_diagrams':a['active_diagrams'],'source_requests_excluding_one_target_lookup_per_support':a['source_requests']})
result['diagrams_total']=sum(x['diagrams'] for x in result['families']);result['serialized_bytes']=sum((r/f'diagrams_{f}.bin').stat().st_size for f in ['N','F','L']);result['rule_index_charge_bytes']=result['diagrams_total']*32+1048576
assert result['rule_index_charge_bytes']<=16*1048576
result['combined_empirical_action_seconds']=sum(x['empirical_all_origin_action_seconds'] for x in result['families']);result['tenfold_empirical_action_seconds']=10*result['combined_empirical_action_seconds'];result['production_gate_180_seconds']='FAIL_EMPIRICAL_PROJECTION';result['fundamental_infeasibility_claim']=False;result['analysis_cpu_seconds']=resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime
(r/'analysis.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='families'},indent=2))
