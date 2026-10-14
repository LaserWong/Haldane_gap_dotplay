# All-temperature obstruction for the fixed g=1/4 construction

Updated 2026-10-10 17:28 EDT / 21:28 UTC.

This result bounds the certified lower endpoints produced by one fixed construction. It does not bound the physical partition-function ratios from above or establish physical gaplessness.

Fix the saved 67-dimensional counted denominator and saved two-vector M=8 Rayleigh numerator. Write δ=ρ8−2ρ4>0, and let d=−8+t_triplet−ρ4>0 be the first saved triplet comparison excitation, with multiplicity three. Its values are δ≈0.0156261438569 and d≈0.4949193087213.

Let Q_ub(β) be this recipe's complete upper bound on exp(βρ4)Z4(β). Its ground contribution is at least one, and its first triplet contribution is 3 exp(−βd), hence

Q_ub(β) ≥ 1+3 exp(−βd).

The ideal unrounded recipe outputs are J_rec=exp(−2βδ)/Q_ub(β)^4 and C_rec=exp(−2βδ)/Q_ub(2β)^2. Directed downward rounding can only reduce them. The recipe outputs therefore satisfy

J_rec ≤ exp(−2βδ)/(1+3 exp(−βd))^4,
C_rec ≤ exp(−2βδ)/(1+3 exp(−2βd))^2.

Q_ub bounds the physical denominator from above. A lower estimate for Q_ub therefore constrains only this certification algorithm and gives no physical upper bound on J_actual or C_actual.

For β in an interval [l,h], replace δ by its exact rational lower enclosure δ_l, replace d by its exact rational upper enclosure d_u, evaluate numerator exponentials at l, and denominator exponentials at h. With exact outward exponential enclosures this yields simultaneous rational upper bounds J_u,C_u. They may be capped at one, since the physical ratios and hence their certified lower endpoints are at most one at the even reflected base.

G(x)=1−(1−x)^2/(2x²) is increasing on (0,1]. For positive first initialization a=G(J_rec), the second initialization argument obeys

z=C_rec² a ≤ C_u² max(0,G(J_u)).

The exact program covers [0,12] by 1,200 closed intervals of width 1/100. Their maximum rational upper bound on z is below 0.497092, strictly below 1/2. For β≥12, a≤1 and C_rec≤exp(−2βδ), so z≤exp(−48δ_l)<0.472341<1/2. β=0 is included in the finite cover. It cannot provide a positive-temperature gap certificate.

Whenever initialization is positive, b=G(z)<G(1/2)=1/2. The transported canonical thermal lower endpoint is T_rec=a²b<1/2. The fixed signed-transfer window has I=(1−r)min(S sqrt(D),D), with D=T_rec/(1+r²), hence I≤T_rec<1/2. It cannot certify a positive gap on the mandatory first [8,16] window. Nonpositive initialization already fails. Additional later temperature/canonical cycles cannot replace the missing early window.

This is an all-β obstruction for these exact physical inputs and this specific early-window route, stronger than the initial bounded scan failure. It does not exclude another denominator comparison, another numerator trial, another bootstrap inequality, or independently bridging early sizes.

## Possible input improvements

The smallest natural weighted-energy extension is P=1_{E<4}, dimension 195. It contains the present 67 states plus 108 three-triplet states and all twenty single quintets at energy three. Q then starts at weighted energy four. Repeat the full residual-Gram and counted-Schur inertia construction with exact magnetic block decomposition. Quintets have energy three, and isolation of the full reference band cannot be assumed. M=8 can remain Rayleigh-only.

A hypothetical-numerator sensitivity scan also shows that lowering δ to 0.01 while retaining the current denominator would produce a positive floating proposal. This is a target, not a certified available trial or a promise that such a Rayleigh energy exists. It corresponds to ρ8≤−16.3596559234426. The saved input has δ≈0.01562614, so improving the two-vector optimization alone is not established as a feasible route. The larger small-reference comparison is the more direct next calculation.
