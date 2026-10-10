"""Revalidate frozen interval artifacts from exact fixed integer vectors.
No eigensolver is called. This is producer replay, not independent review.
"""
from certify_intervals import *

def main():
 summary=json.loads((HERE/'coverage_summary.json').read_text());rows=[]
 for item in summary['intervals']:
  path=HERE/item['file'];saved=json.loads(path.read_text());lo,hi=map(F,saved['coupling_interval'])
  v=[r['integer_coefficients'] for r in saved['denominator_patches']]+[saved['largest_first_moment_trial']['integer_coefficients']]
  data=interval_data(lo,hi,v);actual=certify(data,F(saved['beta_initial']))
  assert actual=={k:x for k,x in saved.items() if k!='float_proposal_score'},path.name
  assert actual['accepted'] and F(actual['all_integer_L_ge2_gap'])==F(item['gap_lower'])
  rows.append(actual);exp_interval.cache_clear()
 assert F(rows[0]['coupling_interval'][0])==0 and F(rows[-1]['coupling_interval'][1])==F(7,100)
 assert all(a['coupling_interval'][1]==b['coupling_interval'][0] for a,b in zip(rows,rows[1:]))
 target=min(F(r['all_integer_L_ge2_gap']) for r in rows)
 assert target==F(summary['all_integer_L_ge2_uniform_gap'])
 out=dict(status='PASS producer exact fixed-vector replay; independent review still required',closed_interval_count=len(rows),covered_coupling_interval=['0','7/100'],all_integer_L_ge2_uniform_gap=str(target),zero_coupling_exact_gap='1',eigencalls=0)
 (HERE/'replay_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
