"""Independent 100-digit corroboration; analytic proof reviewed separately."""
import json
from fractions import Fraction as F
import mpmath as mp
from gapflow.seed_obstruction import split_bound,exp_negative_bounds
mp.mp.dps=100
M=lambda q:mp.mpf(q.numerator)/q.denominator
records=[]
for model,g,factor,c,B in [('bilayer_s_half',F(1,190),4,3,F(9,2)),('square_spin_one_large_D',F(1,250),6,2,F(4))]:
 for N in [4,8,16]:
  for multiplier in [1,2]:
   gg=g*multiplier;b=M(factor*gg)
   def logj(beta):return -7*(beta*b*N)**2-8*N*mp.log1p(c*mp.exp(-beta))
   def derivative(beta):return -14*b*b*N*N*beta+8*N*c*mp.exp(-beta)/(1+c*mp.exp(-beta))
   lo=mp.mpf(0);hi=mp.mpf(100)
   for _ in range(400):
    mid=(lo+hi)/2
    if derivative(mid)>0:lo=mid
    else:hi=mid
   beta=(lo+hi)/2;maximum=mp.exp(logj(beta))
   sampled=max(mp.exp(logj(mp.mpf(i)/20)) for i in range(1,1001))
   cert=split_bound(model,gg,B,N);upper=M(F(cert['all_beta_joint_seed_upper']))
   assert sampled<=maximum+mp.mpf('1e-90') and maximum<=upper and upper<mp.mpf(2)/5
   records.append({'model':model,'g':str(gg),'N':N,'stationary_beta':mp.nstr(beta,30),'stationary_joint_max':mp.nstr(maximum,30),'grid_max':mp.nstr(sampled,30),'rational_split_upper':str(cert['all_beta_joint_seed_upper'])})
for i in range(161):
 x=F(i,10);lo,hi=exp_negative_bounds(x);actual=mp.exp(-M(x))
 assert M(lo)<=actual<=M(hi)
print(json.dumps({'status':'passed','precision_decimal_digits':100,'grid_samples_per_case':1000,'grid_interval':'[0.05,50] in increments 0.05','exp_enclosure_checks':161,'cases':records,'scope':'High precision numerical corroboration, not the all-beta proof'},indent=2))
