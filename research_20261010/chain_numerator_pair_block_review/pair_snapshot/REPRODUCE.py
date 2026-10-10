import os,sys,json,tempfile,shutil,subprocess
from pathlib import Path
p=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='pair_replay_',dir=p.parent) as temp:
 q=Path(temp)
 for f in ['build_pair_extension.py','verify.py']:shutil.copy2(p/f,q/f)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
 for f in ['build_pair_extension.py','verify.py']:subprocess.run(['taskset','-c','3',sys.executable,str(q/f)],env=env,check=True,capture_output=True,text=True)
 a=json.loads((p/'pair_extension.json').read_text());b=json.loads((q/'pair_extension.json').read_text())
 for x in ['cpu_seconds','peak_rss_kib']:a.pop(x);b.pop(x)
 assert a==b
 print(json.dumps(dict(status='PASS',scope='Clean sibling construction and exact verification; all mathematical fields identical'),indent=2))
