from pathlib import Path
p=Path(__file__).resolve().parent;s=(p/'controller22_reference.py').read_text()
s=s.replace('import os,sys,time,json,hashlib,resource,signal,math,fcntl,ctypes,re,tempfile','import os,sys,time,json,hashlib,resource,signal,math,fcntl,ctypes,re,tempfile,datetime')
s=s.replace("P=Path(__file__).resolve().parent","P=Path(__file__).resolve().parent\nSCHEMA='bilayer-moment24-v1'\nDEADLINE=datetime.datetime(2026,10,14,tzinfo=datetime.timezone.utc).timestamp()")
s=s.replace("'ppid':int(z[1])","'state':z[0],'ppid':int(z[1])")
s=s.replace("ledger['hard_cap']==120 and ledger['soft_stop']==90","ledger['hard_cap']==90 and ledger['soft_stop']==75")
s=s.replace("0<=ledger['charged']<=120","0<=ledger['charged']<=90")
s=s.replace("{'hard_cap':120,'soft_stop':90,","{'hard_cap':90,'soft_stop':75,")
s=s.replace("validate_budget(ledger);assert ledger['charged']+cap<=90","validate_budget(ledger);reconcile_stale(ledger);admit(ledger,cap,0,0,time.time())")
s=s.replace("t=time.monotonic();pid=os.fork()","t=time.monotonic();parent_pid=os.getpid();os.set_inheritable(lock.fileno(),True);pid=os.fork()")
s=s.replace("if pid==0:\n  os.setsid();", "if pid==0:\n  assert libc.prctl(1,signal.SIGKILL,0,0,0)==0\n  if os.getppid()!=parent_pid:os.kill(os.getpid(),signal.SIGKILL)\n  os.setsid();")
s=s.replace("rec['pid']=pid;rec['state']='running'", "rec['pid']=pid;rec['pid_start']=scan()[pid]['start'];rec['state']='running'")
s=s.replace("if test in ('interrupt','observer'):","if test in ('interrupt','observer','controller_death'):")
s=s.replace("if time.monotonic()-t>max(10,2*cap):reason='external_wall_guard'","if time.monotonic()-t>max(10,2*cap):reason='external_wall_guard'\n  if time.time()>=DEADLINE:reason='absolute_deadline'")
s=s.replace("{'job','sector','begin','end','N','values'}","{'schema','job','sector','begin','end','N','values'}")
s=s.replace("assert v['sector'] in (0,2,4,6)","assert v['schema']==SCHEMA\n assert v['sector'] in (0,2,4,6)")
s=s.replace("len(v['values'])==22","len(v['values'])==24").replace("[0]*22","[0]*24")
pos='def run(name,cap,args,test=None):'
helpers='''def admit(ledger,cap,remaining_reserved,remaining_wall,now):
 assert isinstance(cap,int) and cap>0
 assert remaining_reserved>=0 and remaining_wall>=0
 assert ledger['charged']+cap<=ledger['soft_stop'],'soft_admission_stop'
 assert ledger['charged']+cap+remaining_reserved<=ledger['hard_cap'],'remaining_plan_exceeds_total_budget'
 assert now+max(10,2*cap)+remaining_wall+30<DEADLINE,'deadline_forecast_rejected'

def reconcile_stale(ledger):
 stats=scan()
 for rec in ledger['attempts']:
  if rec['state'] not in ('reserved','running'):continue
  pid=rec.get('pid');live=stats.get(pid)
  if live and live['start']==rec.get('pid_start') and live['state']!='Z':
   raise RuntimeError('previous_worker_still_live_refuse_admission')
  rec['state']='abandoned_charged';rec['reconciled_no_refund']=True

'''
s=s.replace(pos,helpers+pos)
# Replace main block with verified adoption layer.
s=s[:s.index("if __name__=='__main__':")]+'''def adopt_completed(out):
 out=Path(out);receipt=read(out/'receipt.json');ledger=read(P/'BUDGET_LEDGER.json');validate_budget(ledger)
 assert any(x==receipt for x in ledger['attempts']),'receipt_not_bound_to_ledger'
 assert receipt['state']=='complete' and receipt['test'] is None
 assert receipt['identity']==read(P/'PINNED_INPUTS.json') and identities()==receipt['identity']
 needed={'chunk.json','targets.jsonl','result.json','result.json.accumulators.json','result.json.schema.json'}
 assert needed<=set(receipt['output_sha256'])
 for name,sha in receipt['output_sha256'].items():
  assert Path(name).name==name and digest((out/name).read_bytes())==sha,'output_digest_mismatch'
 assert read(out/'result.json.schema.json')=={'schema':SCHEMA,'fields':24}
 args=receipt['args'];assert args[0]=='chunk';kind=args[1];nx,q,begin,count=map(int,args[2:]);large=kind=='sample';n=nx*(4 if large else 2)
 N=math.comb(n-1,q-1) if large and q in (4,6) else math.comb(n,q)
 stride=(65536 if q==6 else 1024 if q==4 else 127 if q==2 else 1) if large else (N-1 if N>1 else 1)
 meta=read(out/'chunk.json');assert (meta['q'],meta['begin'],meta['end'],meta['N'],meta['stride'])==(q,begin,begin+count,N,stride)
 rows=[json.loads(x) for x in (out/'targets.jsonl').read_text().splitlines()]
 assert [x['id'] for x in rows]==list(range(begin,begin+count)) and all(x['rank']==stride*x['id']%N for x in rows)
 val=read(out/'result.json.accumulators.json');result=read(out/'result.json');assert len(val)==24 and result['complete']
 assert list(result['terms'].values())==val[:15]
 z=list(map(int,val));mom=[z[15],z[16],z[17]+121*z[20],z[18]+193600*z[20]+1331*sum(z[:4])+z[21],z[19]+sum(z[4:10])+14641*sum(z[10:15])]
 assert mom==list(map(int,result['moments']))
 job=digest(json.dumps({'identity':receipt['identity'],'kind':kind,'nx':nx,'schema':SCHEMA},sort_keys=True).encode())
 payload=dict(schema=SCHEMA,job=job,sector=q,begin=begin,end=begin+count,N=N,values=val)
 d=P/'committed'/job;commit(d,payload,job);return d,job,payload

if __name__=='__main__':
 if sys.argv[1]=='test':run(sys.argv[2],int(sys.argv[3]),sys.argv[5:],sys.argv[4])
 else:
  out=run(sys.argv[1],int(sys.argv[2]),sys.argv[3:])
  if sys.argv[3]=='chunk':adopt_completed(out)
'''
(p/'controller.py').write_text(s)
