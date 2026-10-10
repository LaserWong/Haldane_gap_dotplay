import os,sys,json,tempfile,shutil,subprocess
from pathlib import Path
p=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='pair_block_replay_',dir=p.parent) as temp:
 q=Path(temp)
 for f in ['block.py','verify.py']:shutil.copy2(p/f,q/f)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
 for level in [1,2]:
  subprocess.run(['taskset','-c','3',sys.executable,str(q/'block.py'),str(level)],env=env,check=True,capture_output=True,text=True)
  a=json.loads((p/f'block_{level}.json').read_text());b=json.loads((q/f'block_{level}.json').read_text())
  for x in ['cpu_seconds','peak_rss_kib']:a.pop(x);b.pop(x)
  assert a==b
 subprocess.run(['taskset','-c','3',sys.executable,str(q/'verify.py')],env=env,check=True,capture_output=True,text=True)
 print(json.dumps(dict(status='PASS',scope='Clean sibling reconstruction and exact verification of rank13 and rank17; mathematical fields identical'),indent=2))
