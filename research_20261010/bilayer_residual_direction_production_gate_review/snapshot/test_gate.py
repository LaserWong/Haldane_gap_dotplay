from pathlib import Path
import copy,json,shutil
import checkpoint as c
c.limit_supervisor()
p=Path(__file__).resolve().parent;folder=p/'fixture_checkpoint';assert not folder.exists();folder.mkdir()
s=c.initialize(folder,p.parent/'bilayer_complete_residual_8x4/geometry_4x2.txt',p/'fixture_coefficients.txt',4,2,10)
tests=[]
def rejects(name,fn):
 try:fn()
 except (AssertionError,ValueError,KeyError):tests.append(name);return
 raise AssertionError('failed to reject '+name)
rejects('incomplete initial assembly',lambda:c.assemble(folder,s))
c.run_chunk(folder,s,'q4',17,2)
rejects('incomplete q4 assembly',lambda:c.assemble(folder,s))
# Resume from on-disk state between each chunk, preserving binding and ledger.
s=json.loads((folder/'state.json').read_text());c.run_chunk(folder,s,'q4',18,2)
rejects('missing q6 assembly',lambda:c.assemble(folder,s))
s=json.loads((folder/'state.json').read_text());c.run_chunk(folder,s,'q6',10,2)
rejects('incomplete q6 assembly',lambda:c.assemble(folder,s))
s=json.loads((folder/'state.json').read_text());c.run_chunk(folder,s,'q6',11,2)
out=c.assemble(folder,s);reference=json.loads((p.parent/'bilayer_residual_direction_fixture/fixture_4x2.json').read_text())
for k,v in out['rows'].items():assert v==reference[k],k
for k,v in out['scalars'].items():assert v==reference[k],k
bad=copy.deepcopy(s);bad['binding']['chunk_kernel']='0'*64;rejects('changed binary/source binding',lambda:c.verify(bad))
bad=copy.deepcopy(s);bad['coefficients']['sha256']='0'*64;rejects('changed coefficient binding',lambda:c.verify(bad))
bad=copy.deepcopy(s);bad['attempts'].append(copy.deepcopy(bad['attempts'][0]));rejects('duplicate/overlap coverage',lambda:c.read_chunks(folder,bad))
bad=copy.deepcopy(s);bad['attempts'][0]['status']='reserved';rejects('reservation is not completion',lambda:c.read_chunks(folder,bad))
bad=copy.deepcopy(s);bad['attempts'][0]['output_sha256']='0'*64;rejects('changed output digest',lambda:c.read_chunks(folder,bad))
rejects('completed phase rerun',lambda:c.run_chunk(folder,s,'q4',1,2))
# Force a fully charged yet incomplete checkpoint; no retry can exceed its budget.
bad=copy.deepcopy(s);bad['attempts'][-1]['status']='failed';rejects('failed attempt retains budget charge',lambda:c.run_chunk(folder,bad,'q6',11,2))
# Construct exact row from occupation identities and replay arbitrary rational couplings.
from fractions import Fraction as F
G=list(map(int,out['rows']['G']));A=list(map(int,out['polynomial']['A_row']));A2=list(map(int,out['polynomial']['A2_row']));cross=list(map(int,out['polynomial']['QA_AQ_row']))
for g in (F(0),F(11,100),F(217,2000),F(1,8)):
 h=[6*z+g*a/2 for z,a in zip(G,A)];j=[36*z+g*x/2+g*g*y/4 for z,x,y in zip(G,cross,A2)]
 if g==F(11,100):assert h==[F(int(v),200) for v in out['rows']['H200']];assert j==[F(int(v),40000) for v in out['rows']['H200_squared']]
result=dict(status='PASS_SMALL_NORMALIZED_ROW_AND_CHECKPOINT_GATES',geometry=[4,2],old_columns=21,new_row_length=22,all_new_G_H200_H200_squared_entries_equal_full_physical_fixture=True,sector_normalizations={'q4':'8/4','q6':'8/6'},chunks=4,reloaded_state_between_chunks=True,rejection_tests=tests,charged_cpu_seconds=s['charged_cpu_seconds'],observed_kernel_cpu_seconds=sum(a['observed_cpu_seconds'] for a in s['attempts']),peak_rss_kib=max(json.loads((folder/a['output']).read_text())['raw']['peak_rss_kib'] for a in s['attempts']),scope='No 8x4 support work or full production pass')
(p/'gate_tests.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
