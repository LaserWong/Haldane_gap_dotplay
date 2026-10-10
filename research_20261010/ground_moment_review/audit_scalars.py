"""Independent replay of all accepted scalar endpoints and selected failures.
Uses a sealed prior independent arithmetic implementation, never producer code.
"""
from independent_math import *
from verify_inputs import check_hashes
import independent_scalar as I
import time
HERE=Path(__file__).resolve().parent;SRC=HERE/'snapshot';COMP=SRC/'low_band/ground_moment_pencil';OUT=HERE/'results'
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def small_sizes():
 rows=[]
 for side in range(2,8):
  rec=load(SRC/f'low_band/frontier_g006/small_sizes/number_bins_{side}x{side}_g3d50.json')
  a=I.number_bins(rec,'original')[0][1];assert a>0 and F(rec['g'])==F(3,50)
  rows.append(dict(side=side,gap=str(a),valid_coupling_interval=['0','3/50'],comparison_form_uniformity=True))
 bridges=load(SRC/'low_band/frontier_g006/all_size_bridges.json')
 for row in bridges:
  assert [(x['side'],F(x['gap_lower'])) for x in row['small_sizes']]==[(x['side'],F(x['gap'])) for x in rows]
 (OUT/'small_size_006_review.json').write_text(json.dumps(rows,indent=2)+'\n')
 return min(F(x['gap']) for x in rows)

def main():
 start=time.monotonic();check_hashes();I.symbolic_paths();short06=small_sizes();short10=I.short_sizes()
 accepted=[];failed=[];extra=[];comparisons=[];summaries=load(COMP/'scalar_summary.json');assert len(summaries)==7
 for summary,g in zip(summaries,map(F,['3/100','1/25','1/20','3/50','7/100','2/25','1/10'])):
  short=short06 if g<=F(3,50) else short10;tag='g'+str(g).replace('/','d')
  assert summary==load(COMP/f'scalar_{tag}.json') and F(summary['g'])==g
  for p,h in summary['source_sha256'].items():assert sha(SRC/p)==h,p
  recs=[load(COMP/f'temple_{nx}x{ny}_{tag}.json') for nx,ny in [(4,4),(8,4),(8,8)]]
  baselinepath=next(p for p in summary['source_sha256'] if Path(p).name.startswith(('recombined_','frontier_results')))
  baseline=load(SRC/baselinepath)['results']
  assert [r['order_before_transport'] for r in summary['results']]==['xyt','xty','txy']
  for row in summary['results']:
   if row['accepted']:
    result=I.audit_seed(recs,row,'quadratic_ground_moment',g,short);accepted.append(result)
    prev=[r for r in baseline if r.get('accepted') and r['order_before_transport']==row['order_before_transport']]
    if prev:
     old=max(F(r['all_integer_L_ge2_gap']) for r in prev)
     comparisons.append(dict(g=str(g),order=result['order'],old_gap=str(old),new_gap=result['all_integer_L_ge2_gap'],gain=str(F(result['all_integer_L_ge2_gap'])-old),new_beta=result['beta_initial'],old_betas=[r['beta_initial'] for r in prev]))
    print('PASS exact all-size',g,result['order'],result['gap_display'],flush=True)
   else:
    failed.append(I.audit_failure(recs,row,g));print('PASS selected failed sufficient bound',g,row['order_before_transport'],flush=True)
   for alternate in row.get('additional_baseline_beta_replays',[]):
    if alternate['accepted']:
     r=I.audit_seed(recs,alternate,'quadratic_ground_moment_baseline_beta',g,short);extra.append(r)
     assert F(row['all_integer_L_ge2_gap'])>=F(alternate['all_integer_L_ge2_gap'])
    else:extra.append(I.audit_failure(recs,alternate,g))
   (OUT/'accepted_certificates.json').write_text(json.dumps(accepted,indent=2)+'\n')
   (OUT/'selected_failures.json').write_text(json.dumps(failed,indent=2)+'\n')
   (OUT/'baseline_beta_replays.json').write_text(json.dumps(extra,indent=2)+'\n')
 (OUT/'old_new_comparison.json').write_text(json.dumps(comparisons,indent=2)+'\n')
 assert len(accepted)==14 and len(failed)==7
 check_hashes();out=dict(status='PASS independent scalar and all-integer-size audit',accepted_certificates=len(accepted),selected_failures=len(failed),additional_baseline_beta_replays=len(extra),all_beta_exclusion=False,
  best=[max((r for r in accepted if r['g']==str(g)),key=lambda r:F(r['all_integer_L_ge2_gap'])) for g in map(F,['3/100','1/25','1/20','3/50','7/100'])],seconds=time.monotonic()-start,maximum_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (OUT/'scalar_summary.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS ALL SCALAR REPLAYS',time.monotonic()-start,flush=True)
if __name__=='__main__':main()
