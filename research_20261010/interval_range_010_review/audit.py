#!/usr/bin/env python3
"""Independent exact closed-interval extension audit; producer JSON is data only."""
import os,sys,resource
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
try:os.sched_setaffinity(0,{6})
except OSError:os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,importlib.util,ast,time,math
HERE=Path(__file__).resolve().parent;R=HERE.parent;ROOT=R.parent;S=HERE/'snapshot'
OUT=Path(os.environ.get('REVIEW_OUTPUT',str(HERE/'results')));OUT.mkdir(parents=True,exist_ok=True)
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,x):(OUT/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def seal(p,h):
 assert sha(p)==h,('manifest',str(p));r=load(p);fs=r.get('files',r)
 for f,v in fs.items():assert sha(p.parent/f)==v,('file',f)
 return len(fs)
PINS=load(HERE/'PINS.json')
assert PINS['old_review']=='09937dcdee71981b15990ff2696a72eafb5d4967e6cbae9d71392c9b802d2334'
assert PINS['complete_review']=='47ca2166342038a845f45d774bd9e2d91429496235df6e6d0fc39fb678a2b081'
def verify():
 rows={}
 for name,key in [('interval_range_009_review','old_review'),('bilayer_complete_residual_8x4_review','complete_review')]:rows[name]=seal(R/name/'MANIFEST_SHA256.json',PINS[key])
 for f,d in load(R/'bilayer_complete_residual_8x4_review/INPUT_SHA256.json').items():assert sha(R/'bilayer_complete_residual_8x4_review'/f)==d
 for name,v in load(R/'bilayer_complete_residual_8x4_review/DEPENDENCIES.json').items():seal(R/name/v['seal'],v['sha256'])
 assert sha(HERE/'PRODUCER_FREEZE.json')==PINS['producer']
 rows['producer']=seal(R/'interval_range_010/FROZEN_MANIFEST.json',PINS['producer'])
 for f,h in load(HERE/'PRODUCER_FREEZE.json')['files'].items():assert sha(S/f)==h
 seal(S/'PHYSICAL_MANIFEST.json',PINS['producer_physical']);seal(S/'SCALAR_MANIFEST.json',PINS['producer_scalar'])
 for f,h in load(S/'INPUT_SHA256.json').items():assert sha(ROOT/f)==h,('input',f)
 for name in ['fixed_vector_coupling_polynomials.json','ground_8x4_trial.json']:
  assert sha(S/name)==sha(R/'bilayer_complete_residual_8x4'/name)
 for row in load(S/'INHERITED_SEALS.json'):seal(R/row['folder']/row['manifest'],row['sha256'])
 return rows
VERIFIED=verify()
def module(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
N=module('accepted_interval009',R/'interval_range_009_review/audit.py');A=N.A;E=N.E;np=E.np
N.save=lambda n,x:save('inherited009_'+n,x);A.save=lambda n,x:save('inherited0085_'+n,x)
try:os.sched_setaffinity(0,{6})
except OSError:pass
src=(R/'interval_range_009_review/scalar_record.py').read_text().replace('F(17,200)<=lo<hi<=F(9,100)','F(9,100)<=lo<hi<=F(1,10)')
assert ast.dump(ast.parse(src),include_attributes=False)==ast.dump(ast.parse((HERE/'scalar_record.py').read_text()),include_attributes=False)
FP=module('independent_fixed_polynomial',HERE/'fixed_polynomial.py').RESULT
# Check decomposition is the sealed independent implementation, with only path/output changes.
fs=(R/'bilayer_complete_residual_8x4_review/audit_polynomial.py').read_text();fs=fs[:fs.index('out=dict(')].replace('R=Path(__file__).resolve().parent;P=R.parent',"R=Path(__file__).resolve().parent.parent/'bilayer_complete_residual_8x4_review';P=R.parent")
assert (HERE/'fixed_polynomial.py').read_text().startswith(fs)
FIXED_REPORT=[]
def check_fixed(t,lo,hi):
 assert t['geometry']==[8,4] and t['N']==32 and t['trial_dimension']==43
 assert F(t['center'])==(lo+hi)/2 and t['integer_coefficients']==FP['coefficients']
 assert F(t['integer_metric_norm'])==FP['norm']>0
 rho=FP['mean'];var=FP['variance'];A.eqseq(rho,t['rayleigh_coefficients']);A.eqseq(FP['second'],t['full_second_moment_coefficients']);A.eqseq(var,t['full_residual_squared_coefficients'])
 assert t['max_trial_triplet_number']==6 and t['max_full_residual_triplet_number']==8
 assert t['complete_residual_source']=='bilayer_complete_residual_8x4/fixed_vector_coupling_polynomials.json'
 assert var[2]>0 and var[0]>0 and 4*var[0]*var[2]-var[1]**2>0
 ve=[A.poly(var,p) for p in (lo,hi)];A.eqseq(ve,t['residual_endpoint_values']);vmax=max(ve);assert vmax==F(t['residual_squared_max'])
 ends=[[E.reference(32,p,k)-A.poly(rho,p) for p in (lo,hi)] for k in range(1,33)]
 assert len(ends)==len(t['reference_minus_rayleigh_endpoint_lowers'])
 for a,b in zip(ends,t['reference_minus_rayleigh_endpoint_lowers']):A.eqseq(a,b)
 lower=[min(x) for x in ends];A.eqseq(lower,t['reference_minus_rayleigh_uniform_lowers'])
 assert lower[0]>0 and lower[0]==F(t['ground_identification_margin'])
 assert lower[1]>0 and lower[1]==F(t['even_Temple_denominator'])
 width=vmax/lower[1];assert width==F(t['uniform_Temple_width'])
 odd=A.check_odd(t,rho,lo,hi)
 # Exact diagnostic checks supplement the global convexity/concavity proof.
 for j in range(17):
  p=lo+(hi-lo)*F(j,16);assert A.poly(var,p)<=vmax
  assert E.reference(32,p,1)-A.poly(rho,p)>=lower[0]
  assert E.reference(32,p,2)-A.poly(rho,p)>=lower[1]
 out=dict(width=width,lower=lower,variance=var,minimum_ground_margin=lower[0],even_denominator=lower[1],odd_lowers=odd)
 FIXED_REPORT.append(dict(interval=list(map(str,(lo,hi))),variance_max=str(vmax),ground_margin=str(lower[0]),sector_Temple_denominator=str(lower[1]),Temple_width=str(width)))
 return rho,out

def check_trial(t,m,lo,hi,denominator=True):
 if denominator and t['N']==32:return check_fixed(t,lo,hi)
 return N.check_trial(t,m,lo,hi,denominator)
check_numerator_metadata=N.check_numerator_metadata
ns=dict(vars(A));ns.update(check_trial=check_trial,check_numerator_metadata=check_numerator_metadata)
exec(compile((HERE/'scalar_record.py').read_text(),str(HERE/'scalar_record.py'),'exec'),ns);audit_record=ns['audit_record']
scalar_audit_record=audit_record
def audit_record(r,models):
 for w in r['finite_windows']:assert w['included_in_final_minimum']==(w['n']<r['bootstrap']['n'])
 for state in r['joint_ladder_states']:
  n=state['n'];beta=F(state['beta']);base=[n,n,str(beta)]
  assert state['physical_base']==state['joint_product_physical_base']==base
  for order,key in [('xyt','canonical_edge_labels'),('txy','permuted_edge_labels')]:
   if order=='txy' and state['permuted'] is None:
    assert state[key] is None;continue
   loc=[n,n,beta];labels=[]
   for axis in order:
    nxt=loc.copy();nxt['xyt'.index(axis)]*=2
    labels.append(dict(axis=axis,base=[loc[0],loc[1],str(loc[2])],endpoint=[nxt[0],nxt[1],str(nxt[2])]))
    loc=nxt
   assert labels==state[key]
 return scalar_audit_record(r,models)

def prepare():
 A.literal_definition_check();A.physical_normalization();models=A.models_rebuilt();G,K,_=N.numerator()
 N.check_numerator_export(load(S/'numerator_matrix_polynomial.json'),G,K)
 # Shape sentinel only: all 8x4 contractions use the independent fixed physical polynomial.
 models=[models[0],(np.zeros((43,43),dtype=object),None,None),(G,K,None)];A.ODD=A.odd_polynomials()
 save('fixed_polynomial_reconstruction.json',FP);return models

def coverage(records):
 cursor=F(9,100)
 for r in records:
  lo,hi=map(F,r['coupling_interval']);assert lo==cursor and lo<hi;cursor=hi
 assert cursor==F(1,10)

def main():
 start=time.monotonic();models=prepare();summary=load(S/'coverage_summary.json');records=[load(S/x['file']) for x in summary['intervals']];coverage(records)
 assert summary['coupling_interval']==['9/100','1/10'] and summary['closed_intervals']==len(records)
 reports=[]
 for i,(r,entry) in enumerate(zip(records,summary['intervals']),1):
  assert entry['coupling_interval']==r['coupling_interval'] and entry['gap']==r['all_integer_L_ge2_gap']
  report=audit_record(r,models);reports.append(report);print('PASS',i,report['coupling_interval'],report['gap_display'],flush=True)
 gap=min(F(x['all_integer_L_ge2_gap']) for x in reports);assert gap==F(summary['uniform_gap'])
 assert summary['search_dimensions']==[11,43,43] and summary['largest_retained_states']==1 and summary['denominator_retained_states']==[49,97]
 old=load(R/'interval_range_009_review/REVIEW_STATUS.json');assert old['combined_coupling_interval']==['0','9/100'] and old['combined_closed_intervals']==56
 oldgap=F(old['combined_all_integer_L_ge2_uniform_gap']);assert oldgap==F('0.001945771244')
 A.basepoint_ledger(records);save('complete_residual_interval_checks.json',FIXED_REPORT);save('odd_endpoint_checks.json',A.ODD_REPORTS);save('numerator_trials.json',N.NREPORT)
 allowed=[HERE]+[R/f for f in ['interval_range_009_review','interval_range_0085_review','third_moment_review','interval_joint_review','interval_extension_review']];mods=[]
 for n,m in list(sys.modules.items()):
  p=getattr(m,'__file__',None)
  if p and Path(p).resolve().is_relative_to(ROOT):
   assert any(Path(p).resolve().is_relative_to(a) for a in allowed),(n,p);mods.append(str(Path(p).resolve().relative_to(ROOT)))
 result=dict(status='PASS independent continuous .10 extension',accepted=True,producer_manifest_sha256=PINS['producer'],extension_interval=['9/100','1/10'],extension_closed_intervals=len(records),extension_all_integer_L_ge2_uniform_gap=str(gap),extension_gap_display=float(gap),combined_coupling_interval=['0','1/10'],combined_closed_intervals=56+len(records),combined_all_integer_L_ge2_uniform_gap=str(min(gap,oldgap)),combined_gap_display=float(min(gap,oldgap)),unique_finite_volume_ground=True,finite_windows=sum(x['finite_window_count'] for x in reports),required_finite_windows=sum(x['required_finite_windows'] for x in reports),short_size_rows=6*len(records),odd_modes=sum(x['modes'] for x in A.ODD_REPORTS),maximum_asymptotic_onset=max(x['asymptotic_onset'] for x in reports),ground_search_dimensions=[11,43,43],denominator_retained_states=[49,97],denominator_total_search_dimensions=[59,139],largest_retained_numerator_states=1,full_Hilbert_dimensions=[str(4**n) for n in [16,32,64]],producer_modules_imported=0,eigensolver_calls=0,imported_mathematical_modules=sorted(set(mods)),sources=VERIFIED,intervals=reports,runtime_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 save('SUMMARY.json',result);print('PASS UNION',result['combined_gap_display'],'seconds',result['runtime_seconds'],flush=True)
if __name__=='__main__':main()
