"""Build exact Q(omega) matrix entries for the spin-2 four-site ring.
Nonorthogonal polynomial basis: S+|r>=(4-r)|r+1>, S-|r>=r|r-1>.
2H has integer entries for twists I,P and Q(omega)-integer entries for C.
"""
from pathlib import Path
import numpy as np
from spectra import sector_ids
ROOT=Path(__file__).resolve().parent
n=4;q=36
for tw in ('I','P','C'):
 with (ROOT/f'thermal4_{tw}.txt').open('w') as f:
  f.write('9\n')
  for m in range(9):
   ids=sector_ids(n,m);d=len(ids);pos={int(x):u for u,x in enumerate(ids)};pw=5**np.arange(n)
   rows=[{} for _ in range(d)]
   def add(i,j,a,b=0):
    old=rows[i].get(j,(0,0));rows[i][j]=(old[0]+int(a),old[1]+int(b))
   for col,x in enumerate(ids):
    r=(x//pw)%5;z=r-2;diag=int((z*np.roll(z,-1)).sum());add(col,col,q-10*n-2*diag)
    for j in range(n):
     k=(j+1)%n
     for ds in (-1,1):
      if not(0<=r[j]+ds<=4 and 0<=r[k]-ds<=4):continue
      row=pos[int(x+ds*pw[j]-ds*pw[k])]
      c=int((4-r[j])*r[k] if ds==1 else r[j]*(4-r[k]))
      if k!=0 or tw=='I':add(row,col,-c)
      elif tw=='P':add(row,col,c)
      elif ds==1:add(row,col,0,-c)
      else:add(row,col,c,c)
   entries=[(i,j,a,b) for i,row in enumerate(rows) for j,(a,b) in row.items() if a or b]
   f.write(f'{d} {1 if m==0 else 2} {len(entries)}\n')
   for i,j,a,b in entries:f.write(f'{i} {j} {a} {b}\n')
print('Built all physical magnetization blocks and all three twists.')
