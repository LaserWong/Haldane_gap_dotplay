"""Independent support-result assembly and full coupling-polynomial derivation."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import resource
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_AS,(250*1024**2,250*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import ast,itertools,json,hashlib,math,time,copy
import numpy as np
HERE=Path(__file__).resolve().parent;S=HERE/'snapshot';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def eq(a,b):assert a==b

def verify():
 for rel,h in load(HERE/'INPUT_SHA256.json').items():assert sha(S/rel)==h
 p=load(S/'PRIOR_PHYSICAL_REVIEW_MANIFEST.json');p=p.get('files',p)
 for name,row in load(HERE/'ENGINE_PROVENANCE.json').items():
  file=HERE/name if name.startswith('independent') else S/name
  assert sha(file)==row['sha256']==p[row['manifest_entry']]
 struct=load(S/'STRUCTURAL_REVIEW_MANIFEST.json');struct=struct.get('files',struct)
 assert sha(S/'MATRIX_REBUILD.py')==struct['audit_matrices.py']
 g=load(S/'producer/physical_result.json')['geometry'];tag='x'.join(map(str,g))
 assert sha(S/f'GEOMETRY_{tag}.json')==struct[f'results/geometry_{tag}.json']
 br=load(S/'BUDGET_REVIEW_MANIFEST_SHA256.json');assert sha(S/'BUDGET_REVIEW_ACCEPTANCE.json')==br['ACCEPTANCE.json']
 assert load(S/'BUDGET_REVIEW_ACCEPTANCE.json')['status']=='PASS_SCOPED_CONDITIONAL_TARGETS_ONLY'
 for name in ('joint_targets.json','reoptimized_saved.json'):assert sha(S/name)==load(S/'BUDGET_PRODUCER_MANIFEST.json')[name]
 return tuple(g)

def reconstruct(shape):
 names=['mat','zero','graph','rebuild'];ns=dict(F=F,np=np,Counter=Counter,defaultdict=defaultdict,itertools=itertools)
 nodes=[x for x in ast.parse((S/'MATRIX_REBUILD.py').read_text()).body if isinstance(x,ast.FunctionDef) and x.name in names]
 assert {x.name for x in nodes}==set(names);exec(compile(ast.Module(body=nodes,type_ignores=[]),'accepted_independent_matrix_rebuild','exec'),ns)
 geo=load(S/f'GEOMETRY_{shape[0]}x{shape[1]}.json');z=ns['rebuild'](*shape,F(0),geo);one=ns['rebuild'](*shape,F(1),geo)
 ed,orbits,ids=ns['graph'](*shape);d=len(orbits);N=math.prod(shape)
 text=(S/f'geometry_{shape[0]}x{shape[1]}.txt').read_text().split();it=iter(map(int,text));assert next(it)==N and next(it)==d;ne=next(it);saved={}
 for _ in range(ne):a,b,w=next(it),next(it),next(it);saved[a,b]=w
 assert dict(ed)==saved
 for a,b in itertools.combinations(range(N),2):assert next(it)==ids[a,b]
 assert list(it)==[]
 return geo,z['G'].tolist(),[z['A'].tolist(),(one['A']-z['A']).tolist()],d

def contract(c,m):return sum(F(c[i])*F(m[i][j])*c[j] for i in range(len(c)) for j in range(len(c)))
def reference(N,g,q):
 D=10**60;x=1-4*g;r=F(math.isqrt(x.numerator*D*D//x.denominator),D);assert r*r<=x<(r+F(1,D))**2
 C=F(3*N,8);return C*(2*g-1)+(C+q)*r

def full_polynomial(c,geo,G,K,mean,second,g):
 # Split the mixed U=R(q4)+M(q6) columns into homogeneous sectors.
 n=len(geo['F']);b=n+1;D=4*n+1;cc=c+c[-n:];q=[0]+[2]*n+[4]*(2*n)+[6]*n
 GG=[[F(0)]*D for _ in range(D)];AA=[[F(0)]*D for _ in range(D)]
 for i in range(b):
  for j in range(b):GG[i][j]=F(G[i][j]);AA[i][j]=2*F(K[1][i][j])
 for i in range(n):
  for j in range(n):
   f,s,v,w,x,y,z=[F(geo[key][i][j]) for key in ('F','S','V','W','X','Y','Z')];li,ri,mi=b+i,b+n+i,b+2*n+i;lj,rj,mj=b+j,b+n+j,b+2*n+j
   GG[li][lj]=f;GG[li][rj]=GG[rj][li]=s;GG[ri][rj]=v;GG[mi][mj]=w
   AA[1+i][lj]=AA[lj][1+i]=f;AA[1+i][rj]=AA[rj][1+i]=s
   AA[li][lj]=s;AA[li][rj]=AA[rj][li]=v;AA[li][mj]=AA[mj][li]=w;AA[ri][rj]=x;AA[ri][mj]=AA[mj][ri]=y;AA[mi][mj]=z
 assert GG==list(map(list,zip(*GG))) and AA==list(map(list,zip(*AA)))
 expect=lambda M,weight:sum(F(cc[i])*M[i][j]*cc[j]*weight(i,j) for i in range(D) for j in range(D))
 norm=expect(GG,lambda i,j:1);q1=expect(GG,lambda i,j:q[j]);q2=expect(GG,lambda i,j:q[i]*q[j]);a1=expect(AA,lambda i,j:1);qa=expect(AA,lambda i,j:q[i]+q[j]);t=g/2
 a2=(second*norm-q2-t*qa)/(t*t);rho=[q1/norm,a1/(2*norm)];h2=[q2/norm,qa/(2*norm),a2/(4*norm)];var=[h2[0]-rho[0]**2,h2[1]-2*rho[0]*rho[1],h2[2]-rho[1]**2]
 assert norm==contract(c,G) and sum(rho[i]*g**i for i in range(2))==mean and sum(h2[i]*g**i for i in range(3))==second
 assert var[0]>=0 and var[2]>=0 and 4*var[0]*var[2]>=var[1]**2
 return dict(norm=str(norm),coefficients=c,rayleigh_coefficients=list(map(str,rho)),full_second_moment_coefficients=list(map(str,h2)),complete_variance_coefficients=list(map(str,var)),expanded_homogeneous_dimension=D,operator_identity_for_all_real_g=True)

def main():
 start=time.monotonic();shape=verify();N=math.prod(shape);geo,G,K,n=reconstruct(shape);dim=3*n+1;b=n+1
 tr=load(S/'producer/trial.json');t=tr['trial'];g=F(tr['g']);assert g==F(21,200)
 c=t['integer_coefficients'];assert len(c)==dim==t['trial_dimension'] and t['geometry']==list(shape) and t['N']==N
 assert all(type(x)is int and abs(x)<=2**48 for x in c)
 den,h=tr['integer_denominator'],tr['integer_A_coefficient'];assert den==400 and h==21 and F(h,den)==g/2
 assert list(map(int,(S/'producer/coefficients.txt').read_text().split()))==[den,h]+c[1:]
 target=next(x for x in load(S/'joint_targets.json')['results'] if F(x['g'])==g)
 if N==32:assert t==target['optimized43D_8x4_trial']
 norm=contract(c,G);rho=[contract(c,m)/norm for m in K];mean=rho[0]+g*rho[1]
 assert norm>0 and F(t['integer_metric_norm'])==norm and list(map(F,t['rayleigh_coefficients']))==rho and mean==F(tr['candidate_shifted_rayleigh'])
 actual=load(HERE/'independent_result.json');saved=load(S/'producer/raw_residual.json')
 for key,value in actual.items():
  if key!='seconds':assert value==saved[key],key
 assert saved['N']==N and saved['fixed_origin'] is True and saved['partial'] is False
 assert actual['q4_processed']==math.comb(N-1,3) and actual['q6_processed']==math.comb(N-1,5)
 assert F(actual['q8_creation_norm'])==F(actual['CM_norm'])+F(actual['commutator_expectation'])>=0
 assert F(actual['Tpsi_q6_norm_on_M_zero_supports'])>0
 Ki=[[den*(F(K[0][i][j])+g*F(K[1][i][j])) for j in range(dim)] for i in range(dim)];assert all(v.denominator==1 for row in Ki for v in row)
 assert all(G[i][j]==0 for i in range(b) for j in range(b) if i!=j)
 kc=[sum(Ki[i][j]*c[j] for j in range(dim)) for i in range(b)]
 sectors={'0':kc[0]**2/F(G[0][0]),'2':sum(kc[i]**2/F(G[i][i]) for i in range(1,b)),'4':F(actual['Tpsi_q4_norm']),'6':F(actual['Tpsi_q6_norm']),'8':h*h*F(actual['q8_creation_norm'])}
 second=sum(sectors.values())/(den**2*norm);var=second-mean*mean;assert var>0
 a1,a=reference(N,g,1),reference(N,g,2);assert mean<a1<a
 # Previously independently verified z=.1 odd directions exhaust the low band.
 rec=next(x['data'] for x in load(S/'reoptimized_saved.json')['results'] if F(x['g'])==g);patch=next(x for x in rec['denominator_patches'] if x['N']==N)
 modes=patch['odd_band']['modes'];assert len(modes)==N and patch['odd_band']['spin_multiplicity']==3
 assert all(max(F(v[1]) for v in m['theta_endpoint_enclosures'])<a for m in modes)
 assert sum(math.comb(3*N+q-1,q) for q in range(N+1))>=4**N
 lower=mean-var/(a-mean);L=F(tr['target_ground_lower']);assert L==F(target[f'target_ground{N}_lower'])
 budget=(mean-L)*(a-mean);assert budget==F(tr['residual_squared_budget'])
 prod=load(S/'producer/physical_result.json');expected=dict(norm=str(norm),shifted_Rayleigh=str(mean),second_moment=str(second),complete_variance=str(var),sector_Tint_norms={k:str(v) for k,v in sectors.items()},global_first_excited_lower=str(a1),even_sector_cutoff=str(a),ground_lower=str(lower),target_variance_budget=str(budget),target_met=var<=budget)
 for k,v in expected.items():assert prod[k]==v,k
 assert prod['full_Hilbert_dimension']==str(4**N) and prod['search_dimension']==dim and prod['retained_ground_states']==1
 polynomial=full_polynomial(c,geo,G,K,mean,second,g)
 out=dict(status='PASS_COMPLETE_NEW_VECTOR_PHYSICAL_RESIDUAL_AND_TEMPLE',g=str(g),geometry=list(shape),trial_dimension=dim,full_Hilbert_dimension=str(4**N),**expected,variance_display=float(var),ground_lower_display=float(lower),full_q8_verified=True,M_zero_q6_image_kept=True,physical_gap_claim=False,polynomial=polynomial,independent_contraction=load(HERE/'independent_resources.json'),assembly_seconds=time.monotonic()-start,assembly_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (HERE/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print({k:out[k] for k in ('status','geometry','variance_display','ground_lower_display','target_met','assembly_seconds','assembly_peak_rss_kib')})
if __name__=='__main__':main()
