from certify_points import *
import hashlib
ROOT=RES.parent
paths={ROOT/k for k in json.load(open(RES/'interval_range_010/INPUT_SHA256.json'))}
paths.update([RES/'interval_range_010/coverage/interval_010.json',RES/'interval_range_010_review/MANIFEST_SHA256.json',RES/'bilayer_direct_window_extension/MANIFEST_SHA256.json',RES/'bilayer_direct_window_extension/PROSE_ERRATUM.json',RES/'bilayer_direct_window_continuation/MANIFEST_SHA256.json'])
for mod in list(sys.modules.values()):
 p=getattr(mod,'__file__',None)
 if p:
  p=Path(p).resolve()
  if p.is_relative_to(ROOT) and not p.is_relative_to(HERE):paths.add(p)
for raw in P.L.RAW.values():paths.update(RES/p for p in raw['source_sha256'])
(HERE/'POINT_DEPENDENCIES.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)},indent=2)+'\n')
files=['explore.py','exploration.json','nearby.json','domain.json','domain_and_nearby.py','certify_points.py','points.json','POINT_PROOF.md','POINT_DEPENDENCIES.json','freeze_points.py']
(HERE/'POINT_MANIFEST_SHA256.json').write_text(json.dumps({f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in files},indent=2)+'\n')
print(hashlib.sha256((HERE/'POINT_MANIFEST_SHA256.json').read_bytes()).hexdigest())
