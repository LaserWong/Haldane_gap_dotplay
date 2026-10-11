from pathlib import Path
import resource,os,json,hashlib
os.sched_setaffinity(0,{2});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(30,30))
P=Path(__file__).resolve().parent;R=P.parents[1]
def ints(p):return {k:int(v) for line in p.read_text().splitlines() for k,v in [line.split('=')]}
a=ints(P/'anchor48.out');src=R/'research_20261010/mps_excited_seed_witnesses/ground_lengths.out';b=ints(src)
assert a['H0_48']==b['H0_48'] and a['N0_48']==b['N0_48'];assert a['N0_48']>0 and 500000*a['H0_48']+48*700741*a['N0_48']<0
(P/'anchor_check.json').write_text(json.dumps({'status':'MATCH_ACCEPTED48_AND_NEGATIVE_SHIFT','accepted_input':str(src.relative_to(R)),'accepted_input_sha256':hashlib.sha256(src.read_bytes()).hexdigest()},indent=2)+'\n');print('PASS fresh48 matches accepted norm and total energy exactly')
