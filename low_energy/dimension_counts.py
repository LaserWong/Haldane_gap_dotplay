"""Exact combinatorial trial-shell counts; no eigensolver."""
from math import comb
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json

def shell_counts(s,N,qmax):
 s=F(s);local=defaultdict(int)
 for J in range(1,int(2*s)+1):
  for m in range(-J,J+1):local[m]+=1
 coeff={0:1};rows=[];full=0;zero=0
 for q in range(qmax+1):
  if q:
   nxt=defaultdict(int)
   for m,v in coeff.items():
    for n,w in local.items():nxt[m+n]+=v*w
   coeff=nxt
  count_full=comb(N,q)*(int((2*s+1)**2)-1)**q
  count_zero=comb(N,q)*coeff[0]
  full+=count_full;zero+=count_zero
  rows.append(dict(q=q,exact_shell_full=count_full,exact_shell_Sz0=count_zero,up_to_q_full=full,up_to_q_Sz0=zero))
 return rows
if __name__=='__main__':
 out=[]
 for s in [F(1,2),F(1)]:
  for N in [4,8,16,32,64]:out.append(dict(spin=str(s),N_dimers=N,rows=shell_counts(s,N,4)))
 Path(__file__).with_name('dimension_counts.json').write_text(json.dumps(out,indent=2))
 for r in out:
  if r['N_dimers'] in [8,16]:print(r['spin'],r['N_dimers'],[(x['q'],x['up_to_q_Sz0']) for x in r['rows']])
