from pathlib import Path
import json,hashlib,math
r=Path(__file__).resolve().parent;p=r.parent/'bilayer_whole_m4_pipeline';h=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
assert h(p/'MANIFEST_SHA256.json')=='13010f1d1326fd2c76938036b01ce2e912d70f35714a2c473a529910a790a488'
man=json.loads((p/'MANIFEST_SHA256.json').read_text())
for name,sha in man.items():assert h(p/name)==sha,(name,sha)
for name,sha in json.loads((p/'INPUT_SHA256.json').read_text()).items():assert h(p.parent/name)==sha
assert h(p.parent/'bilayer_brauer_rule_review/MANIFEST_SHA256.json')=='2433ba51a63cba8ade95874f3244dea39a7f1acf0bcfe1a327bfb34c1789cfdb'
witness=[int(v) for v in (p/'witness57.txt').read_text().split()];assert len(witness)==57 and witness[0]==2**48
ref=p.parent/'bilayer_symmetry_intermediate_points/fixed011_moment_reference.json';reference=json.loads(ref.read_text());matched=[x for x in reference['moments'] if x['N']==32];assert len(matched)==1 and matched[0]['coefficients']==witness
fullinput=json.loads((p.parent/'bilayer_complete_residual_direction_58d_review/FULL_INPUT_SHA256.json').read_text())
assert h(p/'geometry_8x4.txt')==fullinput['../bilayer_complete_residual_8x4/geometry_8x4.txt']
assert h(p/'reference_coefficients.txt')==fullinput['../bilayer_residual_direction_outer_gate/reference_coefficients.txt']
rows=[];results=[]
for i in range(8):
 d=p/'runs'/('sample_offset0_fixed' if i==0 else f'sample_offset{i}')
 cold=json.loads((d/'cold_result.json').read_text());warm=json.loads((d/'result.json').read_text());assert cold['terms']==warm['terms'] and cold['moments']==warm['moments']
 assert not cold['moments_are_full_physical_fixture_only'] and cold['complete'] and warm['complete']
 assert json.loads((d/'q2_roundtrip.json').read_text())=={'ranks':496,'unique_pairs':496,'roundtrip':True}
 rows += [json.loads(x) for x in (d/'targets.jsonl').read_text().splitlines()];results.append((cold,warm))
checks={}
for phase in ['cold','warm']:
 checks[phase]={}
 for q,N,k in [(6,169911,512),(4,4495,128)]:
  rr=[x for x in rows if x['phase']==phase and x['q']==q];assert sorted(x['sample'] for x in rr)==list(range(k));checks[phase][f'q{q}_sum_cpu']=sum(x['seconds'] for x in rr);checks[phase][f'q{q}_projection_cpu']=N*checks[phase][f'q{q}_sum_cpu']/k
 checked={}
 for q,k,total in [(6,512,169911),(4,128,4495)]:
  def decode(rank,q):
   out=[0]*q;top=30
   for j in range(q-1,0,-1):
    while math.comb(top,j)>rank:top-=1
    out[j]=top+1;rank-=math.comb(top,j);top-=1
   return out
  supports=[decode(i*(total-1)//(k-1),q) for i in range(k)];assert len({tuple(x) for x in supports})==k
  assert all(len(set(x))==q and x==sorted(x) and x[0]==0 and x[-1]<32 for x in supports);checked[q]=k
checks['support_index_checks']=checked
summary=json.loads((p/'SUMMARY.json').read_text())
for phase in ['cold','warm']:
 for q in [4,6]:assert abs(summary['phases'][phase][f'q{q}']['projection_cpu']-checks[phase][f'q{q}_projection_cpu'])<1e-7
checks['producer_manifest_files']=len(man);checks['fixed_57_witness_matches_accepted_source']=True;checks['reference_source_sha256']=h(ref)
checks['producer_all_sample_scalars_repeat']=True
runs=[json.loads(x) for x in (r/'fixtures/independent.jsonl').read_text().splitlines()];assert len(runs)==6
for x in runs:
 expected=json.loads((p/f"runs/checked_{x['type']}_{x['nx']}x2/result.json").read_text());assert x['moments']==expected['moments']
checks['independent_dense_fixtures']=6
sample=json.loads((r/'sample/checkpoint.json').read_text());old=json.loads((p/'runs/sample_offset0/checkpoint.json').read_text());assert sample['terms']==old['terms'] and sample['moments']==old['moments'];ownrows=[json.loads(x) for x in (r/'sample/targets.jsonl').read_text().splitlines()];assert sum(x['q']==6 for x in ownrows)==64 and sum(x['q']==4 for x in ownrows)==16;assert json.loads((r/'sample/ABORT.json').read_text())['reason']=='CPU_CHECKPOINT_CAP';checks['replayed_8x4_checkpoint_exact_q6_targets']=64;checks['replayed_8x4_q4_steps_completed_without_final_scalar_checkpoint']=16;checks['independent_8x4_repeated_phase']='NOT_REACHED_budget_stop_no_retry'
obs=json.loads((r/'observer_selftest/resources.json').read_text());assert obs['max_observed_processes']==2 and obs['stop_reason']=='unexpected_runtime_descendant' and obs['live_group_after_cleanup']==[] and len(obs['orphan_wait4'])==1
for op,b in json.loads((r/'fixtures/operator_bounds.json').read_text()).items():assert b['coefficient_max']<=64 and b['records']<2**15
assert 2**15*32*15*64*3**6<2**40
checks['checked_intermediate_amplification_lt_2power40']=True
checks['source_snapshot_sha256']={str(x.relative_to(r/'source')):h(x) for x in (r/'source').rglob('*') if x.is_file()}
(r/'CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
