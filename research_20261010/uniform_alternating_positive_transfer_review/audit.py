#!/usr/bin/env python3
"""Independent positive-transfer scalar review; frozen data, no producer imports."""
import copy,hashlib,json,math,os,resource,sys,time
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(30,30));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});sys.set_int_max_str_digits(100000)
START=time.process_time();WALL=time.monotonic();HERE=Path(__file__).resolve().parent;ROOT=HERE/'snapshot';BASE=ROOT/'research_20261010';GRID=1<<600;PGRID=10**120
EXPECTED='ea050102bb50eea1a287e7e674de0f43aa091a4fcd17a3d8279870f5e26ab529'
PINS={'uniform_alternating_positive_transfer':EXPECTED,'uniform_smaller_second_initialization':'fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84','uniform_smaller_second_initialization_review':'54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f','uniform_gap_0248_all_sizes_review':'5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf','uniform_second_thermal_full_review':'792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94','uniform_alternating_robustness_proposal':'836816261bc679b35d03e13e35141e3f7224fbbf56224ee4d428dc41b653cebd','uniform_alternating_robustness_review':'7c819d4758ee43bedba3298a15735d981f7b42ffeeabff40be8dd6a9e4e8bdf0','uniform_alternating_positive_cell_review':'abb8e04fa7478e939d18c831a3a4b201c0ec6baf9b8e3e494b5b867a4347f872'}
def require(v,s):
 if not v:raise AssertionError(s)
def js(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
snapshot=js(HERE/'SNAPSHOT_SHA256.json')
for f,h in snapshot.items():require(sha(ROOT/f)==h,'snapshot '+f)
member_count=0
for name,pin in PINS.items():
 folder=BASE/name;require(sha(folder/'MANIFEST_SHA256.json')==pin,'source manifest '+name)
 for f,h in js(folder/'MANIFEST_SHA256.json').items():require(sha(folder/f)==h,'source member '+name+'/'+f);member_count+=1
prod=BASE/'uniform_alternating_positive_transfer'
for f,h in js(prod/'INPUT_SHA256.json').items():require(sha(ROOT/f)==h,'producer input '+f)
cert=js(prod/'certificate.json');require(cert['old_accepted_intervals_preserved'],'old intervals retained')
require(cert['source_uniform_seed_physical_lengths']==[30,32,34] and cert['source_anchor_physical_lengths']==[60,64,68],'global physical source labels')
require(cert['linear_trial_dimension']==1 and cert['MPS_bond_dimension']==26,'trial dimensions')
seeds={r['n']:r for r in js(BASE/'uniform_smaller_second_initialization/certificate.json')['rows']}
accepted={r['n']:r for r in js(BASE/'uniform_smaller_second_initialization_review/scalar_results.json')['rows']}
anchors={r['length']:r for r in js(BASE/'uniform_smaller_second_initialization_review/anchor_results.json')['rows']}
bridge=js(BASE/'uniform_gap_0248_all_sizes_review/results.json');require(Q(bridge['gap'])==Q(31,1250) and bridge['all_integer_L_at_least']==2 and bridge['unique_ground_state'],'uniform finite gap source')
source={}
for n in [30,32,34]:
 a=anchors[2*n];r=Q(a['total_H_numerator'])/Q(a['norm'])+2*n*Q(700741,500000)
 require(Q(a['norm'])>0 and r==Q(a['shifted_total_Rayleigh'])==Q(seeds[n]['shifted_Rayleigh'])==Q(accepted[n]['anchor_shifted_total_Rayleigh'])<0,'own anchor '+str(n))
 require(Q(seeds[n]['beta'])==Q(49,4) and seeds[n]['anchor_length']==2*n and accepted[n]['anchor_length']==2*n,'source beta/anchor '+str(n))
 s=Q(seeds[n]['S']);t=Q(seeds[n]['T']);require(s==Q(accepted[n]['S_seed']) and t==Q(accepted[n]['T_2n_seed']),'source accepted seed '+str(n))
 source[n]=(s,t,r)
def down(x):return Q(x.numerator*GRID//x.denominator,GRID)
def up(x):return -down(-x)
def pdown(x):return Q(x.numerator*PGRID//x.denominator,PGRID)
@lru_cache(None)
def exp_bounds(x):
 if x<0:
  lo,hi=exp_bounds(-x);return down(1/hi),up(1/lo)
 halvings=0
 while x>Q(1,4):x/=2;halvings+=1
 term=total=Q(1)
 for k in range(1,113):term=term*x/k;total+=term
 lo=down(total);hi=up(total+(term*x/113)/(1-x/114))
 for _ in range(halvings):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi
@lru_cache(None)
def root(x):
 require(x>=0,'sqrt domain');k=math.isqrt(x.numerator*GRID*GRID//x.denominator);lo,hi=Q(k,GRID),Q(k+1,GRID)
 require(lo*lo<=x<=hi*hi,'sqrt bounds');return lo,hi
def G(x):require(0<x<=1,'G domain');return 1-(1-x)**2/(2*x*x)
# Recheck precisely every even physical finite prefix used by any of the rows.
finite={r['L']:Q(r['purity_lower']) for key in ['cached_prefix_4_to25','new_direct26_to33'] for r in bridge[key]}
for L in range(4,33,2):
 C=finite[L];require(C-exp_bounds(Q(49,4)*Q(31,1250))[1]*(1-C)>0,'actual uniform finite purity '+str(L))
SPECS=[(32,Q(1,20000),Q(1,50)),(32,Q(7,100000),Q(3,200)),(32,Q(17,200000),Q(1,100)),(32,Q(9,100000),Q(1,200)),(34,Q(69,1000000),Q(3,200)),(34,Q(89,1000000),Q(1,200)),(30,Q(1,25000),Q(3,200)),(30,Q(7,100000),Q(1,200))]
def verify(row,n0,radius,gap):
 s0,t0,ray=source[n0];cell0=n0//2
 require(row['initial_physical_base']==n0 and row['initial_cell_base']==cell0>=2 and n0==2*cell0,'initial cell map')
 require(Q(row['eta_radius'])==radius and Q(row['physical_gap_target'])==gap,'radius and target')
 require(Q(row['g_lower'])==(1-radius)/(1+radius) and Q(row['g_upper'])==(1+radius)/(1-radius),'closed interval endpoints')
 require(Q(row['uniform_S_lower'])==s0 and Q(row['uniform_T_lower'])==t0,'row source endpoints')
 require(row['anchor_physical_length']==2*n0 and Q(row['shifted_anchor_Rayleigh'])==ray,'own physical anchor')
 require(Q(row['initial_normalized_beta'])==Q(49,4) and row['shift_per_physical_site']=='c * 700741/500000','initial beta/shift')
 A=Q(9,8)*(Q(49,4)*n0*radius)**2;require(Q(row['A_at_physical_seed'])==A,'physical Gaussian exponent')
 s,t=Q(row['S_lower']),Q(row['T_lower']);require(0<s<=s0/exp_bounds(2*A)[1] and 0<t<=t0/exp_bounds(8*A)[1],'degraded seed direction')
 prior=None;windows=[]
 for j,st in enumerate(row['states']):
  cell=cell0*2**j;beta=Q(49,4)*2**j;maxbeta=beta*(1+radius)
  require(st['round']==j and st['cell_base']==cell and st['physical_base']==2*cell,'state cell/physical coordinates')
  require(Q(st['normalized_beta'])==beta and Q(st['physical_beta_upper'])==maxbeta,'physical temperature scaling')
  ss,tt=Q(st['S_lower']),Q(st['T_lower']);require(0<ss<=1 and 0<tt<=1,'purity domain')
  require(ss==pdown(ss) and tt==pdown(tt),'120-digit endpoint grid')
  if prior is None:require((ss,tt)==(s,t),'initial recorded state')
  else:
   expected_s=pdown(G(prior[2]));require(ss==expected_s,'exact spatial update')
   expected_t=pdown(G(pdown(prior[1]**2*ss)));require(tt==expected_t,'exact sequential thermal update')
  K=Q(st['K_lower']);require(0<K<=1 and K==pdown(ss*ss*tt),'exact joint endpoint')
  own=min(ss*root(tt)[0],tt);C=Q(st['window_purity_lower']);require(Q(1,2)<C<=own<=1,'positive-cell window lower bound')
  require(C==pdown(C),'window grid')
  require((st['window_cell_from'],st['window_cell_to'])==(cell,2*cell),'complete integer window')
  margin=C-exp_bounds(maxbeta*gap)[1]*(1-C);require(0<Q(st['window_margin'])<=margin,'directed window margin')
  windows.append({'cell_interval':[cell,2*cell],'physical_even_interval':[2*cell,4*cell],'normalized_beta':str(beta),'physical_beta_upper':str(maxbeta),'S':str(ss),'T':str(tt),'positive_window_purity':str(C),'strict_margin':str(margin),'display_margin':float(margin)})
  prior=(ss,tt,K)
 require(prior is not None,'nonempty states');end=row['terminal'];u=max(1-ss,1-tt)
 require(end['cell_from']==cell and end['physical_from']==2*cell and Q(end['defect'])==u<=Q(1,100),'terminal base and defect')
 tm=1-5*u*exp_bounds(maxbeta*gap)[1];require(0<Q(end['margin'])<=tm,'directed terminal margin')
 fb=row['finite_bridge'];low=(Q(31,1250)-3*(n0-2)*radius)/(1+radius)
 require((fb['cell_min'],fb['cell_max'],fb['physical_min'],fb['physical_max'])==(2,cell0-1,4,n0-2),'complete finite bridge')
 require(Q(fb['uniform_gap_premise'])==Q(31,1250) and Q(fb['worst_gap_lower'])==low and Q(fb['margin'])==low-gap>0,'finite Weyl bound')
 require(row['all_integer_cells_at_least']==2 and row['unique_ground_state'],'all-cell conclusion')
 return {'status':'ACCEPTED','physical_seed':n0,'cell_seed':cell0,'own_anchor_physical_length':2*n0,'eta_radius':str(radius),'g_closed_interval':[row['g_lower'],row['g_upper']],'gap':str(gap),'all_integer_cells_at_least':2,'unique_ground_state':True,'finite_bridge_lower':str(low),'finite_bridge_margin':str(low-gap),'windows':windows,'terminal_cell':cell,'terminal_physical':2*cell,'terminal_normalized_beta':str(beta),'terminal_defect':str(u),'terminal_strict_margin':str(tm),'terminal_display_margin':float(tm)}
require(len(cert['rows'])==len(SPECS),'exact row count')
rows=[verify(row,*spec) for row,spec in zip(cert['rows'],SPECS)]
# Exact recurrence constants inherited by the odd/even positive-cell tail.
u=Q(1,100);require(Q(9,2)/(1-3*u)**2<5,'small-defect constant');require(2*u+5*u*u<=3*u,'thermal small-defect argument')
fixtures=[]
def reject(label,index,change):
 r=copy.deepcopy(cert['rows'][index]);change(r)
 try:verify(r,*SPECS[index])
 except AssertionError as e:fixtures.append({'case':label,'status':'REJECTED','reason':str(e)});return
 raise AssertionError('corruption accepted: '+label)
reject('inflated initial S',0,lambda r:r.__setitem__('S_lower','1'))
reject('inflated initial T',0,lambda r:r.__setitem__('T_lower','1'))
reject('missing beta/c correction',0,lambda r:r['states'][0].__setitem__('physical_beta_upper','49/4'))
reject('wrong Gaussian physical length',0,lambda r:r.__setitem__('A_at_physical_seed','0'))
reject('wrong g endpoint',3,lambda r:r.__setitem__('g_upper','1'))
reject('physical seed relabeled as cell seed',0,lambda r:r.__setitem__('initial_cell_base',32))
reject('missing intermediate window',0,lambda r:r['states'].pop(2))
reject('wrong odd cell17 base',4,lambda r:r['states'][0].__setitem__('cell_base',16))
reject('wrong odd cell15 base',6,lambda r:r['states'][0].__setitem__('cell_base',16))
reject('wrong anchor64 for physical30',6,lambda r:r.__setitem__('anchor_physical_length',64))
reject('wrong own Rayleigh',6,lambda r:r.__setitem__('shifted_anchor_Rayleigh',str(source[32][2])))
reject('inflated joint endpoint',0,lambda r:r['states'][0].__setitem__('K_lower','1'))
reject('inflated spatial update',0,lambda r:r['states'][1].__setitem__('S_lower','1'))
reject('inflated thermal update',0,lambda r:r['states'][1].__setitem__('T_lower','1'))
reject('premature terminal',0,lambda r:r['terminal'].__setitem__('cell_from',16))
reject('erased late defect',6,lambda r:r['terminal'].__setitem__('defect','0'))
reject('late purity rounded to one',6,lambda r:r['states'][-1].__setitem__('window_purity_lower','1'))
reject('60-digit floor substituted for late S',6,lambda r:r['states'][-1].__setitem__('S_lower',str(1-Q(1,10**60))))
reject('short bridge misses cell16',4,lambda r:r['finite_bridge'].__setitem__('cell_max',15))
reject('omit finite perturbation loss',0,lambda r:r['finite_bridge'].__setitem__('worst_gap_lower','31/1250'))
reject('nonpositive recurrence domain',0,lambda r:r['states'][0].__setitem__('S_lower','0'))
reject('wrong terminal physical scale',0,lambda r:r['terminal'].__setitem__('physical_from',r['terminal']['cell_from']))
preliminary=js(prod/'preliminary_certificate.json');prelim_status=[{'physical_seed':r['initial_physical_base'],'radius':r['eta_radius'],'gap':r['physical_gap_target'],'status':r['status']} for r in preliminary['rows']]
require(any(r['status']!='EXACT_PRODUCER_PASS_INDEPENDENT_REVIEW_REQUIRED' for r in preliminary['rows']),'preliminary failures preserved')
output={'status':'ACCEPTED all eight positive-cell interval certificates','producer_manifest_sha256':EXPECTED,'positive_cell_structural_review':PINS['uniform_alternating_positive_cell_review'],'snapshot_files':len(snapshot),'verified_manifest_members':member_count,'finite_uniform_even_purities_rechecked':list(range(4,33,2)),'rows':rows,'adversarial_rejections':fixtures,'preliminary_statuses_preserved_as_diagnostics':prelim_status,'new_physical_work':False,'uniform_all_physical_lengths_gap_0248_unchanged':True,'resources':{'hard_CPU_seconds':30,'hard_address_space_MiB':256,'process_CPU_seconds':time.process_time()-START,'monotonic_wall_seconds':time.monotonic()-WALL,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'affinity':sorted(os.sched_getaffinity(0))},'limitations':['Physical thermal and own60/64/68 MPS inputs are inherited accepted evidence; no physical recomputation.','These are sufficient nested neighborhoods, not optimal radii, actual gaps or phase labels.','Preliminary 60-digit failures are finite-recipe diagnostics, not no-go statements.','Producer historical resource accounting is preserved; this review measures only its own new scalar run.']}
(HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'status':output['status'],'rows':[{k:r[k] for k in ['physical_seed','cell_seed','eta_radius','gap','terminal_cell','terminal_display_margin']} for r in rows],'adversarial_rejections':len(fixtures),'source_members':member_count,'resources':output['resources']},indent=2))
