# A two-state full-Hilbert short-size bridge

2026-10-10 23:19 UTC / 19:19 America/New_York. Exact producer candidate pending independent review. Scope is ONLY periodic square sides L=2,...,7, not an all-size bootstrap certificate.

For the ordinary spin-half bilayer with unit rung coupling and straight intralayer coupling g, the following uniform short-size bounds hold subject to review:

- 0<=g<=.15: gap>=.050426624396;
- 0<=g<=.1525: gap>=.006136044669;
- 0<=g<=.1528: gap>=.000696608341.

Each listed finite volume has a unique ground state. The prior vacuum-only bridge lost positivity near.1203824229. The new two-dimensional trial space, together with the SAME full-Hilbert second-eigenvalue comparison, has its limiting zero bracketed at

 .15283831215983548 < g_critical < .15283831215983637

(up to the displayed outward-rounded endpoints; the exact rational bracket is in result.json). The limiting size is L7. This is a limitation of the specified comparison/trial method, not a physical transition or an all-method obstruction.

## 1. Full-Hilbert second-level lower bound and uniqueness

The accepted quadratic-boson comparison is reviewed in ../quadratic_boson_review/PROOF.md, sections1–3, and its physical embedding/normalization in ../bosonic_tail_review/PROOF.md. Let H'=H+3N/4, N=L². Combine each unordered periodic edge's multiplicity into w_e. Every weighted degree is4, including L2. Write S=sum_e w_e², C=3S/16, alpha=1−2g and delta=sqrt(1−4g).

For0<=g<1/4, the full physical Hamiltonian admits the hard-core form comparison H'>=P L_bos P. The stable bosonic quadratic operator has an equal-frequency lower comparison E_b+delta Q_ref, with E_b=−(3g²S/4)/(alpha+delta)=C(2g−1+delta). Form-domain min–max after hard-core compression counts the ENTIRE4^N-dimensional physical spectrum, not merely a spin, parity or magnetization sector. Since the reference vacuum is unique and its next shell has energy E_b+delta,

 lambda2(H') >= ell2(g)=C(2g−1)+(C+1)sqrt(1−4g).

The sign/normalization and multiedge-square dependence are inherited from the accepted full-Hilbert theorem. No new full-spectrum diagonalization is used.

Any normalized physical trial with Rayleigh upper R<ell2 gives lambda1<=R<ell2<=lambda2. Consequently the full ground is unique and gap>=ell2−R. A residual is NOT required for a Rayleigh upper bound. This argument does not assume the trial itself is the ground or that a sector contains every low state.

## 2. Explicit two-state trial and graph moments

Let |0> be the rung-singlet vacuum. Let |Omega_ij> be the normalized-coordinate, unnormalized singlet pair

 |t0_i t0_j>−|t+_i t−_j>−|t−_i t+_j>,

with all other rungs in their singlets. Its squared norm is3. Let B=sum_e w_e|Omega_e>. Distinct occupied pairs are orthogonal, so <B|B>=3S. Put H'=Q+(g/2)A.

The restricted matrices on {|0>,B} are

 G=diag(1,3S),
 H'=[[0,3Sg/2],[3Sg/2,3S(2+k g)]],
 k=−(sum_e w_e³)/S+3T/S,
 T=sum_{unordered triangles ijk} w_ij w_ik w_jk.

Indeed <B|A|0>=3S. The two occupied triplets form a singlet, so same-edge preserving action contributes−6 sum_e w_e³. A triplet hop between two edges contributes only if those edges complete a triangle. Each triangle has six ordered edge-pair transitions, each with color inner product3, giving+18T. Thus <B|A|B>=−6 sum_e w_e³+18T. The weighted edges must be aggregated BEFORE squares and cubes.

The exact square-torus cases are:

 L2: four distinct edges of weight2; S16, cube sum32, T0, k−2.
 L3: eighteen unit edges; S18, cube sum18, six triangles, k0.
 L4,...,7: 2L² unit edges; S=2L², cube sumS, T0, k−1.

No bipartite assumption is made. In particular the L3 triangle correction is essential; odd L5 and L7 have no triangles.

replay.py independently reconstructs A=2(S_i0.S_j0+S_i1.S_j1) on the16 physical two-rung basis states from spin-half flips and diagonal Sz products. It transforms to the exact unnormalized rung basis (s,t+,t0,t−) with metric(2,1,2,1), then explicitly evaluates all matrix elements above on the finite vacuum/pair supports for every L2,...,7. No global Hamiltonian matrix or spectrum is formed. Matrix elements with states outside the two-state bra vanish by orthogonality; no residual claim is made about those omitted output components.

## 3. Exact fixed rational trials certify entire intervals

For any rational t>=0, use the explicit trial

 psi_t=(|0>−tB)/sqrt(1+3S t²).

Its exact Rayleigh quotient is

 R_t(g)=3S[(2+k g)t²−g t]/(1+3S t²),

which is affine in g for fixed t. For each size and desired interval[0,b], choose a rational t near the optimum atb, using a downward18-decimal approximation to

 t_opt=b/[2+k b+sqrt((2+k b)²+3S b²)].

The same rational vector is then held FIXED throughout[0,b]. Since ell2(g) is concave and R_t(g) is affine, ell2−R_t is concave. Its minimum over[0,b] is therefore at an endpoint. Exact lower bounds at both0 andb, saved for all six sizes, prove the stated continuous windows. The certificates use rational trial coefficients and outward224-bit integer-square-root enclosures; floating displays do not certify anything.

## 4. Optimal two-state envelope and the method boundary

The smallest generalized Ritz value in this two-state span is

 R_opt(g)=[E−sqrt(E²+3Sg²)]/2, E=2+k g.

Define F(g)=ell2(g)−R_opt(g). Let D=E²+3Sg² and delta=sqrt(1−4g). Direct differentiation gives

 F''(g)=−4(C+1)/delta³+6S/D^(3/2).

For k in{−2,0,−1},

 D−4delta²=(4k+16)g+(k²+3S)g²>=0.

Hence F''<=−4(C+1)/delta³+3S/(4delta³)=−4/delta³<0. Also F(0)=1 and F'(0)=−2. Thus F is strictly decreasing throughout[0,1/4). Rational sign-isolating bisections give a unique zero for eachL; L7 is the earliest. Since R_opt is already the smallest Rayleigh value in the entire two-state span, changing only its two coefficients cannot evade this boundary while retaining the same ell2 comparison.

This optimal-envelope boundary is separate from the fixed rational interval certificates in section3. Negative outputs for g=.153,.154,.155,.16 in result.json are explicitly failed method diagnostics, not positive gap claims.

## 5. Optional next tiny-span budget, not executed

The requested beyond-old-cutoff objective is met by two states. For a future attempt past this method's own boundary, next_span_budget.json records exact sufficient Rayleigh targets for gap.01 atL7,g=.155 and.16. The current two-state span falls short by about.050031726312 and.148334174235, respectively. These targets are relative to the current full-Hilbert ell2 comparison, not necessary for every proof.

A possible three-state extension is span{|0>,B,P_q4 A B}. It would require complete G/H matrix elements in that tiny span, but still no residual. At L7 its q4 configuration support is at most9[binom(98,2)−49 binom(4,2)]=40,131. Only at most16 incident edges per q4 configuration contribute to a q4 bra. Thus q6/q8 states need not be constructed for these Rayleigh matrix elements. A separate120CPU-second/100MiB implementation/verification plan is required before executing this extension. No such extension was computed here.

## Resources and reproducibility

CPU3,120CPU-second/100MiB caps. The full exact local/graph/interval/root pass takes about2 seconds and10.4MiB peakRSS. Source checks and all physical moments are exact rational; no eigensolver, full ED or q6/q8 contraction is run. REPRODUCE.sh verifies predecessor/source seals and reruns into result_check.json without changing frozen results. Prior files, root documentation and GitHub are untouched.
