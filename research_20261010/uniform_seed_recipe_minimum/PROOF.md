# All-cooling exclusions for the specified n48/n50 cooled recipe

2026-10-10 19:02 EDT / 23:02 UTC. Exact producer assessment; independent scalar review pending.

## Scope of the theorem

For n=48 and n=50, the explicitly defined canonical cooled-sector recipe below cannot reach the accepted small-defect region for ANY real cooling ratio r>=1 and ANY even base moment length ell in10,12,...,n. Every permitted finite or infinite leading-mass lower-certificate iteration and every conservative outward rounding is covered. We grant every finite-size bridge for free, so the obstruction is scalar startup/convergence, not an early-window threshold.

This is not a physical gap statement and not a theorem that n52 is the smallest possible seed. It excludes these two specific smaller seeds within one specified grammar. No conclusion about n<48, another moment envelope, another scalar order, mixed base lengths, new physical information or all methods follows. The accepted n52 certificate remains a positive result in this same canonical family.

The proof uses interval branch-and-bound, not a sampled-temperature scan. The compact parameter interval[1,16] is covered by closed rational boxes; each has a finite optimistic scalar failure. Every r>=16 is excluded by a separate analytic bound. Endpoint overlap is checked exactly. An independently accepted MPS96/100 anchor supplement is a physical dependency; the new scalar exclusion requires its own independent review before promotion.

## Exactly which recipe is excluded

The free choices are:

1. n is48 or50;
2. one even base ell in10..n is selected for the spatial initialization;
3. any real r>=1, with beta=r*beta0 and beta0=21/2;
4. any valid number of leading-mass forcing iterations, including their monotone limit;
5. arbitrary conservative upward rounding of upper inputs and downward rounding of lower certificates.

Everything else is fixed as follows.

- Model: periodic uniform spin-one Heisenberg chain with unit bilinear coupling, shift a=700741/500000.
- Inputs: the nine accepted beta0 seam partition-function intervals at lengths6,8,10 and the accepted A4 sector support caps. These are seam rotations, not temperatures.
- Moment envelope: for each sector and even L>=10 use precisely the accepted n52 Hermite construction. Its node is the central Radau formula rounded downward to10^-10. Polynomial coefficients multiply the upper or lower moment endpoint according to their signs. Take the minimum with the accepted support-cap/fifth-moment convex-packing bound, with outward rational roots. These fixed values define A_L,B_L,C_L. Arbitrary reoptimization of the polynomial/node/support cap, integer corrections, new moment inequalities, and correlations between different lengths are outside the present grammar.
- Anchor: the single fixed D26 Rayleigh quotient R_n at length2n, including the extensive shift. R_n<0. W(r)=exp(-r*beta0*R_n) is its fixed Jensen trace lower bound. v=exp(-beta0*R_n) is the fixed ground Boltzmann lower bound. W is not the actual physical trace and is not freely optimized.
- Cooling: z=A_ell+2B_ell+3C_ell, e=A_ell+2B_ell; D=z^r,E=e^r, tau=(D+11E)/12,tau0=(D+3E)/4. One common ell is used; the recipe does not combine different ell values within a seed.
- Let q=n/ell>=1,p=2q. A leading-mass lower certificate starts from total-power forcing D*t0^(p-1)<W (with the usual uniqueness/sector tests) and may be improved by t_new<=[W-R_p(t_old)]^(1/p), or any weaker prior squared-tail version. R_j is the reviewed four-vertex sector-tail maximum. Initializing directly with the closed limit of these iterations is allowed. No other proof of a larger leading-mass lower bound is included.
- Spatial lower certificate: S=[1+R_q(t)/t^q]^-2. Thermal lower certificate: T=[1+(Q/v-1)^r]^-2, where Q=A_(2n)+2B_(2n)+3C_(2n). More conservative values are allowed.
- Canonical continuation only: S_new=G(S^2*T), T_new=G(T^2*S_new), followed by doubling n and beta, where G(z)=1-(1-z)^2/(2z^2). The target is S,T>=99/100. No direction permutation, adaptive order change, time-first delay grammar, or new physical reinitialization is included. Finite windows and all other bridge conditions are granted for free.

Thus choosing ell adaptively as a function of r is covered, since every pair is excluded. Choosing a different moment method or combining information in a new way is not covered. The auxiliary current-operator exclusions at n<=24 concern a different recipe and are not used.

## Physical input provenance

The moment inputs and caps are the accepted uniform_transfer_moment_assessment package. certify.py verifies its frozen result hash and reconstructs the same Hermite node/coefficient rule used for the accepted n52 certificate. The exact96/100 integers are read from the frozen uniform_moment_optimality_assessment/anchors.out, with its manifest checked.

Their physical interpretation is now independently accepted in the SEPARATE uniform_anchor96_100_review, manifest99317ea99db7892f33852e6a0b12b9aa4d3825527852ff605d7d86f22d3f22d7. That review rebuilt the D26 matrices, physical bond insertion and blocks, then reproduced96/100 with sequential multiplication. It checks nonzero norms and the total-energy convention. The old moment-optimality review historically excluded these auxiliary anchors; it is not cited as their approval.

The shifted Rayleigh displays are approximately -1.01012119004e-5 at96 and -1.05193667415e-5 at100. Their exact fractions, not displays, enter the proof. No new thermal trace, spectrum, Hamiltonian diagonalization or MPS contraction is run by this package.

## An optimistic cap on the certificate iteration, not the true eigenvalue

Put

    t_star=W^(1/p)=exp[-r*beta0*R_n/p].

This caps what the DEFINED LOWER-CERTIFICATE iteration can prove. It is NOT an upper bound on the actual physical leading transfer weight, which can exceed t_star.

The code verifies log(z)+beta0*R_n/p>0. Consequently D/t_star>1 for every r>=1. Total-power forcing implies

    t0 < (W/D)^(1/(p-1)) < W^(1/p)=t_star.

Every subsequent polygon-forcing step has t_new^p<=W-R_p(t_old)<=W, so t_new<=t_star. The same holds for all weaker squared-tail steps, any conservative rounding, and every monotone limit. Hence it is safe and optimistic to grant the recipe t_star for free, without actually iterating or testing whether it can establish uniqueness/trivial-sector membership. Granting those missing tests for free only enlarges the class being excluded.

For fixed t, R_q is nondecreasing when D,E increase: its feasible residual-mass polygon expands because D,tau,tau0 all increase. For fixed D,E it is nonincreasing with t, as shown by the four vertex expressions. Thus S grows when D,E decrease and when t increases. Replacing any certified t by t_star and any upward-rounded D,E by their exact values gives an upper bound on the numerical S lower certificate achievable by the recipe.

Likewise the largest thermal lower certificate in the grammar uses the exact fixed v and the smallest prescribed Q. Lower approximations to v or upward rounding of Q can only reduce that certificate. These are statements about the certification algorithm's lower endpoints, not upper bounds on the true physical purities.

## Rational boxes for every real r in[1,16]

For a closed rational interval r in[a,b], compute rigorously

    D_low <= z^a,
    E_low <= e^a,
    t_high >= exp[-b*beta0*R_n/p].

Since z>=e>1 and R_n<0, these imply D(r)>=D_low,E(r)>=E_low,t_star(r)<=t_high for every real r in the interval. The code verifies t_high<tau_low<=tau0_low<=D_low for each box. At the four residual polygon vertices it evaluates lower bounds on every q-power, giving a safe lower R_low. With an upper t_high^q,

    S_recipe(r) <= [1+R_low/(t_high^q)_upper]^-2 = S_box.

For thermal input, choose a directed upper v_high>=v and let b0=Q/v_high-1. The code verifies0<b0<1. Let log_b0_low<=log(b0)<0. Because r<=b,

    (Q/v-1)^r >= b0^r >= b0^b
                       >= exp(b*log_b0_low)_lower.

This gives the safe T_box upper endpoint. All dependence directions are explicit; no center evaluation is used as an interval claim.

Starting from S_box,T_box, the code applies G with upward rounding. G is increasing on0<z<=1. Therefore these optimistic iterates dominate every legal lower-certificate path in the box. A nonpositive optimistic spatial or thermal output prevents all such paths from continuing. Before each update the code checks whether the optimistic path has entered S,T>=99/100; a box is never labeled excluded if this target has been reached.

An unresolved box is bisected. The computation stops only when every leaf has a finite sign failure. A depth limit is a hard failure, not an accepted exclusion; no such unresolved leaf is permitted in a completed certificate. Each leaf records rational endpoints, optimistic initial S,T, every argument/output, failure type and round. Sorted endpoints are checked to cover[1,16] exactly with adjacent closed intervals sharing endpoints. No sampling hypothesis or claim of continuity alone substitutes for these interval bounds.

## Analytic cold ray: all r>=16

The same lower log bound proves, for every allowed ell,

    exp(16*(log(z)+beta0*R_n/p)) >4.

The expression in parentheses is positive, so D/t_star>=4 for every r>=16. The vertex with x=y=0 is always included in the residual polygon. It gives

    R_q(t) >= (D-t)^q/3^(q-1).

For any achievable certificate t<=t_star, this implies

    S <= [1+(D/t-1)^q/3^(q-1)]^-2 <=(1+3)^-2=1/16.

Even granting T=1 yields S^2*T<=1/256 and G(S^2*T)<0. Thus the very first spatial update fails throughout the entire unbounded cold ray. The chosen endpoint16 is justified by exact inequalities for every ell, not by stopping a scan at an arbitrary temperature. r<1 is excluded from the declared cooling-only recipe; it is not silently treated as proved impossible.

## What the exclusion says and what it does not

The obstruction remains after all finite-window tests are waived. It therefore distinguishes failure to sustain canonical scalar purification from an inability to bridge small integer sizes. The direct time-first window lemma can improve a bridge, but cannot fix a path that is already excluded by this relaxed canonical initialization/continuation grammar. A different time-first continuation grammar remains outside the theorem.

The leading bound t_star deliberately overstates what the finite or limiting certificate iteration can achieve. Failure of the resulting optimistic path proves failure of all the declared conservative variants, including exact arithmetic without rounding losses. It does not bound actual physical purity or actual leading eigenvalues.

There is no unrestricted minimum seed conclusion. Together with the accepted n52 result, the new exclusions would establish that neither48 nor50 replaces52 within this fixed family. They do not exclude smaller n<48, other base ranges, a sharper moment envelope, a different numerator, actual quantum identities beyond the fixed inputs, or a different bootstrap inequality.

## Reproduction and resource bounds

Run REPRODUCE.sh. certify.py is constrained to CPU0,700MiB address space and600CPU seconds. It uses exact rational log/exponential/root enclosures, not an optimizer, eigensolver or physical-state contraction. A one-family n50,ell24 pilot closed17 leaves in6.4CPU seconds. The full result records all family and leaf counts, finite failures and runtime. Checkpoints and partial results are kept during work; only the completed results.json is a certificate.

finalize.py checks the accepted physical anchor supplement, full41-family scope, all interval coverage and every saved scalar failure again. It marks the anchor dependency accepted while leaving the new scalar theorem pending independent review. MANIFEST_SHA256.json seals the complete package and INPUT_SHA256.json records the scientific inputs. All predecessor, root and GitHub files remain unchanged.
