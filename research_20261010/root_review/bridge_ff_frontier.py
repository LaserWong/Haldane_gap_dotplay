"""Finite-window completion of independently audited FF epsilon samples."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from finite_window_2d import interpolate_2d,gap
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent

def down(x):return F((x.numerator<<128)//x.denominator,1<<128)
def G(x):return 1-(1-x)**2/(2*x*x)

def main():
 allrows=[]
 for eps in ['1d125','17d2000']:
  p=ROOT/'research_20261010/nonperturbative_audit/epsilon_scan'/f'ff_eps{eps}_selected_seeds.json';source=json.loads(p.read_text());rows=[]
  for seed in source['seeds']:
   boot=seed['bootstrap']
   if not boot.get('accepted'):continue
   C=F(seed['C_lower']);aa=down(G(F(seed['J1_lower'])));bb=down(G(F(seed['J2_lower'])*aa));cc=down(G(C**4*aa**2*bb))
   states=[[F(seed[k]) for k in ['A_lower','B_lower','C_lower']],[aa,bb,cc]]+[list(map(F,x)) for x in boot['updates']]
   beta=F(seed['beta']);windows=[]
   for j,state in enumerate(states):
    n=2*2**j
    if n>=boot['n']:break
    t,details=interpolate_2d(*state);b=beta*2**j;lower=gap(t,b)
    windows.append({'n':n,'through':2*n,'beta':str(b),'purities':list(map(str,state)),'thermal_lower':str(t),'gap_lower':str(lower),'details':details})
   assert windows[0]['n']==2 and windows[-1]['through']==boot['n']
   final=min([F(boot['gap_lower'])]+[F(x['gap_lower']) for x in windows])
   rows.append({'initial_beta':str(beta),'original_asymptotic_n':boot['n'],'original_gap':boot['gap_lower'],'windows':windows,'all_integer_L_ge2_gap':str(final),'gap_display':float(final)})
  best=max(rows,key=lambda r:F(r['all_integer_L_ge2_gap']))
  rec={'epsilon':source['epsilon'],'source':str(p.relative_to(ROOT)),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':'exact scalar bridge; physical seed already independently audited in nonperturbative_audit','records':rows,'best':{k:v for k,v in best.items() if k!='windows'}};allrows.append(rec)
  print(rec['epsilon'],rec['best'])
 (OUT/'ff_frontier_finite_windows.json').write_text(json.dumps(allrows,indent=2)+'\n')
if __name__=='__main__':main()
