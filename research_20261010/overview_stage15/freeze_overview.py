#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
from plot_overview import verify
ROOT_FREEZE_APPROVED=True
assert ROOT_FREEZE_APPROVED, 'Parent requested an explicit freeze decision after partial-outcome and repair scope settle.'
assert not (HERE/'MANIFEST_SHA256.json').exists()
x=json.loads((HERE/'overview_data.json').read_text());n=verify(x)
r=json.loads((HERE/'render_reproducibility.json').read_text());assert r['status'].startswith('PASS') and len(r['files'])==32
for f in r['files']:assert sha(HERE/f['file'])==f['sha256']
t=json.loads((HERE/'transport_reproducibility.json').read_text());assert t['status']=='PASS' and t['clean_restored_paths']==18 and t['idempotent'];assert t['manifest_sha256']==sha(ROOT/'reproducibility/stage11_exact_evidence/MANIFEST.json')
g=json.loads((HERE/'rejection_guards.json').read_text());assert g['status']=='PASS' and all(c['rejected'] for c in g['cases'])
for k in ['claims','dimension_rows','direct_source_hashes','review_seals','sealed_file_hashes_checked','conditional_uniform_rows','bilayer_ground_endpoint_rows','accepted_full_thermal_cases']:assert json.loads((HERE/'validation.json').read_text())[k]==r['replay_validation'][k]
assert (HERE/'VISUAL_QA.md').exists()
frozen=dict(status='FROZEN verified static overview',frozen_utc=datetime.now(timezone.utc).isoformat(),M_or_L_ge2_certificate_rows=len(x['claims']),preserved_stage14_main_rows=320,unconditional_positive_gap_records=330,separate_conditional_uniform_rows=2,new_bilayer_ground_endpoint_records=len(x['bilayer_ground_endpoint_certificates']),ground_endpoint_records_are_not_gap_records=True,new_full8x4_H2_basis_dimensions=[43,57],new_split4x4_basis_dimension=21,original_first_initialization=60,original_second_initialization=36,locally_accepted_uniform_coverage_minimum=48,locally_accepted_uniform_initialization=52,current_all_size_bilayer_endpoint='21/200',current_all_size_bilayer_closed_pieces=80,new_all_size_bilayer_gap=False,accepted_complete_thermal_cases=16,accepted_thermal_lengths=list(range(4,12)),missing_thermal_cases=['L12_I','L12_P'],accepted_saved_batches=990,partial_snapshot_historical_status_at='2026-10-10 23:59 UTC',future_operational_status_belongs_in_root_docs=True,pending_repair_review_and_extension_design_excluded=True,partial_snapshot_terminal='BUDGET_RESERVATION_EXHAUSTED',partial_snapshot_charged_CPU_seconds=16207,partial_snapshot_remaining_CPU_seconds=5393,partial_snapshot_failed_reservations_retained=14640,full18_thermal_premises_discharged=False,conditional_uniform_gaps_unchanged=True,mutable_campaign_data_included=False,resume_reset_refund_authorized_by_snapshot=False,direct_source_hashes=len(x['sources']),review_seals=len(x['review_seals']),sealed_source_files_checked=n,previous_stage14_unchanged=True,root_files_modified=False,remote_publication_performed=False,cpu_affinity=[8],address_space_limit_bytes=1024**3,corruptions_rejected=g['corruptions_rejected'],byte_identical_rendered_files=len(r['files']),scope='Integrity and scoped extraction of immutable independent reviews; not a fresh physical-proof audit')
(HERE/'FROZEN_STATUS.json').write_text(json.dumps(frozen,indent=2)+'\n')
manifest={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST_SHA256.json'}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(dict(status='FROZEN',files=len(manifest),manifest_sha256=sha(HERE/'MANIFEST_SHA256.json'))))
