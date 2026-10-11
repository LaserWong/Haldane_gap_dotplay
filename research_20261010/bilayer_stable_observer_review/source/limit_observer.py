"""Stable /proc observations. Resource enforcement does not depend on sampling."""
import os,json,hashlib
from pathlib import Path
from engine import atomic
class LimitMismatch(RuntimeError):pass

def topology_role(pid,root,rows):
 if pid==root:return 'supervisor'
 if rows[pid]['ppid']==root:return 'controller'
 parent=rows[pid]['ppid']
 if parent in rows and rows[parent]['ppid']==root:return 'native'
 return 'unexpected'

def identity(pid):
 base=Path('/proc')/str(pid);s=(base/'stat').read_text();v=s[s.rfind(')')+2:].split()
 return dict(pid=pid,start=v[19],ppid=int(v[1]),exe=os.readlink(base/'exe'),argv=(base/'cmdline').read_bytes().split(b'\0')[:-1])
def serial_identity(x):return {**x,'argv':[a.decode(errors='replace') for a in x['argv']]}
def sample(pid,role,config):
 record=dict(pid=pid,expected_role=role)
 try:
  before=identity(pid);record['before']=serial_identity(before)
  base=Path('/proc')/str(pid);lines=(base/'limits').read_text().splitlines()
  cpu=tuple(map(int,next(x for x in lines if x.startswith('Max cpu time')).split()[-3:-1]));space=tuple(map(int,next(x for x in lines if x.startswith('Max address space')).split()[-3:-1]))
  status=(base/'status').read_text();aff=next(x.split(':',1)[1].strip() for x in status.splitlines() if x.startswith('Cpus_allowed_list:'))
  record.update(cpu=list(cpu),address_space=list(space),affinity=aff)
  after=identity(pid);record['after']=serial_identity(after)
 except FileNotFoundError:record['outcome']='exited_during_observation';return record
 except Exception as e:record.update(outcome='mismatch',reason='observation_error',error=repr(e));return record
 if before!=after:record['outcome']='exec_or_identity_transition';return record
 return classify(record,config)

def classify(record,config):
 role=record['expected_role'];info=record['after'];exe=info['exe'];argv=info['argv'];script=argv[1] if len(argv)>1 else '';python=str(Path(config['python']).resolve());native=str(Path(config['native']).resolve());scripts=config['scripts']
 runtime=(role=='native' and exe==native) or (role in ('supervisor','controller') and exe==python and script==scripts[role])
 parent={'supervisor':'outer','controller':'supervisor','native':'controller'}.get(role)
 transient=exe==python and parent is not None and script==scripts[parent]
 if not runtime:
  record['outcome']='fork_before_exec' if transient else 'mismatch'
  if not transient:record['reason']='unexpected_stable_executable_or_command'
  return record
 cpus={'supervisor':{(3,20),(3,3)},'controller':{(20,20)},'native':{(3,3),(6,6)}}[role]
 spaces={(128*1024**2,128*1024**2)} if role=='native' else {(64*1024**2,128*1024**2)}
 bad=[]
 if tuple(record['cpu']) not in cpus:bad.append('cpu')
 if tuple(record['address_space']) not in spaces:bad.append('address_space')
 if record['affinity']!='6':bad.append('affinity')
 record['outcome']='mismatch' if bad else 'verified_post_exec'
 if bad:record['reason']='unexpected_post_exec_'+','.join(bad)
 return record

def enforce(record,event_dir):
 if record['outcome']!='verified_post_exec':
  encoded=(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n').encode();key=hashlib.sha256(encoded).hexdigest();path=Path(event_dir)/(key+'.json')
  if not path.exists():atomic(path,record)
 if record['outcome']=='mismatch':raise LimitMismatch(record.get('reason','unknown'))
 return record
