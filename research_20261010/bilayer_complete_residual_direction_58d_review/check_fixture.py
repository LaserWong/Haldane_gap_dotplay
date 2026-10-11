from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;S=P.parent/'bilayer_residual_direction_fixture_review'
assert hashlib.sha256((S/'MANIFEST_SHA256.json').read_bytes()).hexdigest()=='3d3f16691dd1ce39d880b261f9f3fd46c3103c41dd9ee09b5e7e04c5794b0958'
m=json.loads((S/'MANIFEST_SHA256.json').read_text())
for f in ['independent.json','small.vectors.txt']:assert hashlib.sha256((S/f).read_bytes()).hexdigest()==m[f]
a=json.loads((P/'fixture.json').read_text());b=json.loads((S/'independent.json').read_text());c=json.loads((P/'normalized_fixture.json').read_text())
for k in ['G','H200','H200_squared']:assert a[k]==b[k]==c[k]
for k in ['T_norm','CT_norm','T_K_T','q8_creation_norm']:assert a[k]==b['norms'][k]==c[k]
def vectors(f):return {int(t[0]):list(map(int,t[1:])) for line in f.read_text().splitlines() if (t:=line.split())}
assert vectors(P/'fixture_vectors.txt')==vectors(S/'small.vectors.txt')
print('PASS every Cartesian T/CT/DT/KT state,66 fixture moments and origin normalization')
