#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
from plot_overview import verify
assert not (HERE/'MANIFEST_SHA256.json').exists()
x=json.loads((HERE/'overview_data.json').read_text());n=verify(x)
r=json.loads((HERE/'render_reproducibility.json').read_text());assert r['status'].startswith('PASS') and len(r['files'])==18
for f in r['files']:assert sha(HERE/f['file'])==f['sha256']
assert (HERE/'VISUAL_QA.md').exists()
t=json.loads((HERE/'transport_reproducibility.json').read_text());assert t['status']=='PASS' and t['clean_restored_paths']==18 and t['idempotent']
assert t['manifest_sha256']==sha(ROOT/'reproducibility/stage11_exact_evidence/MANIFEST.json')
g=json.loads((HERE/'rejection_guards.json').read_text());assert g['status']=='PASS' and all(c['rejected'] for c in g['cases'])
for k in ['claims','dimension_rows','direct_source_hashes','review_seals','sealed_file_hashes_checked']:assert json.loads((HERE/'validation.json').read_text())[k]==r['replay_validation'][k]
frozen=dict(status='FROZEN verified static overview',frozen_utc=datetime.now(timezone.utc).isoformat(),M_or_L_ge2_certificate_rows=len(x['claims']),preserved_stage10_certificate_rows=225,preserved_stage10_interval_pieces=66,separate_finite_size_certificate_rows=len(x['finite_size_certificates']),separate_uniform_large_size_certificate_rows=len(x['uniform_large_size_certificates']),uniform_large_size_minima=[54,56,60],uniform_large_size_unique_ground=True,total_positive_certificate_records=len(x['claims'])+len(x['finite_size_certificates'])+len(x['uniform_large_size_certificates']),historical_dimension_rows=len(x['dimensions']),current_bilayer_dimension_rows=len(x['stage10_bilayer_dimensions']),direct_source_hashes=len(x['sources']),review_seals=len(x['review_seals']),sealed_source_files_checked=n,previous_stage10_unchanged=True,continuous_interval_endpoint=x['ordinary_interval_endpoint'],continuous_closed_pieces=x['ordinary_interval_piece_count'],chain_candidate_routes=207,integer_window_refinement_included=True,pair_symmetry_scope_erratum_included=True,uniform_transfer_moment_caps_included=True,mps_current_exact74_included=True,mps_even18_22_included=True,mps_direct_relaxed_paths_included=True,uniform_cooled_independent_review_included=True,unreviewed_candidates_included=False,below_L54_claim=False,minimum_seed_claim=False,excluded_new_bilayer_refinements=True,lossless_transport='reproducibility/stage11_exact_evidence/MANIFEST.json',root_README_or_status_modified_by_this_task=False,cpu_affinity=[8],address_space_limit_bytes=1024**3,corruptions_rejected=g['corruptions_rejected'],byte_identical_rendered_files=len(r['files']),scope='Source-integrity and scoped extraction of immutable independent reviews; not a new physical-proof audit')
(HERE/'FROZEN_STATUS.json').write_text(json.dumps(frozen,indent=2)+'\n')
manifest={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST_SHA256.json'}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(dict(status='FROZEN',files=len(manifest),manifest_sha256=sha(HERE/'MANIFEST_SHA256.json'))))
