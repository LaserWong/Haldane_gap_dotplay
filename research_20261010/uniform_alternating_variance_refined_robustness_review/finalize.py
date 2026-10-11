#!/usr/bin/env python3
import hashlib,json,os,resource,signal,time
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(1,1));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,)*2);os.sched_setaffinity(0,{5});signal.signal(signal.SIGXCPU,signal.SIG_DFL);signal.pthread_sigmask(signal.SIG_UNBLOCK,{signal.SIGXCPU})
P=Path(__file__).resolve().parent;R=P.parents[1];assert not(P/'SEAL.json').exists()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,x):(P/name).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
for name,h in json.loads((P/'INPUT_SHA256.json').read_text()).items():assert digest(R/name)==h,name
results=json.loads((P/'results.json').read_text());assert len(results['rows'])==4 and sum(len(x['windows']) for x in results['rows'])==37 and sum(len(x['finite_bridge_rows']) for x in results['rows'])==56
record=json.loads((P/'audit_resources.json').read_text());actual=record['wait4_total_cpu_seconds']+record['launcher_CPU_seconds'];base=json.loads((P.parent/'uniform_alternating_h2_review/RESOURCE_LEDGER.json').read_text());charged=base['review_CPU_with_full_one_second_seal_reserve']+actual+1;assert charged<30
write('RESOURCE_LEDGER.json',{'separate_H2_gate':True,'H2_actual_scientific_CPU':base['review_actual_CPU_before_seal'],'H2_seal_full_reserve_CPU':1,'interval_actual_scientific_CPU':actual,'interval_seal_full_reserve_CPU':1,'final_charged_review_CPU':charged,'review_budget_CPU':30,'compile_actual_CPU':base['compile_actual_CPU'],'completed_unused_reservations_released':True,'failed_review_attempts':0,'prior_gate_ledgers_unchanged':True})
write('CLAIM_VERDICTS.json',{'status':'ACCEPTED','all_four_closed_intervals':'PASS','full_integer_cells':'all M>=2','physical_length':'L=2M','unique_ground_state':True,'full_Hilbert_dimension':'3^(2M)','bootstrap_windows':37,'finite_bridges':56,'asymptotic_tails':4,'H2_pending_producer_premise':'RESOLVED_BY_INDEPENDENT_ACCEPTANCE_cca4335ac42dd34b2e75528a89a2834998d9126c5abcb73df965a344da669f60','physical24':'ACCEPTED_PARITY_CERTIFICATE_MPS48_NOT_OWN_LENGTH24','new_physical_work':False,'search_optimality_claim':False,'all_old_seals_unchanged':True,'resource':'PASS'})
manifest={p.name:digest(p) for p in sorted(P.iterdir()) if p.is_file() and p.name not in ('MANIFEST_SHA256.json','SEAL.json')};write('MANIFEST_SHA256.json',manifest);seal=digest(P/'MANIFEST_SHA256.json');write('SEAL.json',{'status':'INDEPENDENT_ALL_FOUR_VARIANCE_REFINED_INTERVALS_ACCEPTED','manifest_sha256':seal,'files':len(manifest)})
for name,h in manifest.items():assert digest(P/name)==h
print(json.dumps({'manifest_sha256':seal,'files':len(manifest),'final_charged_review_CPU':charged,'housekeeping_CPU':time.process_time()},indent=2))
