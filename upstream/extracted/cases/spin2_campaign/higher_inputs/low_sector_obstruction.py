"""Rigorous all-state low-magnetization bound, without assuming Ritz completeness."""
import json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from verify_cluster_and_tail import rational_exp_minus_upper
ROOT=Path(__file__).resolve().parent

def exp_upper(x):
 if x<=0:return rational_exp_minus_upper(-x)
 K=2*math.ceil(x)+100;term=total=F(1)
 for k in range(1,K+1):term*=x/k;total+=term
 nxt=term*x/(K+1)
 return total+nxt/(1-x/(K+2))
def short_up(x,digits=12):
 sc=10**max(0,digits-math.floor(math.log10(float(x))));return F(-((-x.numerator*sc)//x.denominator),sc)
a=F(5951,1250);beta=8;dim=np.array([1],dtype=object)
for _ in range(10):dim=np.convolve(dim,np.ones(5,dtype=object))
bounds=json.loads((ROOT/'cluster_envelopes.json').read_text())['n10_sector_lower_bounds'];out={'n':10,'beta':beta,'a':str(a),'sectors':[]}
total=F(0);formal=F(0)
for m in range(5):
 E=F(bounds[str(m)]['lower']);mult=1 if m==0 else 2;D=int(dim[20+m]);factor=exp_upper(-beta*(E+10*a));upper=mult*D*factor;omitted=mult*(D-16)*factor
 total+=upper;formal+=omitted
 out['sectors'].append({'abs_m':m,'single_m_dimension':D,'pm_multiplicity':mult,'energy_lower':str(E),'energy_lower_display':float(E),'all_state_trace_upper':str(short_up(upper)),'all_state_trace_upper_display':float(short_up(upper)),'remaining_D_minus_16_upper_display':float(short_up(omitted))})
out['all_low_M_states_trace_upper']=str(short_up(total));out['all_low_M_states_trace_upper_display']=float(short_up(total));out['formal_remaining_D_minus_16_upper_display']=float(short_up(formal));out['important']='D-16 bound is for removing ANY 16 exact energy eigenstates per M sector; no assertion the available Ritz lists have been certified as such. Unconditional result is the all-state trace upper bound.'
(ROOT/'low_sector_obstruction.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
