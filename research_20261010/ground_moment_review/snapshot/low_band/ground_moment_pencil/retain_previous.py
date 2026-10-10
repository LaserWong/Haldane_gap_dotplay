"""Stronger inputs retain old certificates even if early stopping changes."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BAND=HERE.parent
rows=[]
for g in map(F,('3/100','1/25','1/20','3/50','7/100')):
    oldpath=(BAND/'tail_comparison'/'quadratic'/f'recombined_g{g}.json'.replace('/','d')) if g<F(7,100) else (BAND/'frontier_g007_g010'/f'g{g}'.replace('/','d')/'frontier_results.json')
    newpath=HERE/f'scalar_g{g}.json'.replace('/','d')
    olds=json.loads(oldpath.read_text())['results'];news=json.loads(newpath.read_text())['results']
    for old in olds:
        if not old.get('accepted'):continue
        new=next(row for row in news if row['order_before_transport']==old['order_before_transport'])
        candidates=[new]+new.get('additional_baseline_beta_replays',[])
        same=next(row for row in candidates if F(row['beta_initial'])==F(old['beta_initial']))
        diffs=[F(a)-F(b) for a,b in zip(same['canonical_first_purities'],old['canonical_first_purities'])]
        assert len(diffs)==3 and min(diffs)>=0
        rows.append(dict(g=str(g),order=old['order_before_transport'],beta=old['beta_initial'],
          new_minus_previous_canonical_purity=list(map(str,diffs)),
          previous_all_integer_gap_retained=old['all_integer_L_ge2_gap'],
          previous_certificate_source=str(oldpath.relative_to(BAND.parent)),previous_certificate_sha256=hashlib.sha256(oldpath.read_bytes()).hexdigest(),
          new_scalar_source=newpath.name,new_scalar_sha256=hashlib.sha256(newpath.read_bytes()).hexdigest()))
(HERE/'previous_certificate_dominance.json').write_text(json.dumps(dict(status='exact_dominance_checks_passed',rows=rows,
 proof='At identical geometry and beta, every new canonical lower purity is at least the old one. Weakening to the old rational first purities exactly recovers its existing recurrence and all-size certificate; new sharper inputs cannot invalidate that certificate.'),indent=2))
print('PASS',len(rows),'previous certificates retained by exact initial-purity domination')
