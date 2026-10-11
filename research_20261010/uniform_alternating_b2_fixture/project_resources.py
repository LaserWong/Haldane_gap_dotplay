#!/usr/bin/env python3
import resource,time,json,hashlib
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(3,3));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));start=time.process_time();P=Path(__file__).resolve().parent
with (P/'b2_blocks.txt').open() as f:
 nb=int(f.readline());rows=[]
 for _ in range(nb):
  q,d=map(int,f.readline().split());caps={}
  for name in ['T','O_h','O_h2','O_adj_sym']:
   rmax=0;entrybits=0
   for i in range(d):
    vals=list(map(int,f.readline().split()));assert len(vals)==d
    rmax=max(rmax,sum(map(abs,vals)));entrybits=max(entrybits,max(abs(x).bit_length() for x in vals))
   caps[name]={'max_entry_bits':entrybits,'row_abs_sum_upper_power2_bits':rmax.bit_length()}
  rows.append({'charge':q,'side':d,'caps':caps})
 assert not f.read().strip()
T=max(x['caps']['T']['row_abs_sum_upper_power2_bits'] for x in rows);O=max(x['caps']['O_h']['row_abs_sum_upper_power2_bits'] for x in rows);power64=64*T;R61=6+60*T+O
out={'status':'DESIGN_PROJECTION_ONLY_NO_L32_OR_L64_CONTRACTION','local_blocks_sha256':hashlib.sha256((P/'b2_blocks.txt').read_bytes()).hexdigest(),'file_bytes':(P/'b2_blocks.txt').stat().st_size,'rows':rows,'conservative_bit_caps':{'T64_infinity_norm_log2_upper':power64,'R61_infinity_norm_log2_upper':R61},'production_plan':{'L':64,'binary_convolution_N':61,'full_matrix_multiplications_per_charge_block_upper':29,'maximum_block_side':162,'max_simultaneous_matrix_buffers_target':10,'dense_676_matrix_allocation':False,'dense_1352_matrix_allocation':False,'cpu_projection_seconds_not_guaranteed':[20,40],'requested_future_hard_cpu_seconds':60,'requested_future_hard_memory_mib':256,'proposed_wall_watchdog_seconds':180,'execute_authorized':False},'resources':{'cpu_seconds':time.process_time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'RESOURCE_PROJECTION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
