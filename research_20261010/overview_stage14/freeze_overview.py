#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
from plot_overview import verify
assert not (HERE/'MANIFEST_SHA256.json').exists()
x=json.loads((HERE/'overview_data.json').read_text());n=verify(x)
r=json.loads((HERE/'render_reproducibility.json').read_text());assert r['status'].startswith('PASS') and len(r['files'])==28
for f in r['files']:assert sha(HERE/f['file'])==f['sha256']
t=json.loads((HERE/'transport_reproducibility.json').read_text());assert t['status']=='PASS' and t['clean_restored_paths']==18 and t['idempotent'];assert t['manifest_sha256']==sha(ROOT/'reproducibility/stage11_exact_evidence/MANIFEST.json')
g=json.loads((HERE/'rejection_guards.json').read_text());assert g['status']=='PASS' and all(c['rejected'] for c in g['cases'])
for k in ['claims','dimension_rows','direct_source_hashes','review_seals','sealed_file_hashes_checked','conditional_uniform_rows','bilayer_short_size_rows']:assert json.loads((HERE/'validation.json').read_text())[k]==r['replay_validation'][k]
assert (HERE/'VISUAL_QA.md').exists()
frozen=dict(status='FROZEN verified static overview',frozen_utc=datetime.now(timezone.utc).isoformat(),M_or_L_ge2_certificate_rows=len(x['claims']),preserved_stage13_main_rows=320,preserved_stage13_total_positive_records=327,new_unconditional_short_size_rows=3,separate_conditional_uniform_rows=2,unconditional_positive_records=330,conditional_rows_not_merged_with_local_physical_certificates=True,conditional_thermal_premises='18 published integer-total/error certificates beta49/4; no full local physical rerun',locally_accepted_uniform_coverage_minimum=48,locally_accepted_uniform_initialization=52,original_first_initialization=60,original_second_initialization=36,direct_source_hashes=len(x['sources']),review_seals=len(x['review_seals']),sealed_source_files_checked=n,previous_stage13_unchanged=True,current_all_size_bilayer_endpoint='21/200',current_all_size_bilayer_closed_pieces=80,new_short_bridge_endpoint='191/1250',new_short_bridge_size_scope=[2,7],full4x4_H2_fixture_accepted=True,full8x4_H2_included=False,new_pencil_gap=False,supervisor_engineering_gate='PASS',supervisor_review_thermal_jobs=0,supervisor_review_grants_launch_authorization=False,mutable_campaign_data_included=False,full_thermal_campaign_completed=False,root_files_modified=False,remote_publication_performed=False,cpu_affinity=[8],address_space_limit_bytes=1024**3,corruptions_rejected=g['corruptions_rejected'],byte_identical_rendered_files=len(r['files']),scope='Integrity and scoped extraction of immutable independent reviews; not a fresh physical-proof audit')
(HERE/'FROZEN_STATUS.json').write_text(json.dumps(frozen,indent=2)+'\n')
manifest={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST_SHA256.json'}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(dict(status='FROZEN',files=len(manifest),manifest_sha256=sha(HERE/'MANIFEST_SHA256.json'))))
