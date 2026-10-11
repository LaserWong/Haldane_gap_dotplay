from pathlib import Path
import hashlib,json
p=Path(__file__).parent;s=p.parent/'bilayer_brauer_rule_compiler';cart=p.parent/'bilayer_cartesian_indexed_sample';prev=p.parent/'bilayer_cartesian_indexed_review'
# Preserve all seals, and verify the reference action/table is the independently accepted implementation.
for package,want in [(s,'7eeb2e2c2adbfe000471c64e464fbf2b74becbd218ec4e1b4e7245472f72f6ec'),(cart,'760ab0e980cc40bd96028da1bc626353c44f463148d5dd2bc6cef81db566d1bd'),(prev,'8778764242be53f587f68b7416d7cf114cb0182b505089fbd85a7ffe224c1979')]:
 assert hashlib.sha256((package/'MANIFEST_SHA256.json').read_bytes()).hexdigest()==want
 for f,h in json.loads((package/'MANIFEST_SHA256.json').read_text()).items():assert hashlib.sha256((package/f).read_bytes()).hexdigest()==h
for fam in 'NFL':assert (s/f'run/diagrams_{fam}.bin').read_bytes()==(p/f'run/diagrams_{fam}.bin').read_bytes()
for n in (4,5):
 for k in ('fixture','terms'):
  f=f'{k}_{n}x2.json';assert json.loads((s/'run'/f).read_text())==json.loads((p/'run'/f).read_text())
for f in ('geometry_8x4.txt','reference_coefficients.txt'):assert (s/f).read_bytes()==(cart/f).read_bytes()
summary=json.loads((s/'run/summary.json').read_text());rows=[json.loads(x) for x in (s/'run/samples.jsonl').read_text().splitlines()]
for fam in summary['families']:
 rr=[x for x in rows if x['family']==fam['name']];assert len(rr)==512 and [x['sample'] for x in rr]==list(range(512)) and all(x['all_15_channels_equal'] for x in rr)
 for key in ('diagram_hits','active_diagrams','matching_hits','source_requests'):assert sum(x[key] for x in rr)==fam[key]
projection=sum(x['brauer_cpu_seconds'] for x in summary['families'])*169911/512
assert projection>180
assert 12816*16*3**15<2**42
assert 2**15*32*15*2**42*3**6*2**33<2**109
print('Regenerated diagram bytes, all fixture JSON, preceding seals, input files and sample counters PASS.')
print('Empirical three-action projection:',projection,'seconds; timing excludes shared-cache controls and whole-moment overhead.')
