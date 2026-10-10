"""Bounded floating scalar scan only, no physical spectra."""
import replay as R
import math,json
F=R.F
rec=json.loads(R.SOURCE.read_text())[0];s=rec['small'];info=s['expanded_band'];rho=float(F(s['exact_rayleigh']));lo=float(F(s['ground_lower']));alpha=float(F(info['alpha']));B=float(F(info['B']));delta=float(F(rec['large']['exact_rayleigh'])-2*F(s['exact_rayleigh']))
def trace(x):return math.exp(x*(rho-lo))+sum(t['multiplicity']*math.exp(x*(rho+8-float(F(t['lower'])))) for t in info['comparison_endpoints'][1:])+sum(m*math.exp(x*(rho+8-alpha*e+B)) for e,m in info['complete_reference_bins'] if e>=4)
def G(x):return 1-(1-x)**2/(2*x*x) if x>0 else -1
best_bridge=(-1,);best_nextarg=(-1,);best_initial=(-1,);count=0
for i in range(1,12001):
 beta=i/1000;L=math.exp(-2*beta*delta);J=L/trace(beta)**4;C=L/trace(2*beta)**2;a=G(J);b=G(C*C*a) if a>0 else -1
 if b>0:
  P=a*a*b;ap=G(P);arg=b*b*ap
  if arg>best_nextarg[0]:best_nextarg=(arg,beta,a,b,P,ap,G(arg))
  if b>.5:
   uniform=a*a*math.sqrt(2*b-1);count+=uniform>.5
   if uniform>best_bridge[0]:best_bridge=(uniform,beta,a,b)
 if C>.5:
  initial=J*math.sqrt(2*C-1)
  if initial>best_initial[0]:best_initial=(initial,beta,J,C)
out=dict(status='FLOAT_DIAGNOSTIC_NOT_CERTIFICATE_OR_GLOBAL_NO_GO',beta_grid=[.001,12,.001],best_uniform_first_bridge=best_bridge,number_passing_first_bridge=count,best_next_time_spatial_argument=best_nextarg,best_initial_4_8=best_initial)
(R.HERE/'diagnostic.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
