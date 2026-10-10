"""New all-beta upper envelope for the specified mixed joint-cube recursion.

Consumes accepted rational quotient UPPER enclosures as data. It does not
inherit the old fixed-order recurrence exclusion as an assertion.
"""
import os, sys, json, hashlib, resource, time
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
sys.dont_write_bytecode=True
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
if hasattr(os,'sched_setaffinity'):
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OLD=HERE.parent/'small_seed_order_exclusions'
UNIT=2**320
HASHES={}


def read(path):
    HASHES[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    return json.loads(path.read_text())


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serial(v) for v in x]
    return x


def up(x):
    x=F(x)
    return F(-((-x.numerator*UNIT)//x.denominator),UNIT)


def G(z):
    assert 0<z<=1
    return 1-(1-z)**2/(2*z*z)


def envelope(inputs):
    j=max(row[0] for row in inputs)
    q=max(row[1] for row in inputs)
    c=max(row[2] for row in inputs)
    assert all(0<x<=1 for x in (j,q,c))
    out={'max_input_upper':[j,q,c],'caps':[],'arguments':[]}
    for stage in range(1,5):
        if stage==1:z=j
        elif stage==2:z=q*out['caps'][0]
        elif stage==3:z=c**4*out['caps'][0]**2*out['caps'][1]
        else:z=out['caps'][0]**4*out['caps'][1]**2*out['caps'][2]
        out['arguments'].append(z)
        cap=up(G(z));out['caps'].append(cap)
        if cap<=0:
            assert cap<0
            out.update(failed_stage=stage,negative_upper=cap)
            if stage==4:
                # Equivalent exact threshold test, without an irrational constant.
                assert z*z+2*z-1<0
                out['first_doubled_base_joint_upper']=z
            return out
    raise AssertionError(('UNEXCLUDED',list(map(float,(j,q,c)))))


def main():
    start=time.monotonic()
    old=read(OLD/'results.json')
    freeze=read(OLD/'PRODUCER_FREEZE_SHA256.json')
    review=read(OLD/'independent_review'/'ACCEPTANCE.json')
    manifest=read(OLD/'independent_review'/'INPUT_SHA256.json')
    assert str(review['status']).startswith('PASS')
    assert HASHES[str((OLD/'independent_review'/'INPUT_SHA256.json').relative_to(ROOT))]==review['input_manifest_sha256']
    assert freeze==review['reviewed_producer_sha256']
    for name,expected in freeze.items():
        assert hashlib.sha256((OLD/name).read_bytes()).hexdigest()==expected
    # Confirm every previously accepted dependency still has its saved bytes.
    # The manifest uses repository-relative path keys.
    for name,expected in manifest.items():
        if not isinstance(expected,str) or len(expected)!=64:continue
        path=ROOT/name
        if not path.is_file():raise AssertionError(('MISSING_DEPENDENCY',name))
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual==expected,('CHANGED_DEPENDENCY',name)
        HASHES[name]=actual
    key=str((OLD/'results.json').relative_to(ROOT))
    assert key in manifest and HASHES[key]==manifest[key]
    for path in (HERE/'certify_envelope.py',HERE/'PROOF.md',
                 HERE.parent/'joint_ratio_review'/'GENERAL_LEMMA.md'):
        HASHES[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    out={'status':'CANDIDATE all-beta mixed-joint upper envelope; separate analytic review required',
         'scope':'synchronous complete-cube purification, all six initial orders, all partial outputs, arbitrary same-base square/full-product closure, no fresh external trace or inequality injection',
         'couplings':{},'limits':{'cpu':1,'address_space_bytes':1024**3},'new_physical_supports':False}
    for g,t in old['results'].items():
        hot=envelope([[F(t['hot']['common_J1_upper']),F(1),F(1)]])
        assert hot['failed_stage']==1
        middle=[]
        for k in range(320):
            rows=[t['orders'][o]['middle'][k] for o in ('xyt','xty','txy')]
            interval=[4+F(k,20),4+F(k+1,20)]
            assert all(list(map(F,row['beta_interval']))==interval for row in rows)
            inp=[list(map(F,row['input_upper'])) for row in rows]
            middle.append({'beta_interval':interval,'order_input_upper':inp,**envelope(inp)})
        cold=envelope([list(map(F,t['orders'][o]['cold']['input_upper'])) for o in ('xyt','xty','txy')])
        out['couplings'][g]={'g':t['g'],'beta_cover':[[0,4],[4,20],[20,'infinity']],
             'hot':hot,'middle':middle,'cold':cold,
             'middle_failed_stage_histogram':dict(Counter(str(r['failed_stage']) for r in middle)),
             'closest_negative_upper':max(r['negative_upper'] for r in middle)}
        print(g,out['couplings'][g]['middle_failed_stage_histogram'],
              float(out['couplings'][g]['closest_negative_upper']),flush=True)
    out.update(input_sha256=HASHES,seconds=time.monotonic()-start,
               peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (HERE/'envelope_results.json').write_text(json.dumps(serial(out),indent=2)+'\n')
    print('CANDIDATE ENVELOPE COMPLETE',out['seconds'],out['peak_rss_kib'],flush=True)


if __name__=='__main__':main()
