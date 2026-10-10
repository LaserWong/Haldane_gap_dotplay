"""Fresh 384-bit directed replay; algorithm-output ceilings are not physical-ratio ceilings."""
import audit as A
import time,json,resource
F=A.F;S=A.S

def matrix_span(matrix,lam,saved=None):
 G=[[F(x) for x in row] for row in matrix['G']];assert len(G)==2 and all(len(r)==2 for r in G) and G[0][1]==G[1][0]
 assert G[0][0]>0 and G[0][0]*G[1][1]-G[0][1]**2>0
 H=[[F(matrix['K0'][i][j])+F(1,4)*F(int(matrix['K1_scaled'][i][j]),matrix['weak_denominator']) for j in range(2)] for i in range(2)];assert H[0][1]==H[1][0]
 M=[[H[i][j]-lam*G[i][j] for j in range(2)] for i in range(2)]
 # Sylvester determinant criterion is separate from the producer's LDL implementation.
 determinant=M[0][0]*M[1][1]-M[0][1]*M[1][0];assert M[0][0]>0 and determinant>0
 if saved is not None:assert list(map(F,saved))==[M[0][0],determinant/M[0][0]]
 return dict(norm_Gram_positive=True,hermitian_difference=[[str(x) for x in r] for r in M],leading_minor=str(M[0][0]),determinant=str(determinant),rayleigh_lower=str(lam),scope='Every nonzero real or complex coefficient vector in the saved two-dimensional span only')

def replay(ob,delta,d,threshold):
 dl=F(ob['delta_lower']);du=F(ob['triplet_excitation_upper']);assert 0<dl<=delta and du>=d>0 and F(ob['triplet_excitation_exact'])==d and F(ob['delta_exact'])==delta
 assert ob['finite_beta_cover']==[0,12] and F(ob['interval_width'])==F(1,100) and len(ob['intervals'])==1200
 results=[];savedmax=F(0)
 for k,row in enumerate(ob['intervals']):
  lo,hi=F(k,100),F(k+1,100);assert list(map(F,row['beta']))==[lo,hi]
  numerator=S.expbox(-2*lo*dl)[1];den1=1+3*S.expbox(-hi*du)[0];den2=1+3*S.expbox(-2*hi*du)[0]
  j=min(F(1),numerator/den1**4);c=min(F(1),numerator/den2**2)
  a=max(F(0),S.G(j));z=c*c*a;b=max(F(0),S.G(z)) if z>0 else F(0);p=a*a*b
  saved=F(row['joint_after_first_cycle_upper']);assert p<=saved<threshold;savedmax=max(savedmax,saved)
  results.append(str(saved-p))
 assert savedmax==F(ob['maximum_postcycle_joint_upper'])
 tail=S.expbox(-48*dl)[1];assert tail<=F(ob['beta_ge12_second_argument_upper'])<F(1,2)
 # I(P)=(sqrt(2P-1)+2P-1)/2. This is below 1/2 iff sqrt(2P-1)<2-2P.
 q=2*threshold-1;r=2-2*threshold;assert q>0 and r>0 and q<r*r
 return dict(intervals=1200,closed_cover=[0,12],maximum_postcycle_joint_upper=str(savedmax),maximum_display=float(savedmax),strict_joint_cap=str(threshold),window_sqrt_argument=str(q),window_sqrt_upper_witness=str(r),tail_second_argument_upper=str(tail),delta_lower=str(dl),triplet_excitation_upper=str(du),all_interval_rounding_margins_nonnegative=all(F(x)>=0 for x in results),smallest_margin=str(min(map(F,results))))

def main():
 start=time.monotonic();rec=json.loads((A.SNAP/'expanded_inputs.json').read_text())[0];s=rec['small'];rho4=F(s['exact_rayleigh']);matrix=json.loads((A.BASE/'joint_ratio_review/chain_snapshot/M8_two_trial_moments.json').read_text())
 rho8=S.expectation(matrix,list(map(F,rec['large']['combination_integers'])),F(1,4));assert rho8==F(rec['large']['exact_rayleigh']);delta=rho8-2*rho4
 triplet=json.loads((A.HERE/'triplet_review.json').read_text());dtrial=F(triplet['excitation']);dref=-8+F(s['expanded_band']['comparison_endpoints'][1]['lower'])-rho4;assert s['expanded_band']['comparison_endpoints'][1]['multiplicity']==3
 output=[]
 for filename,d,cap in [('obstruction_g1d4.json',dref,F(5,8)),('denominator_obstruction_g1d4.json',dtrial,F(17,25)),('necessary_numerator_target_g1d4.json',dtrial,F(69,100))]:
  ob=json.loads((A.SNAP/filename).read_text());r=replay(ob,delta,d,cap);r['source']=filename
  if 'M8_span_rayleigh_lower' in ob:
   lam=2*rho4+F(ob['delta_lower']);assert lam==F(ob['M8_span_rayleigh_lower']);r['span']=matrix_span(matrix,lam,ob['M8_span_positive_pivots'])
  output.append(r);print('OBSTRUCTION PASS',filename,r['maximum_display'],flush=True)
 assert output[-1]['delta_lower']=='19/1250'
 target=2*rho4+F(19,1250);improvement=rho8-target;assert improvement>0
 report=dict(status='PASS_RECIPE_SCOPED_ALL_BETA_OBSTRUCTIONS',physical_ratio_upper_bound_claimed=False,rank195_fixed_denominator=output[0],every_valid_M4_trace_upper_and_saved_M8_span=output[1],necessary_one_term_numerator_target=output[2],necessary_rayleigh_less_than=str(target),necessary_rayleigh_display=float(target),required_improvement_over_saved_rayleigh=str(improvement),required_improvement_display=float(improvement),saved_large_rayleigh=str(rho8),seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(A.os.sched_getaffinity(0)))
 A.save('obstruction_review.json',report)
if __name__=='__main__':main()
