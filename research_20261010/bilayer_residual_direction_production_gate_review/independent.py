import os,resource,json,subprocess,sys,hashlib,copy
from pathlib import Path
os.sched_setaffinity(0,{4})
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P));import checkpoint as c
R=Path(os.environ.get('RESEARCH_ROOT',P.parent));F=P/'replay';F.mkdir();geo=R/'bilayer_complete_residual_8x4/geometry_4x2.txt'
def cli(*args):
 x=subprocess.run([sys.executable,str(P/'checkpoint.py'),*map(str,args)],capture_output=True,text=True);assert x.returncode==0,x.stderr;return json.loads(x.stdout)
s=cli('init',F,'--geometry',geo,'--coefficients',P/'fixture_coefficients.txt','--nx',4,'--ny',2,'--budget',16)
for phase,count in [('q6',3),('q4',11),('q6',18),('q4',24)]:cli('chunk',F,'--phase',phase,'--count',count,'--cap',2)
out=cli('assemble',F);s=json.loads((F/'state.json').read_text());assert s['charged_cpu_seconds']==10
ref=json.loads((R/'bilayer_residual_direction_fixture_review/independent.json').read_text())
for k,row in out['rows'].items():assert row==ref[k]
assert out['polynomial']['A_row']==ref['A'];assert out['polynomial']['A2_row']==ref['A_squared']
# Independently normalize each distinct sector from the raw persisted files.
raws=[json.loads((F/a['output']).read_text())['raw'] for a in s['attempts']]
for k,row in out['rows'].items():
 independently=[]
 for j in range(22):
  n4=sum(int(r[k][j]) for r in raws if r['phase']=='q4')*8;n6=sum(int(r[k][j]) for r in raws if r['phase']=='q6')*8
  assert n4%4==0 and n6%6==0;independently.append(str(n4//4+n6//6))
 assert independently==row
checks=[]
def reject(name,fn):
 try:fn()
 except (AssertionError,ValueError,KeyError):checks.append(name);return
 raise AssertionError(name)
for key in ['binding','geometry','coefficients']:
 b=copy.deepcopy(s)
 if key=='binding':b[key]['chunk_kernel']='0'*64
 else:b[key]['sha256']='0'*64
 reject(key,lambda:c.verify(b))
b=copy.deepcopy(s);b['configuration_id']='0'*64;reject('configuration',lambda:c.verify(b))
b=copy.deepcopy(s);b['attempts'].append(copy.deepcopy(b['attempts'][0]));reject('overlap',lambda:c.read_chunks(F,b))
b=copy.deepcopy(s);b['attempts'][0]['status']='reserved';reject('uncommitted prefix',lambda:c.read_chunks(F,b))
b=copy.deepcopy(s);b['attempts'][0]['output_sha256']='0'*64;reject('output digest',lambda:c.read_chunks(F,b))
b=copy.deepcopy(s);b['attempts'][-1]['status']='failed';b['charged_cpu_seconds']=16;reject('failed charge cannot refund',lambda:c.run_chunk(F,b,'q4',1,2))
# Complete-row reads must remain bound.
b=copy.deepcopy(s);b['complete_row_sha256']='0'*64;reject('complete row digest',lambda:c.assemble(F,b))
result={'status':'PASS_EXACT_SECTOR_REPLAY_CORRECTED_LAUNCHER','all_66_row_entries':True,'all_44_A_A2_entries':True,'different_chunk_order_and_boundaries':True,'rejections':checks,'charged_cpu_seconds':s['charged_cpu_seconds'],'observed_kernel_cpu_seconds':sum(a['observed_cpu_seconds'] for a in s['attempts']),'correction_seal':'677d95d8f1b7c22f7c76db271078c0f4d0376932eacd4374eeb5c39667e627f7','producer_seal':'7309cb09729f77c39ef870b6c6a69980fecbdb5521a03e89f90836667c4100f0'}
(P/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
