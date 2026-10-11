import os,resource
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(45,45))
import ast,json,math,time,hashlib,subprocess,itertools
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import numpy as np
from scipy.linalg import eigh
HERE=Path(__file__).resolve().parent;RES=HERE.parent;start=time.process_time();D=10**60;GRID=1<<384
load=lambda p:json.loads(p.read_text());serial=lambda m:[[str(v) for v in row] for row in m]
for filename,names in [(RES/'bilayer_symmetry_scalar_pilot/exact_pilot.py',{'down','up','sqrtlo','G','raw','advance','window','canonical','gap_witness'}),(RES/'bilayer_symmetry_intermediate_points/produce.py',{'exp','poly','root60','ref','qload','qadd','qmul','qsign','qbound','qpoly','ratios','score','certificate'}),(RES/'bilayer_symmetry_frontier_010825_0109/produce.py',{'mat','bil','make_witness','optimized_patch','optimized_numerator','diagnostic'})]:
 for node in ast.parse(filename.read_text()).body:
  if isinstance(node,ast.FunctionDef) and node.name in names:exec(compile(ast.Module(body=[node],type_ignores=[]),'accepted_cached_helpers','exec'))
def rational_vector(v,scale):
 v=v*scale;assert abs(v[0])>1e-10;v/=v[0]
 # The raw integer T is large;96bits retain its small coefficient accurately.
 return [int(round(x*2**96)) for x in v]
rt2=root60(F(2));old=load(RES/'bilayer_complete_split_H2_8x4_review/audit.json');row=load(RES/'bilayer_residual_direction_production_run/checkpoint/complete_row.json');assert row['partial'] is False
GG=np.zeros((58,58),dtype=object);GG[:57,:57]=mat(old['gram']);grow=list(map(F,row['rows']['G']));GG[57,:]=grow;GG[:,57]=grow
newks=[];newjs=[]
for oldm,key,factor,group in [(old['H_coefficients'][0],'Q_row',F(1),newks),(old['H_coefficients'][1],'A_row',F(1,2),newks),(old['H2_coefficients'][0],'Q2_row',F(1),newjs),(old['H2_coefficients'][1],'QA_AQ_row',F(1,2),newjs),(old['H2_coefficients'][2],'A2_row',F(1,4),newjs)]:
 m=np.zeros((58,58),dtype=object);m[:57,:57]=mat(oldm);v=[F(x)*factor for x in row['polynomial'][key]];m[57,:]=v;m[:,57]=v;assert np.array_equal(m,m.T);assert np.array_equal(m[:57,:57],mat(oldm));group.append(m)
assert np.array_equal(GG,GG.T) and np.array_equal(GG[:57,:57],mat(old['gram']))
old43=load(RES/'bilayer_complete_H2_8x4/complete_H2_polynomial_8x4.json');indices=[[i] if i<29 else [i,i+14] for i in range(43)]
for m,prior in [(GG,old43['gram'])]+list(zip(newjs,old43['H2_coefficients'])):
 c=[[sum(m[a,b] for a in i for b in j) for j in indices] for i in indices];assert c==mat(prior).tolist()
new=dict(geometry=[8,4],dimension=58,gram=serial(GG),H_coefficients=list(map(serial,newks)),H2_coefficients=list(map(serial,newjs)),basis='vacuum,B14,L14,R14,M14,T; T fixed using saved .11 source',scope='CONDITIONAL on independent full row review; no new physical contractions')
(HERE/'complete_58d_polynomial.json').write_text(json.dumps(new,indent=2)+'\n')
A=2*newks[1];A2=4*newjs[2];q=[0]+[2]*14+[4]*28+[6]*15
assert all(newks[0][i,j]==GG[i,j]*q[j] for i in range(58) for j in range(58));assert all(newjs[0][i,j]==GG[i,j]*q[i]*q[j] for i in range(58) for j in range(58));assert all(2*newjs[1][i,j]==A[i,j]*(q[i]+q[j]) for i in range(58) for j in range(58))
ldljobs=[('Gram58',GG),('A2_58',A2),('complete_operator_Gram116',np.block([[GG,A],[A,A2]]))]
M16=load(RES/'bilayer_split_H2_fixture_review/snapshot/producer/complete_H2_polynomial_4x4.json');M32=old;MN=load(RES/'bilayer_g0105_actual_point_review/snapshot/NUMERATOR_8x8_MATRIX.json')
base=next(x['data'] for x in load(RES/'bilayer_symmetry_scalar_pilot/snapshot/bilayer_frontier_above_010/exploration.json')['results'] if F(x['g'])==F(11,100))
results=[];target_rows=[];gains=[]
for g in [F(217,2000),F(11,100)]:
 p16,w16=optimized_patch(M16,16,g);p57,w57=optimized_patch(old,32,g);p58,w58=optimized_patch(new,32,g);numerator=optimized_numerator(g)
 gain=F(p58['ground_lower'])-F(p57['ground_lower']);assert gain>0;gains.append(float(gain))
 pivots=[F(p16['pivot']),F(p58['pivot']),F(numerator['rayleigh'])];combinations={k:str(sum(a*b for a,b in zip(w,pivots))) for k,w in [('J1',[8,0,-2]),('J2',[16,0,-4]),('C0',[0,4,-2])]}
 phys=dict(g=str(g),patches=[p16,p58],numerator_rayleigh=numerator['rayleigh'],energy_combinations=combinations,retained_counts=[49,97,1],denominator_ground_dimensions=[21,58],numerator_trial_dimension=43)
 grid=[]
 for i in range(140,281):
  beta=F(i,20);value=score(ratios(phys,beta,False),beta)
  if value is not None:grid.append((value,beta))
 record=dict(g=str(g),old57=w57,new58=w58,patch16_witness=w16,numerator_witness=numerator,physical=phys,ground_lower_gain=str(gain),ground_lower_gain_display=float(gain),old57_width=p57['ground_width'],new58_width=p58['ground_width'],successful_beta_grid_candidates=len(grid),scope='CONDITIONAL on independent full8x4 new-row review; floating proposals backed by exact rational witnesses')
 if grid:
  value,beta=max(grid);record['conditional_scalar_certificate']=certificate(phys,beta);record['float_score']=value
 else:
  ds=[diagnostic(phys,F(i,20)) for i in range(140,281)];best=max(ds,key=lambda x:(x['completed_windows'],x['rank_value'],float(F(x['states'][-1]['raw'][2])) if x.get('states') else -1.));record['best_failed_grid_diagnostic']=diagnostic(phys,F(best['beta_initial']),True);record['failure_scope']='Saved vectors and beta7..14 step.05 only; no universal obstruction.'
 K=newks[0]+g*newks[1];J=newjs[0]+g*newjs[1]+g*g*newjs[2];a=ref(32,g,2)
 ldljobs.append(('H2_g'+str(g).replace('/','_'),J))
 if g==F(11,100):
  targets=load(RES/'bilayer_pencil_scalar_assessment/result.json')['results'][0]['hypothetical_ground32_targets']
  for t in targets:
   ell=F(t['target_ground32_lower']);name='target_g011_beta'+str(t['beta']).replace('/','_');ldljobs.append((name,J-(a+ell)*K+a*ell*GG));target_rows.append(dict(name=name,g=str(g),beta=t['beta'],selected_target=str(ell),current58_ground_lower=p58['ground_lower'],shortfall=str(ell-F(p58['ground_lower'])),scope='Previously selected sufficient target, fixed r2 cutoff and58D pencil only; not an all-method obstruction'))
 # A reproducible tight rational endpoint target just above the proposed root.
 ell=F(math.ceil(float(F(p58['ground_lower']))*10**9)+1,10**9);name='near_root_target_'+str(g).replace('/','_');ldljobs.append((name,J-(a+ell)*K+a*ell*GG));target_rows.append(dict(name=name,g=str(g),selected_target=str(ell),scope='Near-root rational target for exact scoped LDL check; not claimed scalar sufficiency'))
 results.append(record);(HERE/'checkpoint.json').write_text(json.dumps(dict(results=results,cpu_seconds=time.process_time()-start),indent=2)+'\n');print('g',g,'gain',float(gain),'lower',float(F(p58['ground_lower'])),'grid',len(grid),flush=True);exp.cache_clear()
with (HERE/'ldl_input.txt').open('w') as f:
 f.write(str(len(ldljobs))+'\n')
 for name,m in ldljobs:f.write(name+' '+str(len(m))+'\n'+'\n'.join(' '.join(map(str,row)) for row in m)+'\n')
def limits():os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_CPU,(10,10));resource.setrlimit(resource.RLIMIT_AS,(64*1024**2,64*1024**2))
before=resource.getrusage(resource.RUSAGE_CHILDREN);run=subprocess.run([str(HERE/'exact_ldl'),str(HERE/'ldl_input.txt'),str(HERE/'ldl_results.json')],preexec_fn=limits,timeout=15);assert run.returncode==0;after=resource.getrusage(resource.RUSAGE_CHILDREN);childcpu=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime
ldl=load(HERE/'ldl_results.json');by={a['name']:a for a in ldl};assert by['Gram58']['PSD'] and by['Gram58']['rank_if_PSD']==58;assert by['A2_58']['PSD'] and by['complete_operator_Gram116']['PSD'];assert all(x['PSD'] for x in ldl if x['name'].startswith('H2_'))
for t in target_rows:t['LDL']=by[t['name']]
result=dict(status='CONDITIONAL_58D_CACHED_ALGEBRA_PENDING_INDEPENDENT_FULL_ROW_AUDIT',results=results,exact_checks=dict(Gram_rank=58,operator_Gram_rank=by['complete_operator_Gram116']['rank_if_PSD'],complete_operator_block_PSD=True,complete_H2_PSD_at_both_g=True,old57_all_polynomial_blocks_exact=True,old43_Gram_and_H2_compressions_exact=True,occupation_identities_exact=True,full_H_moment_block_PSD_by_invertible_congruence='For g!=0 use map [[I,Q],[0,gI/2]] on [basis,A basis]; Q acts inside the fixed-occupation trial space.'),selected_target_checks=target_rows,cpu_seconds=time.process_time()-start,exact_LDL_child_cpu_seconds=childcpu,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,no_physical_contractions=True,no_new_physical_gap_claim=True)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',result['cpu_seconds'],childcpu,result['peak_rss_kib'],flush=True)
