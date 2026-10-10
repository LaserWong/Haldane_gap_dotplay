"""Exact interval/joint scalar replay with the two earlier freezes unchanged."""
from certify_joint_extension import *

def verify_old(folder):
 frozen=json.loads((folder/'FROZEN_MANIFEST.json').read_text())
 for name,digest in frozen['files'].items():assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest,(str(folder),name)
 return json.loads((folder/'coverage_summary.json').read_text())

def main():
 summary=json.loads((HERE/'coverage_summary.json').read_text());rows=[]
 for item in summary['intervals']:
  path=HERE/item['file'];saved=json.loads(path.read_text());lo,hi=map(F,saved['coupling_interval'])
  vs=[r['integer_coefficients'] for r in saved['denominator_patches']]+[saved['largest_base_trial']['integer_coefficients']]
  actual=certify(interval_data(lo,hi,vs),F(saved['beta_initial']))
  assert actual=={k:x for k,x in saved.items() if k!='float_proposal_score'},path.name
  assert actual['accepted'] and F(actual['all_integer_L_ge2_gap'])==F(item['gap_lower']);rows.append(actual);exp_interval.cache_clear()
 assert F(rows[0]['coupling_interval'][0])==F(39,500) and F(rows[-1]['coupling_interval'][1])==F(2,25)
 assert all(a['coupling_interval'][1]==b['coupling_interval'][0] for a,b in zip(rows,rows[1:]))
 target=min(F(r['all_integer_L_ge2_gap']) for r in rows);assert target==F(summary['all_integer_L_ge2_uniform_gap'])
 old=verify_old(R/'ordinary_interval');middle=verify_old(R/'interval_extension')
 assert old['coupling_interval']==['0','7/100'] and middle['coupling_interval']==['7/100','39/500']
 total=min(target,F(old['all_integer_L_ge2_uniform_gap']),F(middle['all_integer_L_ge2_uniform_gap']))
 out=dict(status='PASS exact producer replay; independent joint lemma and interval review required',closed_extension_intervals=len(rows),extension_interval=['39/500','2/25'],extension_uniform_gap=str(target),union_interval=['0','2/25'],union_closed_intervals=old['closed_intervals']+middle['closed_intervals']+len(rows),union_all_integer_L_ge2_gap=str(total),union_gap_display=float(total),asymptotic_max_start_L=max(r['bootstrap']['n'] for r in rows),finite_window_count=sum(len(r['finite_windows']) for r in rows),short_size_count=sum(len(r['short_sizes']) for r in rows),coupled_scalar_states=sum(len(r['joint_ladder_states']) for r in rows),largest_filter_rank=1,largest_augmented_dimension_upper=30,maximum_q=6,odd_trial_inputs=False,eigensolver_calls=0)
 (HERE/'replay_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
