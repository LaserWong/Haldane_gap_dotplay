#!/usr/bin/env python3
"""Fresh optimistic path enumeration; never imports producer replay outcomes."""
from pathlib import Path
base=Path(__file__).resolve().parent
exec((base.parent/'mps_excited_seed_review/independent_scalar.py').read_text().split("p=values('independent_contractions.out')")[0]);P=base
import hashlib
for f,h in json.loads((P/'INPUT_DEPENDENCIES_SHA256.json').read_text()).items():assert hashlib.sha256((P.parent/f).read_bytes()).hexdigest()==h

def continuation(j,c,n):
 a=G(j)
 if a<=0:return {'excluded':True,'failure':'initial first G','output_upper':str(a),'history':[]}
 b=G(c*c*a)
 if b<=0:return {'excluded':True,'failure':'initial second G','output_upper':str(b),'history':[]}
 history=[]
 for delay in range(100):
  assert 0<a<=1 and 0<b<=1
  joint=ceil(a*a*b);direct_square=ceil(a**4*(2*b-1)) if b>F(1,2) else F(0)
  path={'delay':delay,'physical_length':n*2**(delay+1),'beta_multiplier':2**(delay+1),'a_upper':str(a),'b_upper':str(b),'joint_upper':str(joint),'direct_window_square_diagnostic':str(direct_square)};history.append(path)
  if joint>=F(99,100):return {'excluded':False,'reason':'accepted same-base sufficient closure may be reachable','history':history}
  path['canonical']=canonical(a,b)
  if not path['canonical']['excluded']:return {'excluded':False,'reason':'canonical continuation not ruled out','history':history}
  a=G(a*a*b)
  if a<=0:return {'excluded':True,'failure':'time-first first G','output_upper':str(a),'history':history}
  b=G(b*b*a)
  if b<=0:return {'excluded':True,'failure':'time-first second G','output_upper':str(b),'history':history}
 return {'excluded':False,'reason':'finite safety cap is inconclusive','history':history}

sources=[('mps_excited_seed_witnesses/scalar_results.json','rows'),('mps_seed_even_completion/results.json','rows'),('mps_commutator_assessment/fused_current/pi_scalar_results.json','cases')];rows=[]
for filename,key in sources:
 for r in json.loads((P.parent/filename).read_text())[key]:
  n=r.get('n',24);count=r.get('retained_denominator_states',3)
  if (key=='rows' and n==24) or ('mps_seed_even' in filename and count!=3):continue
  assert r['hot_closed_interval']==['0','1/2'];assert all(F(r[k])<F(2,5) for k in ['hot_J_upper','cold_J_upper']) and G(F(2,5))<0
  previous=F(1,2);boxes=[]
  for b in r['warm_boxes']:
   lo,hi=F(b['beta_lower']),F(b['beta_upper']);assert lo==previous and hi>lo;previous=hi
   result=continuation(F(b['J_upper']),F(b['C_upper']),n);assert result['excluded']
   boxes.append({'lo':str(lo),'hi':str(hi),**result})
  assert previous==F(r['cold_closed_interval'][0]);rows.append({'n':n,'states':count,'source':filename,'all_beta_excluded':True,'boxes':boxes})
smallfile='uniform_seed_size_diagnostics/uniform_seed_size_diagnostics.json'
for r in json.loads((P.parent/smallfile).read_text())['rows']:
 n=r['n'];assert n in [6,8,10,12]
 if n in [6,8]:
  assert F(r['early_J_upper'])<F(2,5) and F(r['early_beta_end'])==F(1,2);result=continuation(F(r['J_global_cap']),F(r['late_C_cap']),n);assert result['excluded']
 else:
  output=G(F(r['J_global_cap']));assert output<0;result={'excluded':True,'failure':'global first G','output_upper':str(output),'history':[]}
 rows.append({'n':n,'states':r['denominator_orthogonal_trials'],'source':smallfile,'all_beta_excluded':True,'global_or_late_replay':result})
assert {r['n'] for r in rows}==set(range(6,25,2)) and len(rows)==11
histories=[h for r in rows if r['n']==24 for b in r['boxes'] for h in b['history']];maxP=max(F(h['joint_upper']) for h in histories);maxN=max(h['physical_length'] for h in histories);assert maxP<F(674059,1000000) and maxN==96
review_seal=P.parent/'mps_commutator_review/SEAL.json'
status='PASS independent relaxed-path arithmetic; current physical dependency still pending until its separate seal'
if review_seal.exists():
 seal=json.loads(review_seal.read_text());assert seal['status']=='PASS';manifest=review_seal.parent/seal['manifest'];assert hashlib.sha256(manifest.read_bytes()).hexdigest()==seal['manifest_sha256']
 for f,h in json.loads(manifest.read_text())['files'].items():assert hashlib.sha256((review_seal.parent/f).read_bytes()).hexdigest()==h
 status='PASS independent relaxed paths with independently sealed physical dependencies'
out={'status':status,'scope':'Existing G startup, any whole time-first delays, then inherited same-base P>=0.99 sufficient closure or accepted canonical continuation; all finite bridges granted. No universal necessity of 0.99, no exclusion of other recursions/closures or arbitrary adaptive switching.','rows':rows,'n24_joint_upper_max':str(maxP),'n24_joint_upper_max_display':float(maxP),'n24_max_positive_physical_base':maxN,'CPU_seconds':time.process_time()-t0,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};(P/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
