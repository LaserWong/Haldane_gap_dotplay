"""Independent all-beta obstruction for the specified canonical x-y-T recursion.
Uses separately reviewed 256-bit/70-term rational exponential enclosure, not the
producer 160-bit/40-term implementation. No producer module is imported.
"""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
import sys,resource
sys.dont_write_bytecode=True
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib,time
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.path.insert(0,str(OUT.parent/'low_band_review'))
from fast_exp import exp_interval,up
HASHES={}
def read(path):
    data=path.read_bytes();HASHES[str(path.relative_to(ROOT))]=hashlib.sha256(data).hexdigest();return json.loads(data)
def serialize(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:serialize(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serialize(v) for v in x]
    return x

def energy_lists(rec):
    base=F(rec['blocks'][0]['eigen_upper'][0]);upper=[];lower=[];tail=[]
    for block in rec['blocks']:
        k=block['k'];mult=block['multiplicity']
        assert len(block['eigen_lower'])==len(block['eigen_upper'])==k
        for lo,hi in zip(block['eigen_lower'],block['eigen_upper']):
            assert F(lo)<=F(hi)
            lower.append((F(lo)-base,mult));upper.append((F(hi)-base,mult))
    assert all(x>=0 for x,m in upper)
    assert sum(m for x,m in lower)==rec['retained_full_band_dimension']==1+3*rec['N']
    bins=rec['number_sector_bins']['bins'];assert bins[2]['first_ordered_index']==2+3*rec['N']
    for row in bins[2:]:tail.append((F(row['lower'])-base,row['multiplicity']))
    assert sum(m for x,m in lower+tail)==rec['full_hilbert_dimension']
    return dict(E=F(rec['energy_shift'])+base,lower=lower+tail,upper=upper,ground_width=base-F(rec['blocks'][0]['eigen_lower'][0]))

def sum_bounds(terms,blo,bhi,upper):
    # Bound each signed shifted-energy exponential separately over beta interval.
    result=F(0)
    for energy,m in terms:
        endpoint=(blo if energy>=0 else bhi) if upper else (bhi if energy>=0 else blo)
        result+=m*exp_interval(-endpoint*energy)[int(upper)]
    return result

def quotient_upper(data,blo,bhi):
    low=[sum_bounds(d['upper'],blo,bhi,False) for d in data]
    top=sum_bounds(data[2]['lower'],2*blo,2*bhi,True)
    slopes=[8*data[0]['E']-2*data[2]['E'],8*data[1]['E']-4*data[2]['E']]
    factors=[exp_interval(s*(bhi if s>=0 else blo))[1] for s in slopes]
    vals=[factors[0]*top/low[0]**8,factors[1]*top**2/low[1]**8,top/low[2]**2]
    return [min(F(1),up(v)) for v in vals]

def G(x):
    assert 0<x<=1
    return 1-(1-x)**2/(2*x*x)
def upper_trajectory(v,limit=12):
    j1,j2,c=v;history=[]
    args=[j1]
    for stage in range(limit):
        if stage==0:arg=j1
        elif stage==1:arg=j2*history[0]
        elif stage==2:arg=c**4*history[0]**2*history[1]
        else:arg=history[-3]**4*history[-2]**2*history[-1]
        assert 0<arg<=1
        value=up(G(arg));history.append(value)
        if value<=0:return dict(failed_update=stage+1,nonpositive_upper=value,history=history)
    raise AssertionError('upper iteration stayed positive')

def audit(g,saved):
    data=[]
    for shape in ['2x2','4x2','4x4']:
        data.append(energy_lists(read(OUT.parent/'low_band'/'frontier'/f'bilayer_{shape}_g{g}_symmetric_number_low_band.json')))
    assert saved['hot_range']==[0,'4'] and saved['middle_range']==['4','20'] and saved['cold_range']==['20','infinity']
    # C(beta) is physically monotone nondecreasing for beta>=0.
    hotC=quotient_upper(data,F(4),F(4))[2]
    hotfail=up(G(hotC**4));assert hotfail<0
    assert hotC<=F(saved['thermal_purity_upper'])
    assert hotfail<=F(saved['hot_third_update_upper'])
    rows=saved['intervals'];assert len(rows)==saved['interval_count']==320 and F(saved['step'])==F(1,20)
    checked=[]
    for k,row in enumerate(rows):
        blo=4+F(k,20);bhi=4+F(k+1,20)
        assert list(map(F,row['beta_interval']))==[blo,bhi]
        inp=quotient_upper(data,blo,bhi)
        assert all(a<=F(b) for a,b in zip(inp,row['input_upper']))
        result=upper_trajectory(inp)
        assert result['failed_update']<=row['failed_update']
        # Recheck the producer's coarser inputs directly as a separate exact implication.
        coarse=upper_trajectory(list(map(F,row['input_upper'])))
        assert coarse['failed_update']==row['failed_update']
        assert coarse['nonpositive_upper']<=F(row['nonpositive_upper'])<0
        checked.append(dict(interval=[blo,bhi],input_upper=inp,**result))
        if k%80==79:print('EXACT BOXES PASS',g,k+1,flush=True)
    # Rebase the top trace on the certified physical ground lower endpoint.
    w=data[2]['ground_width'];Elo=data[2]['E']-w
    slopes=[2*Elo-8*data[0]['E'],4*Elo-8*data[1]['E']]
    assert all(s>0 for s in slopes) and slopes==list(map(F,saved['cold_slopes']))
    terms=[(e+w,m) for e,m in data[2]['lower']]
    assert all(e>=0 for e,m in terms)
    U=sum_bounds(terms,F(40),F(40),True)
    cold=[min(F(1),up(exp_interval(-20*slopes[0])[1]*U)),min(F(1),up(exp_interval(-20*slopes[1])[1]*U**2)),F(1)]
    assert all(a<=F(b) for a,b in zip(cold,saved['cold_inputs_upper']))
    coldresult=upper_trajectory(cold);assert coldresult['failed_update']<=saved['cold_recursion']['step']
    maximum=max(r['failed_update'] for r in checked)
    assert maximum==saved['maximum_failed_update']
    closest=max(checked,key=lambda r:r['nonpositive_upper'])
    return dict(g=g,status='PASS independent rational all-beta nonpositive-update obstruction',hot_thermal_upper=hotC,hot_third_update_upper=hotfail,
                beta_partition=[[0,4],[4,20],[20,'infinity']],closed_middle_boxes=320,maximum_middle_failed_update=maximum,
                failure_update_histogram=dict(Counter(str(r['failed_update']) for r in checked)),closest_to_zero_failed_upper=closest,
                cold_positive_slopes=slopes,cold_inputs_upper=cold,cold_trajectory=coldresult,intervals=checked)

def main():
    start=time.monotonic();producer=read(OUT.parent/'trial_size_criteria'/'all_beta_exclusions.json')
    for name in ['criteria.py']:
        p=OUT.parent/'trial_size_criteria'/name;HASHES[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    p=OUT.parent/'low_band_review'/'fast_exp.py';HASHES[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    result=dict(status='running',results={})
    for g in ['1d25','1d20']:
        result['results'][g]=audit(g,producer['results'][g])
        (OUT/'scalar_results.json').write_text(json.dumps(serialize(result),indent=2)+'\n')
        print('ALL BETA PASS',g,flush=True)
    for p,h in producer['input_sha256'].items():assert HASHES[p]==h
    for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
    result.update(status='PASS independent all-beta scalar obstruction; physical audit reported separately',input_sha256=HASHES,seconds=time.monotonic()-start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,limits=dict(cpu_count=1,BLAS_threads=1,address_space_bytes=1024**3))
    (OUT/'scalar_results.json').write_text(json.dumps(serialize(result),indent=2)+'\n')
    print(result['status'],result['seconds'],result['peak_rss_kib'],flush=True)
if __name__=='__main__':main()
