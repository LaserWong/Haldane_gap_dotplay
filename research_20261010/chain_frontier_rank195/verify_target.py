"""Separate high-precision replay of the necessary numerator target intervals."""
exec(open(__file__.replace('verify_target.py','common.py')).read())
A=load('review_target_scalar',HERE.parent/'chain_low_band_review/audit_certificate.py')
ob=json.loads((HERE/'necessary_numerator_target_g1d4.json').read_text());tw=json.loads((HERE/'triplet_witness.json').read_text());rec=json.loads((HERE/'expanded_inputs.json').read_text())[0]
dl=F(19,1250);du=F(ob['triplet_excitation_upper']);assert F(ob['delta_lower'])==dl and du>=F(tw['excitation_relative_to_ground_rayleigh'])>0
assert len(ob['intervals'])==1200;maxp=F(0)
for k,row in enumerate(ob['intervals']):
 l,h=F(k,100),F(k+1,100);assert list(map(F,row['beta']))==[l,h]
 L=A.expbox(-2*l*dl)[1];q1=1+3*A.expbox(-h*du)[0];q2=1+3*A.expbox(-2*h*du)[0];ju=min(F(1),L/q1**4);cu=min(F(1),L/q2**2);a=max(F(0),A.G(ju));z=cu*cu*a;b=max(F(0),A.G(z)) if z>0 else F(0)
 saved=F(row['joint_after_first_cycle_upper']);assert a*a*b<=saved<F(69,100);maxp=max(maxp,saved)
assert maxp==F(ob['maximum_postcycle_joint_upper']);assert A.expbox(-48*dl)[1]<=F(ob['beta_ge12_second_argument_upper'])<F(1,2)
assert F(19,50)<F(31,50)**2 # I(.69)<1/2 exactly.
matrix=json.loads((HERE.parent/'chain_filter_extension/M8_two_trial_moments.json').read_text());lam=2*F(rec['small']['exact_rayleigh'])+dl;assert lam==F(ob['M8_span_rayleigh_lower'])
mm=[[F(matrix['K0'][i][j])+F(1,4)*F(int(matrix['K1_scaled'][i][j]),matrix['weak_denominator'])-lam*F(matrix['G'][i][j]) for j in range(2)] for i in range(2)];piv=[mm[0][0],mm[1][1]-mm[0][1]*mm[1][0]/mm[0][0]];assert min(piv)>0 and piv==list(map(F,ob['M8_span_positive_pivots']))
(HERE/'target_verification.json').write_text(json.dumps(dict(status='SEPARATE_384BIT_INTERVAL_REPLAY_PASS',intervals=1200,max_postcycle_joint=str(maxp),necessary_delta_less_than=str(dl),necessary_rayleigh_less_than=str(lam)),indent=2));print('TARGET REPLAY PASS',float(maxp),flush=True)
