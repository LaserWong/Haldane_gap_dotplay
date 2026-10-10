# Sharpness of the three-moment envelope and integer-count limits

2026-10-10 18:49 EDT / 22:49 UTC. Exact producer assessment; independent review pending.

## Answer and exact scope

The Hermite/Radau upper envelope is exactly sharp for fixed third/fourth/fifth moments and a support cap when arbitrary nonnegative spectral weights are allowed. It is NOT exactly optimal after requiring ordinary integer eigenvalue multiplicities. This package proves both statements, quantifies the small remaining room with explicit integer-count spectra, and supplies a tiny but strictly positive certified integer-count correction.

This does not establish that n50 or n48 is impossible, nor that n52 is minimal for the cooled bootstrap. It certifies a bottleneck in the information available for individual beta0 trace upper bounds. To turn that bottleneck into a recipe obstruction, one still needs a rigorous bound over the specified continuous cooling parameters/base lengths and scalar continuation paths, with a correct cross-temperature formulation. No such minimum-seed theorem is claimed here. No new seed scan was run after the parent requested this freeze.

The distinction between three classes is central:

1. Relaxed moment measures: arbitrary nonnegative weights on[0,h], fixed m3,m4,m5, and the algebraic sector combination I+2O+3N. Exact Radau sharpness applies here.
2. Abstract unit-count transfer spectra: ordinary integer multiplicities in three A4 multiplicity spaces, the nine raw intervals and support caps, with positive seam traces at all integer lengths. Explicit witnesses below belong to this stricter class.
3. The physical uniform Heisenberg family: requires its Hamiltonians, dimension3^L, thermal-history construction, and consistency as beta changes. Neither class1 extremizers nor class2 witnesses are asserted to realize this family. They do not imply any physical gap failure or lower bound on its true traces.

The numerical gaps below limit what follows from the explicitly stated moment information, not the location of the true physical trace inside its upper bound.

## Inputs and exact verification

The model background and shift remain beta0=21/2 and a=700741/500000. The nine inputs are physical length6/8/10 partition functions with seam rotations0,pi,2pi/3. The already reviewed sector intervals and support caps come from uniform_transfer_moment_assessment/results.json, whose seal is checked. All nine original raw certificate hashes are also checked against audit/independent/streamed_heat_audit.json.

For one sector put x=lambda^2, 0<=x<=h. Its moments are mj=sum x_i^j at j=3,4,5, with one occurrence per eigenvalue. Let the formal positive measure be

    dnu(x)=sum x_i^3 delta_(x_i).

Its zeroth/first/second moments are m3,m4,m5. Allowing arbitrary positive masses in dnu is the relaxation; interpreting those masses as freely variable physical eigenvalue multiplicities would be incorrect.

All raw-interval checks use the exact rational endpoints, not the displayed decimals and not only independent sector boxes. Given sector values I,O,N, the raw moments are recombined as

    raw_I=I+2O+3N,
    raw_P=I+2O-N,
    raw_C=I-O.

This checks the cross-sector correlations needed by the nine actual supplied enclosures.

## Exact fixed-moment Radau extremizer

Take fixed rational midpoint moments a=m3,b=m4,c=m5 of the sealed outward sector intervals. With the certified support h, define

    t=(h*b-c)/(h*a-b),
    wh=(b-t*a)/(h-t), wt=a-wh.

The verifier proves0<t<h and wh,wt>0. The two-point measure

    nu=wh delta_h+wt delta_t

has exactly the required moments: wh+wt=a, wh*h+wt*t=b, wh*h^2+wt*t^2=c. These midpoint choices, after sector recombination, lie strictly inside all nine original raw intervals.

For every even L>=10 let k=L/2-3>=2. The quadratic polynomial Q that matches f(x)=x^k and f'(x) at t, and f(h) at h, obeys Q>=f throughout[0,h]. For k=2 it is an identity. For k>=3 the Hermite remainder is f'''(xi)(x-t)^2(x-h)/6<=0. This is the same already reviewed pointwise majorant; x=0 is included and never divided out.

Any measure in this fixed-moment relaxation therefore satisfies integral f dnu <= integral Q dnu. The displayed two-point measure attains equality, because Q=f at both support points. Thus the dual polynomial bound and feasible primal measure agree EXACTLY, proving optimality for every such L. This is a proof, not an optimizer's floating tolerance.

Its effective physical multiplicities would be wh/h^3 and wt/t^3. Their displays are approximately:

- trivial:(0.999999973389,53.0287405863);
- one complex sector:(0.999999081069,85.0585119113);
- vector multiplicity space:(0.999999926566,109.441094623).

The exact fractions are nonintegers. This relaxed extremizer is therefore not itself an ordinary unit-count transfer spectrum. Equality is not silently promoted into a physical or integer-multiplicity realization.

## Correct handling of interval uncertainty

The exact equality above fixes one feasible central moment triple. The supplied moments instead vary over raw correlated intervals. Applying each Hermite coefficient to the correct signed endpoint gives an upper envelope over the sector boxes, hence over the narrower raw-feasible set. The central Radau measures are feasible for the raw intervals, so they give lower witnesses for the optimum of that relaxed information problem.

For the total length26 trace, the outward Hermite upper is about1.195123497082477 and differs from the feasible central relaxed value by at most3.79023e-8. At length100 the difference is at most3.36822e-8. results.json gives exact enclosing fractions for every even length10..120. This bracket proves near-optimality for the raw-interval MOMENT RELAXATION; the central relaxed measures are not claimed to satisfy the separate all-integer seam-positivity condition.

Negative polynomial coefficients use lower moment endpoints, positive coefficients use upper endpoints. Fixing a convenient rational node is allowed; no uncertainty in its numerical optimization is hidden in the certificate.

## Explicit integer-count near-extremizers

No density assumption or generic fractional-to-integer approximation argument is used. build_proposals.py proposes three-atom unit-count lists numerically. verify.py independently checks their stored rational x values exactly. Each list has one leading atom, N identical middle atoms, and one extra atom, where N=53,85,109 in the trivial, complex and vector multiplicity spaces respectively.

For example the exact trivial leading squared eigenvalue is1004816420190331/10^15; all exact rational atoms and integer counts are in unit_atom_proposals.json and results.json. Every atom is strictly positive and below its certified h. The counts are literal positive integers, not weights rounded to nearby integers.

To impose positive seam traces at ALL integer lengths, the trivial list also contains10^15 additional copies at x=10^-10, equivalently positive eigenvalue lambda=10^-5. This is stored as one compressed count, not expanded. Its contributions are:

    length2:10^5,
    length3:1,
    length6:10^-15,
    length8:10^-25,
    length10:10^-35.

The first two repair the small odd/even seam positivity that the three-atom proposal alone need not possess. The last three are negligible but are nevertheless included exactly in every raw interval check. No permission to ignore them is assumed. All18 checks (two families times nine raw intervals) pass strictly; the nearest raw endpoint has a margin exceeding1.95e-11.

The corresponding operator is a finite-dimensional positive diagonal abstract transfer with eigenvalues sqrt(x). It can be placed in A4 isotypic blocks: one trivial copy, the paired conjugate complex copies, and three vector copies as appropriate, with the internal multiplicities listed above. Its dimension is enormous but finite, so it is self-adjoint, compact and Hilbert-Schmidt. No finite transfer-rank bound was available from the nine inputs. This dimension is not3^L and does not purport to be a physical many-body Hilbert space.

### All-integer seam positivity proof

All eigenvalues were chosen positive. Thus I_L,O_L,N_L and raw_I are positive for all integerL>=2. The trivial leading x exceeds1, so I_L>1. Every complex/vector x is below1; their moments decrease with L. Exact rational checks give O6<1 and N8<1. Therefore

    raw_C=I_L-O_L>0 for every L>=6,
    raw_P=I_L+2O_L-N_L>0 for every L>=8.

The remaining L2..7 are checked individually with exact integer-square-root intervals for odd powers, using lower positive terms and upper negative terms. Both raw_P and raw_C have strictly positive rational lower bounds in those finite checks. Inverse rotations give the same character values, so these cover every nonidentity tetrahedral seam class. This is all-length positivity of this abstract single-temperature trace family, not a demonstration of thermal cross-beta consistency or a Heisenberg Hamiltonian.

## Quantified room for integer-count improvement

An upper trace theorem using only the abstract class2 information must allow the explicit integer-count witness. Its claimed upper endpoint cannot be lower than that witness's trace. Comparing it with the current Hermite upper bounds the maximum possible further improvement from this information alone:

- L24: at most8.24317e-5;
- L26: at most7.16428e-5, relative at most5.99459e-5;
- L48: at most2.13507e-5;
- L50: at most2.04181e-5;
- L96: at most2.90022e-5;
- L100: at most3.04812e-5;
- L104: at most3.19930e-5.

These are exact inequalities with outward displayed decimals. They are NOT error bars on the physical Heisenberg trace, which could be appreciably smaller for reasons absent from these moment constraints. Nor do they prove that the cooled bootstrap fails: it mixes several moments, cooling, anchors and scalar steps, and a theorem about its optimized parameter domain would be separate work.

## A rigorous strict integer-count correction

Integer multiplicity can genuinely sharpen the relaxed Hermite bound. integer_correction.py proves a small example uniformly over the archived trivial-sector intervals at L26.

Write k=10 and Delta=sum x_i^3[Q(x_i)-x_i^10], the slack between the actual Hermite moment combination and the length26 moment. Exact polynomial division verifies

    Q(x)-x^10=(x-t)^2(h-x) R(x),

where every coefficient of R is nonnegative and its constant term is at least h^7. Hence Delta >= h^7 sum x_i^3(x_i-t)^2(h-x).

Take eps_t=eps_h=10^-5. If all atoms satisfy x<=h-eps_h, then

    Delta >= eps_h*h^7*(m5-2t*m4+t^2*m3) >= dH>0,

using the correct lower/upper endpoints. Otherwise there is an atom above h-eps_h. If Delta<dH, this latter case is forced, and its unit multiplicity consumes at least(h-eps_h)^3 of m3. The number of atoms in[t-eps_t,t+eps_t] is therefore at most

    floor([m3_upper-(h-eps_h)^3]/(t-eps_t)^3)=53.

Define g(x)=x^3(h-x)/(t^3(h-t))>=0. Its total is(h*m3-m4)/(t^3(h-t)), which has a certified lower endpoint. In the narrow t interval, g is increasing because t+eps_t<3h/4, so each atom contributes at most g(t+eps_t). Outside that interval,

    g(x) <= K*x^3[Q(x)-x^10],
    K=1/[t^3(h-t)*eps_t^2*h^7].

The endpoint x=h has both sides zero and causes no division issue. Thus

    sum g <=53*g(t+eps_t)+K*Delta.

The lower endpoint for sum g exceeds53*g(t+eps_t) by a positive rational deficit. Combining the two cases proves Delta>=min(dH,deficit/K)>1.49e-14 uniformly. Subtracting this certified amount from the directed Hermite upper is valid. Exact values and quotient coefficients are recorded in integer_correction.json.

This deliberately modest example demonstrates that integer optimality cannot be equated with relaxed Radau optimality. It does not estimate the true best integer correction; the explicit unit-count witness provides an upper limit on how large that improvement could be. The available elementary correction is far too small to motivate a claim that it resolves n50 or n48 startup.

## Auxiliary anchors and what remains open

A new exact D26 probe was already underway when the instruction to freeze sharpness arrived. It completed without any seed scan. A fresh48 benchmark matched the accepted integers before the96/100 batch; both stages obeyed oneCPU0,700MiB and600CPU-second limits. The batch took32.3741CPU seconds and35944KiB. anchor_probe.json records exact negative shifted Rayleigh values at96 and100, approximately -1.01012119004e-5 and -1.05193667415e-5. These auxiliary producer contractions are not used in the sharpness proof or any new gap claim and need independent review before use in a new seed certificate.

The sharpness result alone says nothing decisive about feasibility of n50/n48. It shows that improving individual beta0 upper traces using only the defined moment/cap/multiplicity constraints has little remaining room. To establish a scoped obstruction one must still define the admissible cooled-sector algorithm and its parameter domain, prove monotonic dependence on the allowed joint bounds, and enclose every continuous interval and tail. A grid cannot supply those missing steps. Additional physical relations or cross-temperature information can change the conclusion.

## Reproduction and preservation

Run python verify.py followed by python integer_correction.py. The exact checks require no numerical optimizer and consume well below the700MiB/600CPU-second limits. build_proposals.py is only an optional proposal generator; its floating residuals are never accepted as a certificate. The giant trivial multiplicity is processed as one exact integer. INPUT_SHA256.json identifies the proof's input files. MANIFEST_SHA256.json seals this package, including the complete rational witnesses and auxiliary probe outputs.

No root, GitHub, accepted n52/n54/n56/n60 package or older seal was changed. These new analytical claims are producer results awaiting independent review. No minimum-seed theorem or new n50/n48 gap claim is made.
