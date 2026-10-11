# Independent audit of direct two-dimensional time-first windows

Updated 2026-10-10 18:29 EDT / 22:29 UTC. Analytic lemma and all nine model-specific exact replay paths accepted.

## Scope and hypotheses

Let Z(L,W;t)>0 be the physical partition function for every integer L,W>=2 and t>0. At each fixed W,t it must equal Tr X_(W,t)^L for a real self-adjoint Hilbert–Schmidt transfer operator, and likewise in the other spatial direction at every fixed integer L,t. These hypotheses include odd transverse circumferences. They hold for the ordinary antiferromagnetic spin-one-half bilayer under the independently accepted rung-real history transfer construction in bilayer_audit/PROOF.md, section 4. Positivity of the operator or of its kernel is not required. The Hamiltonian has unit antiferromagnetic rung exchange, identical g>=0 horizontal/vertical intralayer couplings, no cross-layer inter-rung bonds, and positive-neighbor multiplicity at side two.

Fix even n,m>=2, beta>0 and simultaneous lower endpoints

 a<=T(n,m;beta), b<=Sx(n,m;2beta), c<=Sy(2n,m;2beta),

with 0<a,b,c<=1. This is the time-first t,x,y staircase from (n,m,beta), not three purities at one geometry. Its full product is a_actual^4 b_actual^2 c_actual=Z(2n,2m;2beta)/Z(n,m;beta)^8. Every spatial purity used as a probability purity has an even base in its own direction; the transverse width can be odd.

## One-axis lemma, including signs

For any pair of strictly positive trace families F(k)=Tr X^k and H(k)=Tr Y^k of real self-adjoint Hilbert–Schmidt operators, fix even q>=2. Suppose 0<A<=H(q)/F(q)^2<=1 and 1/2<B<=H(2q)/H(q)^2<=1. For q<=k<=2q, k integer, the accepted direct lemma gives

 H(k)/F(k)^2 >= A^2 sqrt(2B-1).

For completeness normalize |lambda_j(Y)|^q by H(q). Purity >1/2 implies a unique largest normalized weight w_* >= (1+sqrt(2B-1))/2 >1/2. Its eigenvalue is positive: a negative unique largest-modulus eigenvalue would force all sufficiently large odd traces to be negative, contradicting H(k)>0. Compactness and summability of qth powers make the tail relative to the leader decay to zero, so this argument applies in infinite-dimensional transfer spaces. With p=k/q in [1,2], the normalized numerator is at least w_*^p-(1-w_*)^p for odd k and w_*^p for even k. These are at least sqrt(2B-1): for the odd bracket use concavity in w on [1/2,1] of w^p-(1-w)^p-(2w-1), whose endpoint values vanish. The denominator obeys 0<F(k)<=sum |lambda_j(X)|^k<=F(q)^p. Since A<=1, A^p>=A^2. No equality or spectral identification between X and Y is needed. This proves the lemma for thermal ratios and for transverse spatial ratios alike.

## Independent derivation in the required order

At thermal parameter 2beta put d_actual=Sy(n,m;2beta) and e_actual=Sx(n,2m;2beta). Exact cancellation gives

 b_actual^2 c_actual = d_actual^2 e_actual.

Because e_actual<=1 (its x base n is even), d_actual>=b_actual sqrt(c_actual)>=d:=b sqrt(c).

First vary y, keeping x=n. Apply the one-axis lemma with F(W)=Z(n,W;beta), H(W)=Z(n,W;2beta), A=a and B=d. For every integer m<=W<=2m,

 T(n,W;beta)>=a^2 sqrt(2d-1).

Independently apply it with F(W)=Z(n,W;2beta), H(W)=Z(2n,W;2beta), A=b and B=c. This yields

 Sx(n,W;2beta)>=s:=b^2 sqrt(2c-1).

Finally keep this particular integer W fixed and vary x, using F(L)=Z(L,W;beta), H(L)=Z(L,W;2beta). The new thermal endpoint is a^2 sqrt(2d-1), and the needed x purity is at least s. Thus every integer n<=L<=2n, m<=W<=2m satisfies

 T(L,W;beta)>=I:=a^4 (2b sqrt(c)-1) sqrt(2b^2 sqrt(2c-1)-1).

The stated gates are c>1/2, d>1/2, s>1/2. In fact s>1/2 implies d>1/sqrt(2), since sqrt(2c-1)<=c, but keeping all three explicit is useful in verification. All factors are nonnegative on this domain and I is increasing in a,b,c. Directed lower square roots therefore safely lower I, provided gates are checked on those lower endpoints before evaluation. Boundaries with zero square root do not supply the positive uniqueness/gap conclusion.

## No common-base or parity shortcuts

Odd W is allowed because the outer x transfer exists at every fixed integer W. No statement Sy(n,W)<=1 with odd y base W is used. The second one-axis application uses even y base m, and its numerator is at x=2n. The third uses even x base n. Swapping the order without changing the ladder endpoints would not give the same input statement. A full rotating t,x,y purification cycle doubles n,m,beta together. A window at the new base is at that doubled beta, not at the old beta.

An accepted window with I>1/2 gives a unique physical ground state and a gap >=d_gap when exp(beta*d_gap)<I/(1-I). Every finite box before asymptotic closure must be checked; a late successful cycle cannot repair omitted earlier boxes. Rectangle windows do not certify all aspect ratios. The square all-integer application must additionally cover every smaller side below the first even base.

No physical full-spectrum calculation is part of this review. All model-specific thermal inputs must remain hash-matched to their accepted independent predecessor.

## Exact model-specific acceptance

The now-frozen producer manifest is SHA256 92735c1564f97640afb420b7fb5136e5e26e8390f2428a072faba3f1b0ef0572. All frozen files and dependency hashes were checked. Three scalar input files match the accepted complete-residual independent review's manifest byte-for-byte. Their 4x4/8x4 denominator low-band counts are 49/97; the 8x8 numerator retains one Rayleigh contribution. Maximum physical dimension remains 2^128. No new physical inputs were inferred from floating scans.

Fresh independent 544-bit directed rational arithmetic, 150 Taylor terms, positive geometric exponential tail and exact integer square roots accept all nine saved paths. The selected rational gap is 55807148827/10^12=.055807148827 for g=1/10, every integer square side L>=2. It uses initial beta=187/20, windows at bases 8,16,32,64,128,256,512, and asymptotic onset 1024 at beta=11968/5. Each window's saved lower endpoint, gap witness, physical base and raw/canonical edge labels were checked. Independent, slightly tighter initial ratio bounds are propagated monotonically to validate the saved state endpoints. The existing counted short-size comparison was rebuilt for edge multiplicities at L=2,...,7 and supplies a bound above .3. The small-defect theorem then closes every L>=1024. The accepted interval [0,.10] bound is unchanged; this is a pointwise improvement only.

The independent test suite has 7,680 exact separable-lattice rectangle comparisons, including 1,080 rectangles with both side lengths odd and 6,272 signed-subleading-spectrum comparisons. These models have actual self-adjoint tensor-product transfer representations in both directions. Eighteen formal staircase identities cover unequal spatial bases and every axis permutation. Twelve adversarial changes are rejected: wrong temperature, wrong edge label, wrong base, missing window, oversized final gap, inflated window endpoint, false terminal defect, odd x base, odd y base, c=1/2, failed outer gate, and a>1. These numerical tests supplement the analytic proof, rather than replace it.

The frozen producer proof has a prose-only numerator typo: its displayed fraction 55580714827/10^12 should read 55807148827/10^12. The decimal .055807148827 and all machine certificate values were correct. The original frozen proof is preserved, with the producer's explicit separately saved erratum. No sealed file was edited.

Audit and clean-directory replay use CPU4, at most 600 CPU seconds and 700MiB address space per batch. The final audit takes about three seconds and 13MiB RSS. The shared working tree has no Git metadata; no root document, producer artifact or GitHub state was modified.
