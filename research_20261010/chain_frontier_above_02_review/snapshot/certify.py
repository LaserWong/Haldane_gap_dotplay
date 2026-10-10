exec(open(__file__.replace('certify.py','explore.py')).read().split('records=[];results=[]')[0])
sc=load('scalar',HERE.parent/'chain_filter_extension/certify_extension.py')
C=p.C

def trace_exact(s,beta):
 beta=F(beta);info=s['expanded_band'];rho=F(s['exact_rayleigh']);lo=F(s['ground_lower']);alpha=F(info['alpha']);B=F(info['B'])
 terms=[C.exp_bounds(beta*(rho-lo))[1]]
 terms += [m['multiplicity']*C.exp_bounds(-beta*(-8+F(m['lower'])-rho))[1] for m in info['comparison_endpoints'][1:]]
 terms += [mult*C.exp_bounds(-beta*(-8+alpha*e-B-rho))[1] for e,mult in info['complete_reference_bins'] if e>=3]
 return C.ceil(sum(terms),30),dict(complete_count=6561)
sc.C.trace_bound=trace_exact;sc.TRACE.clear()
def bridge(rec,row):
 beta=F(row['beta']);J=F(row['J_lower']);S=C.floor(sc.sqrt_lower(J));initial=sc.window(S,J,J,beta,4)
 lc=rec['small']['relative_form_bound']['local_certificate'];C.local_psd(lc);a=F(lc['a']);b=F(lc['b']);rows=[]
 for M in [2,3]:
  gap=1-2*a-M*b;assert gap>0
  rows.append(dict(M=M,physical_sites=2*M,full_dimension=9**M,trial='singlet product',rayleigh_upper=str(-2*M),second_eigenvalue_lower=str(-2*M+gap),gap_lower=str(gap)))
 target=min(F(row['M_ge8_gap_lower']),F(initial['gap_lower']),*(F(r['gap_lower']) for r in rows))
 return dict(local_comparison=lc,M2_M3=rows,initial_M4_M8_window=initial,all_M_ge2_gap_lower=str(target))
def main():
 started=time.monotonic();recs=json.loads((HERE/'expanded_inputs.json').read_text());scans=json.loads((HERE/'expanded_scan.json').read_text());results=[]
 for rec,scanrow in zip(recs,scans):
  assert rec['g']==scanrow['g'];best=scanrow['best']
  if not best:continue
  rows=[];beta=F(str(best['beta']));ts=best['time_steps'];cs=best['canonical_steps']
  C.DATA=HERE;ground_check=C.check_ground(rec['small'])
  for j in [-1,0,1]:
   for t in range(max(0,ts-1),ts+2):
    for c in range(max(0,cs-1),cs+2):
     r=sc.cycle(rec,beta+F(j,20),t,c)
     if not r.get('M_ge8_gap_lower') or F(r['M_ge8_gap_lower'])<=0:continue
     bb=bridge(rec,r)
     if F(bb['all_M_ge2_gap_lower'])>0:rows.append(dict(**r,all_size_bridge=bb,all_M_ge2_gap_lower=bb['all_M_ge2_gap_lower']))
  selected=max(rows,key=lambda x:F(x['all_M_ge2_gap_lower']))
  out=dict(status='EXACT_CANDIDATE_PENDING_INDEPENDENT_REVIEW',g=rec['g'],input=rec,ground_replay=ground_check,rows=rows,best=selected)
  (HERE/('candidate_g'+rec['g'].replace('/','d')+'.json')).write_text(json.dumps(out,indent=2))
  summary=dict(g=rec['g'],gap=selected['all_M_ge2_gap_lower'],display=float(F(selected['all_M_ge2_gap_lower'])),beta=selected['beta'],time_steps=selected['time_steps'],canonical_steps=selected['canonical_steps'],asymptotic_from=selected['final']['cells'],paths=len(rows),initial_window=selected['all_size_bridge']['initial_M4_M8_window']['gap_lower']);results.append(summary);print('EXACT',summary,flush=True)
 (HERE/'summary.json').write_text(json.dumps(dict(results=results,seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2))
if __name__=='__main__':main()
