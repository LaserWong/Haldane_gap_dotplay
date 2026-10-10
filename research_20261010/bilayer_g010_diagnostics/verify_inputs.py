from replay import *
seals=['low_band/third_moment_exact/PHYSICAL_MANIFEST.json','third_moment_review/MANIFEST_SHA256.json','low_band/frontier_g009/FROZEN_MANIFEST_1920.json','ground_moment_review/MANIFEST_SHA256.json','combined_ground_review/MANIFEST_SHA256.json','interval_range_009/FROZEN_MANIFEST.json','interval_range_009_review/MANIFEST_SHA256.json']
checks=[]
for s in seals:
 p=RES/s;rec=load(p);files=rec.get('files',rec)
 for name,h in files.items():assert sha(p.parent/name)==h,(s,name)
 checks.append(dict(path=s,sha256=sha(p),verified_files=len(files)))
for shape in ['4x4','8x4','8x8']:
 for rel in [f'low_band/combined_ground_bounds/combined/patch_{shape}_g1d10.json',f'low_band/frontier_g007_g010/g1d10/block1_{shape}_g1d10.json']:
  assert sha(RES/rel)==sha(RES/'combined_ground_review/snapshot/research_20261010'/rel)
 geom=f'geometry_{shape}_origin.json'
 assert sha(RES/'low_band/third_moment_exact'/geom)==sha(RES/'third_moment_review/snapshot/producer'/geom)
# Pin source modules actually reused by producer diagnostics/builds as well as
# all direct witness inputs. No source file is changed.
paths=set()
for r in load(HERE/'weighted_summary.json'):paths.update(r['sources'])
paths.update(['low_band/third_moment_exact/enlarged_8x8_g1d10.json','low_band/third_moment_exact/enlarged_numerator.py','low_band/third_moment_exact/exact_filter.py','low_band/frontier_g009/scan_joint.py','low_band/small_seed_orders/scan_transported.py','low_band/frontier_g006/transport_orders.py','low_band/joint_trace_bootstrap/joint_scalar.py','low_band/correlated_low_band.py','low_band/tail_comparison/integrate_tails.py','symmetry/symmetric_ground.py'])
pins={p:sha(RES/p) for p in sorted(paths)}
(HERE/'INPUT_SHA256.json').write_text(json.dumps(pins,indent=2)+'\n')
(HERE/'INHERITED_SEALS.json').write_text(json.dumps(checks,indent=2)+'\n')
print('All inherited seals and source/snapshot equalities pass:',sum(x['verified_files'] for x in checks),'sealed files.')
