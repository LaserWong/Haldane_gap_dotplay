from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent
for sub,seal in [('snapshot','7309cb09729f77c39ef870b6c6a69980fecbdb5521a03e89f90836667c4100f0'),('correction_snapshot','677d95d8f1b7c22f7c76db271078c0f4d0376932eacd4374eeb5c39667e627f7')]:
 s=P/sub;f=s/'MANIFEST_SHA256.json';assert hashlib.sha256(f.read_bytes()).hexdigest()==seal
 for name,h in json.loads(f.read_text()).items():assert hashlib.sha256((s/name).read_bytes()).hexdigest()==h,name
for name,h in json.loads((P/'snapshot/INPUT_SHA256.json').read_text()).items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==h,name
assert hashlib.sha256((R/'bilayer_residual_direction_fixture_review/MANIFEST_SHA256.json').read_bytes()).hexdigest()=='3d3f16691dd1ce39d880b261f9f3fd46c3103c41dd9ee09b5e7e04c5794b0958'
print('PASS provenance')
