"""Exact posterior size-budget examples. No eigensolves or physical-input mutation."""
from criteria import *
from math import isqrt

def display_row(**kwargs):return {k:float(v) if isinstance(v,F) else v for k,v in kwargs.items()}
def qform(mat,v):return sum(v[i]*sum(F(a)*v[j] for j,a in enumerate(row)) for i,row in enumerate(mat))
def sqrt_lower(x,digits=40):
 s=10**digits;n=isqrt(x.numerator*s*s//x.denominator);assert F(n,s)**2<=x<F(n+1,s)**2;return F(n,s)
def inverse_G_upper(p):return 1/(1+sqrt_lower(2*(1-p)))
def replay_state(p):
 p=list(p);hist=[]
 for n in range(180):
  if min(p)>=F(499,500):return dict(status='accepted',updates=n,final=p,history=hist)
  q=down(G(p[0]**4*p[1]**2*p[2]));hist.append(q)
  if q<=0:return dict(status='nonpositive',updates=n+1)
  p=p[1:]+[q]
 return dict(status='inconclusive')
def bands_at_beta(g,beta):
 recs=load_band(g);rows=[]
 for r in recs:
  a=F(r['global_lambda_kplus1_lower']);L0=F(r['global_ground_lower']);rr=F(r['ritz_max_upper']);eps=F(r['residual_squared_bound']);delta=a-rr
  sigma=min(F(1),eps/delta**2);b=a-(a-L0)*sigma
  assert b==F(r['orthogonal_complement_lower']);assert b>rr
  lo,hi,tail,bandhi=trace(r,beta);cut=F(r['number_sector_bins']['bins'][1]['lower']);shift=F(r['blocks'][0]['eigen_upper'][0]);q1=3*r['N']*exp_bounds(-beta*(cut-shift))[1]
  widths=[F(u)-F(l) for bl in r['blocks'] for l,u in zip(bl['eigen_lower'],bl['eigen_upper'])]
  rows.append(dict(N=r['N'],full_hilbert=r['full_hilbert_dimension'],retained_rank=r['retained_full_band_dimension'],ground_search_dimension=r['blocks'][0]['trial_dimension'],ground_configuration_support=r['blocks'][0].get('expanded_trial_dimension'),full_ground_action_support=r['blocks'][0]['reached_dimension'],a=a,L0=L0,ritz_max=rr,separation=delta,residual_squared_bound=eps,complement_lower=b,sufficient_residual_limit_for_positive_complement=delta**3/(a-L0),uniform_schur_width_bound=eps/(b-rr),actual_maximum_width=max(widths),ground_width=widths[0],beta=beta,trace_lower=lo,trace_upper=hi,relative_width_cost=(bandhi-lo)/lo,relative_omitted_tail=tail/lo,q1_omitted_bin_upper=q1,retained_thermal_excitation_lower=lo-1,tail_start_q=2))
 return dict(g=g,beta=beta,patches=rows,canonical_inputs_lower=input_lower(recs,beta),lower_replay=recursion(input_lower(recs,beta)),canonical_inputs_upper=input_upper(recs,beta,beta),upper_replay=recursion(input_upper(recs,beta,beta),True))

def startup_budget_example():
 recs=load_band('3d100');beta=F(909,100);target=[F(9706,10000),F(9567,10000),F(987,1000)];replay=replay_state(target);assert replay['status']=='accepted'
 h=[inverse_G_upper(p) for p in target];assert all(G(x)>=p for x,p in zip(h,target))
 ts=[trace(r,beta) for r in recs];Lup=[sum_exp(spectrum_terms(r)[0],beta,True) for r in recs];es=energy_shifts(recs);n=trace(recs[2],2*beta)[0]
 star=[down(exp_bounds(beta*(-2*es[2]+8*es[0]))[0]*n/Lup[0]**8),down(exp_bounds(beta*(-4*es[2]+8*es[1]))[0]*n*n/Lup[1]**8),down(n/Lup[2]**2)]
 H=[up(t[1]/t[0]) for t in ts]
 budget8=[star[0]/h[0],star[1]*target[0]/h[1],star[2]**4*target[0]**2*target[1]/h[2]]
 assert all(H[i]**8<=budget8[i] for i in range(3))
 return dict(beta=beta,target_first_state=target,target_state_replay=replay,inverse_G_upper=h,idealized_truncated_inputs_lower=star,allowed_trace_factor_eighth_power=budget8,actual_trace_factor_upper=H,maximum_relative_trace_excess_display=[float(x)**(1/8)-1 for x in budget8],actual_relative_trace_excess_display=[float(x-1) for x in H],status='PASS exact eighth-power startup-budget inequalities')

def ground_moment_examples():
 out=[]
 for g in ['1d50','3d100','1d25','1d20']:
  for shape in ['4x4','8x4','8x8']:
   d=read(f'research_20261010/large_seed_moments/block1_{shape}_g{g}.json');v=list(map(int,d['coefficients']));norm=qform(d['gram'],v);den=F(d['integer_matrix_denominator']);e=qform(d['shifted_hamiltonian_numerator'],v)/(norm*den);rs=qform(d['shifted_H2_numerator'],v)/(norm*den**2)-e*e
   rho=F(d['E00'])+e;assert rho==F(d['exact_rayleigh']);assert rs==F(d['exact_residual_squared']);assert rs>=0
   threshold=F(d['second_eigenvalue_lower']);width=rs/(threshold-rho) if threshold>rho else None
   if width is not None:assert F(d['ground_lower'])==rho-width
   out.append(dict(g=g,shape=shape,full_hilbert=d['full_dimension'],compressed_ground_dimension=d['trial_subspace_dimension'],retained_ground_states=d['retained_states'],exact_residual_squared=rs,affine_separation=threshold-rho,old_affine_Temple_width=width,status='PASS exact scalar contraction of all saved G,H,H2 entries; underlying physical moments retain source review status'))
 return out

def g002_example():
 source=read('seed_size/results/optimized_bilayer_tail_results.json');d=next(x['best_grid_gap'] for x in source if x['g']=='1/50' and x['order']=='xyt');beta=F(d['beta_initial']);nodes=d['thermal_tail_nodes'];ts=[]
 for nd in nodes:
  par=nd['parameters'];N=nd['N_dimers'];bb=F(nd['beta']);a=F(par['alpha']);B=F(par['B_upper']);eu=F(nd['ground_upper']);el=F(nd['ground_lower']);E00=F(nd['E00'])
  tail=sum(F(math.comb(N,q)*3**q)*exp_bounds(-bb*(E00+a*q-B-eu))[1] for q in range(1,N+1));qu=exp_bounds(bb*(eu-el))[1]+tail
  assert qu<=F(par['upper_Q']);ts.append(qu)
 e=[F(n['ground_upper']) for n in nodes[:3]]
 inp=[down(exp_bounds(beta*(-2*e[2]+8*e[0]))[0]/ts[0]**8),down(exp_bounds(beta*(-4*e[2]+8*e[1]))[0]/ts[1]**8),down(1/ts[2]**2)]
 replay=recursion(inp);assert replay['status']=='entered_small_defect_domain'
 return dict(g='1/50',beta=beta,retained_rank=[1,1,1],search_dimensions=[x['trial_subspace_dimension'] for x in d['ground_certificate_records']],configuration_action_support=[x['reached_support_dimension'] for x in d['ground_certificate_records']],trace_uppers=ts,inputs_lower=inp,replay=replay,audited_uniform_gap=F(d['gap_lower']),status='PASS newly recomputed positive-sum traces and startup; physical and integer-size proof supplied by bilayer_audit')

def ff_examples():
 audit=read('research_20261010/epsilon_interval_review/audit_results.json');extensions=read('research_20261010/epsilon_interval_extension/extension_certificates.json')+read('research_20261010/epsilon_interval_extension/frontier_certificates.json');out=[]
 for a in audit['intervals']:
  d=next(r for r in extensions if r['epsilon_interval']==a['epsilon_interval']);l,h=map(F,a['epsilon_interval']);blocks=[]
  for r in d['ground_records']:
   p=audit['physical_polynomials'][r['polynomial_key']];rho=list(map(F,p['Rayleigh_coefficients']));res=list(map(F,p['full_residual_squared_coefficients']));assert res[2]>=0
   rmax=max(res[0]+res[1]*x+res[2]*x*x for x in (l,h));rhomax=max(rho[0]+rho[1]*x for x in (l,h));sep=F(r['uniform_second_eigenvalue_lower'])-rhomax;assert sep>0
   delta=rmax/sep;assert rmax==F(r['residual_squared_max']);assert delta==F(r['uniform_Temple_correction'])
   blocks.append(dict(geometry=p['geometry'],search_dimension=p['trial_dimension'],retained_rank=1,support_full_action=p['full_action_union'],residual_squared_max=rmax,uniform_separation=sep,uniform_width=delta))
  inp=[down(exp_bounds(-F(a['initial_beta'])*F(a['correlated_energy_maxima']['J1']))[0]/F(a['independent_shifted_trace_uppers'][0])**8),down(exp_bounds(-F(a['initial_beta'])*F(a['correlated_energy_maxima']['J2']))[0]/F(a['independent_shifted_trace_uppers'][1])**8),down(1/F(a['independent_shifted_trace_uppers'][2])**2)]
  replay=recursion(inp,max_steps=100);assert replay['status']=='entered_small_defect_domain'
  out.append(dict(epsilon_interval=[l,h],beta=F(a['initial_beta']),blocks=blocks,inputs_lower=inp,replay=replay,independently_audited_gap=F(a['uniform_gap'])))
 return dict(baseline=audit['baseline'],baseline_trial_dimension=1,baseline_retained_rank=1,intervals=out,uniform_audited_gap=F(audit['uniform_gap']),status='PASS posterior polynomial extrema, residual/separation widths and startup independently re-evaluated; complete physical proof remains epsilon_interval_review')

if __name__=='__main__':
 start=time.monotonic();result=dict(status='PASS exact posterior criteria on saved certificates; source scientific review status preserved',g002=g002_example(),band_examples=[bands_at_beta(g,F(909,100)) for g in ['3d100','1d25','1d20']],startup_budget=startup_budget_example(),large_ground_moments=ground_moment_examples(),fully_frustrated=ff_examples())
 for p,h in READ_HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
 result.update(input_sha256=READ_HASHES,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (OUT/'examples.json').write_text(json.dumps(serial(result),indent=2)+'\n')
 print('PASS',result['seconds'],'seconds',result['peak_rss_kib'],'KiB')
 for x in result['band_examples']:
  print(x['g'],x['lower_replay']['status'],x['upper_replay']['status'])
  for r in x['patches']: print(r['N'],'rank',r['retained_rank'],'width cost',float(r['relative_width_cost']),'tail cost',float(r['relative_omitted_tail']))
 print('budget',result['startup_budget']['maximum_relative_trace_excess_display'],result['startup_budget']['actual_relative_trace_excess_display'])
