#!/usr/bin/env python3
"""Independent rational optimality audit; no optimizer or contraction execution."""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import os,resource,sys,json,hashlib,time,itertools
sys.set_int_max_str_digits(1000000)
P=Path(__file__).resolve().parent;ROOT=P.parents[1];A=P.with_name('uniform_moment_optimality_assessment');M=P.with_name('uniform_transfer_moment_assessment')
aff=os.sched_getaffinity(0);os.sched_setaffinity(0,{5 if 5 in aff else min(aff)});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600));start=time.process_time();hashes={}
def read(p):
 b=p.read_bytes();hashes[str(p.relative_to(ROOT))]=hashlib.sha256(b).hexdigest();return b
def js(p):return json.loads(read(p))
def ex(v):return F(v['exact'])
def ceil(v,B=10**30):return F(-((-v.numerator*B)//v.denominator),B)
def floor(v,B=10**30):return F(v.numerator*B//v.denominator,B)
def sqrtiv(v):
 B=10**40;n=isqrt(v.numerator*B*B//v.denominator)
 lo,hi=F(n,B),F(n+1,B);assert lo*lo<=v<=hi*hi;return lo,hi
counts={}
for folder in (A,M,P.with_name('uniform_transfer_moment_review'),P.with_name('uniform_seed_frontier_review')):
 seal=js(folder/'MANIFEST_SHA256.json')
 for name,h in seal.items():assert hashlib.sha256(read(folder/name)).hexdigest()==h
 counts[folder.name]=len(seal)
assert hashes[str((A/'MANIFEST_SHA256.json').relative_to(ROOT))]=='c862245e77fdf20e4e85859cbca804d888c96c11efcab2c30b5cbfedca3906cd'
for name,h in js(A/'INPUT_SHA256.json').items():assert hashlib.sha256(read(ROOT/name)).hexdigest()==h
source=js(M/'results.json');prod=js(A/'results.json');proposal=js(A/'unit_atom_proposals.json');audit=js(ROOT/'audit/independent/streamed_heat_audit.json')
trusted={v['certificate']:v['sha256'] for v in audit['independent_aggregate_intervals']}
raw={};mom={s:{} for s in ('trivial','complex','vector')};multip={'trivial':1,'complex':2,'vector':3}
co={'trivial':[F(1,12),F(1,4),F(2,3)],'complex':[F(1,12),F(1,4),F(-1,3)],'vector':[F(1,4),F(-1,4),F(0)]}
for L in (6,8,10):
 vals=[]
 for twist,theta in [('I','0'),('P','pi'),('C','2*pi/3')]:
  name=f'heat_trace/results/A_L{L}_{twist}_full/certificate.json';c=js(ROOT/name);assert hashes[name]==trusted[name]
  assert (c['L'],c['theta'],c['beta'],c['energy_shift_a'])==(L,theta,'21/2','700741/500000')
  raw[L,twist]=tuple(F(int(c['interval'][side]['numerator']),int(c['interval'][side]['denominator'])) for side in ('lower','upper'));vals.append(raw[L,twist])
 for sector,cs in co.items():
  lower=sum(c*val[int(c<0)] for c,val in zip(cs,vals));upper=sum(c*val[int(c>=0)] for c,val in zip(cs,vals))
  mom[sector][L//2]=(floor(lower,10**12),ceil(upper,10**12))
  assert mom[sector][L//2]==tuple(ex(v) for v in source['hankel_caps'][sector]['moment_intervals'][str(L//2)])
radau={};unit={};meta={}
for s in multip:
 h=ex(source['hankel_caps'][s]['x_cap']);a,b,c=[sum(mom[s][j])/2 for j in (3,4,5)]
 t=(h*b-c)/(h*a-b);wh=(b-t*a)/(h-t);wt=a-wh
 assert 0<t<h and wh>0 and wt>0
 assert (wh+wt,wh*h+wt*t,wh*h*h+wt*t*t)==(a,b,c)
 effective=(wh/h**3,wt/t**3);assert all(v.denominator!=1 for v in effective)
 radau[s]=(h,t,wh,wt,(a,b,c))
 pp=proposal[s];unit[s]=[(n,F(x)) for n,x in zip(pp['counts'],pp['x_rational'])]
 if s=='trivial':unit[s].append((10**15,F(1,10**10)))
 assert all(type(n)==int and n>0 and 0<x<h for n,x in unit[s])
 assert [{'count':n,'x':str(x)} for n,x in unit[s]]==[{'count':z['count'],'x':z['x']['exact']} for z in prod['sectors'][s]['unit_atoms']]
 assert (h,t)==(ex(prod['sectors'][s]['support_cap']),ex(prod['sectors'][s]['radau_node']))
 assert effective==tuple(ex(v) for v in prod['sectors'][s]['effective_physical_counts'])
 meta[s]={'h':str(h),'t':str(t),'nu_weights':[str(wh),str(wt)],'effective_counts':[str(x) for x in effective],'integer_list':[{'count':n,'x':str(x)} for n,x in unit[s]]}
def rm(s,j):
 h,t,wh,wt,_=radau[s];return wh*h**(j-3)+wt*t**(j-3)
def um(s,j):return sum(n*x**j for n,x in unit[s])
def combine(ms):
 i,o,n=ms;return {'I':i+2*o+3*n,'P':i+2*o-n,'C':i-o}
raw_checks=[]
for L in (6,8,10):
 for tag,fn in [('relaxed_center',rm),('unit_count',um)]:
  triplet=combine([fn(s,L//2) for s in multip])
  for seam,value in triplet.items():
   lo,hi=raw[L,seam];assert lo<value<hi
   rec=next(x for x in prod['raw_interval_checks'] if (x['L'],x['seam'],x['witness'])==(L,seam,tag))
   margin=min(value-lo,hi-value);assert value==ex(rec['value']) and margin==ex(rec['distance_to_nearest_raw_endpoint'])
   raw_checks.append({'L':L,'seam':seam,'witness':tag,'margin':str(margin)})
assert min(F(v['margin']) for v in raw_checks)>F('1.95e-11')
def poly(s,L):
 h,t,wh,wt,center=radau[s];k=L//2-3
 C=(h**k-t**k-k*t**(k-1)*(h-t))/(h-t)**2;B=k*t**(k-1)-2*C*t;AA=(1-k)*t**k+C*t*t
 assert AA+B*t+C*t*t==t**k and B+2*C*t==k*t**(k-1) and AA+B*h+C*h*h==h**k
 return (AA,B,C)
def polymul(a,b):
 out=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 return out
factor_checks={}
for s,L in itertools.product(multip,(10,26,100)):
 h,t,*_=radau[s];k=L//2-3;coeff=poly(s,L)
 if k==2:assert coeff==(0,0,1);continue
 fac=[sum((a+1)*t**a*h**(k-3-j-a) for a in range(k-2-j)) for j in range(k-2)]
 assert all(v>0 for v in fac)
 assert polymul(polymul([h,-F(1)],[t*t,-2*t,F(1)]),fac)==list(coeff)+[F(0)]*(k-3)+[-F(1)]
 factor_checks[f'{s}_{L}']={'degree':k,'factor_coefficients_positive':True}
bounds=[]
for L in range(10,122,2):
 outer=relaxed=integer=F(0)
 for s,multi in multip.items():
  coeff=poly(s,L);central=sum(c*v for c,v in zip(coeff,radau[s][4]));assert central==rm(s,L//2)
  upper=sum(c*mom[s][j][int(c>=0)] for c,j in zip(coeff,(3,4,5)))
  # The finite witness itself satisfies all sector endpoint enclosures.
  assert all(mom[s][j][0]<=um(s,j)<=mom[s][j][1] for j in (3,4,5))
  assert upper>=central and upper>=um(s,L//2)
  outer+=multi*upper;relaxed+=multi*central;integer+=multi*um(s,L//2)
 rec=next(v for v in prod['long_trace_comparisons'] if v['L']==L)
 assert ex(rec['rigorous_Hermite_upper'])==ceil(outer)
 assert ex(rec['relaxation_feasible_lower'])==floor(relaxed) and ex(rec['unit_count_feasible_lower'])==floor(integer)
 assert ex(rec['interval_uncertainty_gap_upper'])==ceil(outer-relaxed)
 assert ex(rec['maximum_possible_improvement_over_unit_witness'])==ceil(outer-integer)
 assert ex(rec['relative_unit_gap_upper'])==ceil((outer-integer)/outer)
 # Explicitly include outer display-rounding if comparing to the recorded upper endpoint.
 safe_gap=ceil(ceil(outer)-integer)
 bounds.append({'L':L,'outer_upper':str(ceil(outer)),'unit_trace_lower':str(floor(integer)),'raw_relaxed_optimum_bracket_gap':str(ceil(ceil(outer)-relaxed)),'maximum_improvement_of_recorded_upper':str(safe_gap),'gap_display':float(safe_gap)})
for L,claim in [(26,'0.000071643'),(100,'0.000030482')]:assert F(next(v['maximum_improvement_of_recorded_upper'] for v in bounds if v['L']==L))<F(claim)
# Small compressed block, exact even-length contributions.
tiny={L:str(F(10**15)*F(1,10**5)**L) for L in (2,3,6,8,10)}
assert tiny=={2:'100000',3:'1',6:'1/1000000000000000',8:'1/10000000000000000000000000',10:'1/100000000000000000000000000000000000'}
assert unit['trivial'][0][1]>1 and all(x<1 for s in ('complex','vector') for n,x in unit[s])
assert um('complex',3)<1 and um('vector',4)<1
finite=[]
for L in range(2,8):
 iv=[]
 for s in multip:
  lo=hi=F(0)
  for n,x in unit[s]:
   r=(F(1),F(1)) if L%2==0 else sqrtiv(x)
   lo+=n*x**(L//2)*r[0];hi+=n*x**(L//2)*r[1]
  iv.append((lo,hi))
 i,o,n=iv;pl=i[0]+2*o[0]-n[1];cl=i[0]-o[1]
 assert pl>0 and cl>0
 rec=next(z for z in prod['all_length_seam_positivity']['finite_L2_through7'] if z['L']==L)
 assert pl>=ex(rec['P_lower']) and cl>=ex(rec['C_lower'])
 finite.append({'L':L,'P_lower':str(pl),'C_lower':str(cl)})
# Independently reconstruct the strict integer correction without SymPy.
corr=js(A/'integer_correction.json');s='trivial';h,t,*_=radau[s];a,b,c=poly(s,26)
fac=[sum((a+1)*t**a*h**(7-j-a) for a in range(8-j)) for j in range(8)]
assert all(v>0 for v in fac) and fac[0]>=h**7
assert list(reversed(fac))==[F(v) for v in corr['polynomial_quotient_coefficients']]
et=eh=F(1,100000);assert 0<t-et<t+et<h-eh<h and t+et<3*h/4
variance=mom[s][5][0]-2*t*mom[s][4][1]+t*t*mom[s][3][0];dH=eh*h**7*variance
N=int((mom[s][3][1]-(h-eh)**3)//(t-et)**3);assert N==53
ge=(t+et)**3*(h-t-et)/(t**3*(h-t));effective=(h*mom[s][3][0]-mom[s][4][1])/(t**3*(h-t));K=1/(t**3*(h-t)*et*et*h**7);deficit=effective-N*ge;dT=deficit/K;delta=min(dH,dT)
assert variance>0 and deficit>0 and delta>F(149,10**16)
for name,value in [('variance_lower',variance),('large_gap_threshold',dH),('effective_tail_count_lower',effective),('g_max_near_t',ge),('outside_ratio_K',K),('count_deficit',deficit),('minimum_Hermite_slack',delta)]:assert value==ex(corr[name])
upper=sum(co*mom[s][j][int(co>=0)] for co,j in zip((a,b,c),(3,4,5)));assert ex(corr['Hermite_upper'])==upper and ex(corr['safe_improved_upper'])==upper-delta
rank=sum(multip[s]*sum(n for n,x in unit[s]) for s in unit);assert rank==10**15+562
out={'status':'PASS scoped moment optimality, explicit unit-count feasibility, and strict integer correction','seals_verified':counts,'sectors':meta,'raw_interval_checks':raw_checks,'hermite_factor_checks':factor_checks,'long_trace_comparisons':bounds,'seam_finite_checks':finite,'seam_tail_conditions':{'I_leading_x_gt1':True,'O6_lt1':True,'N8_lt1':True,'all_eigenvalues_positive':True},'tiny_block_contributions':tiny,'abstract_rank':str(rank),'integer_correction':{'delta':str(delta),'delta_display':float(delta),'simple_lower':'149/10000000000000000','near_t_count_max':N},'auxiliary96_100_contractions':'not independently reviewed or used','resources':{'cpu_seconds':time.process_time()-start,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(P/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n');print(json.dumps({'status':out['status'],'selected_bounds':[v for v in bounds if v['L'] in (26,100)],'integer_correction':out['integer_correction'],'abstract_rank':out['abstract_rank'],'resources':out['resources']},indent=2))
