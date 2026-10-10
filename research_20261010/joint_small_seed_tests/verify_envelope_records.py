"""Second exact record implementation; no producer imports and no floats.

This is an arithmetic self-check, not a separate reviewer acceptance.
"""
import json, hashlib, resource, os
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
if hasattr(os,'sched_setaffinity'):
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
U=1<<320


def ceiling(x):
    scaled=x*U
    n,r=divmod(scaled.numerator,scaled.denominator)
    return Q(n+(r!=0),U)


def verify(row, inputs):
    limits=[max(Q(x[i]) for x in inputs) for i in range(3)]
    assert limits==list(map(Q,row['max_input_upper']))
    xs=list(map(Q,row['arguments']));ys=list(map(Q,row['caps']))
    assert len(xs)==len(ys)==row['failed_stage']
    for n,(x,y) in enumerate(zip(xs,ys)):
        assert 0<x<=1
        assert x==(limits[0] if n==0 else limits[1]*ys[0] if n==1 else
                   limits[2]**4*ys[0]**2*ys[1] if n==2 else ys[0]**4*ys[1]**2*ys[2])
        assert y==ceiling((x*x+2*x-1)/(2*x*x))
        assert y>0 if n+1<len(xs) else y<0
    assert Q(row['negative_upper'])==ys[-1]
    if len(xs)==4:
        assert Q(row['first_doubled_base_joint_upper'])==xs[-1]
        assert xs[-1]**2+2*xs[-1]<1


def main():
    path=HERE/'envelope_results.json'
    r=json.loads(path.read_text())
    old=json.loads((HERE.parent/'small_seed_order_exclusions'/'results.json').read_text())
    for name,expected in r['input_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected
    count=0;hist={}
    for tag,data in r['couplings'].items():
        prior=old['results'][tag]
        verify(data['hot'],[[prior['hot']['common_J1_upper'],'1','1']]);count+=1
        verify(data['cold'],[prior['orders'][o]['cold']['input_upper'] for o in ('xyt','xty','txy')]);count+=1
        assert len(data['middle'])==320
        for k,row in enumerate(data['middle']):
            assert list(map(Q,row['beta_interval']))==[4+Q(k,20),4+Q(k+1,20)]
            inputs=[prior['orders'][o]['middle'][k]['input_upper'] for o in ('xyt','xty','txy')]
            assert row['order_input_upper']==inputs
            verify(row,inputs);count+=1
        hh=dict(Counter(str(row['failed_stage']) for row in data['middle']))
        assert hh==data['middle_failed_stage_histogram'];hist[tag]=hh
    out={'status':'PASS second exact arithmetic implementation; separate analytic review still required',
         'records_checked':count,'middle_histograms':hist,
         'envelope_results_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'verification_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'record_verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__=='__main__':main()
