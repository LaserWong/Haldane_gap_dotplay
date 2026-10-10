exec(open(__file__.replace('diagnose.py','explore.py')).read().split('records=[];results=[]')[0])
import math
rec=json.loads((HERE/'expanded_inputs.json').read_text())[-1];assert rec['g']=='1/4'
def trace(s,beta):
 info=s['expanded_band'];rho=float(F(s['exact_rayleigh']));lo=float(F(s['ground_lower']));alpha=float(F(info['alpha']));B=float(F(info['B']))
 return math.exp(beta*(rho-lo))+sum(m['multiplicity']*math.exp(-beta*(-8+float(F(m['lower']))-rho)) for m in info['comparison_endpoints'][1:])+sum(mult*math.exp(-beta*(-8+alpha*e-B-rho)) for e,mult in info['complete_reference_bins'] if e>=3)
scan.trace=trace
rows=[]
for delta in [0,.0025,.005,.0075,.01,.0125,float(F(rec['large']['exact_rayleigh'])-2*F(rec['small']['exact_rayleigh']))]:
 results=[]
 for j in range(40,1601):
  beta=j/20;r=scan.run(rec['small'],2*float(F(rec['small']['exact_rayleigh']))+delta,beta)
  if r:
   J=math.exp(-2*beta*delta)/trace(rec['small'],beta)**4;initial=scan.interpolate(math.sqrt(J),J,beta,J);r['all_M_ge4_gap']=min(initial,r['all_M_ge8_gap']);results.append(r)
 best=max(results,key=lambda x:x['all_M_ge4_gap']) if results else None
 rows.append(dict(hypothetical_Rayleigh_shift=delta,passes=len(results),best=best));print(rows[-1],flush=True)
(HERE/'diagnostic_sensitivity.json').write_text(json.dumps(dict(status='FLOAT_DIAGNOSTIC_HYPOTHETICAL_INPUTS_NOT_CERTIFICATES',g='1/4',rows=rows,note='Only delta is changed; no corresponding new M8 trial or energy has been certified. Bounded scans are not all-beta impossibility results.'),indent=2))
