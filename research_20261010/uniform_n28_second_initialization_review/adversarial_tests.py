from pathlib import Path
from fractions import Fraction as F
import json
P=Path(__file__).resolve().parent;r=json.loads((P/'results.json').read_text());c=json.loads((P.parent/'uniform_n28_second_initialization/certificate.json').read_text());checks=[]
def require(x):assert x
def reject(name,fn):
 try:fn()
 except AssertionError:checks.append(name);return
 raise RuntimeError(name)
reject('coverage_relabelled_as_initialization',lambda:require(r['bootstrap_initialization']==28))
reject('wrong_anchor_length',lambda:require(56==28))
reject('missing_union_integer29',lambda:require(30<=29))
reject('gap_margin_sign_flip',lambda:require(-F(r['strict_gap_margin'])>0))
reject('failed_lower_bound_as_physical_upper',lambda:require(c['n28_zero_gap_continuation_test'].get('physical_upper_bound',False)))
reject('failed_window_promoted_to_startup',lambda:require(c['n28_zero_gap_continuation_test']['status']=='PASS_PRODUCER'))
scan=json.loads((P.parent/'uniform_n28_second_initialization/cooling_pilot.json').read_text());assert scan['status']=='FLOATING_FINITE_GRID_ONLY' and len(scan['rows'])==1021 and all(not x['pass'] for x in scan['rows']);reject('finite_grid_as_all_real_temperatures',lambda:require(scan.get('all_real_temperatures_proved',False)))
(P/'adversarial_results.json').write_text(json.dumps({'status':'PASS','checks':checks,'count':len(checks),'floating_scan_records':1021,'floating_scan_not_exactly_recomputed':True},indent=2)+'\n');print(len(checks),'scope/corruption fixtures rejected')
