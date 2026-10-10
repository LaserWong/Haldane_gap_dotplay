import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'symmetry'))
import symmetric_ground as S
S.OUT=HERE/'symmetry'
for g in ['1/25','1/20']:
    for nx,ny in [(2,2),(4,2),(4,4)]:
        target=S.OUT/f'symmetry_{nx}x{ny}_g{g}_block1.json'.replace('/','d')
        if not target.exists():S.run(nx,ny,g,1)
