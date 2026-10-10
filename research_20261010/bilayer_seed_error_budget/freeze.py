from budget import *
import hashlib
ROOT=RES.parent
out=[]
for row in json.load(open(HERE/'reoptimized_saved.json'))['results']:
 g=F(row['g']);vals=[]
 for kind,d in [('original',DATA[g]),('reoptimized_existing',row['data'])]:
  for p in d['denominator_patches']:
   rho=C.poly(list(map(F,p['rayleigh_coefficients'])),g);w=F(p['uniform_Temple_width']);vals.append({'source':kind,'N':p['N'],'rayleigh_upper':str(rho),'certified_ground_lower':str(rho-w),'width':str(w)})
 out.append({'g':str(g),'ranges':vals})
(HERE/'endpoint_ranges.json').write_text(json.dumps(out,indent=2)+'\n')
deps=json.load(open(RES/'bilayer_frontier_above_010/POINT_DEPENDENCIES.json'))
paths=[RES/'bilayer_frontier_above_010/exploration.json',RES/'bilayer_frontier_above_010/points.json',RES/'bilayer_frontier_above_010/POINT_MANIFEST_SHA256.json',RES/'bilayer_complete_residual_8x4/residual_8x4_origin.json',RES/'low_band/third_moment_exact/enlarged_8x4_g9d100.json',RES/'low_band/third_moment_exact/geometry_8x4_origin.json']
for mod in list(sys.modules.values()):
 p=getattr(mod,'__file__',None)
 if p:
  p=Path(p).resolve()
  if p.is_relative_to(ROOT) and not p.is_relative_to(HERE):paths.append(p)
for p in paths:deps[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
(HERE/'DEPENDENCIES.json').write_text(json.dumps(deps,indent=2)+'\n')
files=['PROOF.md','budget.py','screen.json','targets.py','targets.json','reoptimize_saved.py','reoptimized_saved.json','ritz_bound.py','ritz_bounds.json','joint_targets.py','joint_targets.json','compare_orders.py','order_comparison.json','endpoint_ranges.json','DEPENDENCIES.json','freeze.py']
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps({f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in files},indent=2)+'\n');print(hashlib.sha256((HERE/'MANIFEST_SHA256.json').read_bytes()).hexdigest())
