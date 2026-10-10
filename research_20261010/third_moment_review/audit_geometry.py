"""Independently rebuild each graph; run full or origin support contractions."""
from audit_matrices import *
import subprocess
rows=[]
subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra',str(OUT/'independent_geometry.cpp'),'-o',str(OUT/'independent_geometry')],check=True)
prior=load(SNAP/'prior_reviews/large_seed_review/MANIFEST_SHA256.json')
for nx,ny in ((2,2),(4,2),(4,4),(8,4),(8,8)):
 shape=f'{nx}x{ny}';N=nx*ny;edges,orbits,ids=graph(nx,ny)
 text=f'{N} {len(orbits)}\n{len(edges)}\n'+''.join(f'{i} {j} {w}\n' for (i,j),w in sorted(edges.items()))+' '.join(str(ids[i,j]) for i,j in itertools.combinations(range(N),2))+'\n'
 assert text==(SNAP/'prior_geometry'/f'geometry_{shape}.txt').read_text()
 assert sha(SNAP/'prior_geometry'/f'geometry_{shape}.json')==prior[f'results/geometry_{shape}.json']
 for dx,dy in ((1,0),(0,1)):
  perm=lambda i:((i//ny+dx)%nx)*ny+(i%ny+dy)%ny
  assert {tuple(sorted((perm(a),perm(b)))):w for (a,b),w in edges.items()}==dict(edges)
  assert all(ids[tuple(sorted((perm(a),perm(b))))]==i for (a,b),i in ids.items())
 inp=OUT/'results'/f'geometry_{shape}.txt';inp.write_text(text)
 for mode in (('origin','full') if N<=16 else ('origin',)):
  path=OUT/'results'/f'geometry_{shape}{"_full" if mode=="full" else ""}.json';log=OUT/'logs'/f'geometry_{shape}_{mode}.log'
  with log.open('w') as f:subprocess.run([str(OUT/'independent_geometry'),str(inp),str(path),mode],stdout=f,stderr=f,check=True)
  r=load(path);prod=load(P/f'geometry_{shape}_{mode}.json');old=load(SNAP/'prior_geometry'/f'geometry_{shape}.json')
  assert all(r[k]==prod[k] for k in 'F S V W X Y Z'.split())
  assert all(r[k]==old[k] for k in 'F S V W'.split())
  assert r['all_q4']==math.comb(N-1,3) if mode=='origin' else r['all_q4']==math.comb(N,4)
  assert r['all_q6']==(math.comb(N-1,5) if N>=6 else 0) if mode=='origin' else r['all_q6']==(math.comb(N,6) if N>=6 else 0)
  assert r['active_q6']==prod['q6_subsets']==prod['q6_processed']
  assert r['active_q6']*N==old['active_q6']*6 if mode=='origin' else r['active_q6']==old['active_q6']
  rows.append(dict(shape=shape,mode=mode,all_seven_matrices_exact=True,old_F_S_V_W_exact=True,all_q4=r['all_q4'],all_q6=r['all_q6'],active_q6=r['active_q6'],seconds=r['seconds'],peak_rss_kib=r['peak_rss_kib'],generating_translations_preserve_edges_and_orbits=True))
  save('geometry_review.json',rows);print('PASS GEOMETRY',shape,mode,r['seconds'],r['peak_rss_kib'],flush=True)
