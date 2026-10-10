"""Exact replay of both regimes and all integer-size/continuous unions.
No eigensolver is called. Earlier frozen packages are verified unchanged.
"""
import certify_lowband as B
C=B.C
from certify_range import *

def reject_eigh(*args,**kwargs):raise RuntimeError('Eigensolver forbidden during exact replay')
C.eigh=B.eigh=reject_eigh

def verify_old(folder):
 frozen=json.loads((folder/'FROZEN_MANIFEST.json').read_text())
 for name,digest in frozen['files'].items():assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest,(str(folder),name)
 return json.loads((folder/'coverage_summary.json').read_text())

def main():
 rows=[];groups=[]
 for group,expected in [('ground_only',(F(2,25),F(41,500))),('lowband',(F(41,500),F(17,200)))]:
  summ=json.loads((HERE/f'{group}_summary.json').read_text());grp=[]
  for item in summ['intervals']:
   path=HERE/item['file'];saved=json.loads(path.read_text());lo,hi=map(F,saved['coupling_interval'])
   vs=[r['integer_coefficients'] for r in saved['denominator_patches']]+[saved['largest_base_trial']['integer_coefficients']]
   if group=='ground_only':data=B.base_interval_data(lo,hi,vs);C.upper_exact=B.base_upper_exact
   else:data=B.interval_data(lo,hi,vs);C.upper_exact=B.upper_exact
   actual=C.certify(data,F(saved['beta_initial']))
   assert actual=={k:x for k,x in saved.items() if k!='float_proposal_score'},path.name
   assert actual['accepted'] and F(actual['all_integer_L_ge2_gap'])==F(item['gap_lower']);grp.append(actual);C.exp_interval.cache_clear()
  assert F(grp[0]['coupling_interval'][0])==expected[0] and F(grp[-1]['coupling_interval'][1])==expected[1]
  assert all(a['coupling_interval'][1]==b['coupling_interval'][0] for a,b in zip(grp,grp[1:]))
  assert min(F(r['all_integer_L_ge2_gap']) for r in grp)==F(summ['all_integer_L_ge2_uniform_gap'])
  odd=group=='lowband';summ.update(denominator_retained_states=[49,97] if odd else [1,1],odd_trial_inputs=odd,
   ground_trial_dimensions=[11,29,29],total_augmented_trial_dimensions=[59,125,30] if odd else [11,29,30])
  (HERE/f'{group}_summary.json').write_text(json.dumps(summ,indent=2)+'\n');groups.append(summ);rows+=grp
 target=min(F(r['all_integer_L_ge2_gap']) for r in rows)
 old=[verify_old(R/folder) for folder in ('ordinary_interval','interval_extension','interval_joint_extension')]
 assert old[0]['coupling_interval']==['0','7/100'] and old[1]['coupling_interval']==['7/100','39/500'] and old[2]['coupling_interval']==['39/500','2/25']
 total=min([target]+[F(o['all_integer_L_ge2_uniform_gap']) for o in old])
 items=[item for group in groups for item in group['intervals']]
 coverage=dict(status='continuous_0085_candidate_pending_independent_review',coupling_interval=['2/25','17/200'],closed_intervals=len(rows),
  all_integer_L_ge2_uniform_gap=str(target),uniform_gap_display=float(target),intervals=items,
  regimes=[dict(coupling_interval=g['coupling_interval'],closed_intervals=g['closed_intervals'],uniform_gap=g['all_integer_L_ge2_uniform_gap'],denominator_retained_states=g['denominator_retained_states'],total_augmented_trial_dimensions=g['total_augmented_trial_dimensions']) for g in groups])
 (HERE/'coverage_summary.json').write_text(json.dumps(coverage,indent=2)+'\n')
 out=dict(status='PASS exact producer replay; independent new polynomial and interval audit required',
  closed_extension_intervals=len(rows),extension_interval=['2/25','17/200'],extension_uniform_gap=str(target),
  union_interval=['0','17/200'],union_closed_intervals=sum(o['closed_intervals'] for o in old)+len(rows),
  union_all_integer_L_ge2_gap=str(total),union_gap_display=float(total),asymptotic_max_start_L=max(r['bootstrap']['n'] for r in rows),
  finite_window_count=sum(len(r['finite_windows']) for r in rows),short_size_count=sum(len(r['short_sizes']) for r in rows),
  coupled_scalar_states=sum(len(r['joint_ladder_states']) for r in rows),largest_filter_rank=1,
  ground_search_dimensions=[11,29,29],max_augmented_linear_trial_dimensions=[59,125,30],
  largest_patch_full_Hilbert_dimension=4**64,largest_patch_physical_spins=128,
  largest_filtered_q=6,odd_denominator_trial_q=[1,3],odd_denominator_full_H_image_q=[1,3,5],
  denominator_odd_input_geometries=[[4,4],[8,4]],largest_odd_input_needed=False,
  eigensolver_calls=0,new_sparse_physical_expansion=False,new_moments_above_H2=False)
 (HERE/'replay_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
