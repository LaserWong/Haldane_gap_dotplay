"""Independent floating diagnostic on the producer's finite grid only.
Neither all-beta exclusion nor mathematical gap acceptance uses this scan.
"""
from independent_math import *
from verify_inputs import check_hashes
HERE=Path(__file__).resolve().parent;SRC=HERE/'snapshot/low_band/frontier_g007_g010'

def prepare(g):
 tag='g'+str(g).replace('/','d');directory=SRC/tag;prepared=[]
 for nx,ny in [(4,4),(8,4),(8,8)]:
  r=json.loads((directory/f'temple_{nx}x{ny}_{tag}.json').read_text());shift=F(r['blocks'][0]['eigen_upper'][0]);lo=[];hi=[]
  for b in r['blocks']:
   lo.extend((b['multiplicity'],float(F(z)-shift)) for z in b['eigen_upper'])
   hi.extend((b['multiplicity'],float(F(z)-shift)) for z in b['eigen_lower'])
  hi.extend((q['multiplicity'],float(F(q['lower'])-shift)) for q in r['number_sector_bins']['bins'][2:])
  prepared.append((lo,hi,float(F(r['energy_shift'])+shift)))
 return prepared,json.loads((directory/'frontier_results.json').read_text())

def stages(prepared,beta,order):
 def tr(i,b):
  lo,hi,_=prepared[i];return sum(m*math.exp(-b*z) for m,z in lo),sum(m*math.exp(-b*z) for m,z in hi)
 q0=tr(0,beta);q3=tr(2,2*beta);e=[x[2] for x in prepared]
 i1,b1=(0,2*beta) if order[0]=='t' else (1,beta)
 i2,b2=(2,beta) if order[-1]=='t' else (1,2*beta)
 q1=tr(i1,b1);q2=tr(i2,b2)
 j1=math.exp(-2*beta*e[2]+8*beta*e[0])*q3[0]/q0[1]**8
 j2=math.exp(-4*beta*e[2]+8*b1*e[i1])*q3[0]**2/q1[1]**8
 c0=math.exp(-2*beta*e[2]+2*b2*e[i2])*q3[0]/q2[1]**2
 def GG(x):return 1-(1-x)**2/(2*x*x)
 abc=[]
 for i in range(3):
  p=j1 if i==0 else j2*abc[0] if i==1 else c0**4*abc[0]**2*abc[1]
  abc.append(GG(p))
  if abc[-1]<=0:return abc,None
 a,b,c=abc
 canonical=[a,b,c] if order=='xyt' else [a,b*math.sqrt(c),b*b*c] if order=='xty' else [a*math.sqrt(b),a*a*b*math.sqrt(c),a**4*b*b*c]
 return abc,canonical

def score(canonical,beta):
 if canonical is None:return 1.
 abc=canonical[:]
 for j in range(16):
  u=max(1-x for x in abc)
  if u<=.002:return -math.log(1/(32*u))/(beta*2**(j+1)) if u>0 else -1.
  for _ in range(3):
   p=abc[0]**4*abc[1]**2*abc[2];new=1-(1-p)**2/(2*p*p)
   if new<=0:return 1+u
   abc=abc[1:]+[new]
 return max(1-x for x in abc)

def main():
 check_hashes();out=[];samples=[]
 for g in map(F,['7/100','2/25','1/10']):
  prepared,summary=prepare(g)
  for order,stored in zip(['xyt','xty','txy'],summary['results']):
   scores=[];best=None;positive=0
   for bi in range(100,601):
    beta=F(bi,20);prefix,canonical=stages(prepared,float(beta),order);value=score(canonical,float(beta));scores.append((value,beta))
    rank=(sum(x>0 for x in prefix),min(prefix if canonical is None else canonical))
    if best is None or rank>best[0]:best=(rank,beta)
    positive+=canonical is not None
    samples.append(dict(g=str(g),order=order,beta=str(beta),score=value,positive_steps=sum(x>0 for x in prefix)))
   accepted=sum(s<0 for s,b in scores);minimum,beta=min(scores);selected=beta if minimum<0 else best[1]
   assert accepted==stored['accepted_float_proposals']
   assert selected==F(stored['beta_initial'])
   assert abs(minimum-stored['best_float_score'])<1e-10
   if g>F(7,100):assert accepted==0
   out.append(dict(g=str(g),order=order,grid='beta 5..30 step .05',sample_count=len(scores),accepted_float_proposals=accepted,positive_first_cycles=positive,best_score=minimum,selected_beta=str(selected),selected_exact_replay_in='selected_failures.json' if not stored['accepted'] else 'accepted_certificates.json',all_beta_exclusion=False,diagnostic_only=True))
 (HERE/'results/bounded_grid_diagnostic.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'results/bounded_grid_samples.json').write_text(json.dumps(samples,indent=2)+'\n')
 check_hashes();print('PASS independent finite-grid diagnostic',len(samples),'samples',flush=True)
 for r in out:print(r['g'],r['order'],r['accepted_float_proposals'],r['selected_beta'],flush=True)
if __name__=='__main__':main()
