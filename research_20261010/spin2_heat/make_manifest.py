#!/usr/bin/env python3
"""Hash reproducible sources, proofs, inputs, results and logs; omit executables."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
allowed={'.py','.cpp','.sh','.md','.json','.txt','.log','.stdout','.stderr'}
files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob('*')) if p.is_file() and p.suffix in allowed and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
(ROOT/'MANIFEST.json').write_text(json.dumps({'scope':'New spin2 heat optimization checkpoint; executable hashes are separately recorded in benchmark metadata','files':files},indent=2)+'\n')
print(len(files),'files')
