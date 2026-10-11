"""Pure production plan/admission functions. No numerical work on import."""
import math,time,datetime
DEADLINE=datetime.datetime(2026,10,14,tzinfo=datetime.timezone.utc).timestamp()
HARD=21600;SOFT=20000;CONTROLLER=1200;RETRY=3600

def plan():
 rows=[]
 for q,N,width,cap in [(0,1,1,3),(2,496,64,3),(4,4495,16,3),(6,169911,64,6)]:
  for begin in range(0,N,width):rows.append({'q':q,'begin':begin,'count':min(width,N-begin),'cap':cap,'N':N})
 assert len(rows)==2945 and sum(x['cap'] for x in rows)==16800
 return rows

def key(args):
 assert len(args)==6 and args[:3]==['chunk','sample','8']
 q,begin,count=map(int,args[3:]);return q,begin,count

def validate_ledger(l):
 assert l['hard_cap']==HARD and l['soft_stop']==SOFT and l['controller_reserved']==CONTROLLER
 assert l['charged']==CONTROLLER+sum(x['charged'] for x in l['attempts']) and l['charged']<=HARD
 assert all(x['charged']>=x['reserved']>0 for x in l['attempts'])
 assert len({x['name'] for x in l['attempts']})==len(l['attempts'])

def forecast(l,args,cap,now,allow_retry=False):
 validate_ledger(l);target=key(args);rows=plan();bykey={(x['q'],x['begin'],x['count']):x for x in rows};assert target in bykey and bykey[target]['cap']==cap
 succeeded={key(x['args']) for x in l['attempts'] if x['state']=='complete'};assert target not in succeeded,'already_complete_range'
 previous=[x for x in l['attempts'] if key(x['args'])==target]
 assert not any(x['state'] in ('reserved','running') for x in previous),'unreconciled_range'
 assert not previous or allow_retry,'retry_requires_specific_authority'
 failed=sum(x['charged'] for x in l['attempts'] if x['state']!='complete');retry_remaining=RETRY-failed;assert retry_remaining>=0,'retry_bucket_exhausted'
 pending=sum(x['cap'] for x in rows if (x['q'],x['begin'],x['count']) not in succeeded and (x['q'],x['begin'],x['count'])!=target)
 total=l['charged']+cap+pending+retry_remaining;assert total<=HARD,'full_remaining_plan_exceeds_hard_cap'
 assert l['charged']+cap<=SOFT,'soft_admission_stop'
 wall_required=2*(cap+pending+retry_remaining)+1200
 assert now+wall_required<DEADLINE,'full_remaining_plan_misses_deadline'
 return dict(pending_reserved=pending,retry_remaining=retry_remaining,total_reserved_forecast=total,remaining_wall_forecast=wall_required)
