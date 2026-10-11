"""Resource limits and exact provenance helpers for a static research overview."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
if hasattr(os,'sched_getaffinity'):
    os.sched_setaffinity(0,{8 if 8 in os.sched_getaffinity(0) else min(os.sched_getaffinity(0))})
import resource
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
import hashlib,json,csv
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
R='research_20261010/'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def ptr(doc,pointer):
    for p in pointer.strip('/').split('/') if pointer else []:
        p=p.replace('~1','/').replace('~0','~')
        doc=doc[int(p)] if isinstance(doc,list) else doc[p]
    return doc
def floor12(s):
    f=F(s);n=f.numerator*10**12//f.denominator
    return f'{n//10**12}.{n%10**12:012d}'
def csv_write(name,rows):
    with (HERE/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)))
        w.writeheader()
        for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()})
def manifest_check(path):
    path=ROOT/path;d=json.loads(path.read_text())
    assert d and isinstance(d,dict)
    if 'files' in d:
        assert isinstance(d['files'],dict) and (isinstance(d.get('scope'),str) or d.get('status')=='sealed_independent_review_PASS' or str(d.get('status','')).startswith('FROZEN independent'))
        d=d['files']
    for name,h in d.items():
        assert isinstance(h,str) and len(h)==64,(path,name)
        assert sha(path.parent/name)==h,(str(path),name)
    return len(d)
