from pathlib import Path
import importlib.util,copy,json,time
P=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('s',P/'supervisor.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
p=P/'ledger_extension_fixture_final';base=s.read(p/'ledger.json');l=s.Ledger.__new__(s.Ledger);l.folder=p;l.path=p/'ledger.json';l.data=copy.deepcopy(base);l.validate_prefix();passed=[]
for key,value in [('authorization_id','other'),('old_limit',0),('additional_budget',43200),('new_limit',99999),('retained_charge',0),('deadline',s.DEADLINE+1),('original_terminal_sha256','0'*64),('original_bindings_sha256','0'*64),('original_attempt_count',0),('recorded_utc',s.DEADLINE+1)]:
 l.data=copy.deepcopy(base);l.data['extensions'][0][key]=value
 try:l.validate_prefix()
 except (AssertionError,FileNotFoundError):passed.append(key)
 else:raise AssertionError('mutation accepted: '+key)
l.data=copy.deepcopy(base);l.data['extensions'].append(copy.deepcopy(l.data['extensions'][0]))
try:l.validate_prefix()
except AssertionError:passed.append('duplicate event')
else:raise AssertionError('duplicate accepted')
# Reaching the deadline rejects BEFORE any history/ledger write, even in a fixture.
raw=l.path.read_bytes();l.data=copy.deepcopy(base);real=s.time.time;s.time.time=lambda:s.DEADLINE
try:
 try:l.extend(s.sources())
 except AssertionError:passed.append('deadline before write')
 else:raise AssertionError('late extension accepted')
finally:s.time.time=real
assert l.path.read_bytes()==raw
(P/'event_mutations.json').write_text(json.dumps({'status':'PASS','rejected_fields':passed,'ledger_unchanged':True},indent=2)+'\n');print(passed)
