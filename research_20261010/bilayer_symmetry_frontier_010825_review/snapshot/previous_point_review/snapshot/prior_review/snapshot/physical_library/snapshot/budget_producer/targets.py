from budget import *
import copy

def sufficient_numerator(r,b):
 # Least multiple1e-10 passing the three fixed target ratios; rigorous witness.
 step=F(1,10**10);guess=max([0.]+[math.log(float(TARGET[k]/r[k]))/float(b*(4 if k=='J2' else 2)) for k in TARGET])
 eps=F(math.ceil(guess*10**10),10**10)
 def good(e):return all(exp(b*(4 if k=='J2' else 2)*e)[0]*r[k]>=TARGET[k] for k in TARGET)
 while not good(eps):eps+=step
 while eps>=step and good(eps-step):eps-=step
 lower=eps-step;failed=[k for k in TARGET if exp(b*(4 if k=='J2' else 2)*lower)[1]*r[k]<TARGET[k]];assert failed
 return eps,dict(epsilon=str(eps),epsilon_display=float(eps),rejected_previous_gridpoint=str(lower),failed_ratios_at_previous=failed,certified_ratios={k:str(exp(b*(4 if k=='J2' else 2)*eps)[0]*r[k]) for k in TARGET})

def exact_conditional_path(d,b,r):
 r={k:C.down(v,80) for k,v in r.items()};assert all(0<x<=1 for x in r.values())
 a=C.down(C.G(r['J1']),80);bb=C.down(C.G(r['J2']*a),80);c=C.down(C.G(r['C0']**4*a*a*bb),80);rr=[a,bb,c];assert min(rr)>0
 can=C.transport(*rr,C.sqrt_down);short,ss=C.short_gap(F(d['coupling_interval'][1]))
 inp=dict(coupling_interval=d['coupling_interval'],beta_initial=str(b),J1=str(r['J1']),J2=str(r['J2']),C0=str(r['C0']),permuted_first_purities=C.st(rr),canonical_first_purities=C.st(can),short_sizes=ss,all_integer_L_ge2_gap='0')
 return improve(inp)

if __name__=='__main__':
 out=[];start=time.time();b=F(47,5)
 for g in (F(21,200),F(11,100)):
  d=DATA[g];r,cc=ratios(d,b,exact=True);eps,witness=sufficient_numerator(r,b)
  saved=d['largest_base_trial'];rho=C.poly(list(map(F,saved['rayleigh_coefficients'])),g)
  vec=C.optimized_vector(P.NUM,g);trial=C.trial(P.NUM,g,vec);newrho=C.poly(list(map(F,trial['rayleigh_coefficients'])),g);gain=rho-newrho
  # This small43D rational Rayleigh evaluation is real, not a hypothetical trace improvement.
  newr,newcc=ratios(d,b,epsilon=gain,exact=True)
  epsr,_=ratios(d,b,epsilon=eps,exact=True);conditional=exact_conditional_path(d,b,epsr)
  row={'g':str(g),'beta':str(b),'current_ratios':{k:str(v) for k,v in r.items()},'target_ratios':{k:str(v) for k,v in TARGET.items()},'components':R.S.serial(cc),'sufficient_numerator':witness,'current_numerator_rayleigh':str(rho),'target_numerator_rayleigh':str(rho-eps),'existing43D_reoptimized_rayleigh':str(newrho),'existing43D_exact_improvement':str(gain),'existing43D_improvement_display':float(gain),'existing43D_fraction_of_target':float(gain/eps),'existing43D_trial':trial,'existing43D_startup':float_path({k:float(v) for k,v in newr.items()},b),'hypothetical_only_conditional_path':conditional}
  out.append(row);print(g,'target',float(eps),'available43D',float(gain),'fraction',float(gain/eps),'conditionalgap',conditional['gap_display'],flush=True)
  (HERE/'targets_checkpoint.json').write_text(json.dumps(out,indent=2)+'\n');exp.cache_clear()
 (HERE/'targets.json').write_text(json.dumps({'status':'exact_conditional_targets_not_new_physical_gap_certificates','results':out,'seconds':time.time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2)+'\n')
