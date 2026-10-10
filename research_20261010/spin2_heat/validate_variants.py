#!/usr/bin/env python3
import json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
 t=time.monotonic();checks=[]
 for n,m in [(3,0),(4,0),(4,-1)]:
  for tw in ['I','P','C']:
   args=[str(n),tw,str(m),'0','9',str(ROOT/'coefficients_chebyshev_Q56.txt'),'dump']
   ref=subprocess.check_output([str(ROOT/'heat_columns_ubsan')]+args,stderr=subprocess.DEVNULL)
   for b in [1,2,4,8]:
    got=subprocess.check_output([str(ROOT/'heat_fast_ubsan')]+args+[str(b)],stderr=subprocess.DEVNULL)
    assert got==ref,(n,m,tw,b)
    checks.append({'L':n,'M':m,'twist':tw,'block_columns':b,'fast_ubsan_bitwise_match':True})
 # Large benchmark first columns must agree across all algorithms implementing
 # the same Chebyshev polynomial; Horner uses a different polynomial, excluded.
 groups={}
 for p in (ROOT/'results').glob('benchmark_*.json'):
  r=json.loads(p.read_text());i=r['identity']
  if i['algorithm']!='chebyshev' or r['exit_code']!=0:continue
  lines=(ROOT/r['stdout']).read_text().splitlines();groups.setdefault((i['L'],i['M'],i['twist']),[]).append((p.name,lines[1]))
 big=[]
 for key,rows in groups.items():
  assert all(v==rows[0][1] for _,v in rows)
  big.append({'L':key[0],'M':key[1],'twist':key[2],'records':len(rows),'first_column_bitwise_identical':True})
 out={'small_checks':checks,'large_first_column_checks':big,'seconds':time.monotonic()-t};(ROOT/'results/variant_validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
