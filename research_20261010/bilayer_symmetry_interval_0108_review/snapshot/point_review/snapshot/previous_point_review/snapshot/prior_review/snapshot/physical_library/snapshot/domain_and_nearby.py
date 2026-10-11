from explore import *
O=P.L.O
base=data(F(1,10))
def reference_interval(g,N,q):
 c=F(3*N,8);r=C.sqrt_down(1-4*g);return [c*(2*g-1)+(c+q)*r,c*(2*g-1)+(c+q)*(r+F(1,10**60))]
def margins(g):
 out={}
 for patch in base['denominator_patches']:
  N=patch['N'];rho=C.poly(list(map(F,patch['rayleigh_coefficients'])),g)
  for q,name in ((1,'ground'),(2,'even')):out[f'{N}_{name}']=[v-rho for v in reference_interval(g,N,q)]
  for mode in patch['odd_band']['modes']:
   theta=[O.Quad(*map(F,x)) for x in mode['theta_coefficients']];lo,hi=O.evaluate(theta,g).bounds(160);ref=reference_interval(g,N,2)
   out[f'{N}_odd_{mode["momentum"]}']=[ref[0]-hi,ref[1]-lo]
 c=F(147,8);r=C.sqrt_down(1-4*g);out['short_L7']=[c*(2*g-1)+(c+1)*r,c*(2*g-1)+(c+1)*(r+F(1,10**60))]
 return out
def isolate(key):
 lo,hi=F(1,10),F(249,1000)
 assert margins(lo)[key][0]>0 and margins(hi)[key][1]<0
 for _ in range(30):
  mid=(lo+hi)/2;m=margins(mid)[key]
  if m[0]>0:lo=mid
  elif m[1]<0:hi=mid
  else:raise AssertionError('uncertain interval')
 return [str(lo),str(hi)]
if __name__=='__main__':
 start=time.time();roots={k:isolate(k) for k in ('16_ground','32_ground','16_even','32_even','short_L7','16_odd_[2, 2]','32_odd_[4, 2]','16_odd_[0, 0]','32_odd_[0, 0]')}
 out={'roots':roots,'margin_at_11':{k:list(map(str,v)) for k,v in margins(F(11,100)).items()},'domain':'exact polynomials all real; stable bosonic reference 0<=g<1/4; witnesses require listed positive cutoffs; short L2..7 additionally requires short_L7>0'}
 x=F(roots['short_L7'][0]);mm=margins(x);assert min(v[0] for v in mm.values())>0
 out['all_margins_at_legal_upper_inner']={k:list(map(str,v)) for k,v in mm.items()};out['legal_closed_domain']=['1/10',str(x)]
 (HERE/'domain_check.json').write_text(json.dumps(out,indent=2)+'\n');print({k:list(map(lambda s:float(F(s)),v)) for k,v in roots.items()},flush=True)
 points=[]
 for g in (F(1001,10000),F(201,2000),F(101,1000),F(203,2000),F(51,500)):
  d=data(g);vals=[(v,F(i,40)) for i in range(240,601) if (v:=path_float(d,i/40)) is not None];best=max(vals) if vals else None
  points.append({'g':str(g),'best_float':None if best is None else [best[0],str(best[1])],'successful_temperatures':len(vals),'margins':margin_record(d),'data':d});print(g,points[-1]['best_float'],flush=True)
  (HERE/'nearby_checkpoint.json').write_text(json.dumps(points,indent=2)+'\n')
 (HERE/'nearby.json').write_text(json.dumps({'results':points,'seconds':time.time()-start},indent=2)+'\n')
