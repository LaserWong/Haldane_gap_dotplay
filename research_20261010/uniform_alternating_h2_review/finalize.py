#!/usr/bin/env python3
import hashlib,json,os,resource,signal,time
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(1,1));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,)*2);os.sched_setaffinity(0,{5});signal.signal(signal.SIGXCPU,signal.SIG_DFL);signal.pthread_sigmask(signal.SIG_UNBLOCK,{signal.SIGXCPU})
P=Path(__file__).resolve().parent;R=P.parents[1];assert not(P/'SEAL.json').exists();inputs={}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(rel,want=None):
 h=digest(R/rel)
 if want is not None:assert h==want,rel
 inputs[rel]=h
def write(name,x):(P/name).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
for config in json.loads((P/'PRODUCER_PINS.json').read_text()).values():
 folder=config['path'];pin(folder+'/MANIFEST_SHA256.json',config['manifest'])
 for name,h in json.loads((R/folder/'MANIFEST_SHA256.json').read_text()).items():pin(folder+'/'+name,h)
 for name in ('INPUT_SHA256.json','SCALAR_INPUT_SHA256.json'):
  for rel,h in json.loads((R/folder/name).read_text()).items():pin(rel,h)
old='research_20261010/uniform_alternating_b2_fixture_review';pin(old+'/MANIFEST_SHA256.json','8d26c955fb5500893be65dbbc6e639a86b230d299c9b59ed201a6f89728875ee')
for name,h in json.loads((R/old/'MANIFEST_SHA256.json').read_text()).items():pin(old+'/'+name,h)
for rel,h in json.loads((P/'SCALAR_INPUT_SHA256.json').read_text()).items():pin(rel,h)
write('INPUT_SHA256.json',inputs)
numeric=sum(sum(json.loads((P/(m+'_resources.json')).read_text())[k] for k in ('wait4_total_cpu_seconds','launcher_CPU_seconds')) for m in ('review64','review32','scalar'))
compile_record=json.loads((P/'compile_resources.json').read_text());comp=compile_record['wait4_total_cpu_seconds']+compile_record['launcher_CPU_seconds']
assert numeric+1<30 and comp<30
write('RESOURCE_LEDGER.json',{'separate_new_gate':True,'review_actual_CPU_before_seal':numeric,'review_CPU_with_full_one_second_seal_reserve':numeric+1,'review_budget_CPU':30,'compile_actual_CPU':comp,'compile_budget_CPU':30,'housekeeping_CPU_at_record':time.process_time(),'old_ledgers_unchanged':True,'all_attempts_first_pass':True})
write('CLAIM_VERDICTS.json',{'status':'ACCEPTED','mathematical_positive_H2_formula':'PASS','independent_physical32_and64':'PASS_ALL_22_CHECKPOINTS_132_FIELDS','exact_total_variances':'PASS','new_Rayleigh_ground_weights':'PASS','new_finite_energy_lowers_and_gaps':'PASS','pairwise_variance_correct_F_above_half_branch':'PASS','Gibbs_kappa32_upper':'969/10000','Gibbs_kappa64_upper':'119/1000','beta':'49/4','new_all_size_interval':False,'resource':'PASS_SEPARATE_GATE','prior_seals_unchanged':True,'producer_failed_scalar_history':'PRESERVED_NOT_RETRIED_BY_REVIEW'})
manifest={p.name:digest(p) for p in sorted(P.iterdir()) if p.is_file() and p.name not in ('MANIFEST_SHA256.json','SEAL.json')};write('MANIFEST_SHA256.json',manifest);seal=digest(P/'MANIFEST_SHA256.json');write('SEAL.json',{'status':'INDEPENDENT_H2_32_64_VARIANCE_FIDELITY_GIBBS_ACCEPTED','manifest_sha256':seal,'files':len(manifest)})
for name,h in manifest.items():assert digest(P/name)==h
print(json.dumps({'manifest_sha256':seal,'files':len(manifest),'input_files':len(inputs),'review_actual_CPU_before_seal':numeric,'review_full_seal_reserve_CPU':numeric+1,'compile_CPU':comp,'housekeeping_CPU':time.process_time()},indent=2))
