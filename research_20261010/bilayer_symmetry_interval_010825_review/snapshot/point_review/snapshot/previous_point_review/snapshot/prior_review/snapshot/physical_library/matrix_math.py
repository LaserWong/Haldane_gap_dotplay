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
 start=time.monotonic();mf=load(S/'PHYSICAL_MANIFEST.json');assert sha(S/'PHYSICAL_MANIFEST.json')=='6c19485312d08ad0cca2fc76367d5c9172d3aab8ea843d0a740324b69837b331'
 for f in ['independent_residual','independent_residual.cpp']:assert sha(H/f)==mf[f]
 for f in ['geometry_8x4.txt','GEOMETRY_8x4.json','MATRIX_REBUILD.py']:assert sha(S/f)==mf['snapshot/'+f]
 assert sha(S/'PHYSICAL_AUDIT.json')==mf['audit.json'];prior=load(S/'PHYSICAL_AUDIT.json')
 fm=S/'FIXTURE_MANIFEST_SHA256.json';assert sha(fm)=='a4eec8140e891b53cc9bd4c237c95236dd32a7069180ed9bc9355df82e4060fb'
 assert sha(S/'FIXTURE_audit.json')==load(fm)['audit.json'] and sha(S/'FIXTURE_PROOF.md')==load(fm)['PROOF.md']
 fixture=load(H/'fixture4x4.json');old=load(S/'FIXTURE_audit.json')
 for k in ('PP','TT','CMCM','COMM'):assert np.array_equal(mat(fixture[k]),mat(old['blocks'][k]))
 actual=load(H/'independent_matrix_8x4.json');assert actual['N']==32 and actual['d']==14 and actual['partial'] is False and actual['q4_processed']==4495 and actual['q6_processed']==169911
 blocks={k:mat(actual[k]) for k in ('PP','TT','CMCM','COMM')}
 for m in blocks.values():assert np.array_equal(m,m.T)
 q8=blocks['CMCM']+blocks['COMM'];pivots={k:psd(v) for k,v in blocks.items() if k!='COMM'};pivots['q8']=psd(q8)
 tz=mat(actual['TT_on_M_zero']);assert np.array_equal(tz,tz.T);pivots['TT_on_M_zero']=psd(tz);assert actual['M_zero_supports']>0 and any(x>0 for x in tz.diagonal())
 # Existing three independent scalar forms corroborate the shared-array algorithm.
 raw={tuple(r['indices']):load(H/'polarization'/('result_'+'_'.join(map(str,r['indices']))+'.json')) for r in load(H/'benchmark.json')['runs']}
 for ids,row in raw.items():
  v=[F(int(i in ids)) for i in range(14)]
  for k,key in [('PP','P_norm'),('TT','T_norm'),('CMCM','CM_norm'),('COMM','commutator_expectation')]:assert contract(v,blocks[k])==F(row[key])
  assert contract(v,q8)==F(row['q8_creation_norm']) and contract(v,tz)==F(row['T_norm_on_M_zero_supports'])
 geo=load(S/'GEOMETRY_8x4.json');Ff,Ss,V,W,X,Y,Z=[mat(geo[k]) for k in ('F','S','V','W','X','Y','Z')]
 base=ns['rebuild'](8,4,F(0),geo);G=mat(base['G']);b=15;oldsize=29;n=43;Dinv=mat([[F(i==j,G[i,i]) for j in range(1,b)] for i in range(1,b)])
 D2=Ss.T@Dinv@Ss;A2=D2+blocks['PP']+blocks['TT']+q8;quu=16*V+36*W;qauu=8*X+10*(Y+Y.T)+12*Z
 def assemble(g):
  r=ns['rebuild'](8,4,g,geo);K=mat(r['A']);T=mat(r['Hmap']);assert np.array_equal(G@T,K[:,:oldsize]);rows=T.T@K
  J=np.zeros((n,n),dtype=object);J[:oldsize,:]=rows;J[oldsize:,:oldsize]=rows[:,oldsize:].T;J[oldsize:,oldsize:]=quu+(g/2)*qauu+(g*g/4)*A2
  assert np.array_equal(J,J.T) and np.array_equal(J[:oldsize,:oldsize],T.T@G@T);return K,J
 K0,J0=assemble(F(0));K1,J1=assemble(F(1));Km,Jm=assemble(F(-1));coeff=[J0,(J1-Jm)/2,(J1+Jm)/2-J0]
 assert np.array_equal(coeff[0][oldsize:,oldsize:],quu) and np.array_equal(2*coeff[1][oldsize:,oldsize:],qauu) and np.array_equal(4*coeff[2][oldsize:,oldsize:],A2)
 c=list(map(F,prior['polynomial']['coefficients']));norm=contract(c,G);assert norm==F(prior['norm'])
 assert [str(contract(c,m)/norm) for m in coeff]==prior['polynomial']['full_second_moment_coefficients']
 gi=inverse(G);assert np.array_equal(G@gi,np.eye(n,dtype=object));gram_pivots=psd(G,True);checks=[]
 for g in map(F,['0','21/200','-1/3']):
  K,J=assemble(g);assert np.array_equal(J,sum((coeff[i]*g**i for i in range(3)),np.zeros((n,n),dtype=object)))
  rem=J-K@gi@K;piv=psd(rem);assert any(F(v)>0 for v in piv)
  checks.append(dict(g=str(g),full_H2_psd_pivots=psd(J),omitted_image_Gram_psd_pivots=piv))
 g=F(21,200);K,J=assemble(g);assert contract(c,J)/norm==F(prior['second_moment']);a=F(prior['even_sector_cutoff']);ell=F(prior['ground_lower']);rho=contract(c,K)/norm
 evalp=lambda l:contract(c,J-(a+l)*K+a*l*G)/norm
 assert rho<a and evalp(ell)==0 and evalp(ell-F(1,10**6))<0 and evalp(ell+F(1,10**6))>0
 for ids,row in raw.items():
  v=[F(0)]*n
  for i in ids:v[oldsize+i]=1
  sector02=contract(v,K[:b,:].T@inverse(G[:b,:b])@K[:b,:])
  direct=sector02+(F(row['Tpsi_q4_norm'])+F(row['Tpsi_q6_norm'])+21**2*F(row['q8_creation_norm']))/400**2
  assert contract(v,J)==direct
 pm=S/'PRODUCER_MANIFEST.json';assert sha(pm)=='554c761bdb4ce1dfc6e8543ef145af43f30f1929f8553ff821e1c633a4f31118'
 for rel,h in load(pm).items():assert sha(S/'producer'/rel)==h
 prod=load(S/'producer/matrix_8x4.json');assert prod['partial'] is False and prod['q4_processed']==4495 and prod['q6_processed']==169911
 for key,block in blocks.items():assert np.array_equal(mat(prod[key]),block)
 pol=load(S/'producer/complete_H2_polynomial_8x4.json');assert pol['dimension']==43 and pol['geometry']==[8,4] and np.array_equal(mat(pol['gram']),G)
 for actual,saved in zip(coeff,pol['H2_coefficients']):assert np.array_equal(actual,mat(saved))
 out=dict(status='PASS_INDEPENDENT_COMPLETE_8X4_H2_MATRIX_AND_COUPLING_POLYNOMIAL',geometry=[8,4],trial_dimension=43,missing_block_dimension=14,full_Hilbert_dimension=str(4**32),blocks={k:serialize(v) for k,v in blocks.items()},q8_Gram=serialize(q8),TT_on_M_zero=serialize(tz),M_zero_supports=load(H/'independent_matrix_8x4.json')['M_zero_supports'],UU_Q_squared=serialize(quu),UU_QA_plus_AQ=serialize(qauu),UU_A_squared=serialize(A2),complete_H2_coefficients_g0_g1_g2=[serialize(m) for m in coeff],Gram_rank_pivots=gram_pivots,block_psd_pivots=pivots,coupling_checks=checks,existing_complete_0105_vector_exact_match=True,all_three_independent_scalar_forms_exact_match=True,negative_pencil_uses_even_singlet_cutoff_not_full_Hilbert_lambda2=True,producer_manifest_sha256=sha(pm),producer_all_four_blocks_and_full_polynomial_exact_match=True,no_new_gap_claim=True,independent_run_resources=load(H/'full_run_resources.json'),seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (H/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['seconds'],out['peak_rss_kib'])
if __name__=='__main__':main()
