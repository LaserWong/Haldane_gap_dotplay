from certify_points import *
from replay_intervals import R
out=[]
for p in json.load(open(HERE/'exploration.json'))['results']:
 if not p.get('legal'):continue
 d=p['data'];best=None;counts={'positive_first_cycle':0,'accepted_small_defect':0,'direct_initial_above_half':0}
 for i in range(100,401):
  b=i/20;raw=raw_float(d,b)
  if raw is None:continue
  counts['positive_first_cycle']+=1;can=C.transport(*raw,math.sqrt)
  states,status=R.S.sequence({'permuted_prefix':raw,'canonical':can},b,'txy',False,rounds=12)
  if status=='accepted_small_defect':counts['accepted_small_defect']+=1
  pp=R.direct_exact(*map(F,raw))[0]
  if pp>F(1,2):counts['direct_initial_above_half']+=1
  u=min(s['u'] for s in states);rank=(u,-len(states))
  if best is None or rank<best[0]:best=(rank,{'beta':str(F(i,20)),'minimum_canonical_defect':u,'states':states,'status':status,'initial_direct_purity':float(pp)})
 out.append({'g':p['g'],'counts':counts,'best':best[1] if best else None})
(HERE/'startup_diagnostic.json').write_text(json.dumps({'status':'bounded_float_diagnostic_not_all_temperature_exclusion','grid':'beta5..20 step.05; max12 joint-coupled cycles','results':out},indent=2)+'\n')
for x in out:print(x['g'],x['counts'],x['best']['beta'] if x['best'] else None,x['best']['minimum_canonical_defect'] if x['best'] else None)
