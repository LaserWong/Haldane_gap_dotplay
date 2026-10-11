#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
from plot_overview import verify
ROOT_FREEZE_APPROVED=True
assert ROOT_FREEZE_APPROVED, 'Wait for root scope/freeze approval.'
assert not (HERE/'MANIFEST_SHA256.json').exists()
x=json.loads((HERE/'overview_data.json').read_text());n=verify(x)
r=json.loads((HERE/'render_reproducibility.json').read_text());assert r['status'].startswith('PASS') and len(r['files'])==36
for f in r['files']:assert sha(HERE/f['file'])==f['sha256']
t=json.loads((HERE/'transport_reproducibility.json').read_text());assert t['status']=='PASS' and t['clean_restored_paths']==18 and t['idempotent'];assert t['manifest_sha256']==sha(ROOT/'reproducibility/stage11_exact_evidence/MANIFEST.json')
g=json.loads((HERE/'rejection_guards.json').read_text());assert g['status']=='PASS' and all(c['rejected'] for c in g['cases'])
for k in ['claims','dimension_rows','direct_source_hashes','review_seals','sealed_file_hashes_checked','conditional_uniform_rows','stage16_finite_bilayer_rows']:assert json.loads((HERE/'validation.json').read_text())[k]==r['replay_validation'][k]
assert (HERE/'VISUAL_QA.md').exists()
frozen=dict(status='FROZEN verified static overview',frozen_utc=datetime.now(timezone.utc).isoformat(),M_or_L_ge2_certificate_rows=len(x['claims']),preserved_stage16_main_rows=326,unconditional_positive_certificate_records=350,separate_conditional_uniform_rows=2,nested_covers=x['stage17_nested_covers'],selected_new_ground_search_dimensions=[21,57],selected_new_numerator_search_dimension=43,retained_counts=[49,97,1],pair_product_scope='g11/100,z-11/400 fixed-parameter variance lower bound only',full18_thermal_premises_discharged=False,mutable_campaign_data_included=False,direct_source_hashes=len(x['sources']),review_seals=len(x['review_seals']),sealed_source_files_checked=n,previous_stage16_unchanged=True,root_files_modified=False,remote_publication_performed=False,cpu_affinity=[8],address_space_limit_bytes=1024**3,corruptions_rejected=g['corruptions_rejected'],byte_identical_rendered_files=len(r['files']),scope='Integrity and exact scoped extraction of immutable independent reviews; not a fresh physical-proof audit')
(HERE/'FROZEN_STATUS.json').write_text(json.dumps(frozen,indent=2)+'\n')
manifest={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST_SHA256.json'}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(dict(status='FROZEN',files=len(manifest),manifest_sha256=sha(HERE/'MANIFEST_SHA256.json'))))
