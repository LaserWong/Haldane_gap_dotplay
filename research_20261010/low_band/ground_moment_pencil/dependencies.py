"""Freeze external code and physical inputs used by this isolated package."""
import json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
files=[
'research_20261010/low_band/low_band_certificate.py',
'original/Haldane_extensions/code/inertia_trace.py',
'original/Haldane_extensions/code/exact_heat_trace.py',
'original/Haldane_extensions/code/analytic_certificates.py',
'research_20261010/low_band/correlated_low_band.py',
'research_20261010/low_band/translation_band/large_refined_pipeline.py',
'research_20261010/low_band/translation_band/translated_band.py',
'research_20261010/low_band/tail_comparison/integrate_tails.py',
'research_20261010/low_band/small_seed_orders/scan_transported.py',
'research_20261010/low_band/frontier_g006/transport_orders.py',
'research_20261010/root_review/finite_window_2d.py']
files.append('two_d_theory/three_purity_certificate.py')
out={}
for rel in files:
    p=ROOT/rel
    if p.is_file():out[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in HERE.glob('ground_*.json'):
    if p.name=='ground_summary.json':continue
    for rel,digest in json.loads(p.read_text())['source_sha256'].items():
        full=ROOT/'research_20261010'/rel
        assert hashlib.sha256(full.read_bytes()).hexdigest()==digest
        out[str(full.relative_to(ROOT))]=digest
(HERE/'EXTERNAL_DEPENDENCIES_SHA256.json').write_text(json.dumps(out,indent=2,sort_keys=True))
print('external dependencies',len(out))
