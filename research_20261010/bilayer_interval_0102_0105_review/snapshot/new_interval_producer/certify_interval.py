from export import *
import copy
sys.path.insert(0,str(RES/'bilayer_frontier_above_010'))
from certify_points import exact_initial
from explore import path_float
from replay_intervals import improve
# Restore this package's output paths after imports.
HERE=Path(__file__).resolve().parent;RES=HERE.parent
GROUND=[json.load(open(HERE/f'ground_polynomial_{shape}.json')) for shape in ('4x4','8x4')]
NUM=json.load(open(RES/'bilayer_seed_error_budget/reoptimized_saved.json'))['results'][0]['data']['largest_base_trial']

def base_data(lo,hi,vectors=None):
 assert F(51,500)<=lo<=hi<=F(21,200);trials=copy.deepcopy(GROUND)+[copy.deepcopy(NUM)];patches=[]
 for tr in trials[:2]:
  N=tr['N'];rho=list(map(F,tr['rayleigh_coefficients']));var=list(map(F,tr['full_residual_squared_coefficients']));ends=[C.poly(var,g) for g in (lo,hi)];assert min(ends)>=0
  refs=[[C.reference(g,N,q)-C.poly(rho,g) for g in (lo,hi)] for q in range(1,N+1)];low=[min(v) for v in refs];assert low[0]>0 and low[1]>0
  patches.append(dict(**tr,residual_endpoint_values=C.st(ends),residual_squared_max=str(max(ends)),reference_minus_rayleigh_endpoint_lowers=[C.st(v) for v in refs],reference_minus_rayleigh_uniform_lowers=C.st(low),ground_identification_margin=str(low[0]),even_Temple_denominator=str(low[1]),uniform_Temple_width=str(max(ends)/low[1])))
 rr=[list(map(F,t['rayleigh_coefficients'])) for t in trials];joint={}
 for name,w in [('J1',[8,0,-2]),('J2',[16,0,-4]),('C0',[0,4,-2])]:
  cs=[sum(w[i]*rr[i][k] for i in range(3)) for k in range(2)];ends=[C.poly(cs,g) for g in (lo,hi)];joint[name]={'weights':w,'affine_coefficients':C.st(cs),'endpoint_values':C.st(ends),'uniform_lower':str(min(ends))}
 return {'coupling_interval':C.st((lo,hi)),'fixed_vector_center':'21/200','denominator_patches':patches,'largest_base_trial':trials[2],'correlated_energy_combinations':joint}
P.L.base_interval_data=base_data
vectors=[p['integer_coefficients'] for p in GROUND]+[NUM['integer_coefficients']]
def data(lo,hi):
 d=P.L.interval_data(lo,hi,vectors)
 for p in d['denominator_patches']:p['odd_band']['fixed_center']='1/10'
 return d
if __name__=='__main__':
 start=time.time();queue=[];x=F(51,500);hi=F(21,200);step=F(1,2000);minimum=F(4499695659,10**12)
 while x<hi:y=min(x+step,hi);queue.append((x,y));x=y
 out=[];attempts=[];target=HERE/'coverage_check';target.mkdir(exist_ok=True)
 while queue:
  lo,hi=queue.pop(0);d=data(lo,hi);proposals=[(score,b) for b in (F(8),F(47,5),F(19,2),F(10),F(11)) if (score:=path_float(d,float(b))) is not None];best=max(proposals) if proposals else None;row={'interval':C.st((lo,hi)),'proposal':None if best is None else [best[0],str(best[1])]};attempts.append(row)
  if best:
   init=exact_initial(d,best[1]);cert=improve(init);row['gap']=cert['gap'];rec={'status':'closed_fixed_witness_interval_candidate_pending_independent_review','input':init,'certificate':cert}
  else:rec=None
  if rec is None or F(cert['gap'])<minimum:
   assert hi-lo>=F(1,10**6) and len(attempts)<128,row
   mid=(lo+hi)/2;queue[:0]=[(lo,mid),(mid,hi)];C.exp_interval.cache_clear();continue
  out.append(rec);(target/f'interval_{len(out):03d}.json').write_text(json.dumps(rec,indent=2)+'\n');print(row,flush=True);C.exp_interval.cache_clear()
  (HERE/'checkpoint.json').write_text(json.dumps({'accepted':len(out),'last':row,'remaining':len(queue)},indent=2)+'\n')
 assert F(out[0]['input']['coupling_interval'][0])==F(51,500) and F(out[-1]['input']['coupling_interval'][1])==F(21,200)
 assert all(a['input']['coupling_interval'][1]==b['input']['coupling_interval'][0] for a,b in zip(out,out[1:]))
 summary={'status':'exact_closed_interval_extension_pending_independent_review','coupling_interval':['51/500','21/200'],'count':len(out),'uniform_gap':str(min(F(r['certificate']['gap']) for r in out)),'uniform_gap_display':min(r['certificate']['gap_display'] for r in out),'candidate_joined_0_through_0105_gap':str(minimum),'attempts':attempts,'intervals':[{'file':f'coverage/interval_{i:03d}.json','interval':r['input']['coupling_interval'],'gap':r['certificate']['gap']} for i,r in enumerate(out,1)],'seconds':time.time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 (HERE/'summary_check.json').write_text(json.dumps(summary,indent=2)+'\n');print('DONE',summary['count'],summary['uniform_gap_display'],summary['seconds'],flush=True)
