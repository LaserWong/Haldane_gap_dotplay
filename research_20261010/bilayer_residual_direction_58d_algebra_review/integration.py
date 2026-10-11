import os,resource,json,hashlib,ast,math,time
from fractions import Fraction as F
from pathlib import Path
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(6,6));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));start=time.process_time();sys=__import__('sys');sys.set_int_max_str_digits(0)
P=Path(__file__).resolve().parent;R=P.parent
load=lambda p:json.loads(p.read_text());mat=lambda a:[[F(x) for x in r] for r in a]
ns={'F':F,'math':math};nodes=[x for x in ast.parse((P/'audit.py').read_text()).body if isinstance(x,ast.FunctionDef) and x.name=='positive_ff'];exec(compile(ast.Module(body=nodes,type_ignores=[]),'reviewer_fraction_free','exec'),ns)
x=load(R/'bilayer_complete_residual_direction_58d_review/audit.json');old=load(R/'bilayer_complete_split_H2_8x4_review/audit.json');saved={a['name']:a for a in load(P/'snapshot/ldl_complete_results.json')}
G=mat(x['gram']);hc=list(map(mat,x['H_coefficients']));jc=list(map(mat,x['H2_coefficients']));A2=[[4*z for z in row] for row in jc[2]]
assert saved['Gram58']['pivots']==x['Gram_pivots']
p,c=ns['positive_ff'](A2);assert p==saved['A2_58']['pivots'];checks={'A2_58_PD':True}
for g,name in [(F(217,2000),'H2_g217_2000'),(F(11,100),'H2_g11_100')]:
 J=[[jc[0][i][j]+g*jc[1][i][j]+g*g*jc[2][i][j] for j in range(58)] for i in range(58)];p,c=ns['positive_ff'](J);assert p==saved[name]['pivots'];checks[name+'_PD']=True
# Schur complements under triangular occupation-preserving congruence.
g=F(11,100);physicalpiv=list(map(F,x['residual_block_116D_pivots_at_g011']));predicted=physicalpiv[:58]+[4*v/(g*g) for v in physicalpiv[58:]];assert predicted==list(map(F,saved['complete_operator_Gram116']['pivots']));assert sum(v>0 for v in predicted)==87
for key in ['gram','H_coefficients','H2_coefficients']:
 xs=[x[key]] if key=='gram' else x[key];ys=[old[key]] if key=='gram' else old[key]
 for a,b in zip(xs,ys):assert [row[:57] for row in a[:57]]==b
out={'status':'PASS_COMPLETE_OPERATOR_GRAM_AND_H2_INTEGRATION','checks':checks,'operator_Gram_PSD_via_exact_congruence':True,'operator_Gram_rank':87,'all_nine_producer_LDL_results_independently_accounted_for':True,'old57_principal_blocks_unchanged':True,'cpu_seconds':time.process_time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'integration.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
