#!/usr/bin/env python3
"""Single-column bounded benchmarks with atomic, content-addressed records."""
import argparse,datetime,hashlib,json,os,re,resource,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def limits():
    resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
    resource.setrlimit(resource.RLIMIT_CPU,(590,600))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--L',type=int,default=9);ap.add_argument('--M',type=int,default=0);ap.add_argument('--twists',nargs='+',default=['I','C']);ap.add_argument('--fast',action='store_true');ap.add_argument('--profile',action='store_true');ap.add_argument('--phase',action='store_true');ap.add_argument('--native-baseline',action='store_true');ap.add_argument('--compressed',action='store_true');ap.add_argument('--block',type=int,default=1);ap.add_argument('--count',type=int,default=1);ap.add_argument('--algorithms',nargs='+',default=['chebyshev','horner']);args=ap.parse_args()
    for tw in args.twists:
      for alg in args.algorithms:
        cf=ROOT/f'coefficients_{alg}_Q56.txt';source='compressed_profile.cpp' if args.profile else 'compressed_fast.cpp' if args.fast else 'compressed_phase.cpp' if args.phase else 'compressed_columns.cpp' if args.compressed else 'chebyshev_columns.cpp';exe='heat_profile' if args.profile else 'heat_fast' if args.fast else 'heat_phase' if args.phase else 'heat_compressed' if args.compressed else 'heat_columns_native' if args.native_baseline else 'heat_columns';tag=f'L{args.L}_{tw}_M{args.M}_{alg}_r0'+(f'_compressed_b{args.block}_c{args.count}' if args.compressed else '')+('_profile' if args.profile else '_fast' if args.fast else '_phase' if args.phase else '_native' if args.native_baseline else '');record=ROOT/f'results/benchmark_{tag}.json'
        identity={'L':args.L,'twist':tw,'M':args.M,'start':0,'count':args.count,'block_columns':args.block,'compressed':args.compressed,'algorithm':alg,'source_sha256':sha(ROOT/source),'executable_sha256':sha(ROOT/exe),'coefficient_sha256':sha(cf)}
        if record.exists():
            old=json.loads(record.read_text())
            if old['identity']==identity and old['exit_code']==0:print('REUSE',tag,flush=True);continue
            raise RuntimeError('mismatched existing record '+str(record))
        cmd=[str(ROOT/exe),str(args.L),tw,str(args.M),'0',str(args.count),str(cf),'horner' if alg=='horner' else 'compute']
        if args.compressed:cmd.append(str(args.block))
        stdout=ROOT/f'logs/benchmark_{tag}.stdout';stderr=ROOT/f'logs/benchmark_{tag}.stderr'
        started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
        env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
        with stdout.open('w') as so,stderr.open('w') as se:
            p=subprocess.Popen(cmd,stdout=so,stderr=se,env=env,preexec_fn=limits)
            while True:
                done,status,ru=os.wait4(p.pid,os.WNOHANG)
                if done:break
                if time.monotonic()-t>600:
                    p.kill();done,status,ru=os.wait4(p.pid,0);break
                time.sleep(.05)
            ret=os.waitstatus_to_exitcode(status);p.returncode=ret
        text=stderr.read_text();data={k:float(v) if k.endswith('_seconds') else int(v) for k,v in re.findall(r'(compute_seconds|compute_cpu_seconds|accumulator_cpu_seconds|matvec_cpu_seconds|dimension|nnz|block_reps|degree|components|completed|block_columns)=([0-9.e+-]+)',text)}
        rss=ru.ru_maxrss
        data.update({'identity':identity,'started_utc':started,'wall_seconds':time.monotonic()-t,'exit_code':ret,'max_rss_kib':rss,'cpu_user_seconds':ru.ru_utime,'cpu_system_seconds':ru.ru_stime,'stdout':str(stdout.relative_to(ROOT)),'stderr':str(stderr.relative_to(ROOT)),'command':cmd})
        if ret==0:assert len(stdout.read_text().splitlines())==args.count+1
        tmp=record.with_suffix('.tmp')
        with tmp.open('w') as f:json.dump(data,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        tmp.replace(record);print(json.dumps(data),flush=True)
        if ret:raise RuntimeError('benchmark failed '+tag)
if __name__=='__main__':main()
