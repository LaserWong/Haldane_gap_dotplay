from certify_points import *
import hashlib
if __name__=='__main__':
 start=time.time();lo=F(1,10);hi=F(51,500);step=F(1,4000);minimum=F(4499695659,10**12);queue=[];x=lo
 while x<hi:y=min(x+step,hi);queue.append((x,y));x=y
 out=[];attempts=[];target=HERE/'extension_check';target.mkdir(exist_ok=True)
 while queue:
  left,right=queue.pop(0);d=data(left,right)
  for patch in d['denominator_patches']:patch['odd_band']['fixed_center']='1/10'
  vals=[(v,F(i,20)) for i in range(120,301) if (v:=path_float(d,i/20)) is not None]
  best=max(vals) if vals else None;row={'interval':C.st((left,right)),'float_proposal':None if best is None else [best[0],str(best[1])]};attempts.append(row)
  if best is None:rec=None
  else:
   init=exact_initial(d,best[1]);cert=improve(init);rec={'status':'closed_interval_frontier_candidate_pending_independent_review','input':init,'certificate':cert};row['gap']=cert['gap']
  if rec is None or F(cert['gap'])<minimum:
   assert right-left>=F(1,10**6) and len(attempts)<128,row
   mid=(left+right)/2;queue[:0]=[(left,mid),(mid,right)];C.exp_interval.cache_clear();continue
  out.append(rec);(target/f'interval_{len(out):03d}.json').write_text(json.dumps(rec,indent=2)+'\n')
  (HERE/'extension_checkpoint.json').write_text(json.dumps({'accepted':len(out),'remaining':C.st([a for a,b in queue]),'last':row},indent=2)+'\n');print(row,flush=True);C.exp_interval.cache_clear()
 assert F(out[0]['input']['coupling_interval'][0])==lo and F(out[-1]['input']['coupling_interval'][1])==hi
 assert all(a['input']['coupling_interval'][1]==b['input']['coupling_interval'][0] for a,b in zip(out,out[1:]))
 summary={'status':'exact_new_closed_coupling_interval_pending_independent_review','coupling_interval':C.st((lo,hi)),'count':len(out),'uniform_gap':str(min(F(r['certificate']['gap']) for r in out)),'uniform_gap_display':min(r['certificate']['gap_display'] for r in out),'preserved_whole_0_through_0102_gap':str(minimum),'attempts':attempts,'intervals':[{'file':f'extension/interval_{i:03d}.json','interval':r['input']['coupling_interval'],'gap':r['certificate']['gap']} for i,r in enumerate(out,1)],'seconds':time.time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 (HERE/'extension_summary_check.json').write_text(json.dumps(summary,indent=2)+'\n');print('DONE',summary['count'],summary['uniform_gap_display'],summary['seconds'],flush=True)
