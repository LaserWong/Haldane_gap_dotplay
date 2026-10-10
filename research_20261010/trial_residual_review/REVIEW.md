# Independent fixed-space residual and budget review

Updated 2026-10-10 14:19 America/New_York (EDT) / 18:19 UTC.

## Verdict and scope

**PASS.** The four fixed-space residual obstructions, their constructive 11-dimensional comparisons, the residual-to-width criterion, the entropy-rank arithmetic, and the startup-budget arithmetic are independently verified.

The physical model is the ordinary spin-1/2 square bilayer with unit vertical exchange, equal straight intralayer exchange g, no crossed exchange, and positive-direction periodic edges. The new obstruction concerns the 4×4 rung torus at the four discrete values g=1/50, 3/100, 1/25, and 1/20. It does not certify a coupling interval.

The fixed six-dimensional trial space consists of the vacuum and the five pair-orbit singlet sums invariant under translations and the square point group. It has q≤2 triplets. This is a symmetry-adapted trial space, not a six-dimensional invariant subspace of the full Hamiltonian. Its nonzero q4 leakage is essential to the result.

Every normalized vector in this fixed space whose shifted Rayleigh quotient lies in the stated interval has residual squared strictly above its specified target. A saved vector in the 11-dimensional one-block enlargement has residual squared strictly below that target and a Rayleigh quotient inside the same interval. All inequalities are accepted by exact rational arithmetic.

| g | Producer interval residual² floor | Target | Saved 11D residual² | Wider audited-Temple interval floor |
|---|---:|---:|---:|---:|
| .02 | 3.2153152532954e-5 | 1e-6 | 4.5837523377598e-8 | 3.2153155213250e-5 |
| .03 | 1.7775668441767e-4 | 1e-6 | 5.3153677990051e-7 | 1.7775669846902e-4 |
| .04 | 5.7589265266514e-4 | 1e-5 | 3.0371078672386e-6 | 5.7575051732544e-4 |
| .05 | 1.4104340263072e-3 | 1e-4 | 1.1767949328026e-5 | 1.4089877260590e-3 |

These are approximate displays of exact fractions in `results/residual_review.json`. The first two wider intervals equal the producer intervals. Their slightly larger certified floors come from a tighter independent scalar search. At .04 and .05 the independently used intervals genuinely extend the lower endpoint downward.

The full physical Hilbert dimension is 4^16=4,294,967,296. The numbers 6 and 11 are independent linear search dimensions. Each compared trial retains one candidate ground state. Neither is the retained thermal-band rank, the number of configurations in a representation, nor an MPS bond dimension.

## 1. Independent reconstruction and inherited inputs

The executable `audit_residual.py` imports no producer module and no earlier audit arithmetic. It explicitly constructs the pair orbits by all translations and D4 actions, giving orbit sizes 32,16,32,32,8 and Gram diagonal 1,96,48,96,96,24.

Write H′=H+12=Q+(g/2)A. In the vacuum/pair basis the code directly assembles the q≤2 image using the pair-creation, annihilation, hopping, and occupied-pair terms. It streams all C(16,4)=1,820 four-site sets and their three pairings. The pairing Gram is 6I+3eeᵀ. For each pair column the q4 amplitude before the factor g/2 is

    L_(ij|kl)=m_ij c_kl+m_kl c_ij.

This independently yields the entire F=L*L matrix. Its entries exactly match the previous independent geometry audit. Therefore the new six-dimensional obstruction does not merely assume the producer's H² corner.

If D is the pair Gram and C the projected coefficient action, the independently rebuilt q2 second moment is

    B_q2 = C* D C + (g/2)^2 diag(0,F).

The executable separately checks

    B_q2 - A_q2 G_q2^(-1) A_q2 = (g/2)^2 diag(0,F) ≠ 0.

Replacing B_q2 by the compressed square would omit exactly this term and would invalidate the obstruction proof. No sector above q4 can occur after one H application to q≤2.

For the 11-dimensional comparison the audit reconstructs all of G, A, and B from the fresh q2 action and F, together with the earlier independent geometry tensors S, V, and W. The complete H′ image decomposes into q≤2, q4, and q6 components. In particular, the LL second-moment block contains

    16F + 8tS + t²(V+W+E*D^(-1)E),   t=g/2.

The q6 term W is retained. Every reconstructed entry agrees with the saved matrices. Exact positive leading principal minors establish the Gram ranks 6 and 11. The stored rational vector's norm, Rayleigh quotient, and full residual squared are recomputed without an eigensolver.

The physical matching identities and the S,V,W tensors are inherited from `../large_seed_review/REVIEW.md`. Their original review independently assembled the local physical-spin exchange and all geometry contractions. This audit verifies the exact geometry and all four ground-file hashes against that review's manifest, including its frozen snapshots. It does not claim to have repeated the entire earlier local-spin audit.

## 2. Generalized-Gram obstruction and uniformity

Let W have linearly independent columns, G=W*W>0, A=W*H′W, and B=(H′W)*(H′W). The definition of B uses the full physical image. The same statement applies to a nonorthonormal physical coordinate system with its metric inserted in all three matrices.

For I=[l,u], define c=(l+u)/2 and h=(u−l)/2. Suppose

    P = B−2cA+c²G−γG > 0.

For any complex coefficient vector z with z*Gz=1,

    ||(H′−c)Wz||² = z*(B−2cA+c²G)z ≥ γ.

The real symmetric certificate also proves the complex Hermitian inequality. The identity does not require z to be a Ritz eigenvector.

For every real t∈I, the reverse triangle inequality gives

    ||(H′−t)Wz|| ≥ ||(H′−c)Wz||−|t−c| ≥ sqrt(γ)−h.

A rational α satisfying α²≤γ and α>h consequently proves

    ||(H′−t)Wz||² ≥ (α−h)².

Choosing t=z*Az proves the claimed full-residual lower bound whenever the Rayleigh quotient is in I. The proof covers the entire closed interval, including both endpoints. It is not a sampled-energy assertion.

The producer proposed γ and exact LDL pivots. This audit independently computes every leading principal determinant by Bareiss elimination and verifies positivity by Sylvester's criterion. The determinant ratios also reproduce every proposed LDL pivot exactly. The saved square-root direction α²≤γ, the strict α>h condition, the squared floor, and its strict comparison to the target are all checked.

### Endpoint provenance and a stronger robustness check

The producer upper endpoint is always the saved 11D shifted Rayleigh quotient plus 1/1000. At .02 and .03 the lower endpoint is its saved Temple lower bound. At .04 and .05 it instead uses a stronger complete-band frontier ground lower bound.

The numerical matrix obstruction on a stated rational interval does not depend on interpreting its lower endpoint as a ground-energy bound. For a conclusion tied directly to previously audited ground intervals, this audit additionally takes

    I_old = [ρ−r²/(a_old−ρ), ρ+1/1000],

where ρ and r² are the independently reconstructed shifted 11D moments and a_old is the old all-sector second-level threshold accepted in the hash-verified large-seed review. The denominator a_old−ρ is positive at all four couplings. These intervals contain the producer intervals. Fresh exact PSD certificates still exceed every target, as shown in the last table column.

Since the old Temple endpoint is a global ground lower bound, every normalized trial with Rayleigh quotient at most ρ+1/1000 automatically lies above the lower endpoint of I_old. The wider-interval conclusion therefore needs no unreviewed improved endpoint. The .04/.05 frontier data are also independently handled by the separate small-seed exclusion review.

## 3. What the dimension result does and does not prove

The result is a lower bound on attainable residual within a fixed ansatz and energy range. It proves that altering coefficients or increasing numerical precision inside that six-dimensional ansatz cannot reach the stated accuracy. The demonstrated 11-dimensional enlargement can reach it.

It does not prove that arbitrary trial spaces must have dimension at least 7, 11, or any number greater than one. The span of an exact ground eigenvector is a one-dimensional perfect trial space. Even the saved successful vector spans a one-dimensional space with its saved residual. Dimension only becomes a meaningful lower-bound question after fixing the permitted ansatz or construction.

Nor does this audit exclude a 7-, 8-, 9-, or 10-dimensional enlargement of the fixed ansatz, or every vector in the uncompressed q≤2 space with other symmetries. The tested catalog here contains the specified 6D and 11D spaces. Residual success alone establishes neither completeness of a low-energy band nor a thermodynamic gap.

## 4. Residual-to-width budget

The producer's Section 2 is analytically valid. Assume a self-adjoint H, a k-column isometry Q, T=Q*HQ≤rI<aI, and residual R=HQ−QT with R*R≤εI. Full-space spectral information must separately establish λ₁≥L0 and λ_(k+1)≥a. Set δ=a−r>0 and c0=a−L0≥δ.

Min-max gives exactly k eigenvalues below a. The separated Sylvester equation for the high-spectral component of Q bounds its norm by sqrt(ε)/δ. Equal-rank projector-angle symmetry then implies for the orthogonal trial complement

    C ≥ bI,   b=a−c0 min(1,ε/δ²).

If ε<δ³/c0, then b>r and the cap is inactive. For t<b the Schur complement gives

    T−tI−R*(C−tI)^(-1)R ≥ T−tI−ε/(b−t)I.

At t=θ_i−ε/(b−r), this matrix has at most i−1 negative eigenvalues. The complement is positive. Hence λ_i≥θ_i−ε/(b−r), while min-max gives λ_i≤θ_i. This checks the eigenvalue ordering and lower-endpoint direction rather than relying on a residual-nearness statement without a spectral count.

For a desired finite width ω≥0, the rational condition

    ε ≤ ωδ³/[δ²+ωc0]

is sufficient. Indeed ε/(δ−c0ε/δ²)≤ω is exactly equivalent after multiplication by its positive denominator. For finite positive ω, the displayed threshold is strictly below δ³/c0. At ω=0 it requires ε=0. Ritz-interval uncertainty must be added separately when Ritz values are not exact.

For nonorthonormal trial columns, Γ=B−AG^(-1)A is the exact residual Gram. A rational coefficient proposal D produces

    E=B−AD−D*A+D*GD
      =Γ+(D−G^(-1)A)*G(D−G^(-1)A) ≥ Γ.

Thus εG−E≥0 is a valid sufficient whole-band operator-residual test. Diagonal residual bounds alone cannot replace it. These bounds are sufficient and conservative. Their acceptance does not claim an optimal width estimate.

## 5. Entropy ranks and startup budgets

The producer's Sections 3 and 4 are analytically valid under their stated complete-band and ordered spectral-bin hypotheses. With retained intervals [l_i,u_i], shifted retained lower sum L, upper trace bound U, omitted-bin sum T, and widths w_i=u_i−l_i, direct subtraction gives

    U/L−1 = Σ_i e^(−β(u_i−s))(e^(βw_i)−1)/L + T/L.

This is an exact decomposition of the chosen bound. The uniform-width replacement e^(β max w_i)−1 is a safe upper bound. It is generally looser because it removes the Boltzmann weights. The affine-bin estimate using the ratio x(N−q)/(q+1), with x=3e^(−βα), also has the correct geometric-tail direction whenever the first ratio is below one.

For the explicitly fixed one-triplet majorant T(r)=T_(q≥2)+r exp[−β(a₁−s)], the claimed integer floor is legitimate. It gives a minimum retained rank for that test, not a universal thermal rank. `audit_budgets.py` independently evaluates the positive sums with signed Taylor intervals at 256-bit fixed-point precision, using 80 terms, a two-sided Lagrange remainder, and repeated squaring. It does not import the producer's exponential routine.

All 18 saved rank cases reproduce. At g=.03, β=9.09, and tolerance 1e−4, ranks 13,25,49 are required by this majorant on N=4,8,16. At tolerance 1e−3 those ranks become 8,21,45. At g=.05, N=16, and tolerance 1e−4, the independent lower bound on T_(q≥2) itself exceeds the tolerance. This strengthens the producer's inconclusive status to a proved failure of that particular majorant tolerance even after every one-triplet slot is retained. It is not a bootstrap impossibility claim.

For startup, the J1 and J2 trace ratios produce the eighth powers H0^8 and H1^8. The thermal input has H2^2 and enters the third update to the fourth power, giving H2^8. Monotonicity of G(x)=1−(1−x)²/(2x²) on 0<x≤1 and sequential substitution prove all three displayed startup-budget inequalities. The inverse threshold is bounded in the safe direction by taking a lower bound on its square root.

The independent replay verifies all three exact eighth-power inequalities at g=.03 and β=9.09, using target (.9706,.9567,.987). The target reaches the common-defect domain 1/500 after 13 cyclic updates. The replay uses its own 256-bit downward rounding rather than the producer's 160-bit denominator. The physical bands and transfer-to-gap theorem retain their separate review dependencies. This audit does not use a successful scalar budget alone to claim a new physical gap.

## 6. Parameter intervals and remaining review boundaries

For a fixed trial space and affine H(t), the full residual Gram associated with any affine rational proposal D(t) is a quadratic matrix polynomial. Its leading coefficient is a positive Gram matrix. Therefore its value inside a closed interval is bounded above by the linear interpolation of the two endpoint values. Endpoint bounds by the same εG are sufficient throughout. The scalar variance has the same convexity because its quadratic coefficient is Var(V)≥0.

This analytic interval observation is sound, but it does not turn the four discrete residual obstructions into a continuous coupling claim. The residual-obstruction matrix is not the same endpoint-convex upper-bound problem. Any parameter-uniform lower-bound certificate requires its own analysis.

The all-temperature canonical small-ladder exclusion, frontier physical-band reconstruction, fully frustrated interval certificates, and all-integer-size transfer bridges are reviewed elsewhere. They are not re-proved by the residual checker. No external theorem attribution or literature claim was added here.

## Reproduction and resources

Run `REPRODUCE.sh`. Both scripts restrict themselves to one available CPU, set BLAS/OpenMP thread counts to one, and impose a 1 GiB address-space cap. The residual audit took about 2.53 seconds with 11 MiB peak RSS. The budget replay took about 0.06 seconds with 11.3 MiB peak RSS. Timing is machine- and load-dependent.

Outputs and frozen inputs are confined to this review directory. The first run snapshots every JSON input. Subsequent runs reject changed input bytes rather than silently replacing a snapshot. Exact input hashes accompany both result files, and the package manifest identifies review artifacts. No producer file, root status file, or remote state was modified.

The provided source tree contains no usable `.git` metadata. Its branch and commit could not be established locally. The review identifies concrete input bytes by SHA-256 rather than inheriting a commit claim from the root README.
