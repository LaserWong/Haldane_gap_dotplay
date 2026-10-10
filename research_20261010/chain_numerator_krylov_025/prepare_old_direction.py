from probe import *
with (HERE/'packed_input.txt').open() as f:header=[next(f) for _ in range(82)]
with (HERE/'packed_old_direction.txt').open('w') as f:
 f.writelines(header)
 for key,x in zip(keys,vectors[0]):f.write(f'{key} {int(x)}\n')
print('Prepared independent old direction',len(keys))
