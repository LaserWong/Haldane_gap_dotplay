#!/usr/bin/env python3
"""Exact rational verification of a finite-moment counterexample.
No floating fit or external spectrum is trusted by this verification.
"""
import json,math,hashlib,resource,time
from fractions import Fraction as F
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
P=Path(__file__).resolve().parent;start=time.time()
rows=json.loads((P/'full_integer_witnesses.json').read_text());spectra={}
for row in rows:
 assert row['beta']==8 and row['a']=='5951/1250'
 n=row['counts'];xs=list(map(F,row['nodes']))
 assert len(n)==len(xs) and all(type(z)is int and z>0 for z in n)
 assert xs[0]==({'J':F(103,100),'N':F(51,50)}[row['sector']])
 assert all(abs(x)<F(3,4)for x in xs[1:])
 spectra[row['sector']]=list(zip(n,xs))
def ms(s,k):return sum(n*x**k for n,x in spectra[s])
def z(t,k):return ms('J',k)+(3 if t=='I' else -1)*ms('N',k)
checks=[]
for r in json.loads((P/'copied_beta8_lower_trace_intervals.json').read_text()):
 actual=z(r['twist'],r['n']);lo,hi=F(r['lower']),F(r['upper'])
 assert lo<actual<hi,(r['n'],r['twist'])
 checks.append({'L':r['n'],'twist':r['twist'],'strict_interval_inclusion':True,'actual_rational':str(actual),'margin_to_nearer_endpoint':str(min(actual-lo,hi-actual))})
old=json.loads((P.parent/'spin2_heat/seed_feasibility/exploratory_moment_inputs.json').read_text())[1]
prospective=[]
for k,epsilon in [(9,F(6,10**6)),(10,F(5,10**5))]:
 j,n=[F(str(old['moments'][s][str(k)]))for s in ['J','N']]
 for tw,mid in [('I',j+3*n),('P',j-n)]:
  actual=z(tw,k)
  assert abs(actual-mid)<F(1,10**48)<epsilon
  prospective.append({'L':k,'twist':tw,'center':str(mid),'prospective_absolute_error_radius':str(epsilon),'actual_error':str(abs(actual-mid)),'strict_inclusion':True})
# All-length positivity from a finite check and a rigorous geometric tail bound.
a,b,r=F(103,100),F(51,50),F(3,4)
CJ=sum(n*x**10 for n,x in spectra['J'][1:]);CN=sum(n*x**10 for n,x in spectra['N'][1:])
K=32
finite=[]
for k in range(2,K):
 for tw in ['I','P']:
  val=z(tw,k);assert val>0,(k,tw)
  finite.append({'L':k,'twist':tw,'positive':True})
tail_I=a**K+3*b**K-(CJ+3*CN)*r**(K-10)
tail_P=a**K-b**K-(CJ+CN)*r**(K-10)
assert tail_I>0 and tail_P>0
# At larger k the positive leading terms increase and the geometric tails decrease.
# a^(k+1)-b^(k+1)>a^k-b^k follows from a>b>1.
# Thus these inequalities prove both traces positive at every integer k>=K.
lengths=[]
for L in [128,256,512,1024]:
 spatial=z('I',L)/z('I',L//2)**2
 sp_lo=F(math.floor(float(spatial)*10**9),10**9)
 assert sp_lo<spatial<sp_lo+F(1,10**9)
 # Odd Taylor truncation is a lower bound for exp(-x), by the signed Lagrange remainder.
 x=F(8*L)*F(41,100000)
 exp_negative_lower=sum((-x)**j/F(math.factorial(j))for j in range(42))
 assert exp_negative_lower>0
 # Avoid huge rational output: accept a simpler downward rounded bound after exact comparison.
 unshifted_leading=a**L+3*b**L
 shifted_leading=unshifted_leading*exp_negative_lower
 lower=F(math.floor(float(shifted_leading)*10**6),10**6)
 while lower>=shifted_leading:lower-=F(1,10**6)
 assert lower>1
 # Z at these even lengths >= leading sum. At 2beta, the I MPS trial numerator = its beta trace lower squared.
 lengths.append({'L':L,'spatial_purity_display':float(spatial),'spatial_purity_interval':str((F(math.floor(float(spatial)*10**9),10**9),F(math.floor(float(spatial)*10**9)+1,10**9))),'shifted_Z_lower_rational':str(lower),'best_possible_numerator_one_thermal_certificate_upper_display':float(1/lower**2),'N_sector_shifted_leading_mass_lower_display':float(3*b**L*exp_negative_lower)})
result={'status':'EXACT_RATIONAL_INTERVAL_FEASIBLE_COUNTEREXAMPLE_TO_SPECIFIED_FINITE_MOMENT_RELAXATION','scope':'spin-2 beta8 I/P finite moments2..10, real spectra, integer multiplicities, D2 and SO3 singlet/triplet realization, positive I/P traces at every integer L>=2; NOT a Heisenberg spectrum','missing_constraints':['Existing C moments are NOT imposed by this exact witness','No beta/2beta physical semigroup consistency is imposed','No physical locality or quantum-transfer-operator complete positivity construction is claimed'],'all_lower_moment_interval_inclusions':True,'lower_moment_checks':checks,'higher_moment_prospective_checks':prospective,'all_length_positivity':{'finite_checks':finite,'tail_start':K,'nonleading_modulus_upper':'3/4','remainder_moment10_J':str(CJ),'remainder_moment10_N':str(CN),'tail_I_margin_at32':str(tail_I),'tail_P_margin_at32':str(tail_P)},'spectrum_dimensions':{s:sum(n for n,x in spec)for s,spec in spectra.items()},'length_tests':lengths,'seconds':time.time()-start}
(P/'exact_witness_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['lower_moment_checks','all_length_positivity','length_tests']},indent=2))
for v in lengths:print({k:w for k,w in v.items() if k!='spatial_purity_rational'})
