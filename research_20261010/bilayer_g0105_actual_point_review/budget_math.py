"""Independent conditional error budgets and compressed-space limitations."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
import physical_library as P
from physical_library import F,HERE,S,load,sha,poly,eqseq,reference,contract
from independent_point_math import exp,root,full,valid,G,down,labels
import ast,copy,itertools,json,math,resource,time,types
from collections import Counter,defaultdict
import numpy as np
B=S/'budget_producer'

# The accepted matrix contraction allows arbitrary integer witnesses. Remove
# only the old fixed-vector restriction for the newly optimized 11D/43D vectors.
P.extract(HERE/'physical_library.py',['physical_trial'],vars(P),{'physical_trial':[("assert c==vectors[index] and len(c)==dim and all(type(x)is int for x in c)","assert (index!=1 or c==vectors[index]) and len(c)==dim and all(type(x)is int for x in c)"),("assert z==(lo if lo==hi else F(1,10))","assert z in (F(1,10),lo) and lo==hi")]})
ns=dict(F=F,np=np,Counter=Counter,defaultdict=defaultdict,itertools=itertools)
P.extract(S/'MATRIX_REBUILD.py',['mat','zero','graph','rebuild'],ns)
geo=load(S/'GEOMETRY_8x4.json');m0=ns['rebuild'](8,4,F(0),geo);m1=ns['rebuild'](8,4,F(1),geo)
MODEL32=dict(gram=m0['G'].tolist(),affine_A=[m0['A'].tolist(),(m1['A']-m0['A']).tolist()])
assert m0['G'].tolist()==m1['G'].tolist()

scalar_ns=dict(P.scalar_ns)
P.extract(S/'ACCEPTED_SCALAR_AUDIT.py',['replay'],scalar_ns,{'replay':[("assert rec['accepted'] is True","assert rec['conditional_hypotheses_only'] is True"),('0<=lo<hi<=F(1,10)','F(1,10)<=lo==hi<F(1,4)')]})

def ldl(mat):
 n=len(mat);L=[[F(0)]*n for _ in range(n)];D=[]
 for j in range(n):
  d=F(mat[j][j])-sum(L[j][k]**2*D[k] for k in range(j));assert d>0,('nonpositive',j);D.append(d);L[j][j]=1
  for i in range(j+1,n):L[i][j]=(F(mat[i][j])-sum(L[i][k]*L[j][k]*D[k] for k in range(j)))/d
 return D

def certify_data(d):
 g=F(d['coupling_interval'][0]);assert d['coupling_interval']==[str(g),str(g)]
 rr=[];patches=[]
 for i,t in enumerate(d['denominator_patches']+[d['largest_base_trial']]):
  r,p=P.physical_trial(t,i,g,g);rr.append(r);patches.append(p)
 for key,w in [('J1',[8,0,-2]),('J2',[16,0,-4]),('C0',[0,4,-2])]:
  saved=d['correlated_energy_combinations'][key];c=[sum(w[i]*rr[i][j] for i in range(3)) for j in range(2)]
  assert saved['weights']==w;eqseq(c,saved['affine_coefficients']);value=poly(c,g)
  eqseq([value,value],saved['endpoint_values']);assert value==F(saved['uniform_lower'])
 return patches[:2]

def component(p,beta,width=None):
 N=p['N'];width=p['width'] if width is None else width
 assert width>=0
 terms=[exp(beta*width),[F(0),F(0)],[F(0),F(0)]]
 for ell in p['odd']:
  a,b=exp(-beta*ell);terms[1][0]+=3*a;terms[1][1]+=3*b
 for q in range(2,N+1):
  count=math.comb(3*N+q-1,q);a,b=exp(-beta*p['lower'][q-1]);terms[2][0]+=count*a;terms[2][1]+=count*b
 return dict(ground=terms[0],odd=terms[1],tail=terms[2],total=[sum(x[0] for x in terms),sum(x[1] for x in terms)])

def ratios(d,patches,beta,epsilon=F(0),widths=None):
 widths=widths or {};cc=[component(p,b,widths.get(p['N'])) for p,b in [(patches[0],beta),(patches[0],2*beta),(patches[1],2*beta)]]
 ans={}
 for key,i,power,fac in [('J1',0,8,2),('J2',1,8,4),('C0',2,2,2)]:
  en=F(d['correlated_energy_combinations'][key]['uniform_lower'])+fac*epsilon;l,h=exp(beta*en);tl,th=cc[i]['total'];ans[key]=(l/th**power,h/tl**power)
 return ans,cc

def numerator_trial(t,g,model=None):
 model=P.m8 if model is None else model;c=t['integer_coefficients'];assert len(c)==43 and all(type(x)is int for x in c)
 norm=contract(c,model['gram']);assert norm>0 and norm==F(t['integer_metric_norm'])
 coeff=[contract(c,m)/norm for m in model['affine_A']];eqseq(coeff,t['rayleigh_coefficients']);assert F(t['center'])==g
 return poly(coeff,g)

def short_rows(g):
 ans=[]
 for L,ss in zip(range(2,8),(16,18,32,50,72,98)):
  c=F(3*ss,16);x=c*(2*g-1)+(c+1)*P.sqrtdecimal(1-4*g);assert x>0
  ans.append(dict(L=L,N=L*L,edge_square_sum=ss,ground_Rayleigh_upper='0',lambda2_shifted_lower=str(x),gap_lower=str(x)))
 return ans

def conditional(saved,rr,g,beta):
 start=saved['states'][0];raw=list(map(F,start['raw']));js={k:v[0] for k,v in rr.items()}
 assert raw[0]<=G(js['J1']) and raw[1]<=G(js['J2']*raw[0]) and raw[2]<=G(js['C0']**4*raw[0]**2*raw[1])
 can=scalar_ns['convert'](raw);assert all(F(x)<=v for x,v in zip(start['canonical'],can))
 inp=dict(coupling_interval=[str(g),str(g)],beta_initial=str(beta),permuted_first_purities=list(map(str,raw)),canonical_first_purities=list(map(str,can)),short_sizes=short_rows(g),all_integer_L_ge2_gap='0',conditional_hypotheses_only=True,**{k:str(v) for k,v in js.items()})
 out=copy.deepcopy(saved);out['source']='CONDITIONAL_HYPOTHESES_ONLY';return scalar_ns['replay'](out,inp)

def current_ranges(original,reoptimized):
 for rec in load(B/'endpoint_ranges.json'):
  g=F(rec['g']);expected=[]
  for key,records in [('original',original),('reoptimized_existing',reoptimized)]:
   d=records[g]
   for p in d['denominator_patches']:
    rho=poly(list(map(F,p['rayleigh_coefficients'])),g);w=F(p['uniform_Temple_width'])
    expected.append(dict(source=key,N=p['N'],rayleigh_upper=str(rho),certified_ground_lower=str(rho-w),width=str(w)))
  assert expected==rec['ranges']

def scoped_tests(target):
 rejected=[]
 for label,m in [('negative_pivot',[[F(-1)]]),('singular_pivot',[[F(0)]]),('negative_later_pivot',[[F(1),F(2)],[F(2),F(1)]])]:
  try:ldl(m)
  except AssertionError:rejected.append(label)
  else:raise AssertionError('invalid LDL accepted')
 signs=0
 for rho in (F(-1),F(0),F(1,3)):
  for a in (F(1),F(2)):
   for variance in (F(0),F(1,10),F(1)):
    for lower in (F(-2),F(-1,2),F(0),F(1,2)):
     temple=rho-variance/(a-rho);pencil=variance+(rho-a)*(rho-lower)
     assert (temple>lower)==(pencil<0) and (temple>=lower)==(pencil<=0);signs+=1
 # An already certified g=.102 triple weakened strictly below the reference
 # still closes a positive-gap path. Reference dominance is sufficient only.
 r={k:v*(1-F(1,10**8)) for k,v in target.items()};assert all(r[k]<target[k] for k in target)
 raw=[G(r['J1'])];raw.append(G(r['J2']*raw[0]));raw.append(G(r['C0']**4*raw[0]**2*raw[1]));can=scalar_ns['convert'](raw);joint=full(raw);beta=F(94,5);gap=F(1,1000);n=8;windows=0
 for cycle in range(16):
  can=list(map(max,can,scalar_ns['convert'](raw)));joint=max(joint,full(raw),full(can));u=max(1-x for x in can)
  if 0<u<=F(1,500) and exp(beta*gap)[1]*32*u<1:break
  purity=P.direct(*raw,n,n)[0];P.gapcheck(purity,beta,gap);windows+=1
  can=P.advance_canonical(can,joint);raw=P.advance(raw);joint=full(can);n*=2;beta*=2
 else:raise AssertionError('weakened reference path did not close')
 assert min(F(x['gap_lower']) for x in short_rows(F(51,500)))>gap
 return dict(adversarial_LDL_rejections=rejected,exact_Temple_sign_tests=signs,reference_dominance_not_necessary=dict(g='51/500',weakened_all_three_ratios=True,verified_gap=str(gap),finite_windows=windows,asymptotic_onset=n))

def main():
 start=time.monotonic();P.verify()
 assert sha(S/'BUDGET_PRODUCER_MANIFEST.json')=='83bcdf2b8d30ae60dc3f12b0a01857ff82bbdb1ac4ec294001d8d7b79f4cda1e'
 for rel,h in load(S/'BUDGET_PRODUCER_MANIFEST.json').items():assert sha(B/rel)==h
 assert sha(HERE/'physical_library.py')==load(S/'PHYSICAL_REVIEW_MANIFEST.json')['audit.py']
 original={F(x['g']):x['data'] for x in load(S/'exploration.json')['results']}
 reopt={F(x['g']):x['data'] for x in load(B/'reoptimized_saved.json')['results']}
 target_input=load(S/'points.json')['results'][-1]['input'];assert target_input['coupling_interval']==['51/500','51/500'] and F(target_input['beta_initial'])==F(47,5)
 target={k:F(target_input[k]) for k in ('J1','J2','C0')};reports=[];ps={}
 for g in (F(21,200),F(11,100)):
  ps[g,'original']=certify_data(original[g]);ps[g,'reoptimized']=certify_data(reopt[g])
 current_ranges(original,reopt)
 # Positive Grams certify that matrix lower bounds cover the entire indicated spaces.
 gram_pivots={name:len(ldl(m['gram'])) for name,m in [('numerator_8x8',P.m8),('ground_8x4',MODEL32),('ground_4x4',P.m4)]}
 ritz_by={F(r['g']):r for r in load(B/'ritz_bounds.json')['results']}
 for row in load(B/'targets.json')['results']:
  g=F(row['g']);beta=F(row['beta']);assert beta==F(47,5)
  assert {k:F(v) for k,v in row['target_ratios'].items()}==target
  rr,cc=ratios(original[g],ps[g,'original'],beta)
  assert all(0<F(row['current_ratios'][k])<=rr[k][0] for k in rr)
  for saved,calc in zip(row['components'],cc):
   for key in ('ground','odd','tail','total'):assert F(saved[key])>=calc[key][1] and F(saved[key])>=0
   assert F(saved['total'])==sum(F(saved[k]) for k in ('ground','odd','tail'))
  eps=F(row['sufficient_numerator']['epsilon']);previous=F(row['sufficient_numerator']['rejected_previous_gridpoint']);assert eps-previous==F(1,10**10)
  er,_=ratios(original[g],ps[g,'original'],beta,eps);pr,_=ratios(original[g],ps[g,'original'],beta,previous)
  assert all(er[k][0]>=target[k] for k in target)
  failed=[k for k in target if pr[k][1]<target[k]];assert failed and set(row['sufficient_numerator']['failed_ratios_at_previous'])<=set(failed)
  for k,v in row['sufficient_numerator']['certified_ratios'].items():assert target[k]<=F(v)<=er[k][0]
  rho=poly(list(map(F,original[g]['largest_base_trial']['rayleigh_coefficients'])),g);upper=numerator_trial(row['existing43D_trial'],g);gain=rho-upper
  assert rho==F(row['current_numerator_rayleigh']) and rho-eps==F(row['target_numerator_rayleigh']) and upper==F(row['existing43D_reoptimized_rayleigh']) and gain==F(row['existing43D_exact_improvement'])
  rb=ritz_by[g];ell=F(rb['ritz_lower']);assert F(rb['ritz_upper'])==upper and upper-ell==F(1,10**8)
  A=[[sum(g**k*F(m[i][j]) for k,m in enumerate(P.m8['affine_A']))-ell*F(P.m8['gram'][i][j]) for j in range(43)] for i in range(43)]
  piv=ldl(A);eqseq(piv,rb['positive_LDL_pivots']);assert F(rb['max_improvement_from_saved_rayleigh'])==rho-ell<eps
  path=conditional(row['hypothetical_only_conditional_path'],er,g,beta)
  reports.append(dict(g=str(g),type='numerator_only_sufficient_target',epsilon=str(eps),available_Rayleigh_gain=str(gain),entire_43D_gain_upper=str(rho-ell),LDL_positive_pivots=43,conditional_gap=path['gap'],physical_gap_claim=False))
 for row in load(B/'joint_targets.json')['results']:
  g=F(row['g']);beta=F(row['beta']);d=reopt[g];patch=ps[g,'reoptimized'];widths={N:F(row[f'width{N}']['width_cap']) for N in (16,32)}
  rr,_=ratios(d,patch,beta,widths=widths);assert all(rr[k][0]>=target[k] for k in target)
  for N,keys in [(16,['J1','J2']),(32,['C0'])]:
   rec=row[f'width{N}'];lo,hi=map(F,rec['max_sufficient_width_bracket']);original_width=patch[0 if N==16 else 1]['width']
   assert widths[N]==F(lo.numerator*10**6//lo.denominator,10**6)
   assert 0<=widths[N]<=lo<hi<=original_width and rec['keys']==keys and F(rec['current_width'])==original_width and F(rec['ground_lower_improvement'])==original_width-widths[N]
   lr,_=ratios(d,patch,beta,widths={N:lo});hr,_=ratios(d,patch,beta,widths={N:hi})
   assert all(lr[k][0]>=target[k] for k in keys) and any(hr[k][1]<target[k] for k in keys)
  rho16=poly(list(map(F,d['denominator_patches'][0]['rayleigh_coefficients'])),g);rho32=poly(list(map(F,d['denominator_patches'][1]['rayleigh_coefficients'])),g)
  L16=rho16-widths[16];L32=rho32-widths[32];assert L16==F(row['target_ground16_lower']) and L32==F(row['target_ground32_lower'])
  assert F(row['target_current16_variance'])==widths[16]*patch[0]['even_margin']
  assert F(row['current16_variance'])==F(d['denominator_patches'][0]['residual_squared_max']) and F(row['current32_variance'])==F(d['denominator_patches'][1]['residual_squared_max'])
  a=reference(16,g,2);AA=P.m4['shifted_A_coefficients'];BB=P.m4['full_shifted_B_coefficients'];GG=P.m4['gram']
  H=[[sum(g**k*F(m[i][j]) for k,m in enumerate(BB))-(a+L16)*sum(g**k*F(m[i][j]) for k,m in enumerate(AA))+a*L16*F(GG[i][j]) for j in range(11)] for i in range(11)]
  piv=ldl(H);ob=row['11D_Temple_target_obstruction'];assert ob['positive_definite'] is True and F(ob['reference_cutoff'])==a and F(ob['unattainable_Temple_lower'])==L16;eqseq(piv,ob['positive_LDL_pivots'])
  mean=numerator_trial(row['optimized43D_8x4_trial'],g,MODEL32);assert mean==F(row['optimized43D_8x4_rayleigh']);cut=reference(32,g,2);assert mean<cut
  budget=(mean-L32)*(cut-mean);assert budget==F(row['residual_squared_budget_for_optimized43D_8x4']) and row['budget_positive']==(budget>0)
  if g==F(11,100):assert mean<L32 and budget<0
  path=conditional(row['hypothetical_only_conditional_path'],rr,g,beta)
  reports.append(dict(g=str(g),type='joint_sufficient_target',width_caps={str(k):str(v) for k,v in widths.items()},target_ground32_lower=str(L32),optimized_ground32_mean=str(mean),complete_variance_budget=str(budget),entire_11D_fixed_cutoff_Temple_target_unattainable=True,physically_inconsistent_target=(mean<L32),conditional_gap=path['gap'],physical_gap_claim=False))
 tests=scoped_tests(target)
 out=dict(status='PASS_SCOPED_CONDITIONAL_BUDGETS_AND_EXACT_SUBSPACE_LIMITATIONS',results=reports,positive_Gram_dimensions=gram_pivots,new_physical_gap_claim=False,universal_bootstrap_no_go_claim=False,new_complete_residual_computed=False,scope_tests=tests,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)))
 (HERE/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
