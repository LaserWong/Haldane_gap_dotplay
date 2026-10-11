import time,json
import controller as c
p=c.P;l=c.read(p/'BUDGET_LEDGER.json');c.validate_budget(l);dead=c.read(p/'CONTROLLER_DEATH_TEST.json');deathcpu=sum(x['cpu'] for x in dead['all_reaped']);s={'charged_cpu_seconds':l['charged'],'hard_cap':90,'soft_stop':75,'controller_reserved':10,'child_wait4_cpu':sum(x.get('wait4_cpu',0) for x in l['attempts']),'controller_death_supervisor_wait4_cpu':deathcpu,'recorded_controller_cpu':sum(x.get('controller_cpu',0) for x in l['attempts']),'recorded_guard_wall':sum(x.get('wall',0) for x in l['attempts']),'max_rss_kib':max(x.get('peak_rss_kib',0) for x in l['attempts']),'sample_final_O2':{}}
for name,N in [('final_sample6',169911),('final_sample4',4495)]:
 r=c.read(p/'runs'/name/'chunk.json');r['projection_cpu']=N*r['body_cpu']/(r['end']-r['begin']);s['sample_final_O2'][name]=r
s['final_O2_body_projection']=sum(x['projection_cpu'] for x in s['sample_final_O2'].values());s['planning_with_147_25_startup_10_lowq_100_controller_times10']=(s['final_O2_body_projection']+147.25+10+100)*10
s['metadata_cpu']=sum(c.read(p/f).get('controller_cpu',0) for f in ['CONTROLS_AND_PENCILS_TESTS.json','CONSUMER_TESTS.json','FINAL_METADATA_TESTS.json']);s['metadata_children_wait4_cpu']=c.read(p/'CONTROLS_AND_PENCILS_TESTS.json')['children_wait4_cpu'];c.atomic(p/'SUMMARY.json',s);print(json.dumps(s,indent=2))
