import json,math,hashlib,time,resource,os
from pathlib import Path
os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_CPU,(2,2));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
p=Path(__file__).parent;r=p/'run';root=p.parent
for filename in ['fixture_4x2.json','fixture_5x2.json','terms_4x2.json','terms_5x2.json']:
 a=json.loads((root/'bilayer_krylov_local_fixture'/filename).read_text());b=json.loads((r/filename).read_text())
 if filename.startswith('fixture'):a.pop('peak_sparse_states');b.pop('peak_sparse_states')
 assert a==b,filename
ref=list(map(int,(p/'reference_coefficients.txt').read_text().split()));w=json.loads((root/'bilayer_split_pencil_optimization/result.json').read_text())['results'][0]
assert w['shape']==[8,4] and w['g']=='11/100' and ref[14:]==w['integer_coefficients'][-14:]
raw=list(map(int,(p/'geometry_8x4.txt').read_text().split()));N,d,E=raw[:3];position=3;edges={}
for _ in range(E):
 a,b,c=raw[position:position+3];position+=3;edges[min(a,b),max(a,b)]=c
orbit={}
for a in range(N):
 for b in range(a+1,N):orbit[a,b]=raw[position];position+=1
assert position==len(raw)
def matchings(s):
 if not s:yield [];return
 for i in range(1,len(s)):
  for p0 in matchings(s[1:i]+s[i+1:]):yield [(s[0],s[i])]+p0
pairs=list(matchings(list(range(6))))
def coeff(mask):
 sites=[i for i in range(32) if mask>>i&1];vals=[]
 for pairing in pairs:
  es=[tuple(sorted((sites[a],sites[b]))) for a,b in pairing];ws=[edges.get(e,0) for e in es]
  vals.append(sum(2*ws[(k+1)%3]*ws[(k+2)%3]*ref[14+orbit[es[k]]] for k in range(3)))
 return vals
summary=json.loads((r/'summary.json').read_text());samples=[json.loads(x) for x in (r/'sample.jsonl').read_text().splitlines()]
out={'physical_fixture_all_15_terms_m3_m4_sector_norms_equal':True,'peak_sparse_state_count_difference_is_basis_dependent':True,'cm_equals_accepted_57d_g011_witness':True,'sample_target_count':512,'total_origin_containing_q6_supports':169911,'total_unrestricted_q6_supports':math.comb(32,6),'full_class_multiplicities_not_enumerated':True,'projections_are_empirical_not_runtime_bounds':True,'families':[]}
for fam in summary['families']:
 rows=[x for x in samples if x['family']==fam['name']];assert len(rows)==512
 classes={};zeros=0
 for x in rows:
  active=any(coeff(x['mask']));zeros+=not active
  key=f"edges={x['occupied_edges']},m_nonzero={active}";z=classes.setdefault(key,{'sample_count':0,'rule_hits':0,'lookup_calls':0,'lookup_misses':0,'action_cpu_seconds':0.0})
  z['sample_count']+=1
  for key in ['rule_hits','lookup_calls','lookup_misses']:z[key]+=x[key]
  z['action_cpu_seconds']+=x['cpu_seconds']
 totals={key:sum(x[key] for x in rows) for key in ['incidence_visits','embedding_hits','row_hits','rule_hits','lookup_calls','lookup_misses']}
 meanproject=fam['sample_cpu_seconds']/512*169911
 out['families'].append({'name':fam['name'],'source_zero_targets':zeros,'source_nonzero_targets':512-zeros,'totals':totals,'sample_classes':classes,'serialized_rule_bytes':(r/f"rules_{fam['name']}.bin").stat().st_size,'empirical_all_origin_support_action_seconds':meanproject,'tenfold_empirical_action_seconds':10*meanproject,'worst_observed_support_scaled_seconds':fam['maximum_support_seconds']*169911,'note':'Analytic m lookup only; no chi or v cache setup/contraction timing.'})
out['combined_empirical_action_seconds']=sum(x['empirical_all_origin_support_action_seconds'] for x in out['families']);out['combined_tenfold_action_seconds']=10*out['combined_empirical_action_seconds'];out['measured_cartesian_compiler_index_setup_seconds']=sum(x['setup_cpu_seconds'] for x in summary['families']);out['production_gate_180_seconds']='FAIL_EMPIRICAL_RESOURCE_PROJECTION';out['analysis_cpu_seconds']=resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime
(r/'analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='families'},indent=2))
