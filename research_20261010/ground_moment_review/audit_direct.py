"""Fast standalone exact acceptance of all 21 polynomial witnesses."""
from audit_ground import *
check_hashes();rows=[]
for g in map(F,['3/100','1/25','1/20','3/50','7/100','2/25','1/10']):
 for nx,ny in [(4,4),(8,4),(8,8)]:
  p=COMP/f'ground_{nx}x{ny}_g{g}.json'.replace('/','d');r=one(p,False);rows.append(r)
  print('PASS direct exact polynomial witness',g,r['shape'],flush=True)
(OUT/'direct_witness_review.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PASS ALL 21 direct witnesses, normalization and external counts',flush=True)
