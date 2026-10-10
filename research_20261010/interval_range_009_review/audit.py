#!/usr/bin/env python3
"""Independent exact interval replay. Imports only sealed independent reviews."""
import os,sys,resource
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,importlib.util,ast,time,copy,math
HERE=Path(__file__).resolve().parent;R=HERE.parent;ROOT=R.parent;S=HERE/'snapshot'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
OUT=Path(os.environ.get('REVIEW_OUTPUT',str(HERE/'results')));OUT.mkdir(parents=True,exist_ok=True)
def save(n,x):(OUT/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def seal(p,h):
 assert sha(p)==h,('manifest',str(p));raw=load(p);files=raw.get('files',raw)
 for f,v in files.items():assert sha(p.parent/f)==v,('file',str(p.parent/f))
 return len(files)
PINS=load(HERE/'PINS.json')
assert PINS=={'producer':'8a135f1a729f5f00953b96b3b9ed61891653ca3d592e27d492d29031d1652698','old_review':'c14cdb65f0e1b92a6025758e63352e404eef01965f7dde2344a2eaaf86c5a0b9','third_review':'7d85c62626ca0aee9fa90fd5ca9968dac5ce50c34c4d023bf916df593cdfee36'}
def verify():
 assert sha(HERE/'PRODUCER_FREEZE.json')==PINS['producer']
 assert seal(R/'interval_range_009/FROZEN_MANIFEST.json',PINS['producer'])==23
 for f,h in load(HERE/'PRODUCER_FREEZE.json')['files'].items():assert sha(S/f)==h
 for f,h in load(S/'INPUT_SHA256.json').items():assert sha(ROOT/f)==h
 for row in load(S/'INHERITED_SEALS.json'):
  assert seal(R/row['folder']/row['manifest'],row['sha256'])==row['file_count']
 assert sha(R/'interval_range_0085_review/MANIFEST_SHA256.json')==PINS['old_review']
 assert sha(R/'third_moment_review/MANIFEST_SHA256.json')==PINS['third_review']
 old=load(R/'interval_range_0085_review/REVIEW_STATUS.json');third=load(R/'third_moment_review/REVIEW_STATUS.json')
 assert old['accepted'] and old['unique_finite_volume_ground'] and old['combined_coupling_interval']==['0','17/200']
 assert third['finite_volume_unique_ground'] and third['largest_retained_numerator_states']==1 and third['enlarged_exact_search_ranks']==[16,43,43]
 return dict(producer_files=23,direct_inputs=len(load(S/'INPUT_SHA256.json')),inherited_seals=14)
VERIFIED=verify()
def module(name,p):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
A=module('prior_interval_review',R/'interval_range_0085_review/audit.py');A.save=lambda n,x:save('inherited_'+n,x)
M=module('third_matrix_review',R/'third_moment_review/audit_matrices.py')
E=A.E;np=E.np
# Pin the adaptation to exactly the already accepted scalar function.
src=(R/'interval_range_0085_review/audit.py').read_text();node=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='audit_record')
expected=ast.get_source_segment(src,node).replace('F(2,25)<=lo<hi<=F(17,200)','F(17,200)<=lo<hi<=F(9,100)').replace("rr[2],filter_report=E.check_filter(r['largest_interval_filter'],rr[2],pp[2],lo,hi)","filter_report=dict(replaced_by_fixed_43D_numerator=True); check_numerator_metadata(r)")
assert ast.dump(ast.parse(expected),include_attributes=False)==ast.dump(ast.parse((HERE/'scalar_record.py').read_text()),include_attributes=False)
NREPORT=[]
def check_numerator_export(raw,G,K):
 assert raw['dimension']==43 and raw['geometry']==[8,8]
 assert raw['gram']==G.tolist()
 assert [[[F(x) for x in row] for row in block] for block in raw['shifted_A_coefficients']]==[k.tolist() for k in K]
def numerator():
 geom=load(R/'third_moment_review/results/geometry_8x8.json')
 prod=load(ROOT/'research_20261010/low_band/third_moment_exact/geometry_8x8_origin.json')
 assert all(geom[k]==prod[k] for k in ('F','S','V','W','X','Y','Z'))
 # Direct operator assembly in the fixed B,L,U basis, not .09/.10 interpolation.
 z=M.rebuild(8,8,F(0),geom);u=M.rebuild(8,8,F(1),geom)
 G=z['G'];K0=z['A'];K1=u['A']-K0;ids,piv=M.rank_psd(G)
 assert ids==list(range(43)) and np.array_equal(G,u['G'])
 raw=load(S/'numerator_matrix_polynomial.json');check_numerator_export(raw,G,[K0,K1])
 for g,label in [(F(9,100),'9d100'),(F(1,10),'1d10')]:
  r=load(R/f'low_band/third_moment_exact/enlarged_8x8_g{label}.json')
  assert G.tolist()==r['gram'] and r['selected_basis_indices']==ids
  assert ((K0+g*K1)*r['integer_matrix_denominator']).tolist()==r['shifted_H_numerator']
 save('numerator_operator.json',dict(status='PASS direct fixed-basis operator reconstruction',basis_rank=43,positive_LDL_pivots=piv,gram=G.tolist(),affine_A=[K0.tolist(),K1.tolist()],q_sectors=[0,2,4,6],matrix_matches=['9/100','1/10']))
 return G,[K0,K1],None

def check_numerator_metadata(r):
 m=r['largest_numerator'];assert m==dict(retained_states=1,search_dimension=43,max_triplet_number=6,residual_required=False,physical_spins=128,full_dimension=4**64)
 assert 'largest_interval_filter' not in r

def check_trial(t,model,lo,hi,denominator=True):
 if denominator:return A.check_trial(t,model,lo,hi,True)
 G,K,_=model;c=np.array(t['integer_coefficients'],dtype=object)
 assert len(c)==43 and all(type(x) is int for x in c)
 norm=c@G@c;assert norm>0 and F(t['integer_metric_norm'])==norm
 rho=[F(c@k@c)/norm for k in K];A.eqseq(rho,t['rayleigh_coefficients'])
 assert F(t['center'])==(lo+hi)/2
 assert set(t)=={'geometry','N','trial_dimension','center','integer_coefficients','integer_metric_norm','rayleigh_coefficients'}
 for p in (lo,(lo+hi)/2,hi):assert F(c@(K[0]+p*K[1])@c)/norm==A.poly(rho,p)
 NREPORT.append(dict(interval=list(map(str,(lo,hi))),norm=str(norm),rho=list(map(str,rho)),fixed_integer_coefficients=True))
 return rho,None
ns=dict(vars(A));ns['check_trial']=check_trial;ns['check_numerator_metadata']=check_numerator_metadata
exec(compile((HERE/'scalar_record.py').read_text(),str(HERE/'scalar_record.py'),'exec'),ns)
audit_record=ns['audit_record']
def prepare():
 A.literal_definition_check();A.physical_normalization();models=A.models_rebuilt()[:2]+[numerator()];A.ODD=A.odd_polynomials();return models

def coverage(records):
 cursor=F(17,200)
 for r in records:
  lo,hi=map(F,r['coupling_interval']);assert lo==cursor and lo<hi;cursor=hi
 assert cursor==F(9,100) and len(records)==7

def main():
 start=time.monotonic();models=prepare();summary=load(S/'coverage_summary.json');records=[load(S/r['file']) for r in summary['intervals']];coverage(records)
 reports=[]
 for i,(r,entry) in enumerate(zip(records,summary['intervals']),1):
  assert entry['coupling_interval']==r['coupling_interval'] and entry['gap']==r['all_integer_L_ge2_gap']
  report=audit_record(r,models);reports.append(report);print('PASS',i,report['coupling_interval'],report['gap_display'],flush=True)
 assert summary['coupling_interval']==['17/200','9/100'] and summary['closed_intervals']==7
 gap=min(F(r['all_integer_L_ge2_gap']) for r in reports);assert gap==F(summary['uniform_gap'])==F(2894183477,500000000000)
 assert summary['largest_retained_states']==1 and summary['search_dimensions']==[11,29,43] and summary['denominator_retained_states']==[49,97]
 old=load(R/'interval_range_0085_review/REVIEW_STATUS.json');oldgap=F(old['combined_all_integer_L_ge2_uniform_gap']);assert oldgap==F(486442811,250000000000)
 assert old['combined_closed_intervals']==49
 A.basepoint_ledger(records)
 save('numerator_trials.json',NREPORT);save('odd_endpoint_checks.json',A.ODD_REPORTS)
 u=F(1,500);assert 49/(2*(1-7*u)**2)<32 and 32*u<1 and 5*u<=F(1,100) and 20/(1-20*u)<=32
 allowed=[HERE,R/'interval_range_0085_review',R/'third_moment_review',R/'interval_joint_review',R/'interval_extension_review'];mods=[]
 for n,m in list(sys.modules.items()):
  p=getattr(m,'__file__',None)
  if p and Path(p).resolve().is_relative_to(ROOT):
   assert any(Path(p).resolve().is_relative_to(a) for a in allowed),(n,p);mods.append(str(Path(p).resolve().relative_to(ROOT)))
 result=dict(status='PASS independent continuous .09 extension',accepted=True,producer_manifest_sha256=PINS['producer'],extension_interval=['17/200','9/100'],extension_closed_intervals=7,extension_all_integer_L_ge2_uniform_gap=str(gap),extension_gap_display=float(gap),combined_coupling_interval=['0','9/100'],combined_closed_intervals=56,combined_all_integer_L_ge2_uniform_gap=str(min(gap,oldgap)),combined_gap_display=float(min(gap,oldgap)),unique_finite_volume_ground=True,finite_windows=sum(r['finite_window_count'] for r in reports),required_finite_windows=sum(r['required_finite_windows'] for r in reports),short_size_rows=42,odd_modes=sum(x['modes'] for x in A.ODD_REPORTS),maximum_asymptotic_onset=max(x['asymptotic_onset'] for x in reports),largest_retained_numerator_states=1,ground_search_dimensions=[11,29,43],denominator_total_search_dimensions=[59,125],denominator_retained_states=[49,97],full_Hilbert_dimensions=[str(4**n) for n in [16,32,64]],producer_modules_imported=0,eigensolver_calls=0,imported_mathematical_modules=sorted(set(mods)),sources=VERIFIED,intervals=reports,runtime_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 save('SUMMARY.json',result);print('PASS UNION',result['combined_gap_display'],'seconds',result['runtime_seconds'],flush=True)
if __name__=='__main__':main()
