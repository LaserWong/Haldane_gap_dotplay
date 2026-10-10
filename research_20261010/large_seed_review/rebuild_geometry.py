import os,resource
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
resource.setrlimit(resource.RLIMIT_AS,(1536*1024**2,1536*1024**2))
if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
from pathlib import Path
from collections import Counter
import itertools,json,subprocess,time,hashlib
OUT=Path(__file__).resolve().parent;SRC=OUT/'snapshot/research_20261010/large_seed_moments'
def graph(nx,ny):
 e=Counter()
 for x in range(nx):
  for y in range(ny):
   i=x*ny+y
   for j in [((x+1)%nx)*ny+y,x*ny+(y+1)%ny]:e[tuple(sorted((i,j)))]+=1
 ids={};orbits=[];keymap={}
 for i,j in itertools.combinations(range(nx*ny),2):
  a,b=divmod(i,ny);c,d=divmod(j,ny);dx=min((a-c)%nx,(c-a)%nx);dy=min((b-d)%ny,(d-b)%ny)
  key=tuple(sorted((dx,dy))) if nx==ny else (dx,dy)
  if key not in keymap:keymap[key]=len(orbits);orbits.append([])
  k=keymap[key];orbits[k].append((i,j));ids[i,j]=k
 return e,orbits,ids
if __name__=='__main__':
 report=[]
 for nx,ny in [(2,2),(4,2),(4,4),(8,4),(8,8)]:
  t=time.monotonic();e,orbits,ids=graph(nx,ny);name=f'{nx}x{ny}';inp=OUT/'results'/f'geometry_{name}.txt';output=inp.with_suffix('.json')
  content=f'{nx*ny} {len(orbits)}\n{len(e)}\n'+''.join(f'{i} {j} {w}\n' for (i,j),w in sorted(e.items()))+' '.join(str(ids[i,j]) for i,j in itertools.combinations(range(nx*ny),2))+'\n'
  inp.write_text(content)
  subprocess.run([str(OUT/'rebuild_geometry'),str(inp),str(output)],check=True,timeout=1200)
  data=json.loads(output.read_text());old=json.loads((SRC/f'geometry_{name}.json').read_text())
  assert all(data[k]==old[k] for k in ['F','S','V','W'])
  assert data['active_q6']==old['six_subsets'];assert [len(x) for x in orbits]==old['pair_orbit_sizes']
  row=dict(shape=name,exact_geometry_equal=True,all_q4=data['all_q4'],all_q6=data['all_q6'],active_q6=data['active_q6'],pair_orbits=len(orbits),seconds=time.monotonic()-t,child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
  report.append(row);(OUT/'results/geometry_replay.json').write_text(json.dumps(report,indent=2)+'\n');print(row,flush=True)
