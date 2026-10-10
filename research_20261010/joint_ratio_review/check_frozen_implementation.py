"""Compare the sealed producer scalar helper with independent formulas."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib,shutil,random,importlib.util
from fractions import Fraction as Q
from verify_lemma import G,root,I,I2,lower,HERE,ROOT
PRODUCER=ROOT/'research_20261010/low_band/joint_trace_bootstrap'
MANIFEST=PRODUCER/'FROZEN_MANIFEST_1918.json'
assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest()=='905a55c3419a08082c05f8fe011116e2655035c23cb9040e4e92ad856ce4e9bc'
sealed=json.loads(MANIFEST.read_text())
snap=HERE/'lemma_snapshot';snap.mkdir(exist_ok=True)
for name,digest in sealed['files'].items():
    p=PRODUCER/name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,(name,'hash drift')
    q=snap/name
    if q.exists():assert q.read_bytes()==p.read_bytes()
    else:shutil.copy2(p,q)
shutil.copy2(MANIFEST,HERE/'PRODUCER_LEMMA_MANIFEST.json')
spec=importlib.util.spec_from_file_location('sealed_joint_scalar',PRODUCER/'joint_scalar.py')
P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)

def advance_expected(abc,K):
    a,b,c=abc;args=[];values=[]
    z=max(a**4*b*b*c,K);args.append(z);d=lower(G(z),10**80);values.append(d)
    if d<=0:return None,args
    z=max(b**4*c*c,K*K)*d;args.append(z);e=lower(G(z),10**80);values.append(e)
    if e<=0:return None,args
    z=max(c,K)**4*d*d*e;args.append(z);f=lower(G(z),10**80);values.append(f)
    return (values if f>0 else None),args

rng=random.Random(982342);cases=0;positive=0
for i in range(400):
    lo=9800 if i<250 else 1
    abc=tuple(Q(rng.randint(lo,10000),10000) for _ in range(3))
    # A valid supplied constraint may be stronger or weaker than component product.
    K=Q(rng.randint(lo,10000),10000)
    actual,args=P.canonical_advance(abc,K)
    expected,refargs=advance_expected(abc,K)
    assert actual==expected and args==refargs
    ss=Q(rng.randint(lo,10000),10000);tt=Q(rng.randint(lo,10000),10000)
    got,detail=P.interpolate_1d_joint(ss,tt,K)
    assert 0<=got<=I(ss,tt,K)
    got2,detail2=P.interpolate_2d_joint(*abc,K)
    assert 0<=got2<=I2(*abc,K)
    if got2>0:positive+=1
    cases+=1
out=dict(status='PASS sealed general lemma and exact scalar implementation',
    producer_manifest_sha256=hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
    frozen_files_verified=len(sealed['files']),implementation_cases=cases,
    positive_2d_window_cases=positive,source_contract='Every input is a valid lower bound at the same reflected even base; all purity bounds lie in (0,1], joint lies in [0,1].',
    independent_code_imports_producer_math=False,
    comparison_harness_imports_sealed_producer_only_to_compare_outputs=True)
(HERE/'results/frozen_implementation_review.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
