#!/usr/bin/env python3
"""Checkpointed exact-integer Appendix A heat-trace certificates, without ED."""
import argparse, hashlib, json, math, os, platform, resource, subprocess, time
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
UPSTREAM=ROOT.parent/'upstream/extracted/cases/haldane_reference_audit'
if not UPSTREAM.is_dir():UPSTREAM=ROOT/'reference_sources/cases/haldane_reference_audit'
Q=2**56; MU=84; J=256
CENTERS={(6,'I'):8945303,(6,'P'):346734,(6,'C'):939987,
         (8,'I'):3741281,(8,'P'):567167,(8,'C'):984108,
         (10,'I'):2327547,(10,'P'):721090,(10,'C'):1002613}
PRINTED_TOTALS={(6,'I'):93637037510293158533967385845216,
 (6,'P'):3629519998654831111446492683663,(6,'C'):9839536903588146388838689926305,
 (8,'I'):4947327904487991279560670127283,(8,'P'):749999795795292705866802820621,
 (8,'C'):1301346729026243689610427021457,(10,'I'):388818111664728958208623998490,
 (10,'P'):120458568770462253326886628639,(10,'C'):167487042402286114495695779656}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def atomic_json(path,data):
    path=Path(path);tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w') as f:json.dump(data,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    tmp.replace(path)
def coefficients():
    fac=math.factorial(J);v=[MU**j*(fac//math.factorial(j)) for j in range(J+1)]
    s=sum(v);return [Q*x//s for x in v]
def ceilroot(x):r=math.isqrt(x);return r+(r*r<x)
def frac(x):return {'numerator':str(x.numerator),'denominator':str(x.denominator)}
def cert(n,twist,mode,records,metadata):
    assert sum(r['multiplicity'] for r in records)==3**n
    assert len({r['code'] for r in records})==len(records)
    total=sum(r['multiplicity']*int(r['norm_squared']) for r in records)
    coeff=coefficients();kmax=max(j for j,c in enumerate(coeff) if c)
    sj=sum((F(MU**j,math.factorial(j)) for j in range(J+1)),F(0))
    tail=F(MU**(J+1),math.factorial(J+1))/(1-F(MU,J+2))
    truncation_error=2*tail/sj
    assert truncation_error<F(1,Q)
    # Per representative physical Euclidean error <= error_numerator/Q.
    # Include coefficient floors, all Horner vector floors, and normalized tail.
    error_sq=sum(r['multiplicity']*((kmax+1)*ceilroot(r['block_dimension'])+(J+1)+1)**2 for r in records)
    error=ceilroot(error_sq)
    x=F(21,2)*n*(F(3,2)-F(700741,500000))
    el=sum((x**j/F(math.factorial(j)) for j in range(101)),F(0))
    eu=el+x**101/F(math.factorial(101))/(1-x/102)
    rt=math.isqrt(total)
    lo=el*F(max(0,rt-error)**2,Q*Q)
    hi=eu*F((rt+1+error)**2,Q*Q)
    center=F(CENTERS[n,twist],10**6) if (n,twist) in CENTERS else None
    accepted=center is not None and center-F(1,10**5)<lo<=hi<center+F(1,10**5)
    result={'schema':'exact-heat-trace-v1','status':'certified_finite_thermal_input' if accepted else 'computed_interval',
      'model':'spin-1 isotropic Heisenberg, periodic, bilinear coefficient 1; seam phase exp(i theta (column_0-row_0))',
      'L':n,'twist':twist,'theta':{'I':'0','P':'pi','C':'2*pi/3'}[twist],
      'beta':'21/2','energy_shift_a':'700741/500000','target':'Tr exp[-beta (H+a L)]',
      'orbit_mode':mode,'physical_dimension':3**n,'representatives':len(records),
      'Q':str(Q),'mu':MU,'J':J,'kmax':kmax,'total_squared_integer_norm':str(total),
      'weighted_column_error_numerator_squared':str(error_sq),'frobenius_error_numerator':str(error),
      'tail_error_less_than_1_over_Q':True,'tail_error_bound':frac(truncation_error),
      'interval':{'lower':frac(lo),'upper':frac(hi)},
      'display_only':{'lower':float(lo),'upper':float(hi),'width':float(hi-lo),'frobenius_error':error/Q},
      'published_center':str(center),'published_halfwidth':'1/100000','published_interval_accepted':accepted,
      'printed_total_difference':str(total-PRINTED_TOTALS[n,twist]) if (n,twist) in PRINTED_TOTALS else None,
      'proof_file':'PROOF.md','run_metadata':metadata,'scope':'Finite physical thermal input only. No new uniform-gap claim.'}
    if center is not None:assert accepted,result['display_only']
    return result

def run(args):
    n=args.length;twist=args.twist;mode=args.orbits
    out=ROOT/'results'/f'A_L{n}_{twist}_{mode}';out.mkdir(parents=True,exist_ok=True)
    cp=ROOT/'coefficients_A.txt';content=''.join(str(c)+'\n' for c in coefficients())
    if not cp.exists():cp.write_text(content)
    assert cp.read_text()==content
    provenance={'cpp_sha256':sha(ROOT/'stream_horner.cpp'),'binary_sha256':sha(ROOT/'stream_horner'),
      'coefficient_sha256':sha(cp),'upstream_matrix_source_sha256':sha(UPSTREAM/'thermal_small_exact.py'),
      'python':platform.python_version(),'platform':platform.platform(),'single_process':True,
      'omp_num_threads':os.environ.get('OMP_NUM_THREADS'),'openblas_num_threads':os.environ.get('OPENBLAS_NUM_THREADS')}
    records=[];runstart=time.monotonic();computed=0;chunk_times=[]
    blocks=range(-n,1) if mode=='full' else range(-n,n+1)
    for m in blocks:
        cmd=[str(ROOT/'stream_horner'),str(n),twist,mode,str(m)]
        info=subprocess.check_output(cmd+['0','0',str(cp),'list'],text=True).splitlines()
        meta=info[0].split();dim=int(meta[5]);rep_list=[tuple(map(int,line.split())) for line in info[1:]]
        for start in range(0,len(rep_list),args.chunk):
            count=min(args.chunk,len(rep_list)-start)
            path=out/f'M{m:+03d}_start{start:06d}_count{count:04d}.json'
            identity={'L':n,'twist':twist,'mode':mode,'M':m,'start':start,'count':count,
                      'cpp_sha256':provenance['cpp_sha256'],'coefficient_sha256':provenance['coefficient_sha256']}
            if path.exists():
                data=json.loads(path.read_text());assert data['identity']==identity
            else:
                t=time.monotonic()
                proc=subprocess.run(cmd+[str(start),str(count),str(cp),'compute'],text=True,capture_output=True,check=True)
                rows=[]
                for line in proc.stdout.splitlines():
                    code,mult,norm=map(int,line.split());rows.append({'code':code,'multiplicity':mult,'norm_squared':str(norm),'block_dimension':dim,'M':m})
                assert [(r['code'],r['multiplicity']) for r in rows]==rep_list[start:start+count]
                elapsed=time.monotonic()-t
                data={'identity':identity,'seconds':elapsed,'diagnostic':proc.stderr.strip(),'records':rows}
                atomic_json(path,data);computed+=count;chunk_times.append(elapsed)
                print(f'L={n} {twist} {mode} M={m:+d} d={dim} chunk={start}:{start+count}/{len(rep_list)} seconds={elapsed:.3f}',flush=True)
            assert len(data['records'])==count
            records.extend(data['records'])
            if args.max_new_columns and computed>=args.max_new_columns:
                print(json.dumps({'status':'benchmark_checkpoint','new_columns':computed,'wall_seconds':time.monotonic()-runstart,'child_maxrss_kb':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}),flush=True)
                return
    provenance.update({'wall_seconds_this_invocation':time.monotonic()-runstart,
      'total_recorded_compute_seconds':sum(json.loads(p.read_text())['seconds'] for p in out.glob('M*.json')),
      'child_maxrss_kb':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
    result=cert(n,twist,mode,records,provenance)
    atomic_json(out/'certificate.json',result)
    print(json.dumps({k:result[k] for k in ('L','twist','orbit_mode','representatives','total_squared_integer_norm','display_only','printed_total_difference','published_interval_accepted')}),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--length',type=int,required=True);p.add_argument('--twist',choices=['I','P','C'],required=True)
    p.add_argument('--orbits',choices=['none','translation','dihedral','full'],default='full');p.add_argument('--chunk',type=int,default=16);p.add_argument('--max-new-columns',type=int,default=0)
    run(p.parse_args())
