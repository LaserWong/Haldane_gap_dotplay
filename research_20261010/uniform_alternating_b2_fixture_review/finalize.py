#!/usr/bin/env python3
"""One-shot hash verification and review seal. No physical contractions."""
import hashlib,json,os,resource,signal,time
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(2,2));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,)*2);os.sched_setaffinity(0,{5});signal.signal(signal.SIGXCPU,signal.SIG_DFL);signal.pthread_sigmask(signal.SIG_UNBLOCK,{signal.SIGXCPU})
P=Path(__file__).resolve().parent;R=P.parents[1];assert not (P/'SEAL.json').exists()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(P/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
inputs={}
def pin(path,want=None):
    value=digest(R/path)
    if want is not None:assert value==want,path
    if path in inputs:assert inputs[path]==value
    inputs[path]=value
    return value
packages={
 'uniform_alternating_b2_fixture':'0cad4bf9a9bd907cd9be78a6eceaf20ec041b45c3d398fd664c38bd49ee88696',
 'uniform_alternating_b2_64_pilot':'26d1977cf2324cd693c306aecd3b621989364e773413192253670c0951ca3570',
 'uniform_alternating_b2_32_retry1':'eccb1dcbcf423c3c2678bde743bce0882c81473415160bdd24d8beb4e87d9b75',
 'uniform_smaller_second_initialization_review':'54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f',
 'uniform_gap_0248_all_sizes_review':'5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf'}
for package,seal in packages.items():
    base='research_20261010/'+package;manifest=base+'/MANIFEST_SHA256.json';pin(manifest,seal)
    for name,want in json.loads((R/manifest).read_text()).items():pin(base+'/'+name,want)
    if 'b2_' in package:
        for name,want in json.loads((R/base/'INPUT_SHA256.json').read_text()).items():pin(name,want)
# The exact certificates consumed here are members of the historical reviewers' pinned inputs.
for review,pinfile,cert in [
 ('uniform_smaller_second_initialization_review','SCALAR_INPUT_SHA256.json','uniform_smaller_second_initialization/certificate.json'),
 ('uniform_gap_0248_all_sizes_review','INPUT_SHA256.json','uniform_gap_0248_all_sizes/certificate.json')]:
    old=json.loads((R/'research_20261010'/review/pinfile).read_text());path='research_20261010/'+cert;pin(path,old[path])
write('INPUT_SHA256.json',inputs)
numeric=['review','review64','scalar','review32','scalar32'];compiles=['compile','compile_corrected','compile64','compile32']
def total(modes):return sum(sum(json.loads((P/(m+'_resources.json')).read_text())[k] for k in ('wait4_total_cpu_seconds','launcher_CPU_seconds')) for m in modes)
resources={'numerical_CPU_seconds_before_housekeeping':total(numeric),'all_compile_CPU_seconds_including_failed_launcher':total(compiles),'housekeeping_CPU_seconds':time.process_time(),'numeric_budget_CPU_seconds':30,'compile_budget_CPU_seconds':30,'peak_numerical_RSS_KiB':max(json.loads((P/(m+'_resources.json')).read_text())['wait4_peak_rss_kib'] for m in numeric),'peak_compile_RSS_KiB':max(json.loads((P/(m+'_resources.json')).read_text())['wait4_peak_rss_kib'] for m in compiles),'preserved_failed_attempt':'compile_resources.json','all_successful_runs_postexec_guarded':True,'all_successful_runs_whole_tree_empty':True,'no_unapproved_retry':True}
assert resources['numerical_CPU_seconds_before_housekeeping']+resources['housekeeping_CPU_seconds']<30 and resources['all_compile_CPU_seconds_including_failed_launcher']<30
write('RESOURCE_LEDGER.json',resources)
write('CLAIM_VERDICTS.json',{'status':'ACCEPTED','mathematical':{'overlap_safe_formula':'PASS','adjacent_both_orders':'PASS','signed_binary_convolution':'PASS','Gibbs_effect_fidelity_bound':'PASS'},'physical':{'D26_all_saved_local_entries':'PASS','complete_L4_L6_D26_and_two_D2_families':'PASS','independent_exact_L32_all_11_blocks':'PASS','independent_exact_L64_all_11_blocks':'PASS','accepted_N_and_total_H_both_lengths':'PASS','kappa32_upper':'17/125','kappa64_upper':'157/1000','beta':'49/4'},'resource':'PASS_WITH_PRESERVED_PREEXEC_COMPILE_FAILURE_AND_EXPLICITLY_AUTHORIZED_CORRECTION','historical_issues':['Fixture adjacent-omission label actually tests doubled subtraction; true omission independently checked.','Producer first32 wrapper changed162 to130; stopped, retained, and explicitly authorized corrected retry independently verified.'],'not_claimed':['new all-size robust interval','H2 production at32/64','thermal spectral truncation','optimality'],'producer_manifests':packages})
manifest={f.name:digest(f) for f in sorted(P.iterdir()) if f.is_file() and f.name not in ('MANIFEST_SHA256.json','SEAL.json')}
write('MANIFEST_SHA256.json',manifest)
seal=digest(P/'MANIFEST_SHA256.json');write('SEAL.json',{'status':'INDEPENDENT_FORMULA_PHYSICAL32_64_AND_GIBBS_EFFECT_ACCEPTED','manifest_sha256':seal,'files':len(manifest)})
for name,want in manifest.items():assert digest(P/name)==want
print(json.dumps({'manifest_sha256':seal,'files':len(manifest),'input_files':len(inputs),'resources':resources},indent=2))
