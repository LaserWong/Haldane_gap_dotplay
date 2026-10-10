# Rank-195 comparison and a denominator-invariant obstruction at g=1/4

Updated 2026-10-10 17:38 America/New_York (EDT) / 21:38 UTC.

Status: exact producer results pending independent review. No new all-size gap certificate is claimed by this package.

## 1. Model and bounded benchmark

Use the periodic alternating spin-one chain H_M(g)=Σ S_(i,0)·S_(i,1)+gΣ S_(i−1,1)·S_(i,0), strong exchange one, all M weak periodic links retained, and 2M physical sites. The largest physical seed remains M=8, dimension 9^8=43,046,721. Its only input is the sealed two-vector first-moment Rayleigh span; no new largest-seed action, residual, spectrum, or ground-energy lower bound is used.

For the M=4 denominator, set H'=H_4+8=E+gV. Strong-dimer weighted energies are 0,1,3 with multiplicities 1,3,5. P=1_(E<4) has exact dimension

1+12+54+108+20=195.

The 108 three-triplet configurations and all twenty single quintets belong to P, with every quintet still at energy three. Q has dimension 6,366 and E≥4. Complete reference multiplicities remain the coefficients of (1+3x+5x³)^4. Magnetic block sizes are 4,22,44,55,44,22,4.

Exact construction took 0.956 CPU seconds. The complete first-coupling endpoint benchmark took 85.525 CPU seconds, peaked at 106,164 KiB RSS, and ran on CPU3 with one BLAS thread under a one-GiB address-space limit. The builder checks a 600-CPU-second ceiling between endpoint calculations. This is below the requested stopping limit. No full many-body spectrum is diagonalized.

## 2. Exact counted lower comparison

The complete full-action Gram matrices G,K,J and residual Gram R_G=J−KG^−1K are stored in expanded_moments.json. Sparse physical action includes all leaked configurations, including quintets and higher weighted-energy sectors. E preserves P, so the full H' residual Gram is exactly g²R_G.

The exact local positive inequality gV_local+a(h_i+h_j)+bI>0 gives H'≥αE−B with α=1−2a and B=4b. Therefore QH'Q≥A Q, A=4α−B. For each rational t<A, exact inertia of

F(t)=(A−t)(H_PP−tG)−g²R_G

bounds the number of full physical eigenvalues below t from above. This follows from the physical Schur complement, inverse order (C−t)^−1≤(A−t)^−1, and inertia monotonicity. It does not assume 195 physical Ritz values lie below A. Forty-two threshold groups pass exact magnetic-block fraction-free inertia at g=1/4. The final retained bin ends at rank195; all remaining ordered states are bounded using every E≥4 reference bin.

The g=1/4 compression cutoff is A=2.184511611252. The first non-ground comparison endpoint is 0.443193777 relative to H', giving excitation 0.6280217387213062 relative to the saved ground Rayleigh value. The accurate ground enclosure replaces only the first ordered comparison contribution. The complete β=0 count is 195+6,366=6,561.

The bounded scan β=2,2.05,…,80 finds no passing scalar path. This fact alone is not an all-temperature obstruction. The exact arguments below strengthen it.

## 3. Exact rank-195 recipe obstruction

For this fixed denominator upper bound, retain only its ground contribution (at least one in ground-Rayleigh normalization) and its first three-triplet contribution. Let ρ4 be the saved M=4 ground Rayleigh upper value, ρ8 the saved largest Rayleigh value, δ=ρ8−2ρ4, and d the first comparison excitation. The ideal recipe outputs satisfy

J_rec≤exp(−2βδ)/(1+3 exp(−βd))^4,
C_rec≤exp(−2βδ)/(1+3 exp(−2βd))^2.

These are upper bounds on certification outputs, not on physical ratios. The recipe's denominator is an upper bound on the physical trace.

At its first time-first cycle put a=G(J_rec), b=G(C_rec²a), P=a²b, with G(x)=1−(1−x)²/(2x²). If initialization is positive, canonical transport gives S=sqrt(P), T=P before downward rounding. Its signed-transfer window therefore has ideal purity lower endpoint

I(P)=(sqrt(2P−1)+(2P−1))/2, for P>1/2.

This is the existing window formula after substituting S=sqrt(P), T=P and simplifying; it is not a new transfer theorem. If P≤1/2 the window's domain fails. It is increasing in P.

obstruction_g1d4.json covers β∈[0,12] with 1,200 rational intervals and obtains P<0.611884<5/8. Hence I≤3/8<1/2. For β≥12, C_rec²a≤exp(−48δ_l)<0.472341<1/2, so b<1/2 and P<1/2. All exponentials are enclosed rationally outward. Thus no β can make the mandatory first [8,16] window pass with these fixed rank195 inputs. Later scalar rounds cannot repair this missing early window.

## 4. A stronger obstruction: even the exact M=4 denominator is insufficient

The rank195 failure need not be addressed by another M=4 reference expansion. We construct additional exact variational evidence showing that no refinement of this denominator alone can rescue this early-window rule with the saved largest Rayleigh span.

### 4.1 Three genuine spin-one trial vectors

Within the rank195 reference, the M_z=1 space has dimension44. Exact rational total raising has a 22-dimensional nullspace. A rational combination of its basis gives a nonzero vector v_+ annihilated by total raising. In the conventions of the accepted physical kernel, raising/lowering operators are S_tot^±/sqrt(2). Define v_0=L v_+, v_−=L v_0. Exact replay checks

R v_+=0, L v_−=0,
R v_0=v_+, R v_−=v_0,
L v_+=v_0, L v_0=v_−,

and checks equal positive metric norms and equal exact Rayleigh energies. Their distinct magnetizations make them mutually orthogonal. These relations identify an exact spin-one representation, not an inferred floating spin assignment.

The previously certified full M=4 ground is unique. SU(2) invariance forces a unique ground to be a singlet, so it is orthogonal to these three vectors. Peierls/Jensen applied to an orthonormal set consisting of the exact ground and the normalized triplet vectors gives, for β≥0,

Q_actual(β)=exp(βρ4) Z4(β) ≥ 1+3 exp(−β d_trial),

d_trial=0.6780573395118954…,

where the exact rational expectation and all vectors are saved. This is a physical trace lower bound. It requires neither an isolated triplet band nor complete physical spectral diagonalization. Only one retained triplet multiplet is used.

### 4.2 Every vector in the saved M=8 span

Let G8,H8 be the sealed two-dimensional exact metric and Hamiltonian matrices at g=1/4. Set

δ_l=15626143/10^9,
λ=2ρ4+δ_l.

Exact positive LDL pivots verify H8−λG8>0. Thus every nonzero real or complex coefficient vector in this fixed trial span has Rayleigh quotient above λ. This is a lower bound only on quotients in that two-vector span. It is not a lower bound on the full M=8 ground energy.

Consequently any one-term Rayleigh-only numerator chosen from this span is bounded by exp(−2βλ). Let U4(β) be any valid upper bound on the physical M=4 trace, even the exact trace itself. Replacing U4 by the physical trace lower bound above can only increase the recipe's outputs. Therefore all such recipes obey

J_rec≤exp(−2βδ_l)/(1+3 exp(−β d_trial))^4,
C_rec≤exp(−2βδ_l)/(1+3 exp(−2β d_trial))^2.

Changing the normalization of the trace does not evade these raw-ratio inequalities.

### 4.3 Exact all-temperature cover

Round d_trial upward to the saved rational d_u. On every interval [l,h], evaluate exp(−2βδ_l) at l and denominator exponential terms at h, with directed enclosures. Monotonicity of G on (0,1] propagates simultaneous output ceilings through a,b,P; negative initialization is already a failure.

The 1,200 exact intervals covering [0,12] give

P≤0.6693305924892161…<17/25.

At P=17/25, sqrt(2P−1)=3/5 and I(P)=12/25<1/2. The same β≥12 tail bound yields P<1/2. The endpoint β=0 is covered and cannot yield a positive-temperature gap certificate.

Hence, for every β, every numerator Rayleigh vector in the saved two-dimensional M8 span, and every valid M4 trace upper bound (including an exact one), this specified initial time-first/transported-[8,16]-window recipe fails to certify that first window. This is a recipe-scoped obstruction, not a physical no-gap statement, not an upper bound on physical partition ratios, and not an exclusion of other bootstrap inequalities or independent early bridges.

## 5. Consequences and stopping choice

No larger M4 lower-spectrum reference, tighter M4 residual, improved M4 tail, or higher arithmetic precision can by itself fix the strongest obstruction's specified inputs and route. Nor can merely reoptimizing coefficients in the saved two-vector largest span.

Actionable routes require at least one genuinely new ingredient: a different M8 trial outside that span, additional independently certified numerator contributions, an independent bridge of early sizes, another valid inequality/order strategy, or different seed geometry. Such ingredients have not been constructed or certified here. The evidence does not establish that a useful lower M8 Rayleigh value exists outside the span.

The optional .275/.3 calculations were not launched: the first target already exhibits a rigorous denominator-invariant bottleneck, so larger lower-band references or harder couplings on this same route are not a useful next calculation. No conclusion about those couplings is inferred.

All original archives and the frozen rank67 package remain unchanged. This package contains no new all-size gap certificate and makes no GitHub or root-file changes.

## 6. A quantitative necessary numerator target

The same exact triplet witness also gives a useful target for a possible new numerator vector outside the saved span. Repeat the interval proof using δ_l=19/1250=0.0152. The exact post-cycle bound is P≤0.6877367972629488…<69/100. At P=69/100, I(P)=19/100+sqrt(19/50)/2<1/2, because 19/50<(31/50)². The β≥12 tail remains below1/2 at its second-purification argument.

Therefore any one-term Rayleigh numerator with ρ8−2ρ4≥0.0152 fails this particular rule for all β, even with an exact M4 denominator. A numerator-only attempt must attain

ρ8 < 2ρ4+0.0152 = −16.3544559234426…,

an improvement exceeding 0.000426143856862 over the saved selected Rayleigh value. This is necessary, not sufficient, and does not prove such a vector exists. The exact saved-span LDL check also passes at this weaker threshold, independently confirming that coefficient reoptimization in that span cannot meet it. See necessary_numerator_target_g1d4.json and its separate 384-bit interval replay.
