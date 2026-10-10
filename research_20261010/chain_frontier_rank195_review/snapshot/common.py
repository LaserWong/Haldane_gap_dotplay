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
