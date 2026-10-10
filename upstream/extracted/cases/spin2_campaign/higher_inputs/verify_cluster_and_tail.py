"""Verify saved positive integer vectors and bound omitted magnetic sectors.
No eigensolver, square roots, floating comparisons, or interval exponentials are
used in accepted certificate checks. Float values are display only.
"""
from pathlib import Path
from fractions import Fraction as F
import json,math
import numpy as np
from cluster_bounds import matrix,envelope
ROOT=Path(__file__).resolve().parent

def rational_exp_minus_upper(x):
 assert x>=0
 # exp(x) >= positive Taylor partial sum, hence reciprocal is an exact upper bound.
 # x<=1000 here. More terms than necessary chosen to keep close to the true value.
 K=2*math.ceil(x)+100
 term=total=F(1)
 for k in range(1,K+1):term*=x/k;total+=term
 return 1/total

def main():
 checked=[];allrec={}
 for n in [4,6,8]:
  recs=[]
  for m in range(2*n+1):
   rec=json.loads((ROOT/f'open{n}_m{m}.json').read_text());q=json.loads((ROOT/rec['vector_file']).read_text());lo=F(rec['lower']);hi=F(rec['upper']);A2,_,_=matrix(n,m)
   assert len(q)==A2.shape[0] and all(isinstance(x,int) and x>0 for x in q)
   for i in range(len(q)):
    s=sum(int(A2.data[p])*q[int(A2.indices[p])] for p in range(A2.indptr[i],A2.indptr[i+1]))
    assert s*lo.denominator>=2*q[i]*lo.numerator
    assert s*hi.denominator<=2*q[i]*hi.numerator
   recs.append(rec);checked.append({'n':n,'m':m,'rows':len(q),'passed':True})
  allrec[n]=recs
 dim=np.array([1],dtype=object)
 for _ in range(10):dim=np.convolve(dim,np.ones(5,dtype=object))
 a=F(5951,1250);beta=F(8);bounds={}
 for m in range(21):
  cand=[(envelope(10,r,m),l) for l,r in allrec.items()];((bound,h),l)=max(cand,key=lambda x:x[0][0]);bounds[m]=(bound,h,l)
 per_sector={}
 for m in range(5,21):
  bound,h,l=bounds[m];tail=2*int(dim[20+m])*rational_exp_minus_upper(beta*(bound+10*a));per_sector[m]=tail
 tails={}
 for cut in [5,6,7,8]:
  val=sum((x for m,x in per_sector.items() if m>=cut),F(0))
  # round upward to a compact rational bound with a scale appropriate to magnitude
  k=max(1,math.ceil(-math.log10(float(val)))+4);sc=10**k;up=F(-((-val.numerator*sc)//val.denominator),sc)
  tails[str(cut)]={'upper':str(up),'upper_display':float(up),'covers':f'All states in |M| >= {cut}, arbitrary z twist'}
 out={'n':10,'beta':str(beta),'shift':str(a),'certified_cluster_vectors':checked,'integer_rows_verified':sum(r['rows'] for r in checked),'tails':tails,'same_sector_ritz_completeness_verified':False,'uniform_gap_proved':False,'exp_bound':'Exact reciprocal positive Taylor sum; outward decimal rational endpoint'}
 (ROOT/'verified_tail_results.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='certified_cluster_vectors'},indent=2))
if __name__=='__main__':main()
