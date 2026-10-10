from pathlib import Path
import importlib.util,sys,time,json,resource,os
P=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('s',P/'supervisor.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
folder=P/'metadata_integration';l=s.Ledger(folder,10000,time.time()+60,bindings={'test':'frozen-runner metadata only'},test=True);a=l.reserve(s.reservation(4,'prepare'),'worker');case=P.parent/'uniform_second_thermal_supervisor_metadata_fixture';cmd=[sys.executable,str(s.RUNNER/'campaign.py'),'--action','prepare','--length','4','--twist','I','--output',str(case)];pid=s.launch(l,a,cmd,0);active={pid:a}
while active:s.drain(l,active);time.sleep(.02)
assert a['status']=='COMPLETE';assert (case/'case.json').exists() and not (case/'certificate.json').exists();assert not list(case.glob('M*.json'))
out={'status':'PASS frozen runner under lifetime/memory hooks, METADATA ONLY','charged_cpu':a['charge'],'terminal_whole_tree_cpu':a['terminal_wait4_cpu'],'measured_peak_child_rss_kib':a['result']['maxrss_kib'],'no_thermal_columns':True,'source':s.sources()};(P/'integration_test.json').write_text(json.dumps(out,indent=2)+'\n');l.close();print(json.dumps(out,indent=2))
