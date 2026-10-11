#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
from plot_overview import verify
ROOT_FREEZE_APPROVED=True
assert ROOT_FREEZE_APPROVED, 'Wait for root scope/freeze approval.'
assert not (HERE/'MANIFEST_SHA256.json').exists()
x=json.loads((HERE/'overview_data.json').read_text());n=verify(x)
r=json.loads((HERE/'render_reproducibility.json').read_text());assert r['status'].startswith('PASS') and len(r['files'])==46
for f in r['files']:assert sha(HERE/f['file'])==f['sha256']
t=json.loads((HERE/'transport_reproducibility.json').read_text());assert t['status']=='PASS' and t['clean_restored_paths']==18 and t['idempotent'];assert t['manifest_sha256']==sha(ROOT/'reproducibility/stage11_exact_evidence/MANIFEST.json')
g=json.loads((HERE/'rejection_guards.json').read_text());assert g['status']=='PASS' and all(c['rejected'] for c in g['cases'])
for k in ['claims','dimension_rows','direct_source_hashes','review_seals','sealed_file_hashes_checked','conditional_uniform_rows','stage16_finite_bilayer_rows']:assert json.loads((HERE/'validation.json').read_text())[k]==r['replay_validation'][k]
assert (HERE/'VISUAL_QA.md').exists()
new_rows=len(x['stage20_near_uniform_certificates'])+len(x['stage20_positive_cell_certificates'])
frozen=dict(status='FROZEN verified static overview',frozen_utc=datetime.now(timezone.utc).isoformat(),M_or_L_ge2_certificate_rows=len(x['claims']),preserved_stage19_main_rows=339,preserved_stage19_unconditional_positive_certificate_records=413,unconditional_positive_certificate_records=413+new_rows,new_near_uniform_certificate_records=new_rows,historical_conditional_uniform_records_preserved=2,current_undischarged_second_input_claims=0,smallest_genuine_uniform_initialization=30,gap_at_smallest_uniform_initialization='179/10000',uniform_contiguous_coverage_onset=2,strongest_uniform_gap='31/1250',strongest_uniform_gap_tail_initialization=34,full18_thermal_premises_remain_discharged=True,bilayer_nested_covers_unchanged=x['stage17_nested_covers'],new_bilayer_gap=False,full8x4_m4_accepted=False,pipeline_scope=x['stage20_pipeline_scope'],direct25_review_resource_compliance='NOT_ACCEPTED unresolved',prior58D_producer_resource_compliance='UNVERIFIED',guide_first30second_strict_compliance='NOT_ACCEPTED; recorded30.21035921CPU',guide_final60second_recorded_CPU=25.746380744,mutable_campaign_data_included=False,direct_source_hashes=len(x['sources']),review_seals=len(x['review_seals']),sealed_review_entries_checked=n,previous_stage19_unchanged=True,root_files_modified=False,remote_publication_performed=False,cpu_affinity=[8],address_space_limit_bytes=1024**3,corruptions_rejected=g['corruptions_rejected'],byte_identical_rendered_files=len(r['files']),scope='Integrity and exact scoped extraction of independent final reviews; no new thermal or physical production')
(HERE/'FROZEN_STATUS.json').write_text(json.dumps(frozen,indent=2)+'\n')
manifest={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST_SHA256.json'}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(dict(status='FROZEN',files=len(manifest),manifest_sha256=sha(HERE/'MANIFEST_SHA256.json'))))
