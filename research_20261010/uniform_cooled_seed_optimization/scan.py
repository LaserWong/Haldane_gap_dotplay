#!/usr/bin/env python3
"""Floating proposal scan only. No failures here are exclusion certificates."""
import json,time,os,resource
from pathlib import Path
from explore import general,test
P=Path(__file__).resolve().parent
os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
t=time.process_time();rows=[]
for n in range(40,62,2):
 hits=[v for l in range(16,41,2) if l<=n for ri in range(150,321,2) if (v:=general(n,l,ri/100))]
 rows.append({'n':n,'positive_candidates':len(hits),'best_gap_candidate':max(hits,key=lambda v:v['final'][2]) if hits else None})
result={'status':'FLOATING proposal scan only; absence of candidate is not exclusion','anchor_assumption':'Uses only hypothetical/proved shifted ground Boltzmann weight >1; exact selected anchors separately verified','base_even_lengths':[16,40],'cooling_ratios':{'start':'3/2','end':'16/5','step':'1/50'},'rows':rows,'cpu_seconds':time.process_time()-t}
(P/'scan_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
