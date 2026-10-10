import json,itertools,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;RES=HERE.parent

def geometry(nx,ny):
 N=nx*ny;edges={};group=set()
 for i in range(N):
  x,y=divmod(i,ny)
  for xx,yy in [((x+1)%nx,y),(x,(y+1)%ny)]:
   edge=tuple(sorted((i,xx*ny+yy)));edges[edge]=edges.get(edge,0)+1
 for tx in range(nx):
  for ty in range(ny):
   for sx,sy in itertools.product((-1,1),repeat=2):
    for swap in range(2 if nx==ny else 1):
     perm=[]
     for i in range(N):
      x,y=divmod(i,ny)
      if swap:x,y=y,x
      perm.append(((sx*x+tx)%nx)*ny+(sy*y+ty)%ny)
     group.add(tuple(perm))
 remain=set(itertools.combinations(range(N),2));orbits=[];ids={}
 while remain:
  a,b=min(remain);orb={tuple(sorted((p[a],p[b]))) for p in group};assert orb<=remain
  for edge in orb:ids[edge]=len(orbits)
  remain-=orb;orbits.append(orb)
 return N,edges,orbits,ids
# Verify ordering/edges against the accepted8x4 engine fixture before producing4x4.
N,ee,oo,ii=geometry(8,4);tok=list(map(int,(RES/'bilayer_complete_residual_8x4/geometry_8x4.txt').read_text().split()));it=iter(tok);assert next(it)==N and next(it)==len(oo);E=next(it);old={}
for _ in range(E):a,b,w=next(it),next(it),next(it);old[a,b]=w
assert old==ee
for pair in itertools.combinations(range(N),2):assert next(it)==ii[pair]
assert list(it)==[]
N,ee,oo,ii=geometry(4,4);assert len(oo)==5
r=json.load(open(RES/'low_band/third_moment_exact/enlarged_4x4_g9d100.json'));assert [r['gram'][i+1][i+1] for i in range(5)]==[3*len(o) for o in oo]
text=f'{N} {len(oo)}\n{len(ee)}\n'+''.join(f'{a} {b} {w}\n' for (a,b),w in ee.items())+' '.join(str(ii[p]) for p in itertools.combinations(range(N),2))+'\n';(HERE/'geometry_4x4.txt').write_text(text)
r=json.load(open(RES/'bilayer_optimized_residual_g0105/outline_4x4.json'));tr=r['trial'];c=tr['integer_coefficients'];assert len(c)==16
(HERE/'coefficients.txt').write_text('400 21\n'+'\n'.join(' '.join(map(str,c[a:b])) for a,b in [(1,6),(6,11),(11,16)])+'\n')
(HERE/'trial.json').write_text(json.dumps({'g':'21/200','trial':tr,'target_ground_lower':r['target_ground_lower'],'residual_squared_budget':r['complete_residual_squared_budget'],'candidate_shifted_rayleigh':r['shifted_Rayleigh'],'integer_denominator':400,'integer_A_coefficient':21},indent=2)+'\n')
paths=[RES/'bilayer_optimized_residual_g0105/outline_4x4.json',RES/'bilayer_optimized_residual_g0105/MANIFEST_SHA256.json',RES/'bilayer_complete_residual_8x4/residual_scalar',RES/'bilayer_complete_residual_8x4/residual_scalar.cpp',RES/'low_band/third_moment_exact/enlarged_4x4_g9d100.json',RES/'low_band/third_moment_exact/geometry_4x4_origin.json',RES/'bilayer_complete_residual_8x4/geometry_8x4.txt']
(HERE/'INPUT_SHA256.json').write_text(json.dumps({str(p.relative_to(RES)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n')
