"""Source-only audit; no worker, fixture contraction, or resource test."""
import ast,hashlib,json,difflib
from pathlib import Path
P=Path(__file__).resolve().parent;B=P.parent/'bilayer_streaming_hash_revision';K=P.parent/'bilayer_variable_g_control_gate'
def digest(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  while b:=f.read(65536):h.update(b)
 return h.hexdigest()
def functions(p):
 s=p.read_text();lines=s.splitlines(keepends=True);tree=ast.parse(s);return {n.name:(''.join(lines[n.lineno-1:n.end_lineno]),n) for n in tree.body if isinstance(n,ast.FunctionDef)}
a=functions(B/'physical_session.py');b=functions(P/'physical_session.py');same={name:a[name][0]==b[name][0] for name in ['verify_output','worker','required_pins','finalize_physical','stop_after_chunk']};assert all(same.values())
class BudgetBaseline(ast.NodeTransformer):
 def visit_Name(self,n):
  return ast.copy_location(ast.Constant({'CONTROL_POOL':1200,'RETRY_POOL':3600}[n.id]),n) if n.id in ('CONTROL_POOL','RETRY_POOL') else n
old=ast.dump(a['run'][1],include_attributes=False);new=ast.dump(BudgetBaseline().visit(b['run'][1]),include_attributes=False);assert old==new
eng_old=functions(B/'engine.py');eng_new=functions(P/'engine.py');assert eng_old['plan'][0]==eng_new['plan'][0]
assert digest(K/'whole')=='27049851654a544dbc3ea56528c92f56fe6f10b532b3fd8b8c2f80f0a467feb8'
assert digest(K/'whole.cpp')=='d30fb86f35117b0c12e756d949ce6e0e08e95d0f3bbd33d29a3471d9d4a4da91'
assert digest(K/'pencil24.py')=='50e0a5830d4aa2d66cceffa8ac8a649492d077ec72057c42333e557eb8e76893'
# These driver components did not change at all from accepted streaming source.
unchanged={n:digest(P/n)==digest(B/n) for n in ['production_supervisor.py','session_supervisor.py']};assert all(unchanged.values())
report=dict(status='PASS_SOURCE_ONLY',baseline=str(B),scientific_functions_byte_identical=same,dispatcher_AST_identical_except_named_budget_values=True,coverage_plan_byte_identical=True,unchanged_components=unchanged,kernel_executable_sha256=digest(K/'whole'),kernel_source_sha256=digest(K/'whole.cpp'),pencil_source_sha256=digest(K/'pencil24.py'),restored_m3_coefficient=193600,rejected_previous_coefficient=193200,observer_helper_unchanged_from_tested_candidate=digest(P/'limit_observer.py')==digest(P.parent/'bilayer_stable_observer_revision/limit_observer.py'),no_numerical_execution=True)
assert report['observer_helper_unchanged_from_tested_candidate']
(P/'SCIENTIFIC_SOURCE_AUDIT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
with open(P/'FULL_SOURCE_DIFF.patch','w') as out:
 for name in ['engine.py','physical_session.py','production_supervisor.py','session_supervisor.py','outer.py','launch.sh','launch_watchdog.sh']:
  out.writelines(difflib.unified_diff((B/name).read_text().splitlines(True),(P/name).read_text().splitlines(True),fromfile=str(B/name),tofile=str(P/name)))
print(json.dumps(report))
