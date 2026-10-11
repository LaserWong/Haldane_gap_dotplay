from pathlib import Path
import json,time
import controller as c
p=c.P;t=time.process_time();l=c.read(p/'BUDGET_LEDGER.json');c.validate_budget(l)
s={'charged_cpu_seconds':l['charged'],'hard_cap':120,'soft_stop':90,'controller_reserved':10,'numerical_and_guard_wait4_cpu':sum(x['wait4_cpu'] for x in l['attempts']),'recorded_controller_cpu':sum(x['controller_cpu'] for x in l['attempts']),'sum_guard_wall':sum(x['wall'] for x in l['attempts']),'max_rss_kib':max(x['peak_rss_kib'] for x in l['attempts']),'attempts':len(l['attempts']),'sample':{}}
for q,names,N in [(6,['sample6_a','sample6_b'],169911),(4,['sample4_a','sample4_b'],4495)]:
 m=[c.read(p/'runs'/n/'chunk.json') for n in names];r=[c.read(p/'runs'/n/'receipt.json') for n in names];count=sum(x['end']-x['begin'] for x in m);body=sum(x['body_cpu'] for x in m)
 s['sample'][q]={'count':count,'body_cpu':body,'mean_per_target':body/count,'body_projection':N*body/count,'setup_cpu':[x['setup_cpu'] for x in m],'controller_cpu':[x['controller_cpu'] for x in r],'wait4_cpu':[x['wait4_cpu'] for x in r]}
s['body_projection_total']=sum(x['body_projection'] for x in s['sample'].values());s['planning_base_with_147_25_startup_10_lowq_100_controller']=s['body_projection_total']+147.25+10+100;s['planning_times10']=s['planning_base_with_147_25_startup_10_lowq_100_controller']*10
s['metadata_recorded_cpu']=sum(c.read(p/f).get('metadata_cpu',c.read(p/f).get('controller_cpu',0)) for f in ['CHECKPOINT_TESTS.json','RECOVERY_PROCESS_TESTS.json','ADOPTION.json']);s['metadata_children_wait4']=c.read(p/'RECOVERY_PROCESS_TESTS.json')['children_wait4_cpu'];s['summary_cpu']=time.process_time()-t;c.atomic(p/'SUMMARY.json',s);print(json.dumps(s,indent=2))
