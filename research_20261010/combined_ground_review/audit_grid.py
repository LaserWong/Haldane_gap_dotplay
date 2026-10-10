"""Independent finite floating proposal-grid diagnostic, never proof acceptance."""
from audit_combination import *

def proposal_stages(recs,bi,order,cache):
 beta=bi/20
 def z(i,m):
  key=(i,m)
  if key not in cache:
   t=m/20;r=recs[i]
   lo=sum(b['multiplicity']*math.exp(-t*float(F(u))) for b in r['blocks'] for u in b['eigen_upper'])
   hi=sum(b['multiplicity']*math.exp(-t*float(F(l))) for b in r['blocks'] for l in b['eigen_lower'])
   hi+=sum(v['multiplicity']*math.exp(-t*float(F(v['lower']))) for v in r['number_sector_bins']['bins'][2:])
   cache[key]=(lo,hi)
  return cache[key]
 q0=z(0,bi);q3=z(2,2*bi);i1,t1=(0,2*bi) if order[0]=='t' else (1,bi);i2,t2=(2,bi) if order[-1]=='t' else (1,2*bi)
 q1=z(i1,t1);q2=z(i2,t2);j1=q3[0]/q0[1]**8;j2=q3[0]**2/q1[1]**8;c=q3[0]/q2[1]**2
 assert max(j1,j2,c)<=1+1e-10
 def fn(z):return 1-(1-z)**2/(2*z*z)
 v=[]
 for k in range(3):
  p=j1 if k==0 else j2*v[0] if k==1 else c**4*v[0]**2*v[1]
  v.append(fn(p))
  if v[-1]<=0:break
 npositive=sum(x>0 for x in v)
 if len(v)!=3 or min(v)<=0:return 1.,(npositive,min(v))
 a,b,c=v;abc=v if order=='xyt' else [a,b*math.sqrt(c),b*b*c] if order=='xty' else [a*math.sqrt(b),a*a*b*math.sqrt(c),a**4*b*b*c]
 rank=(npositive,min(abc))
 for j in range(16):
  u=max(1-x for x in abc)
  if u<=.002:return (-math.log(1/(32*u))/(beta*2**(j+1)) if u>0 else -1.),rank
  for _ in range(3):
   x=fn(abc[0]**4*abc[1]**2*abc[2])
   if x<=0:return 1.+u,rank
   abc=abc[1:]+[x]
 return max(1-x for x in abc),rank

def main():
 start=time.monotonic();verify_inputs();output=[]
 for variant in ['combined','filter_only']:
  for data in load(C/variant/'summary.json'):
   g=F(data['g']);tag=str(g).replace('/','d');recs=[load(C/variant/f'patch_{nx}x{ny}_g{tag}.json') for nx,ny in [(4,4),(8,4),(8,8)]];cache={}
   for row in data['results']:
    order=row['order_before_transport'];trials=[];best_rank=None
    for bi in range(100,601):
     score,rank=proposal_stages(recs,bi,order,cache);trials.append((score,bi))
     if best_rank is None or rank>best_rank[0]:best_rank=(rank,bi)
    value,bi=min(trials);selected=bi if value<0 else best_rank[1];accepted=sum(score<0 for score,_ in trials)
    assert F(selected,20)==F(row['beta_initial']),(variant,g,order,selected,row['beta_initial'])
    assert accepted==row['accepted_float_proposals']
    assert abs(value-row['best_float_score'])<1e-10
    output.append(dict(variant=variant,g=str(g),order=order,selected_beta=str(F(selected,20)),grid_points=501,accepted_proposals=accepted,best_score_display=value,exact_certificate_acceptance_separate=True,all_beta_exclusion=False))
    print('GRID PASS',variant,g,order,accepted,flush=True)
 save('bounded_grid_review.json',dict(status='PASS finite grid independently reproduced',records=output,total_samples=42*501,beta_min='5',beta_max='30',beta_step='1/20',seconds=time.monotonic()-start,all_beta_exclusion=False))
if __name__=='__main__':main()
