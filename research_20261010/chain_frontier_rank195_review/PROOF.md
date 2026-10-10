# Independent rank-195 and denominator-independent obstruction review

Updated 2026-10-10 17:57 EDT (America/New_York) / 21:57 UTC.

## 1. Exact physical model and reference projector

The model is the periodic spin-one chain with M unit strong dimer bonds and M weak bonds of strength g, including both distinct physical links at M=2. Here g=1/4 and the small seed is M=4, with 8 physical spin-one sites and dimension 9^4=6561. Let H'=H4+8I=E+gV. Each strong dimer has shifted energy 0,1,3 with multiplicity 1,3,5.

The new verifier uses the previously accepted independent physical spin-one matrices, with explicit rational Clebsch–Gordan columns. It checks their orthogonality, positive Gram weights and strong-bond eigenvalue equations. The total raising/lowering matrices are the physical S_tot^±/sqrt(2); the physical dot product has the corresponding exact flip-flop coefficient one.

P is the complete orthogonal reference projector E<4, obtained by enumeration of every 9^4 product reference state, not by counting occupied dimers. Its dimension is 1+12+54+108+20=195. In particular all twenty single-quintet states lie in P at weighted energy three. The complement has 6366 states with E≥4. Complete reference multiplicities are those of (1+3x+5x³)^4.

For all 195 reference columns, the verifier builds the full weak-bond action, including every leaked state. The action union has 1898 configurations, and the residual union has 1703, of which 1624 contain quintets. K=P*VP and J=P*V²P include the physical diagonal metric G. The residual Gram R is independently built directly from configurations outside P, then every entry is checked against J−KG⁻¹K. There are 38,025 checked entries per matrix. The full H' residual is g²R because E preserves P. No truncated-H square is substituted for a physical second moment.

Magnetic-block sizes are 4,22,44,55,44,22,4. Every off-block matrix entry is checked to vanish before using these blocks for spectral counting.

## 2. Exact counted Schur endpoints

The independently reconstructed local 81-dimensional form gV_local+a(h_i+h_j)+bI is positive definite by rational positive pivots. Summing the four edges yields H'≥αE−B, with α=1−2a>0 and B=4b. Thus C=QH'Q≥cQ with c=4α−B.

For t<c, the physical Schur complement and inverse order give

n_−(H'−t) = n_−(D−t−B_PQ*(C−t)⁻¹B_PQ)
           ≤ n_−(D−t−B_PQ*B_PQ/(c−t)).

In unnormalized rational reference coordinates, the congruent matrix is

F(t)=(c−t)(diag(E)G+gK−tG)−g²R.

The reviewer evaluates its inertia by fresh rational symmetric congruence, rather than the producer's integer fraction-free routine. A nonzero diagonal pivot contributes its sign. If every remaining diagonal is zero but an off-diagonal entry is nonzero, a nonsingular 2×2 off-diagonal pivot contributes one positive and one negative direction. An entirely zero remainder contributes its exact nullity. Thus no floating tolerance or unverified nonzero-pivot assumption appears.

For each of the 42 strictly ascending thresholds, the exact negative inertia k means λ_(k+1)(H')≥t. Count differences supply retained bin multiplicities; the final bin ends at rank195. Every later ordered state is bounded by αe−B with the complete e≥4 multiplicities. This is a min–max labeling, not a physical conservation of excitation number, and does not assume that a 195-state physical band lies below c. The certified ground lower endpoint replaces only the first multiplicity-one comparison term after checking its order. The complete trace still counts 195+6366=6561 states.

The original M=4 ground trial is independently replayed by the sealed full-physical-action checker, including complete residual, local form, second-eigenvalue cutoff and Temple lower endpoint. This gives a unique physical ground state. The largest M=8 seed is unchanged: only the previously independently verified two-dimensional first-moment span is used, in full physical dimension 9^8=43,046,721. No M=8 full-spectrum or ground-energy lower bound is introduced.

## 3. Exact spin-one trial multiplet and a physical denominator lower bound

Three rational vectors v_+,v_0,v_- are checked with the independently reconstructed physical total ladder operators. Their nonzero coordinates have magnetizations +1,0,−1, respectively. Exact arithmetic proves

R v_+=0, L v_−=0,
L v_+=v_0, L v_0=v_−,
R v_0=v_+, R v_−=v_0.

All three have the same strictly positive metric norm, are mutually orthogonal, and have the same exact Rayleigh expectation, evaluated from full physical H' action. The verifier also checks the saved raising matrix, its rank22 in the 44-dimensional M_z=1 reference space, 22 linearly independent kernel vectors, and the exact combination that gives v_+.

These are genuine spin-one vectors. The highest-weight M_z=1 vector annihilated by raising has total spin one; the ladder identities exhibit its full three-dimensional representation. This is not an inference from a floating degeneracy. The unique ground state is a singlet because H is SU(2)-invariant and a nontrivial SU(2) multiplet cannot be one-dimensional. It is therefore orthogonal to all three trial vectors.

For an orthonormal set, positivity of exp(−βH) and Jensen's inequality give a trace lower bound by the sum of exponentials of its Rayleigh expectations. Apply this to the exact ground and the three normalized triplet vectors. For β≥0, with ρ4 the certified ground Rayleigh upper endpoint and d_trial=E_trial−ρ4,

Q_actual(β)=exp(βρ4)Z4(β) ≥ 1+3 exp(−β d_trial).

The exact d_trial is verified and is approximately .6780573395118954. The ground contribution is at least one since E0≤ρ4. There is no assumed triplet eigenvalue, isolated triplet band or physical full-spectrum diagonalization in this argument.

## 4. A lower Rayleigh bound for every vector in the saved largest span

At g=1/4, reconstruct the sealed exact 2×2 norm matrix G8 and Hamiltonian matrix H8. Verify G8 is positive definite. For λ=2ρ4+δ_lower, independently verify the first leading minor and determinant of H8−λG8 are strictly positive. This is Sylvester's criterion, separate from the producer's stored LDL pivots, which are also checked against the determinant ratio.

Consequently c†H8c>λ c†G8c for every nonzero real or complex coefficient vector c in that saved two-dimensional span. The claim is strictly limited to Rayleigh quotients in this span; it is not a lower bound for the full physical M=8 ground energy. It includes every reoptimization of the two coefficients, not just the saved optimized vector.

For any one-term Rayleigh numerator from this span, and any valid upper bound U4 on the physical M=4 trace (including the exact trace), the ideal unrounded recipe outputs satisfy

J_rec ≤ exp(−2βδ_lower)/(1+3 exp(−βd_trial))⁴,
C_rec ≤ exp(−2βδ_lower)/(1+3 exp(−2βd_trial))².

These are ceilings on the certificate algorithm's lower endpoints. They are not upper bounds on physical J or C. The denominator-independent statement follows because U4≥Z4 and the preceding inequality lower-bounds Z4 itself. A common normalization shift cancels from these raw trace ratios.

## 5. Exact all-temperature output ceilings and the first-window domain

Let G(x)=1−(1−x)²/(2x²). It is increasing on (0,1], since G'(x)=(1−x)/x³≥0. For positive initialization, the specified time-first cycle gives

a=G(J_rec), b=G(C_rec²a), P=a²b.

Negative or zero a or b already fails this route. The verifier propagates optimistic ceilings using max(0,G(.)); valid physical-ratio upper caps of one ensure the comparison arguments stay in (0,1]. Downward rounding can only decrease the recipe's outputs.

The specified canonical transport supplies S=sqrt(P), T=P and retained joint bound K=P before rounding at (M=8,2β). The signed-transfer window has domain K>1/2 and gives

I=(1−r)min(S sqrt(D),D),
r=(1−sqrt(2P−1))/(1+sqrt(2P−1)), D=P/(1+r²).

Since S sqrt(D)≥D, the minimum is D. Writing s=sqrt(2P−1) and P=(1+s²)/2 gives D=(1+s)²/4 and therefore

I(P)=(s+s²)/2 = (sqrt(2P−1)+2P−1)/2.

It is increasing. For P≤1/2 the required window domain fails. For P>1/2 a positive gap certificate requires I(P)>1/2, equivalently P>(5−sqrt(5))/4. A smaller certified endpoint is not evidence of a physical small gap; it only blocks this particular proof step.

Three separate interval replays use 1200 closed intervals [k/100,(k+1)/100] covering [0,12]. Every exponential is enclosed by the independent 110-term Taylor method with directed 384-bit dyadic rounding. Numerator exponentials use the interval's left endpoint and denominator exponentials its right endpoint. Rational δ_lower and d_upper are checked in their safe directions.

- Saved rank195 denominator: P<5/8. At that cap I=3/8<1/2.
- Any valid M4 denominator, numerator restricted to the saved two-vector span: P<17/25. At that cap I=12/25<1/2.
- Any one-term numerator whose shift δ=ρ8−2ρ4 is at least 19/1250=.0152: P<69/100. At this cap 2P−1=19/50<(31/50)²=(2−2P)², so I<1/2 exactly.

For β≥12 all three proofs use C_rec²a≤exp(−48δ_lower)<1/2. Then b<G(1/2)=1/2 and P≤b<1/2, so the window domain fails. Together these covers handle all β≥0, not merely a finite scan. β=0 cannot certify a positive-temperature gap.

The third obstruction yields the necessary, not sufficient, target ρ8<2ρ4+.0152≈−16.3544559234426 for this same one-term route, requiring an improvement greater than the exact rational threshold .00042614385686183293… over the saved quotient. A safely downward-rounded necessary improvement is >.000426143856861. It does not prove that such a vector exists.

## 6. Exact scope of the no-go

The strongest claim quantifies over every valid M=4 trace upper bound and every one-term Rayleigh numerator in the saved two-dimensional M=8 span, but fixes the initial time-first purification, its canonical transport, and the mandatory first [8,16] signed-transfer window. No improvement of that denominator alone or coefficient reoptimization within that span can repair the failed proof step. Later rounds do not certify a missing earlier integer window.

This does not exclude numerator trial states outside the span with a sufficiently lower quotient, multiple certified numerator contributions, different inequalities or orders, a different seed geometry, or an independently established early-size bridge. It is not a no-gap theorem and does not upper-bound physical purity. No new positive all-size gap is certified at .25; the existing independently sealed .21/.22/.225 results remain unchanged.
