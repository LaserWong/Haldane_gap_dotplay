#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
from plot_overview import verify
assert not (HERE/'MANIFEST_SHA256.json').exists()
x=json.loads((HERE/'overview_data.json').read_text());n=verify(x)
r=json.loads((HERE/'render_reproducibility.json').read_text());assert r['status'].startswith('PASS') and len(r['files'])==24
for f in r['files']:assert sha(HERE/f['file'])==f['sha256']
t=json.loads((HERE/'transport_reproducibility.json').read_text());assert t['status']=='PASS' and t['clean_restored_paths']==18 and t['idempotent'];assert t['manifest_sha256']==sha(ROOT/'reproducibility/stage11_exact_evidence/MANIFEST.json')
g=json.loads((HERE/'rejection_guards.json').read_text());assert g['status']=='PASS' and all(c['rejected'] for c in g['cases'])
for k in ['claims','dimension_rows','direct_source_hashes','review_seals','sealed_file_hashes_checked']:assert json.loads((HERE/'validation.json').read_text())[k]==r['replay_validation'][k]
assert (HERE/'VISUAL_QA.md').exists()
frozen=dict(status='FROZEN verified static overview',frozen_utc=datetime.now(timezone.utc).isoformat(),M_or_L_ge2_certificate_rows=len(x['claims']),preserved_stage12_certificate_rows=311,preserved_stage12_interval_pieces=74,preserved_stage11_interval_pieces=66,separate_finite_size_certificate_rows=len(x['finite_size_certificates']),separate_uniform_large_size_certificate_rows=len(x['uniform_large_size_certificates']),separate_uniform_finite_windows=len(x['uniform_finite_windows']),separate_uniform_coverage_certificates=len(x['uniform_coverage_certificates']),uniform_coverage_minimum=48,uniform_bootstrap_initialization=52,total_positive_certificate_records=len(x['claims'])+len(x['finite_size_certificates'])+len(x['uniform_large_size_certificates'])+len(x['uniform_finite_windows'])+len(x['uniform_coverage_certificates']),direct_source_hashes=len(x['sources']),review_seals=len(x['review_seals']),sealed_source_files_checked=n,previous_stage12_unchanged=True,current_continuous_interval_endpoint=x['current_ordinary_interval_endpoint'],current_continuous_closed_pieces=x['current_ordinary_interval_piece_count'],current_uniform_gap='4499695659/1000000000000',new_frontier_point='21/200',new_frontier_point_gap='31673112867/1000000000000',minimum_seed_claim=False,root_files_modified=False,remote_publication_performed=False,cpu_affinity=[8],address_space_limit_bytes=1024**3,corruptions_rejected=g['corruptions_rejected'],byte_identical_rendered_files=len(r['files']),scope='Integrity and scoped extraction of immutable independent reviews; not a fresh physical-proof audit')
(HERE/'FROZEN_STATUS.json').write_text(json.dumps(frozen,indent=2)+'\n')
manifest={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST_SHA256.json'}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(dict(status='FROZEN',files=len(manifest),manifest_sha256=sha(HERE/'MANIFEST_SHA256.json'))))
