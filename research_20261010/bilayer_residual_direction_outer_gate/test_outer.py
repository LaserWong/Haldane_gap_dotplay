from pathlib import Path
import hashlib,json,os,signal,subprocess,time
p=Path(__file__).resolve().parent;geo=p.parent/'bilayer_complete_residual_8x4/geometry_4x2.txt';ref=json.loads((p.parent/'bilayer_residual_direction_fixture/fixture_4x2.json').read_text());complete=json.loads((p/'fixture_campaign/checkpoint/complete_row.json').read_text())
for k,v in complete['rows'].items():assert v==ref[k]
ledger=[json.loads(s) for s in (p/'fixture_campaign/outer_ledger.jsonl').read_text().splitlines()];assert ledger[-1]['event']=='COMPLETE_SOLE_PATH' and ledger[-1]['invocations']==6 and ledger[-1]['cumulative_reserved']==20
(p/'invalid_fixture_coefficients.txt').write_text('0\n');bad=p/'failure_campaign'
cmd=lambda home,folder,coeff:[str(home/'outer_driver'),'fixture',str(home),str(folder),str(geo),str(coeff)]
r=subprocess.run(cmd(p,bad,p/'invalid_fixture_coefficients.txt'),capture_output=True,text=True,timeout=5);assert r.returncode==2
x=[json.loads(s) for s in (bad/'outer_ledger.jsonl').read_text().splitlines()];assert x[-1]['event']=='STOPPED_ON_FIRST_FAILURE';assert x[-1]['cumulative_reserved']==11;assert sum(t['event']=='reserve_invocation' for t in x)==1
home=p/'death_launcher';home.mkdir()
for name in ['checkpoint.py','chunk_kernel.cpp','base_kernel.inc','init_kernel.inc','outer_driver.cpp','outer_driver']:(home/name).write_bytes((p/name).read_bytes())
(home/'outer_driver').chmod(0o755);(home/'chunk_kernel').write_bytes((p.parent/'bilayer_residual_direction_launcher_correction/interrupt_probe').read_bytes());(home/'chunk_kernel').chmod(0o755)
campaign=p/'death_campaign';env=dict(os.environ,RESIDUAL_TEST_DIR=str(campaign),RESIDUAL_REAL_KERNEL=str(p/'chunk_kernel'))
outer=subprocess.Popen(cmd(home,campaign,p/'fixture_coefficients.txt'),env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
def dead(pid):
 try:return Path(f'/proc/{pid}/stat').read_text().split()[2]=='Z'
 except FileNotFoundError:return True
deadline=time.monotonic()+4
while not (campaign/'child.pid').exists():
 assert outer.poll() is None;assert time.monotonic()<deadline;time.sleep(.01)
child=int((campaign/'child.pid').read_text());outer_inode=(campaign/'outer.lock').stat().st_ino;assert any(f.stat().st_ino==outer_inode for f in Path(f'/proc/{child}/fd').iterdir()),'kernel lacks inherited outer campaign lock'
supervisor=int(Path(f'/proc/{child}/stat').read_text().split()[3]);assert not dead(child) and not dead(supervisor)
os.kill(outer.pid,signal.SIGKILL);outer.wait(timeout=3);deadline=time.monotonic()+3
while not (dead(supervisor) and dead(child)):assert time.monotonic()<deadline;time.sleep(.01)
before=hashlib.sha256((campaign/'outer_ledger.jsonl').read_bytes()).hexdigest();restart=subprocess.run(cmd(home,campaign,p/'fixture_coefficients.txt'),env=env,capture_output=True,timeout=3);assert restart.returncode!=0;assert hashlib.sha256((campaign/'outer_ledger.jsonl').read_bytes()).hexdigest()==before
s=json.loads((campaign/'checkpoint/state.json').read_text());assert s['attempts'][0]['status']=='reserved' and s['charged_cpu_seconds']==3
result=dict(status='PASS_SOLE_PATH_OUTER_GATE_SMALL_TESTS',exact_physical_rows_match=True,fixture_invocations=6,fixture_reserved_including_driver=20,observed_successful_invocation_cpu_seconds=sum(t.get('observed_wait4_cpu_seconds',0) for t in ledger),failed_preflight_charged=True,stop_after_first_failed_invocation=True,outer_death_kills_supervisor_and_kernel=True,outer_lock_retained_by_kernel=True,automatic_restart_rejected=True,interrupted_reservation_preserved=True,production_plan_invocations=46,production_cli_kernel_reservation=350,production_driver_reservation=10,production_whole_campaign_cap=360,memory_split_MiB=[8,32,60],python_path='/usr/bin/python3',no_8x4_work=True)
(p/'outer_tests.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
