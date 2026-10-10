"""Check every comparison-table datum against its exact sealed source."""
from audit_combination import *
def main():
 verify_inputs();comp=load(C/'comparison.json');rows=[];seals=load(HERE/'PRIOR_REVIEW_SHA256.json')
 for item in comp['results']:
  g=item['g'];vals={}
  for variant,v in item['variants'].items():
   p=S/v['source'];assert sha(p)==v['sha256'];source=load(p)
   if variant in ['original','pencil_only']:
    review='ground_moment_review' if variant=='pencil_only' else 'tail_comparison_review' if F(g)<=F(3,50) else 'bilayer_frontier_review'
    assert sha(p) in seals[review]['files'].values()
   candidates=source.get('results',[])
   if not candidates:
    print('SOURCE SHAPE',str(p),list(source));raise AssertionError('Unrecognized source shape')
   row=next(z for z in candidates if z.get('order_before_transport',z.get('order'))=='txy')
   assert row['accepted']==v['accepted']
   assert row['beta_initial']==v['beta_initial']
   if v['accepted']:assert row['all_integer_L_ge2_gap']==v['all_integer_L_ge2_gap']
   vals[variant]=v
  rows.append(dict(g=g,variants=vals))
 save('comparison_review.json',dict(status='PASS exact sources and accepted values checked',comparison='Individually selected temperatures, not fixed-beta causal attribution',results=rows))
 print('ALL COMPARISON SOURCES PASS')
if __name__=='__main__':main()
