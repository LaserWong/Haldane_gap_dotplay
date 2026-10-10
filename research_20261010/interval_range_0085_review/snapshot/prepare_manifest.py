"""Create provenance and a local freeze; call only after verification finishes."""
import certify_lowband as B
C=B.C
import sys,json,hashlib,argparse
from datetime import datetime,timezone
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inputs():
 src=json.loads((C.R/'interval_joint_extension/INPUT_SHA256.json').read_text())
 for mod in list(sys.modules.values()):
  name=getattr(mod,'__file__',None)
  if not name:continue
  p=Path(name).resolve()
  if p.is_relative_to(C.ROOT) and not p.is_relative_to(C.HERE):src[str(p.relative_to(C.ROOT))]=sha(p)
 for raw in B.RAW.values():
  for n,d in raw['source_sha256'].items():src['research_20261010/'+n]=d
 inherited=[]
 reviews=[('large_seed_review','MANIFEST_SHA256.json'),('bilayer_frontier_review','MANIFEST_SHA256.json'),
  ('combined_ground_review','MANIFEST_SHA256.json'),('ordinary_interval_review','MANIFEST_SHA256.json'),
  ('interval_extension_review','MANIFEST_SHA256.json'),('interval_joint_review','MANIFEST_SHA256.json'),
  ('variational_filter_review','MANIFEST_SHA256.json'),('ground_moment_review','MANIFEST_SHA256.json'),
  ('quadratic_boson_review','MANIFEST_SHA256.json'),('joint_ratio_review','LEMMA_REVIEW_MANIFEST.json')]
 for folder,name in reviews:
  p=C.R/folder/name;raw=json.loads(p.read_text());files=raw.get('files',raw)
  for n,d in files.items():assert sha(p.parent/n)==d,(folder,n)
  src[str(p.relative_to(C.ROOT))]=sha(p);inherited.append(dict(folder=folder,manifest=name,sha256=sha(p),file_count=len(files)))
 for folder in ('ordinary_interval','interval_extension','interval_joint_extension'):
  for name in ('FROZEN_MANIFEST.json','coverage_summary.json','PROOF.md'):
   p=C.R/folder/name;src[str(p.relative_to(C.ROOT))]=sha(p)
 for p in [C.R/'joint_ratio_review/GENERAL_LEMMA.md',C.R/'joint_ratio_review/LEMMA_ACCEPTANCE.json']:
  src[str(p.relative_to(C.ROOT))]=sha(p)
 for name,digest in src.items():assert sha(C.ROOT/name)==digest,name
 (C.HERE/'INPUT_SHA256.json').write_text(json.dumps(dict(sorted(src.items())),indent=2)+'\n')
 (C.HERE/'INHERITED_REVIEWS.json').write_text(json.dumps(inherited,indent=2)+'\n')
 print('INPUTS',len(src),'INHERITED',len(inherited),sum(x['file_count'] for x in inherited))
def freeze():
 files={str(p.relative_to(C.HERE)):sha(p) for p in sorted(C.HERE.rglob('*')) if p.is_file() and p.name!='FROZEN_MANIFEST.json' and '__pycache__' not in str(p) and not p.name.endswith('.pyc')}
 out=dict(status='frozen_exact_candidate_for_independent_review',frozen_UTC=datetime.now(timezone.utc).isoformat(),files=files)
 p=C.HERE/'FROZEN_MANIFEST.json';p.write_text(json.dumps(out,indent=2)+'\n');print('FREEZE',len(files),sha(p))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--freeze',action='store_true');args=ap.parse_args()
 if args.freeze:freeze()
 else:inputs()
