import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,resource,importlib.util,time
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,str(HERE.parent/'chain_filter_extension'))
build=load('build_inputs',HERE.parent/'chain_filter_extension/build_inputs.py')
p=load('lowband',HERE.parent/'chain_small_low_band/produce_low_band.py');p.HERE=HERE
scan=load('scan',HERE.parent/'chain_filter_extension/scan_orders.py');scan.trace=p.trace_float
sys.path.insert(0,str(ROOT/'low_energy'));import dimer_subspace as ds;import local_relative_bound as lb
ds.OUT=HERE
mat=json.loads((HERE.parent/'chain_filter_extension/M8_two_trial_moments.json').read_text());mom=json.loads((HERE.parent/'chain_small_low_band/unit_moments.json').read_text())
records=[];results=[]
for g in map(F,['21/100','11/50','9/40','1/4']):
 tag='small_g'+str(g).replace('/','d');path=HERE/(tag+'_ground.json')
 small=json.loads(path.read_text()) if path.exists() else ds.certify_sparse(F(1),4,ds.columnar_bonds(4,1,g,F(0)),tag=tag,relative_bound=lb.optimize_bound(F(1),g,'chain',4),support_depth=4)
 rec=p.patch(dict(g=str(g),small=small,small_folder=str(HERE.relative_to(ROOT)),large=build.evaluate(mat,g)),mom);records.append(rec)
 hits=[]
 for j in range(40,1601):
  beta=j/20;r=scan.run(rec['small'],float(F(rec['large']['exact_rayleigh'])),beta)
  if r:
   import math
   shift=float(F(rec['large']['exact_rayleigh'])-2*F(small['exact_rayleigh']));J=math.exp(-2*beta*shift)/p.trace_float(rec['small'],beta)**4
   w=scan.interpolate(math.sqrt(J),J,beta,J);r['initial_window_gap']=w;r['all_size_gap']=min(w,r['all_M_ge8_gap']);hits.append(r)
 result=dict(g=str(g),passes=len(hits),best=max(hits,key=lambda r:r['all_size_gap']) if hits else None)
 results.append(result);print('RESULT',result,flush=True)
(HERE/'inputs.json').write_text(json.dumps(records,indent=2));(HERE/'scan.json').write_text(json.dumps(results,indent=2))
