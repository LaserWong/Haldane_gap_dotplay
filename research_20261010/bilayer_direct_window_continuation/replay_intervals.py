import sys,os,json,time,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;RES=HERE.parent
sys.path.insert(0,str(RES/'bilayer_direct_window_extension'))
import replay as R
F=R.F;S=R.S

def improve(rec):
 beta=F(rec['beta_initial']);raw=list(map(F,rec['permuted_first_purities']));can=list(map(F,rec['canonical_first_purities']));joint=max(S.J.full_product(raw),S.J.full_product(can),F(rec.get('initial_joint_product','0')))
 # Recheck the saved initial txy bounds directly from saved exact trace-ratio lower endpoints.
 aa=S.J.G(F(rec['J1']));bb=S.J.G(F(rec['J2'])*raw[0]);cc=S.J.G(F(rec['C0'])**4*raw[0]**2*raw[1])
 assert all(0<x<=y<=1 for x,y in zip(raw,[aa,bb,cc]))
 short=min(F(x['gap_lower']) for x in rec['short_sizes']);windows=[];states=[];best=None
 for cycle in range(16):
  if raw:
   conv=S.transport(*raw,'txy',R.sqrtlo);can=conv if can is None else list(map(max,can,conv))
  if can is None:break
  joint=max(joint,S.J.full_product(can),S.J.full_product(raw) if raw else F(0))
  n=8*2**cycle;bb=2*beta*2**cycle;u=max(1-x for x in can)
  state=dict(n=n,beta=str(bb),canonical=S.serial(can),raw=S.serial(raw),joint=str(joint),defect=str(u),physical_base=S.serial([n,n,bb]),canonical_edge_labels=R.labels(n,bb,'xyt'),raw_edge_labels=R.labels(n,bb,'txy') if raw else None)
  states.append(state)
  if 0<u<=F(1,500):
   prop=R.math.log(float(1/(32*u)))/float(bb);g=F(R.math.floor(prop*10**12)-1,10**12)
   while R.exp_upper(bb*g)*32*u>=1:g-=F(1,10**12)
   final=min([g,short]+[F(x['gap']) for x in windows])
   if best is None or final>F(best['gap']):best=dict(gap=str(final),gap_display=float(final),terminal_cycle=cycle,terminal_n=n,terminal_beta=str(bb),asymptotic_gap=str(g),asymptotic_witness=str(R.exp_upper(bb*g)*32*u),windows=windows[:],states=states[:],short_gap=str(short))
   if u<F(1,10**90):break
  p,detail=R.direct_exact(*raw) if raw else (F(0),{})
  old,odetail=S.J.interpolate_2d_joint(*can,joint)
  method='direct_txy' if p>=old else 'inherited_canonical';value=max(p,old)
  if value<=F(1,2):break
  gap=S.J.gap(value,bb)
  windows.append(dict(n=n,through=2*n,beta=str(bb),method=method,purity=str(value),direct_purity=str(p),canonical_purity=str(old),gap=str(gap),details=detail))
  can,_=S.J.canonical_advance(can,joint,True,digits=120);raw=S.J.plain_advance(raw,True,digits=120) if raw else None
  joint=S.J.full_product(can) if can else F(0)
 assert best is not None
 best['previous_gap']=rec['all_integer_L_ge2_gap'];best['coupling_interval']=rec['coupling_interval'];return best

def main():
 start=time.time();out=[];sources={}
 for group in ['ordinary_interval','interval_extension','interval_joint_extension','interval_range_0085','interval_range_009','interval_range_010']:
  summ=json.load(open(RES/group/'coverage_summary.json'))
  for entry in summ['intervals']:
   path=RES/group/entry['file'];r=json.load(open(path));new=improve(r);new['source']=str(path.relative_to(RES));out.append(new);sources[new['source']]=hashlib.sha256(path.read_bytes()).hexdigest()
   (HERE/'checkpoint.json').write_text(json.dumps({'completed':len(out),'last_source':new['source'],'last_gap':new['gap_display']},indent=2)+'\n')
  print(group,len(summ['intervals']),min(x['gap_display'] for x in out),flush=True)
 assert len(out)==66
 assert F(out[0]['coupling_interval'][0])==0 and F(out[-1]['coupling_interval'][1])==F(1,10)
 assert all(a['coupling_interval'][1]==b['coupling_interval'][0] for a,b in zip(out,out[1:]))
 result={'status':'exact_saved_input_interval_candidates_pending_independent_review','interval':["0","1/10"],'count':len(out),'uniform_gap':str(min(F(x['gap']) for x in out)),'uniform_gap_display':min(x['gap_display'] for x in out),'results':out,'source_sha256':sources,'seconds':time.time()-start,'peak_rss_kib':R.resource.getrusage(R.resource.RUSAGE_SELF).ru_maxrss}
 (HERE/'interval_results_check.json').write_text(json.dumps(result,indent=2)+'\n');print('UNIFORM',result['uniform_gap_display'],'seconds',result['seconds'],flush=True)
if __name__=='__main__':main()
