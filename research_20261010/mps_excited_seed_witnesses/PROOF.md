# Exact compact denominator witnesses and recipe-specific exclusions

## 1. Model, fixed state, and orthogonality

Use the orthonormal spin-z basis m=-1,0,1 and periodic

    H_n=sum_(j=0)^(n-1) S_j dot S_(j+1 mod n).

At n=2 this includes both parallel bonds. Its diagonal two-site entries are
m_j*m_(j+1); every allowed exchange transition has coefficient1. The fixed
integer D26 tensors are rebuilt from the archived parameter table. Their
ordinary norm and local-H transfer blocks match the archived bytes exactly.
No identification with an unavailable manuscript is needed or claimed.

Write psi_n(s)=Tr[A_s0 ... A_s(n-1)]. A nonzero local entry satisfies
q_column-q_row=2s. Any closed virtual trace therefore has total physical Sz0.
Cyclicity of trace also gives translation eigenvalue+1 for psi_n.

For even n define

    v_plus=sum_j (-1)^j (S_j^+/sqrt2) psi_n,
    v_minus=F v_plus,
    v_z=sum_j (-1)^j Sz_j psi_n,

where F swaps physical m with -m at every site. The first three states occupy
disjoint Sz sectors0,+1,-1. The fourth remains in Sz0 but has translation
eigenvalue-1; hence it is exactly orthogonal to psi_n and to both transverse
states. Exact positive integer norms certify that each retained vector exists.
The unitary F satisfies F H_n F=H_n, so v_minus and v_plus have identical
norm and Rayleigh energy. No spin-flip invariance of psi_n, exact total-spin
assignment, or SU(2) symmetry of the particular rounded tensors is assumed.

Independent contractions happen to give exactly equal norm and H numerator
for v_z and v_plus at every even length2 through24. This equality is checked,
not inferred from a total-spin label. Direct physical fixtures at2,4,6 check
the full H action, Sz supports, translation signs, and cross inner products.

An explicit bond52 representation uses site matrices

    [[A_s, (-1)^j B_s], [0,A_s]]

and boundary matrix [[0,0],[I,0]] inside the final trace. Here B_s=A_(s-1)
for the normalized raising operator, with B_-1=0, or B_s=s*A_s for v_z.
This represents one vector. It is not a52-dimensional physical retained
space or a52-dimensional linear variational search.

## 2. Exact two-source contraction, including overlap terms

Introduce commuting source variables u,v with u^2=v^2=0 and local tensors
A_s+(-1)^j u B_s on the bra, A_s+(-1)^j v B_s on the ket. Their transfer is

    E_j=T00+(-1)^j u T10+(-1)^j v T01+uv T11,
    Tab=sum_s (a?B_s:A_s) tensor (b?B_s:A_s).

The coefficient uv of Tr product E_j is exactly the unnormalized norm of
the staggered tangent state. For raising, source coefficients00,10,01,11
shift virtual bra-minus-ket charge by0,-2,+2,0 respectively. They occupy
rectangular blocks between charge groups. The group sizes are
1,8,32,80,136,162,136,80,32,8,1. Only299,372 GMP integer entries are retained
across all four coefficient families, rather than a dense2704-square array.
For the longitudinal case all four coefficients preserve charge.

On bond(0,1), set

    W_st,0=A_s A_t,
    W_st,1=B_s A_t-A_s B_t,
    O_ab=sum_(st,xy) h_(st,xy) W_st,a tensor W_xy,b.

This includes both source positions, including bra and ket on the same site
and the opposite-site cross terms. No term overlapping H is discarded.
The remaining n-2 sites begin with positive staggered sign. Since the full
tangent state has momentum pi, all bond expectations agree. Therefore

    <v,H_n v>=n * [uv] Tr[O(u,v) product_(j=2)^(n-1) E_j(u,v)].

The program multiplies by sparse signed-integer local factors, truncating
only source degrees above1 separately. Each integer in the raw contraction
is exact. Ordinary ground-only contraction from the archived blocks supplies
an independent equality check on norm and H numerator and gives the fixed
one-state numerator energies at28,32,40,48.

## 3. Trace lower witnesses and attainable initialization

Let alpha0 be the Rayleigh quotient of psi_n and alpha1 that of v_plus. Let
R be the exact fixed D26 Rayleigh quotient at2n. All recorded sizes satisfy

    delta=R-2alpha0>0,  g=alpha1-alpha0>0.

Numerical displays (exact fractions are stored):

| n | alpha0 | alpha1 | delta |
|---|---|---|---|
|14|-19.655107142692845|-19.118847195700468|0.066363987367940|
|16|-22.446776199528074|-21.927270888442410|0.045008020150802|
|20|-28.040250648164623|-27.540118569609927|0.020966030680521|
|24|-33.640539741732766|-33.149517136259960|0.009882977198363|

Scalar Jensen for each normalized orthogonal trial vector gives

    Z_n(beta)>=exp(-beta alpha0) [1+m exp(-beta g)],

where m=2 for three states or m=3 after adding the independently contracted
longitudinal witness. This is a trace lower bound, not a claim that alpha1
is an eigenvalue or that the omitted spectrum has any certified gap.
Also Tr H_n=0 implies Z_n(beta)>=3^n for beta>=0.

For the fixed numerator L=exp(-2beta R) and arbitrary valid upper traces
U0>=Z_n(beta), U1>=Z_n(2beta), the initialization uses

    J=L/U0^4, C=L/U1^2,
    a=G(J), b=G(C^2 a), G(x)=1-(1-x)^2/(2x^2).

The achievable lower endpoints therefore satisfy upper envelopes

    J<=exp(-2beta delta)/(1+m exp(-beta g))^4,
    C<=exp(-2beta delta)/(1+m exp(-2beta g))^2.

These upper envelopes bound the specified certificate's inputs. Substituting
a variational numerator never gives an upper bound on the true physical
purity ratios.

## 4. Finite exact covering of all beta

The hot interval[0,1/2] uses exp(-R)/3^(4n)<2/5, and G(2/5)<0. The cold
intervals begin at10,20,40,80 for n14,16,20,24 respectively, and use
exp(-2beta delta)<2/5. Between them use every closed box[l,h] of width1/4:

    J<=exp(-2l delta_lower)/(1+m exp(-h g_upper))^4,
    C<=exp(-2l delta_lower)/(1+m exp(-2h g_upper))^2.

Here delta_lower and g_upper are exact outward64-bit dyadic enclosures of
the rational values. The exponential is enclosed by40 Taylor terms after
reduction to argument<=1/16, a geometric positive remainder,160-bit outward
rounding, and outward repeated squaring/reciprocal. Exact rational signs,
not printed decimals, decide each failure.

For positive initial a,b, every complete further time-first cycle is

    a'=G(a^2 b), b'=G(b^2 a').

At each possible fixed delay the accepted joint-aware canonical conversion
starts S=a sqrt(b), T=a^2 b, K=a^2 b, then

    S'=G(max(S^2 T,K)), T'=G(max(T,K)^2 S').

The old K is discarded after that cycle. Monotonicity of G and upward
square-root enclosures make each replay an optimistic upper orbit. A
nonpositive upper update excludes every weaker input. A replay reaching
the target region or the explicit finite replay limit is marked inconclusive,
never excluded. This covers a fixed whole-cycle time-first delay followed by
that conversion; arbitrary adaptive mid-cycle switching is outside scope.

With three states, exact global J upper displays are0.34396778,0.44439687,
0.63463749,0.78025326. Every closed box at n14,16,20 fails the stated recipe.
At n20 some boxes have positive initial a,b; immediate canonical conversion
and the next time-first direction both fail, excluding every legal delay.
The four-state version gives0.31110931,0.41421426,0.61337303,0.76759611 and
preserves those all-temperature exclusions.

At n24, three-state unresolved boxes have union[13/2,45/4]; with four states
the union is[31/4,11]. All beta outside those respective closed unions are
excluded by these screens. Inclusion in a surviving box is not pointwise
feasibility; the interval envelope may be optimistic. The exact endpoints
come from the recorded closed boxes, not a numerical optimizer.

## 5. The hypothetical0.5% trace budget is not available

At n24,beta8, assume hypothetically that valid U0,U1 are each at most201/200
times the corresponding three-state trace sum. A downward rational replay
then reaches common canonical lower endpoint>0.997947735 after two additional
time-first cycles and two canonical cycles. This is a conditional statement
only, explicitly recorded in the extension.

The fourth orthogonal state proves instead

    Z_n(8)/trial_trace_3(8)
       >= [1+3 exp(-8g)]/[1+2 exp(-8g)]
       >1.01893421066079 >201/200.

Thus the first hypothetical trace premise is impossible. This check explains
why richer denominator witnesses can eliminate an apparent opportunity even
though they never certify upper traces. A real success needs independently
certified upper denominator traces, supported by complete omitted-spectrum
control. No residual-only or assumed low-multiplet replacement is made here.

## 6. Momentum refinement and an exactly derived singlet

The later `momentum_extension` contracts the complete24-displacement integer
Gram and H forms of v_j=(S_j^+/sqrt2)psi24. Reality and translation reduce the
required contractions to13 displacements. Its exact H-insertion recurrence
includes the periodic seam and every source-overlap case. Direct fixtures at
n2,4,6 and the prior staggered24-site sums check the construction independently.

Certified15degree radical enclosures supply all Fourier Rayleigh intervals.
The q0 norm is exactly zero; all23 other Fourier modes have positive exact
norm bounds. Counting their spin-flipped partners, psi, and the one previously
certified longitudinalpi state gives48 orthogonal states. The resulting
necessary screen leaves only[533/64,679/64] unresolved at n24.

An additional exact algebraic argument, separately frozen in
`singlet_completion`, strengthens this to70 states without new contractions.
Let R=S_total^+/sqrt2, L=R adjoint, M=Sz_total. The physical spin algebra gives
[R,L]=M. Since Mpsi=0 and the exact Fourier q0 norm gives Rpsi=0, also Lpsi=0.
For each v_j, Rv_j=0 and Mv_j=v_j, hence RLv_j=v_j. Commutation with H implies
that the entire Gram/H forms of L v_j equal those of v_j. Finally
L v_j=-Sz_j psi. Thus all23 missing Sz0 Fourier partners are bona fide
single-source bond52 states with identical Rayleigh values. This is an exact
finite-n24 singlet conclusion, not a premise about arbitrary-length tensors.

The70-state replay uses multiplicity6 at representativesk1 through11 and
multiplicity3 atpi. It excludes all beta outside the closed unresolved union
[539/64,339/32]=[8.421875,10.59375]. It does not eliminate that warm interval
or provide a positive bootstrap certificate. The initial48-state screen and
the70-state strengthening are preserved as separate frozen artifacts.

## 7. Scope and recoverability

All computations stay in this new directory. Frozen archived data, root
status/index files, and GitHub are untouched. Every long calculation runs on
one pinned CPU with explicit address-space/CPU limits. The n20/24 extension
was authorized only after a recorded benchmark projection below600 CPU s and
700MiB. Actual resources were much smaller. No physical support beyond the
tiny n6 fixture is generated.

The3/4/48/70 retained physical states, four polynomial coefficients, MPS bond26/52,
the299,372 auxiliary matrix entries, and full physical Hilbert dimension are
different quantities. The results establish neither exact physical low
eigenvalues nor a physical gap or gaplessness, and neither a universal minimum
seed nor failure of improved numerators or alternative inequalities.
