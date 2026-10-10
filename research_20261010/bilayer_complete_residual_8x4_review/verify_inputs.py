from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in json.loads((R/'INPUT_SHA256.json').read_text()).items():assert sha(R/p)==h,p
seal=R/'snapshot/PHYSICAL_MANIFEST.json';assert sha(seal)=='7d6269e8b080301cf7f941f9c3b9fd9e3f1db339ce2587bd078ed3ded96def95'
for p,h in json.loads(seal.read_text())['files'].items():assert sha(seal.parent/p)==h,p
print('All pinned physical inputs intact')

for name,folder,expected in [('SCALAR_MANIFEST.json','snapshot_scalar','0c7abb4cee911bb2c42990c0402b00dd7ecf62e0d607775d1f1c69c205424555'),('POLYNOMIAL_MANIFEST.json','snapshot_polynomial','96027b2dbe17e94c922a3884122ff96c525354a359e143e38328fbd3abbbc3ed')]:
 seal=R/folder/name;assert sha(seal)==expected
 for rel,h in json.loads(seal.read_text())['files'].items():assert sha(seal.parent/rel)==h,rel
print('Scalar and polynomial seals intact')
