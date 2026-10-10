from scan import *
import hashlib
from finite_window_2d import exp_upper
D=10**120
def sqrtlo(x):
 x=F(x);assert x>=0;k=math.isqrt(x.numerator*D*D//x.denominator);assert F(k*k,D*D)<=x<F((k+1)**2,D*D);return F(k,D)
def down(x):return F(x.numerator*D//x.denominator,D)
def direct_exact(a,b,c):
 assert all(0<x<=1 for x in (a,b,c))
 if c<=F(1,2):return F(0),{}
 d=down(b*sqrtlo(c));s=down(b*b*sqrtlo(2*c-1))
 if min(d,s)<=F(1,2):return F(0),{}
 v=down(a**4*(2*d-1)*sqrtlo(2*s-1))
 return v,dict(transverse_spatial_lower=str(d),interpolated_spatial_lower=str(s))
def labels(n,beta,order):
 state=[n,n,F(beta)];out=[]
 for axis in order:
  k={"x":0,"y":1,"t":2}[axis];end=state[:];end[k]*=2
  out.append(dict(axis=axis,base=S.serial(state),endpoint=S.serial(end)));state=end
 return out
def exact(beta,terminal):
 st=S.stages(recs,beta,'txy',True);raw=st['permuted_prefix'];can=st['canonical'];joint=S.J.full_product(raw);rows=[]
 for cycle in range(terminal+1):
  conv=S.transport(*raw,'txy',sqrtlo) if raw else None
  if conv:can=conv if can is None else list(map(max,can,conv))
  assert can is not None
  joint=max(joint,S.J.full_product(can),S.J.full_product(raw) if raw else F(0));bb=2*beta*2**cycle;u=max(1-x for x in can)
  row=dict(n=8*2**cycle,beta=str(bb),raw=S.serial(raw),canonical=S.serial(can),joint=str(joint),defect=str(u))
  row.update(physical_base=S.serial([row['n'],row['n'],bb]),raw_edge_labels=labels(row['n'],bb,'txy') if raw else None,canonical_edge_labels=labels(row['n'],bb,'xyt'))
  if cycle==terminal:
   assert 0<u<=F(1,500)
   # Floating proposal only. Exact rational exponential assertion accepts it.
   proposal=math.log(float(1/(32*u)))/float(bb)
   g=F(math.floor(proposal*10**12)-1,10**12)
   while exp_upper(bb*g)*32*u>=1:g-=F(1,10**12)
   row.update(asymptotic_gap=str(g),exp_witness=str(exp_upper(bb*g)*32*u));rows.append(row);break
  purity,detail=direct_exact(*raw) if raw else (F(0),{})
  assert purity>F(1,2)
  g=S.J.gap(purity,bb);assert exp_upper(bb*g)*(1-purity)<purity
  row.update(window=[row['n'],2*row['n']],thermal_lower=str(purity),gap=str(g),detail=detail);rows.append(row)
  can,_=S.J.canonical_advance(can,joint,True,digits=120);raw=S.J.plain_advance(raw,True,digits=120) if raw else None
  joint=S.J.full_product(can) if can else F(0)
 shortp=RES/'low_band/frontier_g007_g010/short_sizes/uniform_short_sizes.json';short=F(json.loads(shortp.read_text())['gap_lower'])
 result=min([short]+[F(r.get('gap',r.get('asymptotic_gap'))) for r in rows])
 return dict(status='exact_scalar_candidate_pending_new_2d_lemma_review',coupling='1/10',beta_initial=str(beta),terminal_cycle=terminal,short_L2_through_L7=str(short),all_integer_gap=str(result),gap_display=float(result),states=rows,initial=S.serial(st))
if __name__=='__main__':
 start=time.time();out=[]
 for beta in (F(47,5),F(93,10),F(187,20)):
  for terminal in (5,6,7):
   r=exact(beta,terminal);out.append(r);print(beta,terminal,r['gap_display'],flush=True)
 (HERE/'replay_check.json').write_text(json.dumps({'results':out,'seconds':time.time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2)+'\n')
 print('seconds',time.time()-start)
