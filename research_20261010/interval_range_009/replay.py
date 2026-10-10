"""Replay every exact input, ladder and all-size bridge, without optimization."""
import certify as P
C=P.C;F=P.F;json=P.json;HERE=P.HERE;R=P.R;np=P.np
import hashlib,time,resource,copy

def forbidden(*a,**k):raise RuntimeError('Float eigensolver forbidden in saved exact replay')
C.eigh=P.L.eigh=forbidden

def exact_record(saved):
 lo,hi=map(F,saved['coupling_interval']);vs=[p['integer_coefficients'] for p in saved['denominator_patches']]+[saved['largest_base_trial']['integer_coefficients']]
 data=P.interval_data(lo,hi,vs);actual=C.certify(data,F(saved['beta_initial']))
 actual['status']='continuous_43D_one_state_numerator_candidate_pending_independent_review'
 assert actual=={k:v for k,v in saved.items() if k!='float_proposal_score'}
 return actual

def seal(folder,name):
 p=R/folder/name;raw=json.loads(p.read_text());files=raw.get('files',raw)
 for f,h in files.items():assert hashlib.sha256((p.parent/f).read_bytes()).hexdigest()==h,(folder,f)
 return len(files)

def main():
 start=time.monotonic()
 # Exact independent coupling check: this .10 matrix was separately constructed.
 other=json.loads((P.THIRD/'enlarged_8x8_g1d10.json').read_text());assert P.raw['selected_basis_indices']==other['selected_basis_indices']
 assert np.array_equal(P.G,np.array(other['gram'],dtype=object))
 K10=np.array([[F(x,other['integer_matrix_denominator']) for x in row] for row in other['shifted_H_numerator']],dtype=object)
 assert np.array_equal(P.K0+F(1,10)*P.K1,K10)
 # Check Q positivity and occupation sectors, including U's mixed q4/q6 norm.
 assert np.array_equal(P.K0[:P.d,:P.d],P.G[:P.d,:P.d]@np.diag([0]+[2]*P.n))
 assert np.array_equal(P.K0[P.d+P.n:,P.d+P.n:],4*P.vv+6*P.ww)
 saved_model=json.loads((HERE/'numerator_matrix_polynomial.json').read_text())
 assert saved_model['gram']==P.G.tolist()
 assert saved_model['shifted_A_coefficients']==[[[str(x) for x in row] for row in M] for M in (P.K0,P.K1)]
 summ=json.loads((HERE/'coverage_summary.json').read_text());rows=[];matrix_evaluations=0
 for item in summ['intervals']:
  saved=json.loads((HERE/item['file']).read_text());actual=exact_record(saved);rows.append(actual)
  assert F(item['gap'])==F(actual['all_integer_L_ge2_gap'])
  c=np.array(actual['largest_base_trial']['integer_coefficients'],dtype=object);norm=c@P.G@c;rho=list(map(F,actual['largest_base_trial']['rayleigh_coefficients']))
  lo,hi=map(F,actual['coupling_interval'])
  for g in (lo,(lo+hi)/2,hi):
   assert F(c@(P.K0+g*P.K1)@c,norm)==C.poly(rho,g);matrix_evaluations+=1
  assert len(c)==43 and actual['largest_numerator']['retained_states']==1
  assert [x['retained_states'] for x in actual['trace_upper_certificates']]==[49,49,97]
  assert [x['L'] for x in actual['short_sizes']]==list(range(2,8)) and actual['short_sizes'][0]['edge_square_sum']==16
  assert actual['finite_windows'][0]['n']==8
  assert all(a['through']==b['n'] for a,b in zip(actual['finite_windows'],actual['finite_windows'][1:]))
  assert actual['finite_windows'][-1]['n']==actual['bootstrap']['n']
  C.exp_interval.cache_clear()
 assert summ['coupling_interval']==['17/200','9/100'] and rows[0]['coupling_interval'][0]=='17/200' and rows[-1]['coupling_interval'][1]=='9/100'
 assert all(a['coupling_interval'][1]==b['coupling_interval'][0] for a,b in zip(rows,rows[1:]))
 assert min(F(r['all_integer_L_ge2_gap']) for r in rows)==F(summ['uniform_gap'])
 preserved=seal('interval_range_0085','FROZEN_MANIFEST.json');review=seal('interval_range_0085_review','MANIFEST_SHA256.json')
 old=json.loads((R/'interval_range_0085/replay_result.json').read_text());assert old['union_interval']==['0','17/200']
 union_gap=min(F(old['union_all_integer_L_ge2_gap']),F(summ['uniform_gap']))
 # Intentional corruption must fail equality against the rebuilt certificate.
 mutations=[('numerator_coefficient',lambda r:r['largest_base_trial']['integer_coefficients'].__setitem__(1,r['largest_base_trial']['integer_coefficients'][1]+1)),('correlated_endpoint',lambda r:r['correlated_energy_combinations']['J1'].__setitem__('uniform_lower','0')),('trace_bound',lambda r:r['trace_upper_certificates'][0].__setitem__('normalized_trace_upper','1')),('short_multiedge',lambda r:r['short_sizes'][0].__setitem__('edge_square_sum',8)),('finite_window',lambda r:r['finite_windows'][0].__setitem__('through',15)),('denominator_state_count',lambda r:r['trace_upper_certificates'][2].__setitem__('retained_states',96)),('numerator_retained_count',lambda r:r['largest_numerator'].__setitem__('retained_states',43))]
 rejected=[]
 for name,mutate in mutations:
  bad=copy.deepcopy(rows[0]);mutate(bad)
  try:exact_record(bad)
  except (AssertionError,ValueError):rejected.append(name)
  else:raise AssertionError(('undetected corruption',name))
  C.exp_interval.cache_clear()
 out=dict(status='PASS exact producer replay; independent new interval review required',extension_interval=['17/200','9/100'],closed_extension_intervals=len(rows),extension_gap=summ['uniform_gap'],extension_gap_display=float(F(summ['uniform_gap'])),union_interval=['0','9/100'],union_closed_intervals=old['union_closed_intervals']+len(rows),union_gap=str(union_gap),union_gap_display=float(union_gap),finite_window_count=sum(len(r['finite_windows']) for r in rows),short_size_count=sum(len(r['short_sizes']) for r in rows),asymptotic_max_start_L=max(r['bootstrap']['n'] for r in rows),exact_matrix_endpoint_and_center_checks=matrix_evaluations,independent_g010_matrix_check=True,corruptions_rejected=rejected,preserved_producer_files=preserved,preserved_review_files=review,eigensolver_calls=0,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 if '--save' in P.sys.argv:(HERE/'replay_result.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out),flush=True)
if __name__=='__main__':main()
