from pathlib import Path
import json
R=Path(__file__).resolve().parent;rd=lambda p:json.loads(p.read_text())
local=rd(R/'local_result.json');accepted=rd(R.parent/'hardcore_pair_commutator/TEST_RESULTS.json')
for f,old in zip(local['fixtures'],accepted['fixtures']):
 assert f['q8_gram']==old['q8_gram'];assert f['coherent_Cdag_norm']==old['coherent_q8_norm'];assert f['coherent_C_norm']==old['coherent_q4_norm'];assert f['coherent_commutator']==old['coherent_commutator']
 shape='x'.join(map(str,f['shape']))
 for mode in ['full','origin']:
  p=R/(f'independent_fixture_{mode}.json' if shape=='4x2' else f'independent_{shape}_{mode}.json');r=rd(p)
  for q in ['4','6']:assert int(r[f'Tpsi_q{q}_norm'])==f['full_image_sector_norms'][q]
  assert int(r['q8_creation_norm'])==f['full_image_sector_norms']['8']
print('All fresh physical/matching fixtures and previous cross-Gram entries agree')
