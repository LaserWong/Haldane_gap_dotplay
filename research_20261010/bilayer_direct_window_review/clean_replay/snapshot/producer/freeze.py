from replay import *
r=json.loads((HERE/'replay.json').read_text());candidate=max(r['results'],key=lambda x:F(x['all_integer_gap']));(HERE/'candidate.json').write_text(json.dumps(candidate,indent=2)+'\n')
files=set(paths)
for mod in list(sys.modules.values()):
 p=getattr(mod,'__file__',None)
 if p:
  p=Path(p).resolve()
  if p.is_relative_to(RES) and not p.is_relative_to(HERE):files.add(p)
files.update([RES/'low_band/frontier_g007_g010/short_sizes/uniform_short_sizes.json',RES/'bilayer_complete_residual_8x4_review/MANIFEST_SHA256.json',RES/'integer_window_refinement_review/MANIFEST_SHA256.json'])
(HERE/'DEPENDENCIES.json').write_text(json.dumps({str(p.relative_to(RES)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},indent=2)+'\n')
