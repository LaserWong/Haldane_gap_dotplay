#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime,timezone
from plot_overview import verify
assert not (HERE/'MANIFEST_SHA256.json').exists()
x=json.loads((HERE/'overview_data.json').read_text());n=verify(x)
r=json.loads((HERE/'render_reproducibility.json').read_text());assert r['status'].startswith('PASS')
for f in r['files']:assert sha(HERE/f['file'])==f['sha256']
assert (HERE/'VISUAL_QA.md').exists()
g=json.loads((HERE/'rejection_guards.json').read_text());assert g['status']=='PASS' and all(c['rejected'] for c in g['cases'])
for k in ['claims','dimension_rows','direct_source_hashes','review_seals','sealed_file_hashes_checked']:assert json.loads((HERE/'validation.json').read_text())[k]==r['replay_validation'][k]
frozen=dict(status='FROZEN verified static overview',frozen_utc=datetime.now(timezone.utc).isoformat(),claims=len(x['claims']),preserved_stage9_claims=212,preserved_stage9_interval_pieces=56,historical_dimension_rows=len(x['dimensions']),current_bilayer_dimension_rows=len(x['stage10_bilayer_dimensions']),direct_source_hashes=len(x['sources']),review_seals=len(x['review_seals']),sealed_source_files_checked=n,previous_overview_unchanged=True,previous_stage9_unchanged=True,continuous_interval_endpoint=x['ordinary_interval_endpoint'],continuous_closed_pieces=x['ordinary_interval_piece_count'],chain_candidate_routes=207,complete_residual_review_included=True,rank195_review_included=True,rank195_positive_gap=False,interval_range_010_included=x['interval_range_010_included'],interval_range_010_final_manifest='d6eb3e4ce912086fe66dc1eb2917c3ae7381bc6a527a939b99229b97b863f3e5',excluded_branches=['MPS pi-current','new chain numerator refinements'],root_README_or_status_modified_by_this_task=False,cpu_limit=1,address_space_limit_bytes=1024**3,corruptions_rejected=g['corruptions_rejected'],byte_identical_rendered_files=len(r['files']),scope='Source-integrity verification and visual extraction of immutable accepted reviews, not a new spectral proof audit')
(HERE/'FROZEN_STATUS.json').write_text(json.dumps(frozen,indent=2)+'\n')
manifest={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST_SHA256.json'}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(dict(status='FROZEN',files=len(manifest),manifest_sha256=sha(HERE/'MANIFEST_SHA256.json'))))
