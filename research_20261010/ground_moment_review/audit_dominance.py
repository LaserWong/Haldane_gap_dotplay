"""Verify stronger first-cycle triples at every prior certificate's same beta."""
from independent_math import *
from verify_inputs import check_hashes
import independent_scalar as I
HERE=Path(__file__).resolve().parent;SRC=HERE/'snapshot';COMP=SRC/'low_band/ground_moment_pencil';OUT=HERE/'results'
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
check_hashes();saved=load(COMP/'previous_certificate_dominance.json');assert len(saved['rows'])==14;out=[]
for row in saved['rows']:
 g=F(row['g']);order=row['order'];beta=F(row['beta']);tag='g'+str(g).replace('/','d')
 oldpath=SRC/row['previous_certificate_source'];newpath=COMP/row['new_scalar_source']
 assert sha(oldpath)==row['previous_certificate_sha256'] and sha(newpath)==row['new_scalar_sha256']
 old=next(r for r in load(oldpath)['results'] if r['order_before_transport']==order and F(r['beta_initial'])==beta);assert old['accepted']
 newrows=load(newpath)['results'];candidates=[]
 for r in newrows:
  if r['order_before_transport']==order:candidates+=[r]+r.get('additional_baseline_beta_replays',[])
 new=next(r for r in candidates if F(r['beta_initial'])==beta)
 recs=[load(COMP/f'temple_{nx}x{ny}_{tag}.json') for nx,ny in [(4,4),(8,4),(8,8)]]
 independent=I.ratios(recs,beta,order);stored=[F(new[k]) for k in ['J1','J2','C0']]
 assert all(0<x<=y<=1 for x,y in zip(stored,independent))
 j1,j2,c0=stored;a=floor(G(j1),10**16);b=floor(G(j2*a),10**16);c=floor(G(c0**4*a*a*b),10**16)
 moved=[a,b,c] if order=='xyt' else [a,b*sqrt_lower(c),b*b*c] if order=='xty' else [a*sqrt_lower(b),a*a*b*sqrt_lower(c),a**4*b*b*c]
 triple=[floor(x,10**18) for x in moved];assert triple==list(map(F,new['canonical_first_purities']))
 dif=[x-F(y) for x,y in zip(triple,old['canonical_first_purities'])]
 assert dif==list(map(F,row['new_minus_previous_canonical_purity'])) and min(dif)>=0
 assert row['previous_all_integer_gap_retained']==old['all_integer_L_ge2_gap']
 out.append(dict(g=str(g),order=order,beta=str(beta),new_minus_old_canonical_purity=list(map(str,dif)),prior_gap_retained=old['all_integer_L_ge2_gap'],first_cycle_dominance_exact=True))
 print('PASS same-beta canonical dominance',g,order,flush=True)
(OUT/'dominance_review.json').write_text(json.dumps(out,indent=2)+'\n')
check_hashes();print('PASS 14 prior certificates retained; no optimization regression inferred',flush=True)
