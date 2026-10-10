from probe import *
with (HERE/'packed_input.txt').open('w') as f:
 f.write(str(den)+' '+str(len(keys))+'\n')
 for a in range(9):
  for b in range(9):
   row=kernel[a,b];f.write(str(len(row))+' '+' '.join(f'{x} {y} {c}' for x,y,c in row)+'\n')
 for key,x in zip(keys,vec):f.write(f'{key} {x}\n')
print('Prepared',len(keys),'exact packed coefficients',flush=True)
