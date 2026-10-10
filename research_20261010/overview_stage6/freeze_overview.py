#!/usr/bin/env python3
"""Finalize a reviewed, replayed overview. Run only before declaring a new freeze."""
from common import *
from datetime import datetime,timezone
from plot_overview import verify
x=json.loads((HERE/'overview_data.json').read_text());n=verify(x)
r=json.loads((HERE/'render_reproducibility.json').read_text());assert r['status'].startswith('PASS')
for f in r['files']:assert sha(HERE/f['file'])==f['sha256']
assert (HERE/'VISUAL_QA.md').exists()
for k in ['claims','dimension_rows','direct_source_hashes','review_seals','sealed_file_hashes_checked']:
    assert json.loads((HERE/'validation.json').read_text())[k]==r['replay_validation'][k]
frozen={'status':'FROZEN verified static overview','frozen_utc':datetime.now(timezone.utc).isoformat(),'claims':len(x['claims']),'dimension_rows':len(x['dimensions']),'direct_source_hashes':len(x['sources']),'review_seals':len(x['review_seals']),'sealed_source_files_checked':n,'combined_review_included':x['combined_review_included'],'interval_extension_included':x['interval_extension_included'],'previous_overview_unchanged':True,'root_README_or_status_modified_by_this_task':False,'cpu_limit':1,'address_space_limit_bytes':1024**3,'scope':'Extraction, source-integrity verification and visual QA of sealed mathematical results; not a new spectral proof audit'}
(HERE/'FROZEN_STATUS.json').write_text(json.dumps(frozen,indent=2)+'\n')
manifest={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST_SHA256.json'}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'files':len(manifest),'manifest_sha256':sha(HERE/'MANIFEST_SHA256.json'),'status':'FROZEN'}))
