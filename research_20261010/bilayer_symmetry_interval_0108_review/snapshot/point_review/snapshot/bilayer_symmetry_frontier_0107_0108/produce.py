"""One bounded cached-matrix optimization pilot; stop at first exact success."""
import os,resource,math,json,time,hashlib,ast
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
os.sched_setaffinity(0,{2});resource.setrlimit(resource.RLIMIT_CPU,(115,115));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
import numpy as np
from scipy.linalg import eigh
HERE=Path(__file__).resolve().parent;RES=HERE.parent;start=time.process_time();D=10**60;GRID=1<<384
load=lambda p:json.loads(p.read_text())
for filename,names in [(RES/'bilayer_symmetry_scalar_pilot/exact_pilot.py',{'down','up','sqrtlo','G','raw','advance','window','canonical','gap_witness'}),(RES/'bilayer_symmetry_intermediate_points/produce.py',{'exp','poly','root60','ref','qload','qadd','qmul','qsign','qbound','qpoly','ratios','score','certificate'})]:
 for node in ast.parse(filename.read_text()).body:
  if isinstance(node,ast.FunctionDef) and node.name in names:exec(compile(ast.Module(body=[node],type_ignores=[]),'sealed_scalar_helpers','exec'))
rt2=root60(F(2))
seals={}
for group in ['bilayer_symmetry_intermediate_points','bilayer_split_H2_fixture_review','bilayer_complete_split_H2_8x4_review','bilayer_g0105_actual_point_review']:
 mf=RES/group/'MANIFEST_SHA256.json';seals[group]=hashlib.sha256(mf.read_bytes()).hexdigest()
 for p,h in load(mf).items():assert hashlib.sha256((mf.parent/p).read_bytes()).hexdigest()==h,p
assert seals['bilayer_symmetry_intermediate_points']=='f0964e98022793c1f200e63c290acd340539e59833a6ecffc1610b4ef08132e3'
for p,h in load(RES/'bilayer_symmetry_intermediate_points/INPUT_SHA256.json').items():assert hashlib.sha256((RES/p).read_bytes()).hexdigest()==h,p
M16=load(RES/'bilayer_split_H2_fixture_review/snapshot/producer/complete_H2_polynomial_4x4.json');M32=load(RES/'bilayer_complete_split_H2_8x4_review/audit.json');MN=load(RES/'bilayer_g0105_actual_point_review/snapshot/NUMERATOR_8x8_MATRIX.json')
base=next(x['data'] for x in load(RES/'bilayer_symmetry_scalar_pilot/snapshot/bilayer_frontier_above_010/exploration.json')['results'] if F(x['g'])==F(11,100))
def mat(m):return np.array([[F(x) for x in row] for row in m],dtype=object)
def bil(c,m):return F(np.asarray(c,dtype=object)@m@np.asarray(c,dtype=object))
def rational_vector(v,scale):
 v=v*scale;assert abs(v[0])>1e-10;v/=v[0];return [int(round(x*2**48)) for x in v]

def make_witness(c,Gm,K,J,a,r1):
 norm=bil(c,Gm);rho=bil(c,K)/norm;second=bil(c,J)/norm;var=second-rho*rho;assert norm>0 and var>=0 and rho<r1<a
 low=rho-var/(a-rho);ell=down(low-F(1,10**13));pencil=second-(a+ell)*rho+a*ell;assert pencil<0
 return dict(integer_coefficients=c,norm=str(norm),rho=str(rho),second_moment=str(second),variance=str(var),r1=str(r1),r2=str(a),ground_lower=str(low),strict_endpoint=str(ell),negative_pencil=str(pencil))

def optimized_patch(M,N,g):
 GG=mat(M['gram']);ks=list(map(mat,M['H_coefficients']));js=list(map(mat,M['H2_coefficients']));K=ks[0]+g*ks[1];J=js[0]+g*js[1]+g*g*js[2];a=ref(N,g,2);r1=ref(N,g,1)
 scale=1/np.sqrt(np.array(GG.diagonal(),dtype=float));ss=np.outer(scale,scale);GF=np.array(GG,dtype=float)*ss;KF=np.array(K,dtype=float)*ss;JF=np.array(J,dtype=float)*ss
 vals,vec=eigh(KF,GF,subset_by_index=[0,0]);energy=make_witness(rational_vector(vec[:,0],scale),GG,K,J,a,r1)
 def pencil_eig(ell):return eigh(JF-(float(a)+ell)*KF+float(a)*ell*GF,GF,subset_by_index=[0,0])
 lo=float(F(energy['ground_lower']))-.001;hi=float(F(energy['rho']))+1e-10
 assert pencil_eig(lo)[0][0]<0 and pencil_eig(hi)[0][0]>0
 for _ in range(45):
  mid=(lo+hi)/2
  if pencil_eig(mid)[0][0]<0:lo=mid
  else:hi=mid
 pe=make_witness(rational_vector(pencil_eig(lo)[1][:,0],scale),GG,K,J,a,r1)
 for witness in [energy,pe]:
  cc=witness['integer_coefficients'];nn=F(witness['norm']);rc=[bil(cc,m)/nn for m in ks];sc=[bil(cc,m)/nn for m in js];vc=[sc[0]-rc[0]**2,sc[1]-2*rc[0]*rc[1],sc[2]-rc[1]**2]
  assert poly(rc,g)==F(witness['rho']) and poly(vc,g)==F(witness['variance'])
  witness['rayleigh_coefficients']=list(map(str,rc));witness['full_second_moment_coefficients']=list(map(str,sc));witness['full_variance_coefficients']=list(map(str,vc))
 kind,w=max([('energy',energy),('pencil',pe)],key=lambda t:F(t[1]['ground_lower']));pivot=F(energy['rho']);lower=F(w['ground_lower']);assert lower<=pivot
 odd=[];details=[]
 for mode in base['denominator_patches'][0 if N==16 else 1]['odd_band']['modes']:
  assert qsign(qload(mode['gram_symbol']))>0;theta=qpoly(mode['theta_coefficients'],g);variance=qpoly(mode['residual_squared_coefficients'],g);assert qsign(variance)>=0
  l,u=qbound(theta);vl,vu=qbound(variance);assert u<a;ell=max(r1,l-max(F(0),vu)/(a-u));odd.append(ell-pivot)
  details.append(dict(momentum=mode['momentum'],gram_symbol=mode['gram_symbol'],theta=list(map(str,theta)),variance=list(map(str,variance)),cutoff_margin=str(a-u),lower=str(ell)))
 assert len(odd)==N
 patch=dict(N=N,ground_trial_dimension=len(GG),ground_selection=kind,rho=w['rho'],variance=w['variance'],r1=str(r1),r2=str(a),ground_lower=str(lower),pivot=str(pivot),ground_width=str(pivot-lower),global_ground_margin=str(r1-F(w['rho'])),odd_min_cutoff_margin=str(min(F(m['cutoff_margin']) for m in details)),odd=list(map(str,odd)),odd_details=details,tail=[str(ref(N,g,q)-pivot) for q in range(2,N+1)])
 witness=dict(N=N,g=str(g),dimension=len(GG),energy_optimized=energy,pencil_optimized=pe,selected=kind,float_pencil_root_bracket=[lo,hi],exact_lower_gain_over_energy=str(F(pe['ground_lower'])-F(energy['ground_lower'])))
 return patch,witness

def optimized_numerator(g):
 GG=mat(MN['gram']);ks=list(map(mat,MN['affine_A']));K=ks[0]+g*ks[1];scale=1/np.sqrt(np.array(GG.diagonal(),dtype=float));ss=np.outer(scale,scale)
 val,vec=eigh(np.array(K,dtype=float)*ss,np.array(GG,dtype=float)*ss,subset_by_index=[0,0]);c=rational_vector(vec[:,0],scale);norm=bil(c,GG);rho=bil(c,K)/norm;assert norm>0
 return dict(N=64,g=str(g),dimension=len(c),integer_coefficients=c,norm=str(norm),rayleigh=str(rho),rayleigh_coefficients=[str(bil(c,m)/norm) for m in ks],retained_states=1,full_dimension=str(4**64))

# Pin the accepted predecessor and exact square theorems without modifying them.
for group,expected in [('bilayer_symmetry_interval_01065_review','f6328b280cad0963dd70aa90c71b12ca88fbbf6a2b808376d2948e6aeae77fe2'),('bilayer_square_symmetry_window_review','890e942c8a7e37cbefc5b8de52f40f8d61cbfefe76e03f8a71f9dec8d66648cc'),('bilayer_square_symmetry_recurrence_review','21577fcf285cc7e53c6c4acdbdfa1086f1b7dd88f6f30c4e87e0ebf5f0ac5e83')]:
 mf=RES/group/'MANIFEST_SHA256.json';assert hashlib.sha256(mf.read_bytes()).hexdigest()==expected;seals[group]=expected
 for p,h in load(mf).items():assert hashlib.sha256((mf.parent/p).read_bytes()).hexdigest()==h,p
def diagnostic(phys,beta,exact=False):
 r=ratios(phys,beta,exact);abc=raw(r,exact);states=[]
 if abc is None:return dict(beta_initial=str(beta),failed_gate='initial_raw_positivity',ratios={k:str(v) for k,v in r.items()},completed_windows=0,rank_value=-1.)
 for j in range(20):
  can=canonical(abc,exact);u=max(1-x for x in can);v=window(abc,exact)
  states.append(dict(n=8*2**j,raw=list(map(str,abc)),window_lower=str(v),window_margin=str(v-F(1,2)),common_defect=str(u)))
  if 0<u<=F(1,500):return dict(beta_initial=str(beta),states=states,completed_windows=j,failed_gate='none',rank_value=1.)
  if v<=F(1,2):return dict(beta_initial=str(beta),ratios={k:str(v) for k,v in r.items()},states=states,completed_windows=j,failed_gate='finite_window_purity_above_half',exact_margin=str(v-F(1,2)),rank_value=float(v))
  nxt=advance(abc,exact)
  if nxt is None:return dict(beta_initial=str(beta),ratios={k:str(v) for k,v in r.items()},states=states,completed_windows=j+1,failed_gate='next_raw_positivity',rank_value=-1.)
  abc=nxt
 return dict(beta_initial=str(beta),states=states,completed_windows=20,failed_gate='no_terminal_gate_within_20_cycles',rank_value=-1.)
out=[]
for g in map(F,['107/1000','43/400','27/250']):
 patches=[];witnesses=[]
 for M,N in [(M16,16),(M32,32)]:p,w=optimized_patch(M,N,g);patches.append(p);witnesses.append(w)
 numerator=optimized_numerator(g);rr=[F(p['pivot']) for p in patches]+[F(numerator['rayleigh'])]
 combinations={k:str(sum(a*b for a,b in zip(w,rr))) for k,w in [('J1',[8,0,-2]),('J2',[16,0,-4]),('C0',[0,4,-2])]}
 phys=dict(g=str(g),patches=patches,numerator_rayleigh=numerator['rayleigh'],energy_combinations=combinations,retained_counts=[49,97,1],denominator_ground_dimensions=[21,57],numerator_trial_dimension=43)
 grid=[]
 for i in range(140,281):
  beta=F(i,20);value=score(ratios(phys,beta,False),beta)
  if value is not None:grid.append((value,beta))
 row=dict(g=str(g),physical=phys,matrix_witnesses=witnesses,numerator_witness=numerator,successful_grid_proposals=len(grid))
 if grid:
  sc,beta=max(grid);row['certificate']=certificate(phys,beta);row['float_score']=sc
 else:
  diagnostics=[diagnostic(phys,F(i,20)) for i in range(140,281)]
  best=max(diagnostics,key=lambda x:(x['completed_windows'],x['rank_value']))
  row['best_failed_grid_diagnostic']=diagnostic(phys,F(best['beta_initial']),True)
  row['failure_scope']='Only tested beta grid 7..14 step .05, saved vectors and specified recurrence; not a universal no-go.'
 out.append(row);(HERE/'checkpoint.json').write_text(json.dumps(dict(results=out,cpu_seconds=time.process_time()-start),indent=2)+'\n');print(g,'grid',len(grid),'gap',row.get('certificate',{}).get('gap_display'),flush=True)
 if 'certificate' not in row:break
 exp.cache_clear()
result=dict(status='BOUNDED_OPTIMIZED_MATRIX_POINT_CANDIDATE_PENDING_INDEPENDENT_REVIEW',results=out,source_seals=seals,stop_at_first_failed_grid_candidate=True,cpu_seconds=time.process_time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,no_full_support_contractions=True,floating_eigenvectors_proposals_only=True)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
