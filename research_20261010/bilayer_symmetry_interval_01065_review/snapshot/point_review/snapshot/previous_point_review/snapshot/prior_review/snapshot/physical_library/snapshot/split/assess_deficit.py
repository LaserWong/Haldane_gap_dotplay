import os,sys,resource,json,time,math
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
# Imported predecessors request larger limits. Clamp those calls to this task's hard caps.
real=resource.setrlimit
def clamp(which,limits):
 old=resource.getrlimit(which);cap=old[1];real(which,tuple(min(v,cap) if cap>=0 else v for v in limits))
resource.setrlimit=clamp
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;RES=HERE.parent
sys.path.insert(0,str(RES/'bilayer_frontier_above_010'))
import explore as E
import ast,types
B=types.SimpleNamespace(E=E,C=E.C,P=E.P)
ns=dict(F=F,math=math,C=E.C,exp=E.C.exp_interval)
target=json.loads((RES/'bilayer_frontier_above_010/points.json').read_text())['results'][-1]['input']
ns['TARGET']={k:F(target[k]) for k in ('J1','J2','C0')}
for name,functions in [('budget.py',{'components','ratios','raw'}),('targets.py',{'sufficient_numerator'})]:
 nodes=[x for x in ast.parse((RES/'bilayer_seed_error_budget'/name).read_text()).body if isinstance(x,ast.FunctionDef) and x.name in functions]
 exec(compile(ast.Module(body=nodes,type_ignores=[]),'cached_scalar_functions','exec'),ns)
for k in ('ratios','sufficient_numerator','TARGET'):setattr(B,k,ns[k])
B.float_path=lambda r,b:dict(status='initial_cycle_positive_only' if min(r.values())>1e-30 and ns['raw'](r) is not None else 'initial_cycle_nonpositive')
resource.setrlimit=real
C=B.C;P=B.P;start=time.time();rows=[]
opts=json.loads((HERE/'reoptimization.json').read_text())['results'];polys=[json.loads((RES/'bilayer_interval_0102_0105'/f'ground_polynomial_{s}.json').read_text()) for s in ('4x4','8x4')]
for g in (F(11,100),F(3,25)):
 d=B.E.data(g);op=[x for x in opts if F(x['g'])==g];op.sort(key=lambda x:math.prod(x['shape']))
 oldnum=C.poly(list(map(F,d['largest_base_trial']['rayleigh_coefficients'])),g);gain=oldnum-F(op[2]['split']['rayleigh']);margins=[];current={};ideal={}
 for patch,poly,new in zip(d['denominator_patches'],polys,op):
  N=patch['N'];rho=C.poly(list(map(F,poly['rayleigh_coefficients'])),g);var=C.poly(list(map(F,poly['full_residual_squared_coefficients'])),g);a=C.reference(g,N,2);first=C.reference(g,N,1);assert var>=0 and first>rho and a>rho
  low=rho-var/(a-rho);pivot=C.poly(list(map(F,patch['rayleigh_coefficients'])),g);current[f'width{N}']=pivot-low;ideal[f'width{N}']=pivot-F(new['split']['rayleigh']);assert current[f'width{N}']>0 and ideal[f'width{N}']>0
  oddmargin=min(F(m['uniform_Temple_denominator']) for m in patch['odd_band']['modes']);assert oddmargin>0
  floored=0
  for mode in patch['odd_band']['modes']:
   old=F(mode['eigen_lower_minus_ground_rayleigh_uniform_lower']);floor=first-pivot
   if floor>old:mode['eigen_lower_minus_ground_rayleigh_uniform_lower']=str(floor);floored+=1
  margins.append(dict(reference_floor_improved_odd_modes=floored,N=N,ground_identification=str(first-rho),even_Temple_denominator=str(a-rho),odd_min_cutoff_margin=str(oddmargin),fixed_g0105_polynomial_ground_lower=str(low),split_Rayleigh=str(new['split']['rayleigh']),admissible_ground_interval_width=str(F(new['split']['rayleigh'])-low)))
 tests=[]
 for beta in (F(8),F(47,5),F(11),F(13)):
  for label,sc in [('actual_fixed_residual',current),('hypothetical_ground_energies_equal_split_Rayleigh',ideal)]:
   r,cc=B.ratios(d,beta,scenario=sc,epsilon=gain);eps=max([0.]+[(math.log(float(B.TARGET[k]))-float(beta)*(float(F(d['correlated_energy_combinations'][k]['uniform_lower']))+(4 if k=='J2' else 2)*float(gain))+(8 if k in ('J1','J2') else 2)*math.log(cc[{'J1':0,'J2':1,'C0':2}[k]]['total']))/float(beta*(4 if k=='J2' else 2)) for k in B.TARGET]);row=dict(beta=str(beta),scenario=label,ratios=r,path=B.float_path(r,beta),additional_numerator_improvement_sufficient_target_float=eps,components=cc)
   if beta==F(47,5) and min(r.values())>1e-100:
    er,_=B.ratios(d,beta,scenario=sc,epsilon=gain,exact=True);ee,w=B.sufficient_numerator(er,beta);row['exact_sufficient_target']=w
   tests.append(row)
  C.exp_interval.cache_clear()
 rows.append(dict(g=str(g),physical_cutoffs=margins,new_numerator_gain_from_previous_trace_pivot=str(gain),tests=tests))
 print(g,[(x['beta'],x['scenario'],x['path']['status'],x['additional_numerator_improvement_sufficient_target_float']) for x in tests],flush=True)
 (HERE/'deficit_checkpoint.json').write_text(json.dumps(rows,indent=2,default=str)+'\n')
(HERE/'deficit.json').write_text(json.dumps(dict(status='PLANNING_EXACT_POINT_INPUT_AND_CONDITIONAL_TARGETS_ONLY_NO_NEW_ALLSIZE_CERTIFICATE',results=rows,seconds=time.time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2,default=str)+'\n')
