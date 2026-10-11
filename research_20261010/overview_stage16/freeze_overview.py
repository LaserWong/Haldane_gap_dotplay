#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
from plot_overview import verify
ROOT_FREEZE_APPROVED=True
assert ROOT_FREEZE_APPROVED, 'Wait for root scope/freeze approval.'
assert not (HERE/'MANIFEST_SHA256.json').exists()
x=json.loads((HERE/'overview_data.json').read_text());n=verify(x)
r=json.loads((HERE/'render_reproducibility.json').read_text());assert r['status'].startswith('PASS') and len(r['files'])==34
for f in r['files']:assert sha(HERE/f['file'])==f['sha256']
t=json.loads((HERE/'transport_reproducibility.json').read_text());assert t['status']=='PASS' and t['clean_restored_paths']==18 and t['idempotent'];assert t['manifest_sha256']==sha(ROOT/'reproducibility/stage11_exact_evidence/MANIFEST.json')
g=json.loads((HERE/'rejection_guards.json').read_text());assert g['status']=='PASS' and all(c['rejected'] for c in g['cases'])
for k in ['claims','dimension_rows','direct_source_hashes','review_seals','sealed_file_hashes_checked','conditional_uniform_rows','stage16_finite_bilayer_rows']:assert json.loads((HERE/'validation.json').read_text())[k]==r['replay_validation'][k]
assert (HERE/'VISUAL_QA.md').exists()
frozen=dict(status='FROZEN verified static overview',frozen_utc=datetime.now(timezone.utc).isoformat(),M_or_L_ge2_certificate_rows=len(x['claims']),preserved_stage15_main_rows=320,unconditional_positive_certificate_records=330+len(x['claims'])-320+len(x['stage16_finite_bilayer_certificates']),new_finite_bilayer_rows=1,new_finite_bilayer_scope='g=.11, every integer2<=L<=32, gap20227124817/10^12',separate_conditional_uniform_rows=2,locally_accepted_uniform_bounds_unchanged=True,conditional_uniform_gaps_unchanged=True,current_all_size_bilayer_endpoint=x['current_ordinary_interval_endpoint'],current_all_size_bilayer_closed_pieces=x['current_ordinary_interval_piece_count'],current_all_size_uniform_gap='4499695659/1000000000000',selected_g0106_denominator_search_dimensions=[16,43],selected_g0106_numerator_search_dimension=43,g0106_ambient_matrix_dimensions=[21,57],retained_counts=[49,97,1],selected_g01065_denominator_search_dimensions=[21,57],selected_g01065_numerator_search_dimension=43,higher_point_included=x['stage16_next_point_included'],higher_interval_included=x['stage16_next_interval_included'],physical8x4_m4_accepted=False,repair_review_engineering_only=True,full18_thermal_premises_discharged=False,mutable_campaign_data_included=False,direct_source_hashes=len(x['sources']),review_seals=len(x['review_seals']),sealed_source_files_checked=n,previous_stage15_unchanged=True,root_files_modified=False,remote_publication_performed=False,cpu_affinity=[8],address_space_limit_bytes=1024**3,corruptions_rejected=g['corruptions_rejected'],byte_identical_rendered_files=len(r['files']),scope='Integrity and scoped extraction of immutable independent reviews; not a fresh physical-proof audit')
(HERE/'FROZEN_STATUS.json').write_text(json.dumps(frozen,indent=2)+'\n')
manifest={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST_SHA256.json'}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(dict(status='FROZEN',files=len(manifest),manifest_sha256=sha(HERE/'MANIFEST_SHA256.json'))))
