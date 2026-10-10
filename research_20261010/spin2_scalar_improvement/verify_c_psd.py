"""Independent from the LP/refinement: exact positive-measure moment checks."""
from pathlib import Path
from fractions import Fraction as F
import json,resource
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
P=Path(__file__).resolve().parent
w=json.loads((P/'c_aware_psd_rational_witness.json').read_text());m={s:[]for s in ['I','O','R']}
for s,xs in w['fixed_unit_atoms'].items():m[s].extend((F(1),F(x))for x in xs)
for r in w['items']:
 v,x=F(r['weight']),F(r['node']);assert v>0;m[r['sector']].append((v,x))
def ms(s,k):return sum(v*x**k for v,x in m[s])
def tr(t,k):
 I,O,R=[ms(s,k)for s in ['I','O','R']]
 return {'I':I+5*O+3*R,'P':I+O-R,'C':I-O}[t]
checks=[]
for r in json.loads((P/'copied_beta8_all_trace_intervals.json').read_text()):
 assert F(r['lower'])<tr(r['twist'],r['n'])<F(r['upper'])
 checks.append([r['n'],r['twist']])
old=json.loads((P.parent/'spin2_heat/seed_feasibility/exploratory_moment_inputs.json').read_text())[1]
for k in [9,10]:
 j,n=[F(str(old['moments'][s][str(k)]))for s in ['J','N']]
 assert abs(tr('I',k)-j-3*n)<F(1,10**50)
 assert abs(tr('P',k)-j+n)<F(1,10**50)
result={'status':'EXACT_RATIONAL_POSITIVE_MEASURE_CHECK_PASSED','all_21_lower_trace_interval_checks':checks,'higher_moment_error_upper':'1/10^50','fixed_unit_atoms':w['fixed_unit_atoms'],'residual_integer_multiplicity':False,'all_length_trace_positivity_checked':False,'independent_audit':'pending or not requested'}
(P/'c_aware_psd_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
