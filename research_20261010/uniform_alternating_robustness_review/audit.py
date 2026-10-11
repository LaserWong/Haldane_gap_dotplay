#!/usr/bin/env python3
"""Independent exact scalar review. Read frozen data only; no producer imports."""
import copy, hashlib, json, math, os, resource, sys, time
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (30,30))
resource.setrlimit(resource.RLIMIT_AS, (256*1024**2,256*1024**2))
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
sys.set_int_max_str_digits(100000)
START=time.process_time(); WALL=time.monotonic()
HERE=Path(__file__).resolve().parent; ROOT=HERE/'snapshot'; BASE=ROOT/'research_20261010'
GRID=1<<300
EXPECTED_PRODUCER='836816261bc679b35d03e13e35141e3f7224fbbf56224ee4d428dc41b653cebd'
PINS={
'uniform_smaller_second_initialization':'fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84',
'uniform_smaller_second_initialization_review':'54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f',
'uniform_gap_0248_all_sizes_review':'5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf',
'uniform_second_thermal_full_review':'792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94',
'uniform_alternating_robustness_proposal':EXPECTED_PRODUCER}
def need(v,what):
 if not v: raise AssertionError(what)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
SNAP=read(HERE/'SNAPSHOT_SHA256.json')
for path,h in SNAP.items():need(digest(ROOT/path)==h,'snapshot hash '+path)
member_checks=0
for name,h in PINS.items():
 folder=BASE/name;need(digest(folder/'MANIFEST_SHA256.json')==h,'manifest '+name)
 for f,expected in read(folder/'MANIFEST_SHA256.json').items():
  if (folder/f).is_file():
   need(digest(folder/f)==expected,'manifest member '+name+'/'+f);member_checks+=1
producer=BASE/'uniform_alternating_robustness_proposal'
for rel,h in read(producer/'INPUT_SHA256.json').items():need(digest(ROOT/rel)==h,'producer consumed hash '+rel)
cert=read(producer/'certificate.json')
seed=next(r for r in read(BASE/'uniform_smaller_second_initialization/certificate.json')['rows'] if r['n']==32)
accepted=next(r for r in read(BASE/'uniform_smaller_second_initialization_review/scalar_results.json')['rows'] if r['n']==32)
anchor=next(r for r in read(BASE/'uniform_smaller_second_initialization_review/anchor_results.json')['rows'] if r['length']==64)
bridge=read(BASE/'uniform_gap_0248_all_sizes_review/results.json')
need(seed['anchor_length']==64 and Q(seed['beta'])==Q(49,4),'source coordinates')
S0=Q(accepted['S_seed']);T0=Q(accepted['T_2n_seed']);R=Q(anchor['total_H_numerator'])/Q(anchor['norm'])+64*Q(700741,500000)
need(Q(anchor['norm'])>0 and R==Q(anchor['shifted_total_Rayleigh'])==Q(seed['shifted_Rayleigh'])==Q(accepted['anchor_shifted_total_Rayleigh'])<0,'own64 Rayleigh')
need(S0==Q(seed['S'])==Q(cert['uniform_S_lower']) and T0==Q(seed['T'])==Q(cert['uniform_T64_lower']),'accepted source endpoints')
need(cert['uniform_seed_physical_length']==32 and cert['uniform_seed_cell_length']==16,'global seed cell map')
need(Q(cert['own_physical64_shifted_MPS_Rayleigh'])==R,'global anchor')
need(bridge['status']=='ACCEPTED stronger uniform all-size gap' and Q(bridge['gap'])==Q(31,1250) and bridge['all_integer_L_at_least']==2 and bridge['unique_ground_state'],'finite bridge premise')
# Independently recheck each even short-size physical purity actually needed here.
# The accepted .0248 theorem is not inferred merely from its seal.
need(set(range(4,26,2)) <= {r['L'] for r in bridge['cached_prefix_4_to25']},'finite prefix evidence')
def floorq(x):return Q(x.numerator*GRID//x.denominator,GRID)
def ceilq(x):return -floorq(-x)
@lru_cache(None)
def exp_bounds(x):
 if x<0:
  a,b=exp_bounds(-x);return floorq(1/b),ceilq(1/a)
 count=0
 while x>Q(1,4):x/=2;count+=1
 term=total=Q(1)
 for k in range(1,97):term=term*x/k;total+=term
 # first omitted term is t97; all later ratios <= x/98.
 lo=floorq(total);hi=ceilq(total+(term*x/97)/(1-x/98))
 for _ in range(count):lo=floorq(lo*lo);hi=ceilq(hi*hi)
 return lo,hi
@lru_cache(None)
def sqrt_bounds(x):
 need(x>=0,'sqrt domain');k=math.isqrt(x.numerator*GRID*GRID//x.denominator)
 a,b=Q(k,GRID),Q(k+1,GRID);need(a*a<=x<=b*b,'sqrt direction');return a,b
def G(x):need(0<x<=1,'G domain');return 1-(1-x)**2/(2*x*x)
# Source prefix contains26..33 under a separate list; require exact range mapping.
finite_purities={r['L']:Q(r['purity_lower']) for r in bridge['cached_prefix_4_to25']}
extra=[]
for key,val in bridge.items():
 if isinstance(val,list) and key!='cached_prefix_4_to25':
  for r in val:
   if isinstance(r,dict) and 'L' in r and 'purity_lower' in r:finite_purities[r['L']]=Q(r['purity_lower'])
for L in range(4,31,2):
 need(L in finite_purities,'finite even evidence '+str(L));v=finite_purities[L]
 need(v-exp_bounds(Q(49,4)*Q(31,1250))[1]*(1-v)>0,'finite uniform gap '+str(L))

def verify_row(row,radius,gap):
 need(Q(row['eta_radius'])==radius and Q(row['physical_gap_target'])==gap,'radius/gap target')
 need(Q(row['g_lower'])==(1-radius)/(1+radius) and Q(row['g_upper'])==(1+radius)/(1-radius),'closed interval')
 need(row['initial_cell_base']==16 and Q(row['initial_normalized_beta'])==Q(49,4),'initial cell coordinates')
 need(row['shift_per_physical_site']=='c * 700741/500000','shift')
 A=Q(9,8)*(Q(49,4)*32*radius)**2
 need(Q(row['A_at_physical32'])==A,'Gaussian exponent physical32')
 s,t=Q(row['S_lower']),Q(row['T_lower'])
 need(0<s<=S0/exp_bounds(2*A)[1] and 0<t<=T0/exp_bounds(8*A)[1],'degraded seeds')
 windows=[];prior=None
 for j,state in enumerate(row['states']):
  n=16*2**j;beta=Q(49,4)*2**j;betamax=beta*(1+radius)
  need(state['round']==j and state['cell_base']==n and state['physical_base']==2*n,'round/base map')
  need(Q(state['normalized_beta'])==beta and Q(state['physical_beta_upper'])==betamax,'temperature rescale')
  ss,tt=Q(state['S_lower']),Q(state['T_lower']);need(0<ss<=1 and 0<tt<=1,'purity domain')
  if prior is None:need((ss,tt)==(s,t),'initial values')
  else:need(ss<=G(prior[0]**2*prior[1]) and tt<=G(prior[1]**2*ss),'sequential recursion')
  K=Q(state['K_lower']);need(Q(1,2)<K<=ss*ss*tt,'inverse purity argument')
  z=sqrt_bounds(2*K-1)[0];rho=(1-z)/(1+z);d=tt/(1+rho*rho)
  own=(1-rho)*min(ss*sqrt_bounds(d)[0],d)
  C=Q(state['window_purity_lower']);need(Q(1,2)<C<=own<=1,'window lower endpoint')
  need((state['window_cell_from'],state['window_cell_to'])==(n,2*n),'every integer window')
  margin=C-exp_bounds(betamax*gap)[1]*(1-C)
  need(0<Q(state['window_margin'])<=margin,'window exponential')
  windows.append({'cells':[n,2*n],'physical_sites':[2*n,4*n],'normalized_beta':str(beta),'physical_beta_upper':str(betamax),'purity':str(C),'strict_margin':str(margin),'display_margin':float(margin)})
  prior=ss,tt
 need(prior is not None,'nonempty states')
 terminal=row['terminal'];u=max(1-ss,1-tt)
 need(terminal['cell_from']==n and terminal['physical_from']==2*n and Q(terminal['defect'])==u<=Q(1,100),'terminal coordinates/defect')
 terminal_margin=1-5*u*exp_bounds(betamax*gap)[1]
 need(0<Q(terminal['margin'])<=terminal_margin,'terminal exponential')
 small=row['finite_bridge'];low=(Q(31,1250)-90*radius)/(1+radius)
 need((small['cell_min'],small['cell_max'],small['physical_min'],small['physical_max'])==(2,15,4,30),'finite bridge range')
 need(Q(small['uniform_gap_premise'])==Q(31,1250) and Q(small['worst_gap_lower'])==low and Q(small['margin'])==low-gap>0,'finite bridge bound')
 need(row['all_integer_cells_at_least']==2 and row['unique_ground_state'],'conclusion')
 return {'status':'ACCEPTED','eta_radius':str(radius),'g_closed_interval':[row['g_lower'],row['g_upper']],'gap':str(gap),'all_integer_cells_at_least':2,'unique_ground_state':True,'finite_bridge_lower':str(low),'windows':windows,'terminal_cell_base':n,'terminal_normalized_beta':str(beta),'terminal_defect':str(u),'terminal_strict_margin':str(terminal_margin),'terminal_display_margin':float(terminal_margin)}

# Exact analytic constants for small-defect closure, independent of replay loops.
u=Q(1,100)
need((3-3*u+u*u)**2/(2*(1-u)**6)<=5,'spatial small defect')
need((2+5*u)**2/(2*(1-2*u-5*u*u)**2)<=5,'thermal small defect')
need(Q(2,5)-Q(106,25)*u-2*u*u>0 and u<=Q(1,40),'dominant-weight bound')
rows=[verify_row(row,*args) for row,args in zip(cert['rows'],[(Q(1,20000),Q(3,200)),(Q(1,12500),Q(1,200))])]
need(len(cert['rows'])==2,'two rows')
# Each corruption must fail the exact validation at the affected premise.
fixtures=[]
def rejected(label,change):
 row=copy.deepcopy(cert['rows'][0]);change(row)
 try:verify_row(row,Q(1,20000),Q(3,200))
 except AssertionError as e:fixtures.append({'case':label,'status':'REJECTED','reason':str(e)});return
 raise AssertionError('adversarial accepted: '+label)
rejected('inflated spatial seed',lambda r:r.__setitem__('S_lower','1'))
rejected('inflated thermal seed',lambda r:r.__setitem__('T_lower','1'))
rejected('wrong Gaussian length',lambda r:r.__setitem__('A_at_physical32','0'))
rejected('omit c temperature correction',lambda r:r['states'][0].__setitem__('physical_beta_upper','49/4'))
rejected('physical32 mistaken for cell32',lambda r:r['states'][0].__setitem__('cell_base',32))
rejected('wrong initial cell map',lambda r:r.__setitem__('initial_cell_base',32))
rejected('missing dyadic window',lambda r:r['states'].pop(1))
rejected('odd base inserted',lambda r:r['states'][0].__setitem__('cell_base',17))
rejected('wrong physical doubled size',lambda r:r['states'][0].__setitem__('physical_base',64))
rejected('premature terminal',lambda r:r['terminal'].__setitem__('cell_from',128))
rejected('false small defect',lambda r:r['terminal'].__setitem__('defect','0'))
rejected('inflated window purity',lambda r:r['states'][0].__setitem__('window_purity_lower','1'))
rejected('inverse purity threshold',lambda r:r['states'][0].__setitem__('K_lower','1/2'))
rejected('inflated next spatial value',lambda r:r['states'][1].__setitem__('S_lower','1'))
rejected('inflated next thermal value',lambda r:r['states'][1].__setitem__('T_lower','1'))
rejected('finite bridge hole at15',lambda r:r['finite_bridge'].__setitem__('cell_max',14))
rejected('omit extensive finite loss',lambda r:r['finite_bridge'].__setitem__('worst_gap_lower','31/1250'))
rejected('wrong designated exchange interval',lambda r:r.__setitem__('g_upper','1'))
resource_record={'hard_process_cpu_seconds':30,'hard_address_space_mib':256,'process_cpu_seconds':time.process_time()-START,'monotonic_wall_seconds':time.monotonic()-WALL,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'affinity':sorted(os.sched_getaffinity(0)),'no_physical_contractions':True,'no_eigensolver':True,'no_heat_campaign':True}
output={'status':'ACCEPTED both closed intervals, all integer M>=2','producer_manifest_sha256':EXPECTED_PRODUCER,'frozen_file_count':len(SNAP),'verified_snapshot_manifest_members':member_checks,'source_seed_exact_match':True,'own64_total_rayleigh_recomputed':str(R),'finite_uniform_even_purities_rechecked':list(range(4,31,2)),'rows':rows,'adversarial_cases':fixtures,'resources':resource_record,'limitations':['Inherited physical thermal and MPS acceptance; no fresh physical contraction or thermal recomputation.','No optimal interval/gap or thermodynamic phase-label claim.','Historical direct25 CPU enforcement exception remains unchanged and is not used in this even-size bridge.']}
(HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'status':output['status'],'rows':[{k:v[k] for k in ('g_closed_interval','gap','terminal_cell_base','terminal_display_margin')} for v in rows],'adversarial_rejections':len(fixtures),'resources':resource_record},indent=2))
