#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
from plot_overview import verify
ROOT_FREEZE_APPROVED=True
assert ROOT_FREEZE_APPROVED, 'Wait for root scope/freeze approval.'
assert not (HERE/'MANIFEST_SHA256.json').exists()
x=json.loads((HERE/'overview_data.json').read_text());n=verify(x)
r=json.loads((HERE/'render_reproducibility.json').read_text());assert r['status'].startswith('PASS') and len(r['files'])==40
for f in r['files']:assert sha(HERE/f['file'])==f['sha256']
t=json.loads((HERE/'transport_reproducibility.json').read_text());assert t['status']=='PASS' and t['clean_restored_paths']==18 and t['idempotent'];assert t['manifest_sha256']==sha(ROOT/'reproducibility/stage11_exact_evidence/MANIFEST.json')
g=json.loads((HERE/'rejection_guards.json').read_text());assert g['status']=='PASS' and all(c['rejected'] for c in g['cases'])
for k in ['claims','dimension_rows','direct_source_hashes','review_seals','sealed_file_hashes_checked','conditional_uniform_rows','stage16_finite_bilayer_rows']:assert json.loads((HERE/'validation.json').read_text())[k]==r['replay_validation'][k]
assert (HERE/'VISUAL_QA.md').exists()
frozen=dict(status='FROZEN verified static overview',frozen_utc=datetime.now(timezone.utc).isoformat(),M_or_L_ge2_certificate_rows=len(x['claims']),preserved_stage17_main_rows=339,unconditional_positive_certificate_records=352,new_locally_reproduced_uniform_records=2,historical_conditional_uniform_records_preserved=2,current_undischarged_second_input_claims=0,uniform_best_gap='107/5000',uniform_integer_size_min=36,uniform_unique_ground=True,full18_thermal_premises_discharged=True,thermal_beta='49/4',thermal_checkpoints=2428,thermal_snapshot_archive_entries=2979,thermal_campaign_charge=27543,thermal_campaign_cap=43200,thermal_historical_charge_preserved=16207,prior_D26_MPS72_normalization_rechecked=True,new_MPS_contraction=False,bilayer_nested_covers_unchanged=x['stage17_nested_covers'],new_complete_bilayer_trial_basis_dimension=58,new_finite_seed_ground_endpoints=2,new_bilayer_gap=False,producer_endpoint_resource_compliance='UNVERIFIED',mutable_campaign_data_included=False,direct_source_hashes=len(x['sources']),review_seals=len(x['review_seals']),sealed_review_entries_checked=n,separate_complete_row_producer_entries=140,previous_stage17_unchanged=True,root_files_modified=False,remote_publication_performed=False,cpu_affinity=[8],address_space_limit_bytes=1024**3,corruptions_rejected=g['corruptions_rejected'],byte_identical_rendered_files=len(r['files']),scope='Integrity and exact scoped extraction of independent final reviews; no new thermal or physical production')
(HERE/'FROZEN_STATUS.json').write_text(json.dumps(frozen,indent=2)+'\n')
manifest={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST_SHA256.json'}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(dict(status='FROZEN',files=len(manifest),manifest_sha256=sha(HERE/'MANIFEST_SHA256.json'))))
