from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent;S=P/'snapshot'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(S/'MANIFEST_SHA256.json')=='5748e30e8fc82a454bf9d30f94482357e987721783d55b2f88cdb0c54e28e768'
for f,h in json.loads((S/'MANIFEST_SHA256.json').read_text()).items():assert sha(S/f)==h,f
for f,h in json.loads((S/'INPUT_SHA256.json').read_text()).items():assert sha(R/f)==h,f
identity=json.loads((S/'interpreter_identity.json').read_text());assert sha(Path('/usr/bin/python3'))==identity['sha256'];assert str(Path('/usr/bin/python3').resolve())==identity['resolved_path']
assert sha(S/'reference_coefficients.txt')==sha(R/'bilayer_residual_direction_fixture/reference_coefficients.txt')
assert sha(S/'chunk_kernel')==sha(R/'bilayer_residual_direction_production_gate/chunk_kernel')
assert sha(S/'chunk_kernel.cpp')==sha(R/'bilayer_residual_direction_production_gate/chunk_kernel.cpp')
assert (P/'outer_driver.cpp').read_text()==(S/'outer_driver.cpp').read_text().replace('CPU_SET(3,','CPU_SET(4,').replace('cpu{10,360}','cpu{10,30}').replace('child_cpu{1,360}','child_cpu{1,30}')
assert (P/'checkpoint.py').read_text()==(S/'checkpoint.py').read_text().replace('cpu_affinity=3','cpu_affinity=4')
assert sha(R/'bilayer_residual_direction_fixture_review/MANIFEST_SHA256.json')=='3d3f16691dd1ce39d880b261f9f3fd46c3103c41dd9ee09b5e7e04c5794b0958'
assert 2*6+42*8+1+1==350 and 350+10==360
assert (4495+4095)//4096==2 and (169911+4095)//4096==42
print('PASS seals, exact source deltas, interpreter and fixed schedule')
