#!/usr/bin/env python3
"""Verify the frozen guide, extracted data, and recorded check histories."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent;ROOT=R.parent;G=R/'uniform_proof_guide'
PIN='78514331ec4e434bc633dc2c16520e371bace16e1559e32520aa08ceb095dfd1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads(p.read_text())
assert sha(G/'MANIFEST_SHA256.json')==PIN
manifest=js(G/'MANIFEST_SHA256.json')
for name,h in manifest.items():assert sha(G/name)==h
assert js(G/'SEAL.json')['manifest_sha256']==PIN
sources=js(G/'SOURCE_PINS.json')
for name,h in sources['consumed_file_sha256'].items():assert sha(ROOT/name)==h
packages={**sources['accepted_review_manifests'],**sources['producer_manifests']}
for name,h in packages.items():
 p=R/name;assert sha(p/'MANIFEST_SHA256.json')==h
 for sub,want in js(p/'MANIFEST_SHA256.json').items():assert sha(p/sub)==want
for row in sources['original_sources']:
 raw=(ROOT/row['local_path']).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==row['sha256']
 assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['git_blob_sha1']
D=js(G/'EXACT_DATA.json')
for target,source,key in [
 ('physical_inputs','uniform_second_thermal_full_review/provenance_results.json','cases'),
 ('moment_intervals','uniform_second_moment_optimization/certificate.json','moment_intervals'),
 ('filters','uniform_second_moment_optimization/certificate.json','filters'),
 ('bootstrap_rows','uniform_smaller_second_initialization/certificate.json','rows'),
 ('direct_4_to23','uniform_small_lengths_completion/certificate.json','rows'),
 ('direct_26_to33','uniform_gap_0248_all_sizes/certificate.json','new_rows'),
 ('accepted_stronger_prefix_4_to25','uniform_gap_0248_all_sizes_review/results.json','cached_prefix_4_to25'),
 ('accepted_stronger_26_to33','uniform_gap_0248_all_sizes_review/results.json','new_direct26_to33')]:assert D[target]==js(R/source)[key]
assert D['direct25']==js(R/'uniform_direct25_coverage/certificate.json')
assert D['long_majorants']=={**js(R/'uniform_smaller_second_initialization/long_certificate.json'),**js(R/'uniform_small_lengths_completion/long_certificate.json')}
for target,source in [('bootstrap_anchors','uniform_smaller_second_initialization_review/anchors.out'),('direct_4_to23_anchors','uniform_small_lengths_completion_review/anchors.out'),('direct25_anchors','uniform_direct25_coverage_review/anchor25.out'),('direct_26_to33_anchors','uniform_gap_0248_all_sizes_review/anchors.out')]:
 assert D[target]==dict(line.split('=') for line in (R/source).read_text().splitlines())
assert D['isolated24']['seed']==js(R/'uniform_n24_second_coverage/certificate.json')['zero_gap_window']
assert D['isolated24']['accepted']==next(x for x in js(R/'uniform_n24_second_coverage_review/results.json')['rows'] if x['L']==24)
assert D['isolated24']['anchor48_shifted_total_Rayleigh']==js(R/'uniform_n24_second_coverage_review/results.json')['anchor48_shifted_total_Rayleigh']
final=js(G/'SELF_CHECK.json');initial=js(G/'history/SELF_CHECK_ATTEMPT1.json')
assert initial['resources']['CPU_seconds']==30.21035921>initial['resources']['CPU_limit_seconds']==30
assert final['resources']['CPU_seconds']==25.746380744<final['resources']['CPU_limit_seconds']==60
assert final['full_domain_majorants_checked']==40 and final['finite_purities_checked']==30 and final['strong_tail_n']==34
assert final['status']=='PASS_GUIDE_CONSISTENCY_CHECK_NOT_INDEPENDENT_PHYSICAL_REVIEW'
assert final['physical_work_performed'] is False
text=(G/'PROOF_GUIDE.md').read_text();code=(G/'selfcheck.py').read_text()
assert r'For \(m\ge0\) and \(h>0\)' in text
assert "assert s==F(row['S']) and t==F(row['T'])" in code
assert '30.21035921' in text and '60-second' in text
out={'status':'ACCEPTED frozen guide identity and data extraction','guide_manifest_sha256':PIN,'guide_members':len(manifest),'consumed_file_pins':len(sources['consumed_file_sha256']),'complete_dependency_packages':len(packages),'original_Git_blobs':len(sources['original_sources']),'final_guide_selfcheck_record':final['resources'],'first_guide_selfcheck_record_preserved':initial['resources'],'domain_qualifier_fixed':True,'first_state_join_fixed':True,'guide_selfcheck_executed_by_this_review':False,'guide_selfcheck_source_inspected':True,'exact_scalar_results_independently_replayed':'CHECK_RESULTS.json','member_sha256':manifest}
(P/'GUIDE_PACKAGE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='member_sha256'},indent=2))
