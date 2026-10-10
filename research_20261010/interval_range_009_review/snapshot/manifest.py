"""Bind direct inputs, prior reviews, and the immutable producer package."""
import os,sys
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;R=HERE.parent;ROOT=R.parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_files(parent,raw):
 files=raw.get('files',raw)
 for f,h in files.items():assert sha(parent/f)==h,(str(parent),f)
 return len(files)
def inputs():
 import certify as P
 src=json.loads((R/'interval_range_0085/INPUT_SHA256.json').read_text())
 for mod in list(sys.modules.values()):
  p=getattr(mod,'__file__',None)
  if p:
   p=Path(p).resolve()
   if p.is_relative_to(ROOT) and not p.is_relative_to(HERE):src[str(p.relative_to(ROOT))]=sha(p)
 for p in (R/'low_band/ground_moment_auxiliary').glob('matrix_polynomial_*.json'):src[str(p.relative_to(ROOT))]=sha(p)
 for n in ('enlarged_8x8_g9d100.json','enlarged_8x8_g1d10.json','geometry_8x8_origin.json'):
  p=P.THIRD/n;src[str(p.relative_to(ROOT))]=sha(p)
 for n in ('enlarged_8x8_g9d100.json','enlarged_8x8_g1d10.json'):
  for name,h in json.loads((P.THIRD/n).read_text())['source_sha256'].items():src['research_20261010/'+name]=h
 specs=[('interval_range_0085','FROZEN_MANIFEST.json'),('interval_range_0085_review','MANIFEST_SHA256.json'),('low_band/third_moment_exact','PHYSICAL_MANIFEST.json')]
 if (R/'third_moment_review/MANIFEST_SHA256.json').exists():specs.append(('third_moment_review','MANIFEST_SHA256.json'))
 inherited=json.loads((R/'interval_range_0085/INHERITED_REVIEWS.json').read_text())
 for x in inherited:specs.append((x['folder'],x['manifest']))
 reviews=[]
 for folder,name in specs:
  p=R/folder/name;count=verify_files(p.parent,json.loads(p.read_text()));src[str(p.relative_to(ROOT))]=sha(p)
  reviews.append(dict(folder=folder,manifest=name,sha256=sha(p),file_count=count))
 for n,h in src.items():assert sha(ROOT/n)==h,n
 (HERE/'INPUT_SHA256.json').write_text(json.dumps(dict(sorted(src.items())),indent=2)+'\n')
 (HERE/'INHERITED_SEALS.json').write_text(json.dumps(reviews,indent=2)+'\n')
 print('INPUTS',len(src),'SEALS',len(reviews))
def verify():
 count=verify_files(ROOT,json.loads((HERE/'INPUT_SHA256.json').read_text()))
 for r in json.loads((HERE/'INHERITED_SEALS.json').read_text()):
  p=R/r['folder']/r['manifest'];assert sha(p)==r['sha256'];verify_files(p.parent,json.loads(p.read_text()))
 local=verify_files(HERE,json.loads((HERE/'FROZEN_MANIFEST.json').read_text()))
 print('PASS',count,'direct inputs;',local,'immutable package files; all inherited seals')
def freeze():
 from datetime import datetime,timezone
 files={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='FROZEN_MANIFEST.json' and '__pycache__' not in str(p)}
 p=HERE/'FROZEN_MANIFEST.json';p.write_text(json.dumps(dict(status='frozen_exact_continuous_009_candidate_pending_independent_review',frozen_UTC=datetime.now(timezone.utc).isoformat(),files=files),indent=2)+'\n');print('FROZEN',len(files),sha(p))
if __name__=='__main__':
 if '--inputs' in sys.argv:inputs()
 elif '--freeze' in sys.argv:freeze()
 else:verify()
