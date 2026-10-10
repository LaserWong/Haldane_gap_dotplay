"""Minimal retained rank for one explicitly specified spectral-bin majorant test."""
from criteria import *

def prove_rank(rec,beta,tolerance):
 shift=F(rec['blocks'][0]['eigen_upper'][0]);bins=rec['number_sector_bins']['bins'];exc=3*rec['N'];a1=F(bins[1]['lower']);wlo,whi=exp_bounds(-beta*(a1-shift));lo=hi=F(0)
 for b in bins[2:]:
  l,u=exp_bounds(-beta*(F(b['lower'])-shift));lo+=b['multiplicity']*l;hi+=b['multiplicity']*u
 # Explicit ansatz: kept states get certified spectral intervals; every unkept q1 slot is assigned a1.
 # T(r)=T_q>=2+r exp(-beta(a1-u1)). Exact floors agreeing proves the maximum omitted r.
 if hi>tolerance:return dict(status='inconclusive even after keeping q1',q_ge_2_tail_upper=hi)
 sufficient=max(0,min(exc,(tolerance-hi)//whi));necessary=max(0,min(exc,(tolerance-lo)//wlo));assert sufficient==necessary
 r=int(sufficient);assert hi+r*whi<=tolerance
 if r<exc:assert lo+(r+1)*wlo>tolerance
 return dict(status='PASS exact minimum within the specified bin-majorant tail test',N=rec['N'],beta=beta,absolute_shifted_tail_tolerance=tolerance,first_omitted_bin_energy=a1,one_omitted_q1_weight=[wlo,whi],q_ge_2_tail=[lo,hi],maximum_omitted_q1_states=r,minimum_retained_rank_for_test=1+exc-r,available_full_band_rank=1+exc)
if __name__=='__main__':
 result=[]
 for g in ['3d100','1d25','1d20']:
  for r in load_band(g):
   for tol in [F(1,10000),F(1,1000)]:
    row=prove_rank(r,F(909,100),tol);row['g']=g;result.append(row)
 (OUT/'entropy_rank.json').write_text(json.dumps(serial(dict(results=result,input_sha256=READ_HASHES)),indent=2)+'\n')
 for r in result:print(r['g'],r.get('N'),'tol',r.get('absolute_shifted_tail_tolerance'),r.get('minimum_retained_rank_for_test'),r['status'])
