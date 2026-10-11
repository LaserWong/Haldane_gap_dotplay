import os,resource
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2))
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,math,ast,time,sys
sys.set_int_max_str_digits(0)
H=Path(__file__).resolve().parent;S=H/'snapshot';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names={'mat','zero','tr','mul','add','scale','psd'};nodes=[n for n in ast.parse((S/'MATRIX_MATH.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names];assert {n.name for n in nodes}==names;exec(compile(ast.Module(body=nodes,type_ignores=[]),'accepted_independent_matrix_helpers','exec'))
def bil(c,m):return sum(c[i]*m[i][j]*c[j] for i in range(len(c)) for j in range(len(c)))
def ref(g,q):
 d=10**60;x=1-4*g;k=math.isqrt(x.numerator*d*d//x.denominator);r=F(k,d);assert r*r<=x<(r+F(1,d))**2;return 12*(2*g-1)+(12+q)*r

def positive_ldl_fraction_free(m):
 assert m==tr(m);den=1
 for row in m:
  for x in row:den=math.lcm(den,x.denominator)
 a=[[int(x*den) for x in row] for row in m];previous=1;pivots=[];minors=[]
 for j in range(len(a)):
  pivot=a[j][j];assert pivot>0;minors.append(str(pivot));pivots.append(str(F(pivot,previous*den)))
  for i in range(j+1,len(a)):
   for k in range(i,len(a)):
    v=a[i][k]*pivot-a[i][j]*a[k][j];assert v%previous==0;a[k][i]=a[i][k]=v//previous
  previous=pivot
 return pivots,dict(positive_integer_scale=str(den),leading_principal_minors=minors)

def main():
 start=time.monotonic()
 small=scale(mat([[2,1,0],[1,3,1],[0,1,2]]),F(1,7));assert positive_ldl_fraction_free(small)[0]==psd(small,True)
 try:positive_ldl_fraction_free(mat([[1,2],[2,1]]))
 except AssertionError:pass
 else:raise AssertionError('indefinite control accepted')
 pm=S/'PRODUCER_MANIFEST.json';assert sha(pm)=='c05da7710cba05fcf4e537bd3754eebba87cb826b6ddbf918a52ffb84f96a658'
 for rel,h in load(pm).items():assert sha(S/'producer'/rel)==h
 seals={'MATRIX57':'874c87f1ff9b4b58f795ef5e01aad45ff4f22e560e4721c7a933ed27380166a5','PREVIOUS_ENDPOINT':'9c6a17ceb920c20f323ccd27751b2d863f264566b0b1c8d46d5db4f2ea50c053'}
 for tag,seal in seals.items():
  mf=S/(tag+'_MANIFEST_SHA256.json');assert sha(mf)==seal
  for name in ['audit.json','ACCEPTANCE.json','PROOF.md']:assert sha(S/(tag+'_'+name))==load(mf)[name]
 assert sha(S/'MATRIX_MATH.py')==load(S/'MATRIX57_MANIFEST_SHA256.json')['audit.py']
 oldmf=load(S/'PREVIOUS_ENDPOINT_MANIFEST_SHA256.json');assert sha(S/'REOPTIMIZATION.json')==oldmf['snapshot/split/reoptimization.json'];assert sha(S/'TARGET_LIMIT43.json')==oldmf['snapshot/assessment/target_limit.json']
 physical=load(S/'MATRIX57_audit.json');assert physical['status']=='PASS_INDEPENDENT_COMPLETE57D8X4_SPLIT_H2_MATRIX' and physical['dimension']==57
 G=mat(physical['gram']);ks=list(map(mat,physical['H_coefficients']));js=list(map(mat,physical['H2_coefficients']));old=load(S/'PREVIOUS_ENDPOINT_audit.json')['physical_endpoints'];energy=load(S/'REOPTIMIZATION.json')['results'];rows=load(S/'producer/result.json')['results'];assert len(rows)==2 and {F(r['g']) for r in rows}=={F(11,100),F(3,25)}
 results=[];matrices={}
 for row in rows:
  g=F(row['g']);assert row['shape']==[8,4] and row['dimension']==57;K=add(ks[0],scale(ks[1],g));J=add(js[0],scale(js[1],g),scale(js[2],g*g));a=ref(g,2);r1=ref(g,1)
  prior=next(x for x in old if x['shape']==[8,4] and F(x['g'])==g);assert F(prior['full_even_singlet_sector_cutoff'])==a and prior['unique_global_ground_identified'] is True
  odd=prior['odd_count'];assert odd['fixed_z']=='1/10' and odd['odd_trial_dimension']==96 and odd['reference_levels_below_q2']==97 and len(odd['modes'])==32 and all(F(x['cutoff_margin'])>0 for x in odd['modes'])
  c=list(map(F,row['integer_coefficients']));assert len(c)==57 and all(x.denominator==1 for x in c);norm=bil(c,G);rho=bil(c,K)/norm;second=bil(c,J)/norm;var=second-rho*rho;ell=F(row['strict_pencil_endpoint']);pencil=second-(a+ell)*rho+a*ell
  assert norm>0 and var>=0 and rho<r1<a and ell<a and pencil<0;lower=rho-var/(a-rho);assert lower>ell
  for k,v in dict(norm=norm,rayleigh=rho,variance=var,cutoff=a,global_r1=r1,normalized_pencil_witness=pencil,Temple_lower=lower).items():assert F(row[k])==v,k
  en=next(x['split'] for x in energy if x['shape']==[8,4] and F(x['g'])==g);c0=list(map(F,en['integer_coefficients']));n0=bil(c0,G);r0=bil(c0,K)/n0;v0=bil(c0,J)/n0-r0*r0;l0=r0-v0/(a-r0)
  assert n0==F(en['norm']) and r0==F(en['rayleigh']) and v0>=0 and r0<r1
  assert F(row['energy_optimized_lower'])==l0 and F(row['energy_optimized_variance'])==v0 and F(row['endpoint_improvement'])==lower-l0>0
  assert F(row['previous43D_pencil_lower'])==F(prior['ground_lower']) and F(row['gain_over43D_pencil'])==lower-F(prior['ground_lower'])>0
  results.append(dict(g=str(g),dimension=57,ground_lower=str(lower),downward12_decimal_lower=str(F(lower.numerator*10**12//lower.denominator,10**12)),ground_lower_display=float(lower),norm=str(norm),rayleigh=str(rho),complete_variance=str(var),strict_endpoint=str(ell),normalized_negative_pencil=str(pencil),global_r1_margin=str(r1-rho),full_even_singlet_cutoff=str(a),odd_count_source='independently accepted point review9c6a17ce',gain_over43D=str(lower-F(prior['ground_lower'])),unique_global_ground=True));matrices[g]=(G,K,J,a)
  print('PASS physical57D endpoint',g,float(lower),flush=True)
 G,K,J,a=matrices[F(11,100)];limits=[]
 for target in load(S/'TARGET_LIMIT43.json')['results']:
  ell=F(target['target_lower']);assert ell<a;pmat=add(J,scale(K,-(a+ell)),scale(G,a*ell));piv,ff=positive_ldl_fraction_free(pmat);assert len(piv)==57
  limits.append(dict(beta=target['beta'],target_lower=str(ell),fixed_cutoff=str(a),dimension=57,positive_LDL_pivots=piv,fraction_free_certificate=ff,positive_definite=True,scope='Only current57D complete Temple-pencil test at this target and fixedr2 cutoff; no universal bootstrap obstruction'))
  print('PASS57D target LDL',target['beta'],flush=True)
 out=dict(status='PASS_TWO_PHYSICAL57D_ENDPOINTS_AND_TWO_SCOPED57D_TARGET_EXCLUSIONS',physical_endpoints=results,target_exclusions=limits,all_size_gap_claim=False,float_temperature_failures_not_no_go=True,no_new_physical_support=True,sector_and_global_ground_obligations_preserved=True,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (H/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['seconds'],out['peak_rss_kib'])
if __name__=='__main__':main()
