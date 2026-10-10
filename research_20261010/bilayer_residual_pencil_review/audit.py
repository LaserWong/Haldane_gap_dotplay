import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
os.sched_setaffinity(0,{4})
import resource
resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(250*1024**2,250*1024**2))
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import ast,itertools,json,hashlib,time,math,numpy as np
H=Path(__file__).resolve().parent;S=H/'snapshot';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def extract():
 names=['mat','zero','graph','rebuild'];ns=dict(F=F,np=np,Counter=Counter,defaultdict=defaultdict,itertools=itertools);nodes=[n for n in ast.parse((S/'MATRIX_REBUILD.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names];assert {n.name for n in nodes}==set(names);exec(compile(ast.Module(body=nodes,type_ignores=[]),'pinned_independent_geometry','exec'),ns);return ns
ns=extract()
def mat(a):return np.array([[F(x) for x in row] for row in a],dtype=object)
def psd(m,strict=False):
 a=mat(m).tolist();piv=[]
 for j in range(len(a)):
  p=a[j][j];assert p>0 if strict else p>=0;piv.append(str(p))
  if not p:assert all(a[i][j]==0 for i in range(j+1,len(a)));continue
  for i in range(j+1,len(a)):
   for k in range(i,len(a)):a[k][i]=a[i][k]=a[i][k]-a[i][j]*a[k][j]/p
 return piv

def inverse(a):
 n=len(a);m=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
 for j in range(n):
  pivot=m[j][j];assert pivot;m[j]=[v/pivot for v in m[j]]
  for i in range(n):
   if i!=j:
    p=m[i][j];m[i]=[x-p*y for x,y in zip(m[i],m[j])]
 return mat([r[n:] for r in m])
def contract(c,a):return F(np.array(c,dtype=object)@a@np.array(c,dtype=object))
def serialize(a):return [[str(x) for x in row] for row in a]

def main():
 start=time.monotonic();mf=load(S/'PHYSICAL4_MANIFEST_SHA256.json');assert sha(S/'PHYSICAL4_MANIFEST_SHA256.json')=='928f1e61cee6a273c7d3af70d3caed60628373435b3b0985ae3005e9de70ac90'
 for f in ['independent_residual','independent_residual.cpp']:assert sha(H/f)==mf[f]
 for f in ['geometry_4x4.txt','GEOMETRY_4x4.json','MATRIX_REBUILD.py']:assert sha(S/f)==mf['snapshot/'+f]
 assert sha(S/'PHYSICAL4_audit.json')==mf['audit.json'];prior=load(S/'PHYSICAL4_audit.json')
 raw={tuple(r['indices']):load(H/r['file']) for r in load(H/'polarization_runs.json')['runs']};assert len(raw)==15
 names={'PP':'P_norm','TT':'T_norm','CMCM':'CM_norm','COMM':'commutator_expectation'};blocks={}
 for name,key in names.items():
  b=[[F(0)]*5 for _ in range(5)]
  for i in range(5):b[i][i]=F(raw[i,][key])
  for i,j in itertools.combinations(range(5),2):b[i][j]=b[j][i]=(F(raw[i,j][key])-b[i][i]-b[j][j])/2
  blocks[name]=mat(b)
 for r in raw.values():assert r['q4_processed']==455 and r['q6_processed']==3003 and F(r['q8_creation_norm'])==F(r['CM_norm'])+F(r['commutator_expectation'])
 q8=blocks['CMCM']+blocks['COMM'];pivots={k:psd(v) for k,v in blocks.items() if k!='COMM'};pivots['q8']=psd(q8)
 assert min(blocks['COMM'].diagonal())<0 # signed term must not be discarded
 geo=load(S/'GEOMETRY_4x4.json');Ff,Ss,V,W,X,Y,Z=[mat(geo[k]) for k in ('F','S','V','W','X','Y','Z')]
 base=ns['rebuild'](4,4,F(0),geo);G=mat(base['G']);b=6;old=11;n=16;Dinv=mat([[F(i==j,G[i,i]) for j in range(1,b)] for i in range(1,b)])
 D2=Ss.T@Dinv@Ss;A2=D2+blocks['PP']+blocks['TT']+q8
 quu=16*V+36*W;qauu=8*X+10*(Y+Y.T)+12*Z
 def assemble(g):
  r=ns['rebuild'](4,4,g,geo);K=mat(r['A']);T=mat(r['Hmap']);assert np.array_equal(G@T,K[:,:old]);rows=T.T@K
  J=np.zeros((n,n),dtype=object);J[:old,:]=rows;J[old:,:old]=rows[:,old:].T;J[old:,old:]=quu+(g/2)*qauu+(g*g/4)*A2
  assert np.array_equal(J,J.T) and np.array_equal(J[:old,:old],T.T@G@T);return K,J
 K0,J0=assemble(F(0));K1,J1=assemble(F(1));Km,Jm=assemble(F(-1));coeff=[J0,(J1-Jm)/2,(J1+Jm)/2-J0]
 assert np.array_equal(coeff[0][old:,old:],quu) and np.array_equal(2*coeff[1][old:,old:],qauu) and np.array_equal(4*coeff[2][old:,old:],A2)
 c=list(map(F,prior['polynomial']['coefficients']));norm=contract(c,G)
 assert norm==F(prior['norm']);poly=[contract(c,m)/norm for m in coeff];assert list(map(str,poly))==prior['polynomial']['full_second_moment_coefficients']
 gi=inverse(G);assert np.array_equal(G@gi,np.eye(n,dtype=object));gram_pivots=psd(G,True);checks=[]
 for g in map(F,['0','1/10','21/200','1/4','-1/3']):
  K,J=assemble(g);assert np.array_equal(J,sum((coeff[i]*g**i for i in range(3)),np.zeros((n,n),dtype=object)))
  rem=J-K@gi@K;piv=psd(rem);assert any(F(v)>0 for v in piv)
  checks.append(dict(g=str(g),full_H2_psd_pivots=psd(J),omitted_image_Gram_psd_pivots=piv))
 g=F(21,200);K,J=assemble(g);assert contract(c,J)/norm==F(prior['second_moment']);a=F(prior['even_sector_cutoff']);ell=F(prior['ground_lower']);rho=contract(c,K)/norm
 evalp=lambda l:contract(c,J-(a+l)*K+a*l*G)/norm
 assert rho<a and evalp(ell)==0 and evalp(ell-F(1,10**6))<0 and evalp(ell+F(1,10**6))>0
 # Missing sector uniqueness makes the negative-pencil implication false.
 assert (F(0)-2)*(F(0)+1)<0 and F(-2)<=F(-1)<2
 # Match every coefficient entry to the independent scalar complete form at .105.
 for ids,r in raw.items():
  v=[F(0)]*n
  for i in ids:v[old+i]=1
  sector02=contract(v,K[:b,:].T@inverse(G[:b,:b])@K[:b,:])
  direct=sector02+(F(r['Tpsi_q4_norm'])+F(r['Tpsi_q6_norm'])+21**2*F(r['q8_creation_norm']))/400**2
  assert contract(v,J)==direct
 pm=S/'PRODUCER_MANIFEST.json';assert sha(pm)=='86b34b8fe80d89fa958b777f7af5fbcf81ce9af588d123e02f4d7c2641fe56e6'
 for rel,h in load(pm).items():assert sha(S/'producer'/rel)==h
 prod=load(S/'producer/matrix_4x4.json');assert prod['partial'] is False and prod['q4_processed']==455 and prod['q6_processed']==3003
 for key,block in blocks.items():assert np.array_equal(mat(prod[key]),block)
 pol=load(S/'producer/complete_H2_polynomial_4x4.json');assert pol['dimension']==16 and pol['geometry']==[4,4] and np.array_equal(mat(pol['gram']),G)
 for actual,saved in zip(coeff,pol['H2_coefficients']):assert np.array_equal(actual,mat(saved))
 sample=load(S/'producer/sample_8x4.json');assert sample['partial'] is True and sample['q4_total']==4495 and sample['q6_total']==169911 and sample['q6_processed']<sample['q6_total']
 estimate=sample['cache_seconds']+sample['q4_seconds']*sample['q4_total']/sample['q4_processed']+sample['q6_seconds']*sample['q6_total']/sample['q6_processed']
 out=dict(status='PASS_INDEPENDENT_COMPLETE_4X4_MATRIX_FIXTURE_AND_SECTOR_PENCIL_PROOF',geometry=[4,4],trial_dimension=16,missing_block_dimension=5,independent_polarization_runs=15,blocks={k:serialize(v) for k,v in blocks.items()},q8_Gram=serialize(q8),UU_Q_squared=serialize(quu),UU_QA_plus_AQ=serialize(qauu),UU_A_squared=serialize(A2),complete_H2_coefficients_g0_g1_g2=[serialize(m) for m in coeff],Gram_rank_pivots=gram_pivots,block_psd_pivots=pivots,coupling_checks=checks,existing_complete_0105_vector_exact_match=True,all15_full_scalar_forms_exact_match=True,negative_pencil_uses_even_singlet_cutoff_not_full_Hilbert_lambda2=True,no8x4_contraction=True,no_new_gap_claim=True,producer_manifest_sha256=sha(pm),producer_4x4_all_four_blocks_and_full_polynomial_exact_match=True,partial8x4_timing_projection_seconds=estimate,partial_sample_not_physical_certificate=True,producer4x2_full_matrix_not_independently_reviewed=True,independent_run_resources=load(H/'polarization_runs.json'),seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (H/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['seconds'],out['peak_rss_kib'])
if __name__=='__main__':main()
