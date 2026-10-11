import os,resource,time,json,hashlib
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(60,60));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent;start=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mat(x):return [[F(v) for v in row] for row in x]
def serial(a):return [[str(x) for x in row] for row in a]
def psd(source,strict=False):
 a=[row[:] for row in source];assert all(a[i][j]==a[j][i] for i in range(len(a)) for j in range(len(a)));piv=[]
 for j in range(len(a)):
  p=a[j][j];assert p>0 if strict else p>=0,(j,p);piv.append(str(p))
  if not p:assert all(a[i][j]==0 for i in range(j+1,len(a)));continue
  for i in range(j+1,len(a)):
   if not a[i][j]:continue
   f=a[i][j]/p
   for k in range(i,len(a)):a[k][i]=a[i][k]=a[i][k]-f*a[k][j]
 return piv
for f,h in json.loads((P/'FULL_INPUT_SHA256.json').read_text()).items():assert sha(P/f)==h,f
oldmf=R/'bilayer_complete_split_H2_8x4_review/MANIFEST_SHA256.json';assert sha(oldmf)=='874c87f1ff9b4b58f795ef5e01aad45ff4f22e560e4721c7a933ed27380166a5'
oldfile=R/'bilayer_complete_split_H2_8x4_review/audit.json';assert sha(oldfile)==json.loads(oldmf.read_text())['audit.json'];old=json.loads(oldfile.read_text())
fresh=json.loads((P/'full.json').read_text());assert fresh['partial'] is False and fresh['q4_processed']==4495 and fresh['q6_processed']==169911
prod=json.loads((R/'bilayer_residual_direction_production_run/checkpoint/complete_row.json').read_text())
for k in ['G','H200','H200_squared']:assert fresh[k]==prod['rows'][k],k
for k in ['T_norm','CT_norm','T_K_T']:assert fresh[k]==prod['scalars'][k],k
assert F(fresh['q8_creation_norm'])==F(fresh['CT_norm'])+F(fresh['T_K_T'])>0
G=mat(old['gram']);hc=list(map(mat,old['H_coefficients']));jc=list(map(mat,old['H2_coefficients']));assert len(G)==57
q=[0]+[2]*14+[4]*28+[6]*15;gg=list(map(F,fresh['G']));hh=list(map(F,fresh['H200']));jj=list(map(F,fresh['H200_squared']))
A=[(h-1200*g)/11 for g,h in zip(gg,hh)];A2=[(j-1440000*g-2200*(6+v)*a)/121 for g,j,v,a in zip(gg,jj,q,A)];assert all(x.denominator==1 for x in A+A2)
poly={'Q_row':[6*x for x in gg],'A_row':A,'Q2_row':[36*x for x in gg],'QA_AQ_row':[(6+v)*a for v,a in zip(q,A)],'A2_row':A2}
for k,v in poly.items():assert list(map(str,v))==prod['polynomial'][k],k
# A second, purely cached derivation of the entire new Gram row and its norm.
c=list(map(F,(R/'bilayer_residual_direction_outer_gate/reference_coefficients.txt').read_text().split()));cr,cm=c[:14],c[14:];oldA=[[2*x for x in row] for row in hc[1]]
for i in range(57):
 expect=sum(cr[j]*oldA[29+j][i]+cm[j]*oldA[43+j][i] for j in range(14)) if q[i]==6 else F(0)
 assert gg[i]==expect,i
blocks={k:mat(v) for k,v in old['blocks'].items()};expectednorm=sum(cr[i]*cr[j]*blocks['R6R6'][i][j]+cr[i]*cm[j]*blocks['R6M6'][i][j]+cm[i]*cr[j]*blocks['R6M6'][j][i]+cm[i]*cm[j]*blocks['M6M6'][i][j] for i in range(14) for j in range(14));assert gg[-1]==expectednorm

def extend(a,row):
 assert len(a)==57 and len(row)==58
 return [a[i]+[row[i]] for i in range(57)]+[row[:]]
G=extend(G,gg);hc=[extend(hc[0],poly['Q_row']),extend(hc[1],[a/2 for a in A])];jc=[extend(jc[0],poly['Q2_row']),extend(jc[1],[a/2 for a in poly['QA_AQ_row']]),extend(jc[2],[a/4 for a in A2])]
for i in range(58):
 for j in range(58):
  assert hc[0][i][j]==q[i]*G[i][j] and jc[0][i][j]==q[i]*q[j]*G[i][j]
  assert jc[1][i][j]==(q[i]+q[j])*hc[1][i][j]
gp=psd(G,True);g=F(11,100);H=[[hc[0][i][j]+g*hc[1][i][j] for j in range(58)] for i in range(58)];J=[[jc[0][i][j]+g*jc[1][i][j]+g*g*jc[2][i][j] for j in range(58)] for i in range(58)];jp=psd(J);block=[G[i]+H[i] for i in range(58)]+[H[i]+J[i] for i in range(58)];bp=psd(block)
out={'status':'PASS_INDEPENDENT_COMPLETE58D_RESIDUAL_DIRECTION','dimension':58,'Gram_rank':58,'all_new_physical_entries_verified':174,'all_coupling_row_entries_verified':290,'new_Gram_row_rederived_from_accepted_cached_matrices':True,'new_T_Schur_norm':gp[-1],'full_q8_norm':fresh['q8_creation_norm'],'Gram_pivots':gp,'H2_pivots_at_g011':jp,'residual_block_116D_pivots_at_g011':bp,'residual_block_116D_PSD':True,'gram':serial(G),'H_coefficients':list(map(serial,hc)),'H2_coefficients':list(map(serial,jc)),'coupling_polynomial_complete':True,'physical_trial_scope':'translation-invariant even-singlet basis; no new ground endpoint or all-size gap claim','cpu_seconds':time.process_time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/(__import__('sys').argv[1] if len(__import__('sys').argv)>1 else 'audit.json')).write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['cpu_seconds'],out['peak_rss_kib'])
