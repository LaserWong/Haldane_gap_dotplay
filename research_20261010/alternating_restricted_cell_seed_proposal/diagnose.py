import json,math,time,hashlib
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];st=time.process_time();C=json.loads((P/'certificate.json').read_text());B=10**90
# Import definitions only using AST; do not execute the producer's top-level verification.
import ast
mod=ast.parse((P/'verify.py').read_text());ns={'F':F,'G':B,'math':math};exec(compile(ast.Module(body=[x for x in mod.body if isinstance(x,ast.FunctionDef)],type_ignores=[]),'<scalar-definitions>','exec'),ns)
down,expi,root=(ns[x] for x in ['down','expi','root']);g=lambda x:1-(1-x)**2/(2*x*x)
rows=[]
for row in C['rows']:
 last=row['states'][-1];s,t=F(last['S']),F(last['T']);k=down(s*s*t);sn=down(g(k));tn=down(g(down(t*t*sn))) if sn>0 else None
 assert sn<=0 or tn<=0
 rows.append({'cell_seed':row['cell_seed'],'last_positive_state':last,'next_K':str(k),'next_S':str(sn),'next_T':str(tn) if tn is not None else None,'failed_next_S_display':float(sn),'failed_next_T_display':float(tn) if tn is not None else None})
# Test a concrete sufficient improvement in only the cell17 thermal endpoint.
r=C['rows'][2];s,t=F(r['S']),F(167,200);beta=F(49,4);gap=F(1,200);states=[]
for j in range(16):
 cc=down(min(s*root(t,2)[0],t));e=expi(beta*gap)[1];margin=cc-e*(1-cc);assert margin>0
 u=max(1-s,1-t);states.append({'round':j,'beta':str(beta),'S':str(s),'T':str(t),'Cpos':str(cc),'gap_margin':str(margin)})
 if u<=F(1,100) and 5*u*e<1:break
 s=down(g(down(s*s*t)));assert s>0;t=down(g(down(t*t*s)));assert t>0;beta*=2
else:raise AssertionError('counterfactual did not close')
e2=expi(-F(49,2)*F(r['anchor_R']))[0];qmax=root(e2/F(167,200),2)[0]
# Necessary one-atom conditions are still inconclusive for midpoint data near cap.
m=[(F(a)+F(b))/2 for a,b in C['moments']['J']];t=F(100315,100000);res=[m[i]-t**(i+2) for i in range(5)]
def ldl(A):
 A=[list(r) for r in A];p=[]
 for j in range(len(A)):
  d=A[j][j];assert d>0;p.append(d)
  for k in range(j+1,len(A)):
   for l in range(j+1,len(A)):A[k][l]-=A[k][j]*A[j][l]/d
 return p
H=[[res[i+j] for j in range(3)] for i in range(3)];K=[[res[1+i+j] for j in range(2)] for i in range(2)];hp,kp=ldl(H),ldl(K)
# Pin consumed inherited source members and check uniform anchors against independent outputs.
checks={}
for name in ['uniform_alternating_positive_cell_review','uniform_second_thermal_full_review','uniform_smaller_second_initialization_review']:
 folder=P.parent/name;mf=json.loads((folder/'MANIFEST_SHA256.json').read_text());files=['PROOF.md']
 if name=='uniform_second_thermal_full_review':files+=['progress_results.json']
 if name=='uniform_smaller_second_initialization_review':files+=['anchors.out','anchor_results.json']
 for f in files:
  got=hashlib.sha256((folder/f).read_bytes()).hexdigest();assert mf[f]==got;checks[f'{name}/{f}']=got
ind={k:int(v) for line in (P.parent/'uniform_smaller_second_initialization_review/anchors.out').read_text().splitlines() if '=' in line for k,v in [line.split('=')]}
prod={}
for f in ['anchors.out','anchor60.out']:
 prod.update({k:int(v) for line in (P.parent/'uniform_smaller_second_initialization'/f).read_text().splitlines() for k,v in [line.split('=')]})
for n in [60,64,68]:
 for prefix in ['N0','H0']:assert prod[f'{prefix}_{n}']==ind[f'{prefix}_{n}']
# Confirm each selected table W was independently matched in the accepted full review.
review=json.loads((P.parent/'uniform_second_thermal_full_review/progress_results.json').read_text());selected=[x for x in review['cases'] if int(x['case'].split('_')[0][1:])%2==0];assert len(selected)==10 and all(x['exact_published_match'] for x in selected)
out={'actual_seed_obstructions':rows,'counterfactual_only':{'label':'not an achieved seed; exact sufficient target for future improvement','cell_seed':17,'S_fixed':r['S'],'T_required_sufficient':'167/200','gap':'1/200','Q_sufficient_upper':str(qmax),'Q_sufficient_display':float(qmax),'present_Q_display':float(F(r['Q'])),'states':states,'closure_margin':str(1-5*u*e)},'midpoint_one_atom_nonexclusion':{'atom':str(t),'H3_residual_positive_LDL_pivots':list(map(str,hp)),'positive_half_line_localizer_K2_pivots':list(map(str,kp)),'scope':'necessary positive weighted-moment constraints only; not an integer spectrum or physical realization'},'source_member_checks':checks,'matched_independent_anchors':[60,64,68],'matched_even_heat_cases':[x['case'] for x in selected],'cpu_seconds':time.process_time()-st}
(P/'diagnostics.json').write_text(json.dumps(out,indent=2)+'\n');print('failed states',[(r['cell_seed'],r['failed_next_S_display'],r['failed_next_T_display']) for r in rows]);print('counterfactual gap .005 closure',j,'Q sufficient',float(qmax),'LDL witness',list(map(float,hp)),list(map(float,kp)));print('DONE',out['cpu_seconds'])
