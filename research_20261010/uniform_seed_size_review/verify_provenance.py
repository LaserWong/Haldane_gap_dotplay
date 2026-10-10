#!/usr/bin/env python3
import os,resource,json,hashlib,time
from pathlib import Path
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
checks=[('uniform_seed_size_diagnostics','MANIFEST_SHA256.json','a67ebcf6d8ec1aca3a0fee0013573492b0ad8237d59ebe7695040e16deacdf6b'),('nonperturbative_mps_review','MANIFEST_SHA256.json','ada056e604879bd0f619baccbbb3dd9925e6d61d61429c2af3345b1dfb20bc3f'),('joint_ratio_review','LEMMA_REVIEW_MANIFEST.json',None)]
records=[];inputs={}
for directory,manifest,expected in checks:
 base=P.parent/directory;f=base/manifest;sha=hashlib.sha256(f.read_bytes()).hexdigest()
 if expected is not None:assert sha==expected
 entries=json.loads(f.read_text())
 for name,digest in entries.items():
  target=base/name;assert hashlib.sha256(target.read_bytes()).hexdigest()==digest,(directory,name)
  inputs[str(target.relative_to(ROOT))]=digest
 inputs[str(f.relative_to(ROOT))]=sha
 records.append({'directory':directory,'manifest':manifest,'manifest_sha256':sha,'verified_entries':len(entries)})
for name in ['audit/mps/build_mps.py','audit/mps/mps_blocks.txt','research_20261010/nonperturbative_mps_assessment/trial_n6.json','research_20261010/nonperturbative_mps_assessment/trial_n8.json']:
 inputs[name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
producer_input=json.loads((P.parent/'uniform_seed_size_diagnostics/INPUT_MANIFEST_SHA256.json').read_text())
for name,digest in producer_input.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n')
(P/'provenance_results.json').write_text(json.dumps({'status':'PASS','manifests':records,'producer_input_entries':len(producer_input),'all_source_hashes_match':True,'git_state':'shared extracted snapshot has no Git metadata; no commit or publication claimed'},indent=2)+'\n')
print(json.dumps(records,indent=2))
