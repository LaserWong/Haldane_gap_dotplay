"""Independent all-temperature ceiling for saved algorithmic certificate outputs only."""
import audit as A
import sys,json,time,resource
F=A.F;S=A.S
start=time.monotonic();claim=json.loads((A.SNAP/'obstruction_g1d4.json').read_text());rec=next(r for r in json.loads((A.SNAP/'expanded_inputs.json').read_text()) if r['g']=='1/4');s=rec['small']
sys.path.insert(0,str(A.BASE/'chain_frontier_review'));import independent_core as C
C.DATA=A.SNAP;ground=C.check_ground(s)
mat=json.loads((A.BASE/'joint_ratio_review/chain_snapshot/M8_two_trial_moments.json').read_text());rho8=S.expectation(mat,list(map(F,rec['large']['combination_integers'])),F(1,4));assert rho8==F(rec['large']['exact_rayleigh'])
ep=s['expanded_band']['comparison_endpoints'];assert ep[1]['multiplicity']==3
physical=A.patch(s,F(1,4),A.moments(json.loads((A.SNAP/'expanded_moments.json').read_text())))
rho=F(s['exact_rayleigh']);delta=rho8-2*rho;d=-8+F(ep[1]['lower'])-rho;dl=F(claim['delta_lower']);du=F(claim['triplet_excitation_upper'])
assert F(claim['delta_exact'])==delta and F(claim['triplet_excitation_exact'])==d and 0<dl<=delta and du>=d>0
assert len(claim['intervals'])==1200 and claim['finite_beta_cover']==[0,12] and F(claim['interval_width'])==F(1,100)
upper=[]
for k,row in enumerate(claim['intervals']):
 l=F(k,100);h=F(k+1,100);assert list(map(F,row['beta']))==[l,h]
 # Q_upper(beta) includes ground term >=1 and 3 exp(-beta*d).
 # Consequently these are ceilings on computed certified lower endpoints, never physical ratio upper bounds.
 numerator=S.expbox(-2*l*dl)[1];den1=1+3*S.expbox(-h*du)[0];den2=1+3*S.expbox(-2*h*du)[0]
 j=min(F(1),numerator/den1**4);c=min(F(1),numerator/den2**2);a=max(F(0),S.G(j));z=c*c*a
 assert z<=F(row['second_purity_argument_upper'])<F(1,2);upper.append(F(row['second_purity_argument_upper']))
assert max(upper)==F(claim['maximum_second_purity_argument_upper'])
tail=S.expbox(-48*dl)[1];assert tail<=F(claim['beta_ge12_second_argument_upper'])<F(1,2)
A.save('obstruction_review.json',dict(status='PASS_RECIPE_SCOPED_ALL_BETA_OBSTRUCTION',g='1/4',physical_ratios_not_upper_bounded=True,finite_cover=[0,12],intervals=1200,maximum_saved_argument_upper=str(max(upper)),tail_beta_ge12_upper=str(tail),ground=ground,physical=physical,large_rayleigh=str(rho8),seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
print('OBSTRUCTION REVIEW PASS',float(max(upper)),float(tail),flush=True)
