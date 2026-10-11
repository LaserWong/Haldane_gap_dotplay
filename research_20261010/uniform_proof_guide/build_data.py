#!/usr/bin/env python3
"""Extract unchanged accepted data for the guide. No scientific code is imported."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
R=ROOT/'research_20261010'
FILES={}
def read(rel):
    p=ROOT/rel
    b=p.read_bytes()
    FILES[rel]=hashlib.sha256(b).hexdigest()
    return b

def js(rel):
    return json.loads(read('research_20261010/'+rel))

def ints(rel):
    return {k:v for k,v in (line.split('=') for line in read('research_20261010/'+rel).decode().splitlines())}

def dump(name,obj):
    (P/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

reviews={
 'uniform_source_scope_review':'7c3ca3698dc82ace47e5c76482910404df1e1655e40ef6bc89f5775b2a5358c9',
 'uniform_second_initialization_review':'3e713b2de14407cca8c14e7236c23077998d29ea13268267626859fc5c23511b',
 'uniform_second_moment_review':'dbdea168300fa8a014c4a1fcbb72a6f64d1f8ddb3250949eeeed067d55c329de',
 'uniform_second_thermal_full_review':'792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94',
 'uniform_smaller_second_initialization_review':'54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f',
 'uniform_small_lengths_completion_review':'b5225681662482e5ed219fe85d0cc9247703b21b183f6e6441dd081b7bc9d984',
 'uniform_n24_second_coverage_review':'9d31eeb0dc44f24047943a4ad4dd06e4f8f82aced5ca321857a1aaedf82b8282',
 'uniform_direct25_coverage_review':'a70156f108be662bbb9873ce12f9701701efd0b6680d2d187e677fa1e37b3cc9',
 'uniform_gap_0248_all_sizes_review':'5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf',
}
producers={
 'uniform_second_moment_optimization':'dc81945f85281a33df1b272a7a054b6f5d9b5fa32e8c7a1868c26e07bc97ec85',
 'uniform_smaller_second_initialization':'fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84',
 'uniform_small_lengths_completion':'71606fa80898fb73b6f0fffb359480a1d3e716d98c47791d16d3470618c4af08',
 'uniform_n24_second_coverage':'ef04180cedde73a09aa627c3dc75c2730472c9f425fd29bcec376678fea00240',
 'uniform_direct25_coverage':'abd4e0f0a315ef9878129c56ee884d797707687f07361c83f1cb140f0ebee9fa',
 'uniform_gap_0248_all_sizes':'659d03dd58275338f0a13af5fde6f6e503bca8eb7c3ac5d044a0e98e788e8ab1',
}
# Hash every file in these package manifests, without executing their checkers.
for folder,expected in {**reviews,**producers}.items():
    b=read('research_20261010/'+folder+'/MANIFEST_SHA256.json')
    assert hashlib.sha256(b).hexdigest()==expected
    manifest=json.loads(b)
    for rel,h in manifest.items():
        path=R/folder/rel
        assert hashlib.sha256(path.read_bytes()).hexdigest()==h, str(path)
    if (R/folder/'SEAL.json').exists():
        s=js(folder+'/SEAL.json')
        assert s['manifest_sha256']==expected

physical=js('uniform_second_thermal_full_review/provenance_results.json')
moment=js('uniform_second_moment_optimization/certificate.json')
init=js('uniform_smaller_second_initialization/certificate.json')
longs=js('uniform_smaller_second_initialization/long_certificate.json')
short_longs=js('uniform_small_lengths_completion/long_certificate.json')
finite=js('uniform_small_lengths_completion/certificate.json')
new=js('uniform_gap_0248_all_sizes/certificate.json')
final=js('uniform_gap_0248_all_sizes_review/results.json')
n24=js('uniform_n24_second_coverage/certificate.json')
r24=js('uniform_n24_second_coverage_review/results.json')
n25=js('uniform_direct25_coverage/certificate.json')
for folder,file in [('uniform_source_scope_review','SOURCE_SCOPE.md'),('uniform_second_moment_review','REVIEW.md'),('uniform_second_initialization_review','REVIEW.md')]+[(n,'PROOF.md') for n in reviews if n not in ('uniform_source_scope_review','uniform_second_moment_review','uniform_second_initialization_review')]:
    read('research_20261010/'+folder+'/'+file)
# Authoritative source snapshots and already-verified upstream metadata.
scope=js('uniform_source_scope_review/SOURCES.json')
source_meta=js('uniform_second_moment_review/SOURCE_PROVENANCE.json')
original_sources=[]
for v in scope['sources']:
    rel='research_20261010/uniform_source_scope_review/sources/'+Path(v['path']).name
    b=read(rel)
    original_sources.append({'local_path':rel,'upstream_path':v['path'],'url':v['url'],'git_blob_sha1':v['blob'],'sha256':hashlib.sha256(b).hexdigest()})
for name,v in source_meta.items():
    rel='research_20261010/uniform_second_moment_review/sources/'+name
    b=read(rel)
    original_sources.append({'local_path':rel,'upstream_path':'build/'+name,**v})
for source in original_sources:
    b=read(source['local_path'])
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==source['git_blob_sha1']
    assert hashlib.sha256(b).hexdigest()==source['sha256']
for rel in ['AGENTS.md','audit/APPENDIX_A_BRIDGE.md','research_20261010/uniform_second_moment_review/sources/ATTRIBUTION.md','research_20261010/uniform_second_moment_review/sources/LICENSE','research_20261010/uniform_source_license_supplement/README.md']:
    read(rel)
# Do not pin a mutable root README to a frozen guide. Its state is only orientation.
D={
 'status':'EXPOSITORY_DATA_EXTRACTED_FROM_ACCEPTED_EVIDENCE_NOT_A_NEW_PHYSICAL_RUN',
 'theorem':{k:final[k] for k in ('gap','all_integer_L_at_least','unique_ground_state','bootstrap_initialization_used_for_this_stronger_gap','smallest_separately_certified_initialization','smaller_initialization_gap','prior_direct25_resource_anomaly_still_unresolved')},
 'model':{'coupling':'1','spin':'1','boundary':'periodic untwisted','L2_bond_multiplicity':2,'physical_dimension':'3^L','trial_span_dimension':1,'MPS_bond_dimension':26,'MPS_norm_transfer_dimension':676,'a':'700741/500000','beta0':'49/4'},
 'physical_inputs':physical['cases'],
 'moment_intervals':moment['moment_intervals'],
 'filters':moment['filters'],
 'long_majorants':{**longs,**short_longs},
 'bootstrap_rows':init['rows'],
 'bootstrap_anchors':ints('uniform_smaller_second_initialization_review/anchors.out'),
 'direct_4_to23':finite['rows'],
 'direct_4_to23_anchors':ints('uniform_small_lengths_completion_review/anchors.out'),
 'isolated24':{'seed':n24['zero_gap_window'],'accepted':r24['rows'][0],'anchor48_shifted_total_Rayleigh':r24['anchor48_shifted_total_Rayleigh']},
 'direct25':n25,
 'direct25_anchors':ints('uniform_direct25_coverage_review/anchor25.out'),
 'direct_26_to33':new['new_rows'],
 'direct_26_to33_anchors':ints('uniform_gap_0248_all_sizes_review/anchors.out'),
 'accepted_stronger_prefix_4_to25':final['cached_prefix_4_to25'],
 'accepted_stronger_26_to33':final['new_direct26_to33'],
 'analytic2_3':finite['analytic_small_lengths'],
 'MPS_tensor_definition':{
  'source':'original trials.tex, trial-support and trial-entry equations',
  'virtual_types_ell':[1,1,1,1,3,3,3,5],
  'diagonal_parameters':[-289,-84,-9,33,-22,27,71,-11],
  'pair_parameters':{'1,5':-11,'1,6':-35,'1,7':-28,'2,5':-23,'2,6':16,'2,7':-49,'3,5':-6,'3,6':-25,'3,7':-20,'4,5':-34,'4,6':9,'4,7':-32,'5,8':1,'6,8':2,'7,8':-16},
  'labels':'(alpha,d), alpha increasing, d=-ell_alpha,-ell_alpha+2,...,ell_alpha',
  'support':'row (alpha,d), column (beta,e): e=d+2s, abs(ell_beta-ell_alpha)<=2; equal ell requires alpha=beta',
  'p':'D_alpha if equal ell; P_alpha_beta if k=ell+2; -P_beta_alpha if k=ell-2',
  'r':'(d+ell)/2',
  'f_columns_s_minus1_0_plus1':{'k=ell+2':['2(ell+1-r)(ell+2-r)','2(r+1)(ell-r+1)','(r+1)(r+2)'],'k=ell':['2(ell-r+1)','d','-(r+1)'],'k=ell-2':['2','-2','1']},
  'entry':'p*f on support, zero otherwise'
 },
 'field_provenance':{
  'physical_inputs':'uniform_second_thermal_full_review/provenance_results.json:cases',
  'moment_intervals and filters':'uniform_second_moment_optimization/certificate.json',
  'long_majorants':'uniform_smaller_second_initialization/long_certificate.json and uniform_small_lengths_completion/long_certificate.json',
  'bootstrap_rows':'uniform_smaller_second_initialization/certificate.json:rows',
  'direct_4_to23':'uniform_small_lengths_completion/certificate.json:rows',
  'isolated24':'uniform_n24_second_coverage/certificate.json:zero_gap_window and uniform_n24_second_coverage_review/results.json:rows[0]',
  'direct25':'uniform_direct25_coverage/certificate.json',
  'direct_26_to33':'uniform_gap_0248_all_sizes/certificate.json:new_rows',
  'accepted_stronger_prefix_4_to25 and accepted_stronger_26_to33':'uniform_gap_0248_all_sizes_review/results.json',
  'all anchors':'the corresponding independent review anchors.out as indicated by field name'
 }
}
dump('EXACT_DATA.json',D)
dump('SOURCE_PINS.json',{'status':'DATA_AND_DOCUMENT_SOURCE_PINS','root_relative_to_guide':'../..','accepted_review_manifests':reviews,'producer_manifests':producers,'original_sources':original_sources,'consumed_file_sha256':FILES,'scope_note':'Hashes establish identity. Mathematical and physical acceptance is described by each pinned review, not inferred merely from hashing. Root README is mutable and not an input to the theorem.'})
print(json.dumps({'exact_data_bytes':(P/'EXACT_DATA.json').stat().st_size,'consumed_files':len(FILES),'verified_package_manifests':len(reviews)+len(producers),'original_source_blobs':len(original_sources)}))
