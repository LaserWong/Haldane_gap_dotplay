#!/usr/bin/env python3
"""Collect portable support files and fingerprint all frozen spin-one results."""
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
UP=ROOT.parent/'upstream/extracted'
if UP.is_dir():
    for rel in ['cases/haldane_reference_audit/thermal_small_exact.py',
                'cases/haldane_reference_audit/published_scalar_enclosures.py',
                'cases/haldane_reference_audit/mps_exact_output.txt',
                'cases/haldane_reference_audit/build_mps.py',
                'cases/haldane_reference_audit/mps_exact.cpp',
                'tools/bootstrap_scalar.py']:
        target=ROOT/'reference_sources'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(UP/rel,target)
audit=ROOT.parent/'audit'
if audit.is_dir():
    for src,name in [('APPENDIX_A_BRIDGE.md','APPENDIX_A_BRIDGE.md'),
                     ('independent/streamed_heat_audit.json','streamed_heat_audit.json'),
                     ('mps/contraction.out','mps_contraction.out'),('mps/mps_blocks.txt','mps_blocks.txt'),
                     ('mps/build.log','mps_build.log'),('mps/timing.log','mps_timing.log')]:
        target=ROOT/'audit_inputs'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(audit/src,target)
entries=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or p.name in ('MANIFEST.json',) or '__pycache__' in p.parts or 'spin2' in p.parts:continue
    entries.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
manifest={'scope':'Completed spin-one Appendix A heat inputs and reconstructed route; source archive unchanged',
          'files':entries,'total_bytes':sum(e['bytes'] for e in entries)}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'files':len(entries),'bytes':manifest['total_bytes']}))
