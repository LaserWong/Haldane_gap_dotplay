"""Exact rational two-vector Rayleigh optimization of psi and one full H image."""
import json,math
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
m=json.loads((HERE/'full.json').read_text());rec=json.loads((HERE.parent/'chain_frontier_rank195/expanded_inputs.json').read_text())[0]
N=F(m['norm']);den=m['integer_denominator'];mom=[F(1)]+[F(m[f'moment{k}_scaled'])/(den**k*N) for k in range(1,4)];rho=mom[1];assert rho==F(rec['large']['exact_rayleigh']);var=mom[2]-rho*rho;hrr=mom[3]-2*rho*mom[2]+rho**3;assert var>0
B=hrr/var;off=math.sqrt(float(var));delta=float(B-rho);gain=2*float(var)/(math.sqrt(delta*delta+4*float(var))+delta);tau=F(round(-gain/float(var)*10**12),10**12)
new=(rho+2*tau*var+tau*tau*hrr)/(1+tau*tau*var);assert new<rho
# Exact LDL lower bound on every Rayleigh quotient in the span psi,Hpsi.
target=2*F(rec['small']['exact_rayleigh'])+F(19,1250)
piv1=rho-target;piv2=hrr-target*var-var*var/piv1 if piv1 else F(-1)
within_span_cannot_reach_target=piv1>0 and piv2>0
out=dict(status='EXACT_RAYLEIGH_CANDIDATE_PENDING_INDEPENDENT_REVIEW',g='1/4',moment_file='full.json',trial_dimension=2,image_support=m['image_support'],full_dimension=43046721,base_rayleigh=str(rho),variance=str(var),centered_H_moment=str(hrr),residual_direction_rayleigh=str(B),tau=str(tau),trial_formula='psi + tau*(H-rho)*psi; phi=den*Hpsi saved explicitly. The centered image is a trial direction, not a claimed full residual certificate.',exact_rayleigh=str(new),improvement=str(rho-new),improvement_display=float(rho-new),new_delta=str(new-2*F(rec['small']['exact_rayleigh'])),new_delta_display=float(new-2*F(rec['small']['exact_rayleigh'])),necessary_target_rayleigh=str(target),necessary_target_improvement=str(rho-target),meets_necessary_target=new<target,span_exclusion=within_span_cannot_reach_target,span_target_LDL_pivots=list(map(str,[piv1,piv2])),contract='Numerator-only Rayleigh quotient. No full H^2 output, filtered residual, isolation or omitted-state tail is used.')
(HERE/'rayleigh.json').write_text(json.dumps(out,indent=2));print('GAIN',float(rho-new),'newdelta',float(new-2*F(rec['small']['exact_rayleigh'])),'targetmet',new<target,'spanexcluded',within_span_cannot_reach_target,flush=True)
