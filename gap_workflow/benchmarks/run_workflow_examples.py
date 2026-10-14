"""Run example inputs without accepting stale artifacts after a rejected resume."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time
import uuid

ROOT=Path(__file__).resolve().parents[1]


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-root',type=Path,help='Fresh run root; default results/example_runs/<UTC>-<unique-id>')
    parser.add_argument('--resume',action='store_true',help='Explicitly ask each existing example run to validate and resume')
    parser.add_argument('--summary',type=Path,help='Summary path; default <output-root>/summary.json')
    args=parser.parse_args(argv)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    output_root=(args.output_root or ROOT/'results'/'example_runs'/stamp).resolve()
    output_root.mkdir(parents=True,exist_ok=True)
    summary_path=(args.summary or output_root/'summary.json').resolve()
    summary_path.parent.mkdir(parents=True,exist_ok=True)
    records=[]
    for path in sorted((ROOT/'examples').glob('*.json')):
        out=output_root/path.stem
        command=[sys.executable,'-m','gapflow',str(path),'--output',str(out)]
        if args.resume and out.exists():command.append('--resume')
        started=time.perf_counter()
        try:
            requested=json.loads(path.read_text()).get('budget',{}).get('wall_seconds',30)
            timeout=max(45,float(requested)+15)
            proc=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=timeout)
            stdout,stderr,returncode=proc.stdout,proc.stderr,proc.returncode
            try:
                response=json.loads(stdout)
                if not isinstance(response,dict) or 'status' not in response:
                    raise ValueError('CLI response does not contain a status')
            except (ValueError,TypeError):
                response={'status':'invalid_cli_response','reason':'CLI stdout was not a status object'}
            # The current invocation is authoritative. Rejected resumes/nonempty
            # directories can leave old results.json; never substitute it here.
            result=dict(response)
            accepted_artifact=False
            rejection={'invalid_input_or_resume','invalid_cli_response'}
            artifact=out/'results.json'
            if response['status'] not in rejection and artifact.exists():
                stored=json.loads(artifact.read_text())
                if stored.get('status')==response['status']:
                    result=stored
                    accepted_artifact=True
                else:
                    result={'status':'cli_artifact_status_mismatch',
                            'reason':'Current CLI status disagrees with the on-disk result',
                            'cli_response':response,'artifact_status':stored.get('status')}
        except subprocess.TimeoutExpired as exc:
            stdout=exc.stdout or '';stderr=exc.stderr or ''
            if isinstance(stdout,bytes):stdout=stdout.decode(errors='replace')
            if isinstance(stderr,bytes):stderr=stderr.decode(errors='replace')
            returncode=None;accepted_artifact=False
            response=result={'status':'benchmark_timeout','reason':'Outer benchmark deadline expired; no prior artifact accepted'}
        record={'input':str(path.relative_to(ROOT)),'output':str(out),'status':result['status'],
                'claim':result.get('claim'),'reason':result.get('reason'),
                'elapsed_seconds':time.perf_counter()-started,'exit_code':returncode,
                'uniform_family_claim':result.get('uniform_family_claim',False),
                'artifact_accepted':accepted_artifact,'cli_response':response,
                'stdout':stdout,'stderr':stderr}
        if 'execution_provenance' in result:record['execution_provenance']=result['execution_provenance']
        records.append(record)
        print(path.stem,record['status'],flush=True)
        summary_path.write_text(json.dumps(records,indent=2)+'\n')
    print('Summary:',summary_path,flush=True)
    return 0


if __name__=='__main__':
    raise SystemExit(main())
