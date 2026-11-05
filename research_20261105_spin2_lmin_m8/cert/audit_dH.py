"""Check stored entry-approximation norm bounds using both row and column sums.
Does not regenerate spectral certification or alter enc/cache artifacts."""
import json,pickle,sys
from pathlib import Path
import numpy as np
import flint
from flint import arb,acb
import blocks2
from blocks2 import block
D=Path(__file__).resolve().parent
fail=[]; n=0
for fp in sorted((D/'enc').glob('*.json')):
 r=json.loads(fp.read_text())
 if r['mode']!='hp':continue
 sd=pickle.loads((D/'cache'/f"sd_{r['tw']}_L{r['L']}_sz{r['sz']}.pkl").read_bytes())
 flint.ctx.prec=128;blocks2._wc.clear();blocks2.R6=arb(6).sqrt()
 m,ent,Hf,real=block(r['L'],r['q'],sd)
 oldent=ent
 flint.ctx.prec=256;blocks2._wc.clear();blocks2.R6=arb(6).sqrt()
 _,ent,_,_=block(r['L'],r['q'],sd)
 rows=[arb(0) for _ in range(m)];cols=[arb(0) for _ in range(m)]
 sh=arb(2)**-180; scale=arb(2)**180
 for (i,j),v in ent.items():
  hr=int((oldent[(i,j)].real.mid()*scale).floor().unique_fmpz())
  hi=0 if real else int((oldent[(i,j)].imag.mid()*scale).floor().unique_fmpz())
  hs=acb(arb(hr)*sh,arb(hi)*sh)
  e1=arb(abs(v-hs).upper());e2=arb(abs(ent.get((j,i),acb(0)).conjugate()-hs).upper())
  err=arb(e1.min(e2).upper())
  rows[i]+=err;cols[j]+=err
 # arb.max performs an enclosing maximum, unlike selecting a rounded float key.
 mr=arb(0);mc=arb(0)
 for x in rows: mr=arb(mr.max(arb(x.upper())).upper())
 for x in cols: mc=arb(mc.max(arb(x.upper())).upper())
 bound=(mr*mc).sqrt()
 ok=bool(bound <= arb(r['dH_up']))
 if not ok:fail.append([fp.name,str(bound),r['dH_up']])
 n+=1
out={'checked_hp_blocks':n,'all_stored_dH_bounds_dominate_row_column_bound':not fail,'failures':fail}
(D/'audit_dH_result.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
