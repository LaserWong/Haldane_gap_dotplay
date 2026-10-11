from pathlib import Path
from fractions import Fraction as F
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent;old=R/'uniform_smaller_second_initialization_review'
assert hashlib.sha256((old/'MANIFEST_SHA256.json').read_bytes()).hexdigest()=='54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f'
for f,h in json.loads((old/'MANIFEST_SHA256.json').read_text()).items():assert hashlib.sha256((old/f).read_bytes()).hexdigest()==h
for f in ['contract_sequential','contract_sequential.cpp']:assert (P/f).read_bytes()==(old/f).read_bytes()
for f in ['limited_run.py','rebuild_d26.py']:assert (P/f).read_bytes()==(old/f).read_bytes().replace(b'(60,60)',b'(30,30)')
assert (P/'d26_blocks.txt').read_bytes()==(R.parent/'audit/mps/mps_blocks.txt').read_bytes()
x={k:int(v) for k,v in (l.split('=') for l in (P/'anchors.out').read_text().splitlines())}
for n in (48,52,56):
 separate={k:int(v) for k,v in (l.split('=') for l in (P/f'anchor{n}.out').read_text().splitlines())};assert separate=={k:v for k,v in x.items() if k.endswith('_'+str(n))};assert x[f'N0_{n}']>0 and F(x[f'H0_{n}'],x[f'N0_{n}'])+n*F(700741,500000)<0
print('fresh48/52/56 anchor identities and signs PASS')
