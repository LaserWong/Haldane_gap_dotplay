# Independent review: all-r exclusions at n48 and n50

2026-10-10 19:10 EDT / 23:10 UTC. Independent scoped acceptance.

## Verdict and exact conclusion

PASS. For n=48 or50, every even base ell from10 throughn and every real cooling ratio r>=1 are excluded from reaching S,T>=99/100 under the precisely specified fixed-node cooled-sector initialization and canonical sequential-G continuation below.

All41 parameter families are covered by332 closed rational boxes on[1,16] plus41 analytic cold rays r>=16. Every compact-interval optimistic path reaches an actual nonpositive spatial or thermal G output; none is accepted merely because it misses a target within a round limit. The original and independent strengthened replays both give215 spatial failures,117 thermal failures, and a maximum failure round of7.

The independent replay additionally covers the ideal unrounded value of the fixed Hermite/packing envelope, and hence every conservative evaluation precision. This closes a wording nuance in the producer: its literal original constants are24-decimal outward envelopes, not the ideal exact formula. The frozen producer is not edited; this review supplies the stronger precision-independent exclusion for the same fixed nodes/caps/moment intervals.

This excludes only n48 andn50. Their failure plus success atn52 does NOT prove that52 is minimal even within this recipe: smaller n<48 have not been exhausted, and no size-monotonicity theorem is supplied. No physical gap no-go, upper bound on true purity, upper bound on the actual leading eigenvalue, or all-method obstruction is claimed.

Producer manifest SHA-256: `94b7c842440d46fdb77f197a92e2096313f34afcc975bf0846e8c4b4414d5900`. All producer entries and scientific-input hashes pass. The separate accepted MPS96/100 supplement and prior moment/Hermite review seals pass unchanged. No producer/root/GitHub or older sealed file was modified.

## 1. The grammar being excluded

The allowed free choices are n in{48,50}, one even ell in10..n, any real r>=1, any allowed number of leading-weight certificate updates including their monotone limit, and conservative numerical evaluation/rounding.

The fixed ingredients are:

- Uniform periodic spin-one Heisenberg model, unit bilinear coupling, shift a=700741/500000, beta0=21/2.
- The same nine accepted I/P/C seam inputs at lengths6,8,10 and their inherited outward sector moment intervals/support caps. I/P/C are seam rotations, not temperatures.
- For each sector, the central Radau node rounded down on the10^-10 grid. Use that fixed node's quadratic Hermite upper formula with signed moment endpoints, take its minimum with the support-cap/fifth-moment convex-packing formula, and restore physical sector copy factors1,2,3. No different node, cap, moment interval, integer-count correction, or extra correlation inequality is permitted.
- The single fixed accepted D26 total shifted Rayleigh quotient R_n<0 at length2n. Put v=exp(-beta0 R_n), W(r)=exp(-r beta0 R_n). These are specific lower anchors, not actual ground weights/traces or freely strengthened numerators.
- At the selected ell, z=A+2B+3C and e=A+2B. Cool with D=z^r,E=e^r, tau=(D+11E)/12,tau0=(D+3E)/4. One ell is used for the whole initialization.
- Put q=n/ell>=1,p=2q. A leading-weight lower certificate starts from total-power forcing and may use the reviewed direct-sector-power forcing update, or a valid weaker prior squared-tail version. Its final spatial endpoint is no larger than[1+R_q(t)/t^q]^-2. The thermal endpoint is no larger than[1+(Q/v-1)^r]^-2, with Q the prescribed length2n envelope.
- Continuation is only the canonical staggered update S_new=G(S^2 T), T_new=G(T^2 S_new), with G(z)=1-(1-z)^2/(2z^2), doubling n,beta after the pair. Here S=S(n,beta) and T=T(2n,beta). The second update uses the new S. No time-first delay, adaptive direction permutation, new reinitialization, or change of moment method is included.

All finite-size bridge requirements and leading-sector/uniqueness tests are granted for free in the optimistic exclusion. Thus the result does not arise from failing an early integer-window test. It concerns inability to sustain this canonical scalar path until the chosen small-defect region.

The physical anchors are accepted only through uniform_anchor96_100_review, manifest `99317ea99db7892f33852e6a0b12b9aa4d3825527852ff605d7d86f22d3f22d7`. Their exact total-energy conventions and negative shifted signs are inherited from that independent reconstruction, not from the earlier optimality review which historically excluded them. No new physical contraction or heat computation is needed here.

## 2. t_star bounds a certificate, never the physical leading eigenvalue

Set c=-beta0 R_n/p>0 and

    t_star(r)=W(r)^(1/p)=exp(r c).

The checker proves log(z)-c>0 uniformly for every allowed n,ell, even after replacing z by a rigorously lower enclosure of its ideal fixed-envelope value. Therefore D>t_star.

A total-power initialization certified from D t0^(p-1)<W has

    t0 < (W/D)^(1/(p-1)) < W^(1/p)=t_star.

Any permitted subsequent direct forcing update has t_new^p<=W-R_p(t_old)<=W because the subtracted tail upper bound is nonnegative. Hence t_new<=t_star. The same upper cap holds for a valid weaker squared-tail forcing step, conservative lower W, upward tail rounding, downward t rounding, any finite sequence, and its monotone limit. Granting t_star directly therefore dominates all those certificate constructions.

This is not a cap on the actual eigenvalue weight. A lower trace anchor W cannot provide such a cap: a one-atom example t=2,p=4,D=2,W=1 satisfies the mass upper bound and trace lower bound but has t>W^(1/p)=1. This exact adversarial example is included. The exclusion concerns what the declared lower-certificate iteration can prove, not the underlying physical spectrum.

## 3. Optimistic domination by polygon inclusion

For fixed t,D,E the residual-sector mass domain is

    x,y,zeta>=0,
    x<=tau-t,
    x+y<=tau0-t,
    x+y+zeta<=D-t.

The q-power objective is x^q+2(y/2)^q+3(zeta/3)^q. Its maximum equals the reviewed four-vertex tail bound R_q(t), because it increases with zeta and is convex on the remaining polygon. The independent checker generates the vertices by active-constraint intersections rather than importing the producer's formula list.

Increasing D,E or decreasing t expands that feasible residual domain. Therefore it cannot decrease the maximum tail. This gives a direct set-inclusion proof of the required monotonicity, including noninteger q>=1. Increasing a positive t also increases t^q. Consequently replacing any achievable t by an upper t_star and replacing D,E by smaller legal values can only increase the numerical spatial lower certificate obtainable from the formula.

Likewise, decreasing the prescribed Q or increasing the fixed anchor v increases the thermal certificate[1+(Q/v-1)^r]^-2 wherever the residual ratio is nonnegative. These monotonic comparisons bound numerical lower endpoints produced by the recipe; they are not upper bounds on the true physical purities.

## 4. Precision-independent envelope relaxation

Let A_L^ideal be the exact minimum of the fixed-node rational Hermite formula and the mathematically exact packing formula. Every conservative numerical evaluation of that prescribed upper-envelope formula is at least A_L^ideal. The same holds sectorwise forB,C.

The independent code computes downward rational enclosures of these ideal formula values. For the packing term it uses a lower root; for the Hermite term it retains the exact rational expression before downward rounding. Taking the minimum of these two lower enclosures gives a lower enclosure of the ideal minimum. Combining positive factors1,2,3 preserves the direction.

These are lower bounds on the VALUES OF PRESCRIBED UPPER-ENVELOPE FORMULAS. They are not lower bounds on physical traces. Their only use is to make the algorithm's initial certificates more optimistic than any conservative realization of that fixed method.

This distinction matters because merely recomputing producer histories from their fixed24-decimal upward constants would not by itself exclude a hypothetical ideal exact evaluation with slightly smaller upper constants. The present independent replay uses the ideal lower enclosures and still terminates every optimistic path. It therefore accepts the original fixed-rational grammar and extends the exclusion to arbitrary conservative precision for the same fixed method. It does not extend to optimizing a new polynomial node or using the later integer correction.

## 5. Every real r in each closed interval

For one recorded box r in[a,b] within[1,16], let z_lower,e_lower,Q_lower denote the ideal-envelope lower enclosures just described. The code verifies z_lower>=e_lower>1. Directed logarithms and exponentials produce

    D_low <= z_lower^a <= z_actual^r,
    E_low <= e_lower^a <= e_actual^r,
    t_high >= exp(b c) >= t_star(r).

Here z_actual,e_actual refer to numerical upper-envelope values permitted by the grammar, not actual physical traces. Each box explicitly satisfies t_high<tau_low<=tau0_low<=D_low. Thus its smaller residual polygon is well defined. Its vertex q-powers are enclosed from below; their maximum gives a lower tail R_low. The denominator t_high^q is enclosed from above. Therefore

    S_certificate(r) <= [1+R_low/(t_high^q)_upper]^-2 <= S_box,

with the last rounding upward.

For the thermal endpoint take a directed v_high>=v and b0=Q_lower/v_high-1. Every box family verifies0<b0<1. The actual prescribed residual ratio is at least b0. If log_b0_low<=log(b0), then for any real r<=b,

    (Q_actual/v-1)^r >= b0^r >= b0^b
                         >= exp(b log_b0_low)_lower.

This gives an upper T_box after inversion and upward rounding. The argument remains safe for more conservative Q values even if their own residual ratios exceed1; only the chosen optimistic b0 must lie in(0,1).

No center or endpoint sample is substituted for this interval argument. Its inequalities hold for every real r in each closed box, including irrational r and shared endpoints.

## 6. Finite terminal failures dominate all permitted continuations

For0<z<=1, G'(z)=(1-z)/z^3>=0. On positive legal purity states, both products S^2 T and T^2 S_new are coordinatewise increasing. Therefore upward-rounded optimistic canonical updates dominate exact updates from any smaller initial certificate and dominate all further conservative downward rounding.

Before every full canonical update, the checker verifies that the optimistic state has not entered S,T>=99/100. If a permitted lower path had entered that region, the dominating optimistic state would also have entered. When an optimistic output is nonpositive, any dominated path either already failed or has a nonpositive corresponding output. It cannot legally continue by inserting that negative number or zero into another purification update.

The independent checker separately audits every original saved history, including argument domain0<z<=1, exact24-decimal upward rounding, spatial/thermal alternation, the new-S dependence in the thermal step, failure-round labeling, and the requirement that ONLY the final output is nonpositive. It then constructs entirely new optimistic histories from the stronger ideal-envelope interval bounds, on a10^-40 grid.

Both replays produce215 spatial and117 thermal terminal failures across332 leaves; maximum round7. No accepted leaf merely exhausts32 or100 iterations. A target entry or unresolved finite cap is programmed as a hard verification error, not a failure certificate. Adversarial mutations removing the terminal step, changing a terminal output to positive, inserting an already accepted target state, or changing the round label are rejected.

There are20 allowed ell values for n48 and21 for n50. The checker verifies precisely this41-family key set with no duplicates or omissions. For every family, sorted rational intervals begin at1, end at16, have positive lengths, and share exact adjacent endpoints. An adversarial gap in coverage is rejected. Thus the compact real parameter interval is covered completely.

## 7. Analytic exclusion of the entire unbounded cold ray

For every family the independent exact lower logarithm obeys

    c0=log(z_lower)-c>0,
    exp(16 c0)>4.

Hence D_actual/t_star>=exp(r c0)>=4 for every real r>=16. Any achievable positive lower certificate t<=t_star gives D_actual/t>=4. The residual polygon contains the vertex with x=y=0 and zeta=D_actual-t, so

    R_q(t)/t^q >= (D_actual/t-1)^q/3^(q-1) >=3.

It follows that S_certificate<=1/16. Even granting T=1 gives S^2 T<=1/256, and

    G(1/256)=-65023/2<0.

The first spatial update therefore fails throughout the whole ray r>=16. This is a continuous analytic estimate, not an extrapolation from the last finite sample. The boundary r16 is also included in the compact boxes, providing overlap. Ratios r<1 are outside the declared cooling-only grammar and are not claimed to be excluded.

## 8. Scope limitations and interpretation

The review establishes all-r failure of the specified n48/n50 canonical certificate family even with bridge and dominance tests waived. It does not show that the actual physical ratios are small or that the actual gap vanishes. The true leading transfer weight may exceed t_star. New physical relations, richer variational numerators, alternative moment methods, adaptive/time-first recurrences, mixed-base initializations, or new data can escape the grammar.

Success atn52 and these two exclusions do not establish a minimum. No n<48 exhaustion or size-monotonicity proof is present. The directory's word "minimum" is not a theorem statement; CLAIM_VERDICTS.json explicitly rejects a minimum-seed interpretation.

The valid weaker squared-tail initialization is covered through its same nonnegative-subtracted-tail cap and no-better spatial endpoint. The theorem does not authorize arbitrary new forcing inequalities merely because they are called square filters, and it does not cover a different continuation order.

## 9. Independent arithmetic and reproduction

Run `python independent_check.py > replay.log` and `python adversarial.py > adversarial.log` in a disposable copy. The verifier imports no producer code. It uses integer comparisons for rational roots, a separately implemented80-term directed fixed-point Taylor exponential, and96-term directed atanh logarithms with explicit geometric remainders. The calculations remain on bounded rational grids; every operation has a proved direction.

The adversarial suite compares these transcendental enclosures against longer exact rational Taylor/atanh references, tests root endpoints, rejects malformed histories/coverage, and demonstrates why t_star is not a physical eigenvalue cap. Analytic proofs above supply the continuous-domain and all-round conclusions; finite tests are supplementary.

Measured independent replay cost is about4.19CPU seconds and13.9MiB RSS on CPU5, under700MiB/600CPU-second ceilings. No optimizer, physical heat campaign, eigensolver, or MPS contraction is run. INPUT_SHA256.json records dependencies; independent_results.json contains all new optimistic histories and cold-ray margins; final verdicts and seals preserve the narrow accepted scope.
