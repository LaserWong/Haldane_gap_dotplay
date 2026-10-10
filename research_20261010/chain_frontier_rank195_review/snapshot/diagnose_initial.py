exec(open(__file__.replace('diagnose_initial.py','common.py')).read())
import math
rec=json.loads((HERE/'expanded_inputs.json').read_text())[0]
s=rec['small'];info=s['expanded_band'];rho=float(F(s['exact_rayleigh']));lo=float(F(s['ground_lower']));a=float(F(info['alpha']));B=float(F(info['B']));delta=float(F(rec['large']['exact_rayleigh'])-2*F(s['exact_rayleigh']))
def trace(beta):return math.exp(beta*(rho-lo))+sum(m['multiplicity']*math.exp(-beta*(-8+float(F(m['lower']))-rho)) for m in info['comparison_endpoints'][1:])+sum(mult*math.exp(-beta*(-8+a*e-B-rho)) for e,mult in info['complete_reference_bins'] if e>=4)
bestP=(-1,0);bestWindow=(-1,0)
for j in range(1,20001):
 beta=j/1000;L=math.exp(-2*beta*delta);J=L/trace(beta)**4;cc=L/trace(2*beta)**2;aa=scan.G(J);bb=scan.G(cc*cc*aa) if aa>0 else -1
 if bb>0:
  P=aa*aa*bb;wg=scan.interpolate(math.sqrt(P),P,2*beta,P)
  if P>bestP[0]:bestP=(P,beta,aa,bb,J,cc)
  if wg>bestWindow[0]:bestWindow=(wg,beta)
print('BEST',bestP,bestWindow,flush=True)
(HERE/'initial_diagnostic.json').write_text(json.dumps(dict(status='FLOAT_DIAGNOSTIC_ONLY',best_P=bestP,best_window=bestWindow,first_window_P_threshold=(5-math.sqrt(5))/4),indent=2))
