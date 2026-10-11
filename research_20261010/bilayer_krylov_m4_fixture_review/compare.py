from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;s=p/'snapshot';load=lambda p:json.loads(p.read_text())
assert hashlib.sha256((s/'PRODUCER_MANIFEST.json').read_bytes()).hexdigest()=='8372940215a1b1e06914a42bba957b19e7e4eeb5aa055f38f6ad4fab71d469f1'
m=load(s/'PRODUCER_MANIFEST.json')
for name,h in m.items():assert hashlib.sha256((s/'producer'/name).read_bytes()).hexdigest()==h,name
out=load(p/'independent.json');checks=[]
for x in out['results']:
 shape=str(x['shape'][0])+'x2';z=load(s/'producer'/('fixture_'+shape+'.json'));t=load(s/'producer'/('terms_'+shape+'.json'))
 def eq(v,w):assert int(v)==int(w),(shape,v,w)
 eq(x['integer_T200_11_moments'][0],z['norm']);eq(x['integer_T200_11_moments'][3],z['direct_m3_numerator']);eq(x['integer_T200_11_moments'][4],z['direct_m4_numerator']);eq(x['normal_m3'],z['normal_m3_numerator'])
 for k,v in zip(['D8_2_CM_CDM','D8_minus_CM_DCM','D8_KM_DM','D8_nested_C_E'],x['m3_q8_terms']):eq(v,t[k])
 for k,v in zip(['Q10_gamma_norm','Q10_2_CM_CKM','Q10_minus_CM_KCM','Q10_KM_norm','Q10_L'],x['q10_terms']):eq(v,t[k])
 for k,v in zip(['Q8_Cv_norm','Q8_v_Kv',None,'Q8_EadjM_norm','Q8_Ecomm'],x['q8_terms']):
  if k:eq(v,t[k])
 eq(x['q8_cross_ECM'],t['Q8_cross_ECM']);eq(x['q8_cross_nested'],t['Q8_cross_CE']);eq(x['q10_direct'],z['q10_base_norm'])
 for q,v in z['sector_H2_norms'].items():eq(x['sector_H2_norms'].get(q,0),v)
 assert x['q10_terms'][2]<0 and x['q8_terms'][4]<0
 if shape=='5x2':assert x['q10_terms'][4]<0
 checks.append({'shape':x['shape'],'all15_separate_normal_order_terms_match':True,'all_sector_norms_match':True,'m3_m4_exact_match':True,'nonzero_q10':x['q10_direct']>0})
assert checks[1]['nonzero_q10'] and not checks[0]['nonzero_q10']
r={'status':'PASS_INDEPENDENT_CARTESIAN_PHYSICAL_M3_M4_FIXTURES','checks':checks,'new_large_geometry':False,'production_motif_cost_certified':False}
(p/'comparison.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
