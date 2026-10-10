# Independent review of the residual-direction Rayleigh filter

Updated 2026-10-10 15:03 America/New_York (EDT, UTC−4) / 19:03 UTC.

## Verdict and scope

**PASS for both the global-compression and the triplet-number-resolved variants at all 21 frozen points.** These are rigorous improvements to a variational energy upper endpoint and therefore to an available heat-trace lower contribution. This review does not certify a new residual for the filtered state, a new eigenvalue lower endpoint, a complete thermal ratio, a scalar recurrence, an all-size bridge, or a new physical gap.

The model is the ordinary spin-1/2 square bilayer with unit rung exchange, equal positive straight intralayer exchange g, no crossed exchange, and positive-direction periodic bonds. Both bonds in a period-two direction are retained. The frozen geometries are 4×4, 8×4, and 8×8 rungs, at the seven separate couplings 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, and 0.10. No coupling-interval claim follows from these points.

The final producer manifest is `variational_numerator_filter/FROZEN_MANIFEST.json`, with SHA-256 `6b520dfee4a083c1f9d98561b859ce8a56790a83ad9f1091107d333e3ff11f3e`. Its final code SHA-256 is `d11f6b4b14bcb41842c607f4e8619b3340ce3da737cf1edb1a26ef62c22dfe96`. The final freeze is preserved at `snapshot/reviewed_filter_final/`. The initial snapshot is retained too. The only intervening code and endpoint-file changes add explicit dimension metadata. All earlier endpoint fields are identical.

The executable audit imports no filter producer code. It rebuilds the orthonormal local physical matrix and independently checks every saved scalar relation. It explicitly reuses the previously independently reviewed G/K/J assembly and the previously exhaustively rebuilt F/S/V/W geometry. Their code and geometry hashes are checked against the prior independent manifest before reuse. In particular, the new g≥0.06 G/K/J matrices are rebuilt from that geometry and compared entry-for-entry. This is validated reuse of a previously audited physical input, rather than a fresh 8×8 six-site enumeration. The 93-file input snapshot and exact output fractions are identified in `INPUT_SHA256.json` and `MANIFEST_SHA256.json`.

## 1. Physical input and normalization

Write N=nx ny and H′=H+3N/4. On each rung use an orthonormal singlet and three orthonormal triplets. The physical Hilbert dimension is 4^N. Triplet number Q is not conserved, but its parity is conserved.

The original ground trial basis consists of the vacuum, spatial orbit sums B of two-triplet spin singlets, and L=A42 B, where H′=Q+(g/2)A and A42 maps q=2 to q=4. The vacuum column is omitted in L. The retained independent basis dimensions are 11, 29, and 29. The tensors are spin zero and invariant under the translations and point symmetries used to form those orbits. H′ preserves those symmetries.

In the stored rational dimer coordinates, the common physical Gram factor 2^N has been removed. Thus G, K, and J represent the Gram matrix, den times the first H′ moment, and den² times the Gram matrix of the full H′ images, with that common factor removed. The integer denominator is den=4 denominator(g). For coefficients c and n=cᵀGc,

ρ = cᵀKc/(den n),

σ² = cᵀJc/(den² n) − ρ².

J contains all q=6 leakage. Replacing it by the square of a compressed first moment would invalidate this argument. Every frozen original Rayleigh quotient, full residual square, selected basis index, matrix entry, common factor, and trial dimension was independently checked.

The physical local operator changes q by 0 or ±2. Therefore the normalized original ψ has q=0,2,4 support and r=(H′−ρ)ψ has q=0,2,4,6 support. The exact identities are

⟨ψ,r⟩=0,  ||r||²=σ²,  ⟨ψ,H′r⟩=σ².

They use the full residual, not a projected residual.

## 2. The local upper bound and bosonic normalization

For one straight inter-rung bond, define V=S(i,0)·S(j,0)+S(i,1)·S(j,1). The independently assembled normalized 16×16 matrix is recorded in `results/local_upper.json`. Its number-preserving blocks have spectra

- qlocal=0 gives 0 with multiplicity 1
- qlocal=1 gives −1/2 and +1/2, each with multiplicity 3
- qlocal=2 gives −1, −1/2, and +1/2, with multiplicities 1, 3, and 5

Consequently (Qi+Qj)/2−Vpres is positive semidefinite. Exact rational inertia of the full normalized difference is (negative, zero, positive)=(0,4,12). Weighted graph degree four then gives

Pq H′ Pq ≤ (1+2g) q Pq.

The vacuum-to-pair amplitudes are −1/2 for t−t+, +1/2 for t0t0, and −1/2 for t+t−. No unnormalized dimer vector is being treated as a Euclidean unit vector.

The previously reviewed hard-core bosonic comparison uses Kboson=(g/2) Agraph⊗Jcolor. The color matrix is symmetric orthogonal. The weighted adjacency has norm four. Hence κ²=4g² and v=(3g²/4)Σe we², with parallel-edge multiplicities combined before squaring. Orthogonal compression of the bosonic creation operator bounds the physical creation norm. The reviewed commutator recurrence yields

||P(q+2) H′ Pq||² ≤ bq,

bq=(floor(q/2)+1)v+κ² floor((q+1)²/4).

This normalization and compression direction agree with the newly rebuilt physical kernel. The existing proof is preserved in the input snapshot under `bosonic_tail_review/PROOF.md`.

## 3. Global even-compression bound

For u supported at even q≤6, put xq=||Pq u||. Cauchy–Schwarz and the preceding bounds give

⟨u,H′u⟩ ≤ Σq dq xq² + 2 Σq sqrt(bq) xq x(q+2),

dq=(1+2g)q.

The positive-off-diagonal Jacobi matrix therefore bounds the maximum Rayleigh quotient on this compression. The physical operator need not conserve each q shell. Its compression is what occurs in the expectation.

For a proposed rational R, positive pivots of RI−Jplus are sufficient and necessary for positive definiteness,

p0=R−d0,

pi=R−di−b(previous q)/p(i−1).

Every saved pivot was independently recomputed and is strictly positive. The accepted R is on the stated 10^−16 grid, and the preceding grid point fails positive definiteness. The row-sum starting bound is safe because sqrt(x)≤max(1,x) for x≥0. A second independently chosen rational row bound also passes exact positivity. No floating eigenvalue or square-root approximation enters the accepted upper-R condition.

Although H′r may have q=8 components, those are orthogonal to r and cannot contribute to ⟨r,H′r⟩. Their omission from this compression is justified only for that expectation. It would not justify a filtered-state residual bound.

## 4. Residual-direction optimization and rounding

Suppose ⟨r,H′r⟩≤Rσ² and put C=R−ρ>0. The normalized filtered state is

φ(t)=(ψ−tr)/sqrt(1+t²σ²).

Its energy satisfies

⟨φ(t),H′φ(t)⟩ ≤ ρ+σ²(−2t+Ct²)/(1+t²σ²).

For any δ>0 satisfying δ(C+δ)≤σ², choose t=δ/σ². Direct substitution gives an energy no larger than ρ−δ. Indeed, after multiplying by the positive normalization denominator, the excess over ρ−δ is

δ[δ(C+δ)−σ²]/σ² ≤ 0.

The optimal comparison gain is δ*=(sqrt(C²+4σ²)−C)/2. The discriminant root is rounded down on a rational 10^−24 grid. This rounds the promised improvement down and the energy upper endpoint up. The integer square-root inequalities and the final exact quadratic slack were checked at all 42 endpoint instances, including both variants at each point.

The rational fallback δ0=σ²C/(C²+σ²) is also safe. Its quadratic slack is (σ²)^3/(C²+σ²)^2>0. It supplies a strict improvement when a decimal root grid is too coarse. Zero variance means ψ is already an exact eigenvector and the endpoint is unchanged. Independent exact edge tests cover zero variance, variance 10^−60, and an exactly square discriminant.

## 5. Independent check of the q-resolved extension

Let D be the diagonal B Gram matrix, with the same common factor removed. Reinsert zero coefficients for unused L columns and write c=(cB,cL). The q≤2 part of the full residual belongs to B. At q=2, the total-spin-zero space for a fixed pair of occupied rungs is one-dimensional. Taking orbit sums therefore exhausts the pair states invariant under the trial's spatial symmetries. H′ preserves that invariant space.

Consequently its coordinate vector is

u=D^−1 K(B,all)c/den−ρcB.

This gives w0=D00u0²/n and w2=Σi≥1 Diiui²/n. For the remaining shells put h=(g/2)cB,pairs+(4−ρ)cL. The orthogonality of different number shells and the reviewed contractions give

w4=[hᵀFh+g hᵀS cL+(g²/4)cLᵀV cL]/n,

w6=(g²/4)cLᵀW cL/n.

Here F=L*L, S=L*A44L, V=(A44L)*(A44L), and W=(A64L)*(A64L), all divided by the common factor. The cross coefficient is g because the two conjugate real cross terms each contribute g/2. Every wq is nonnegative and their exact sum equals the original σ² at every frozen point.

It follows that

⟨r,H′r⟩ ≤ Σq dq wq+2Σq sqrt(bq wq w(q+2)).

Each square root is rounded upward on a 10^−36 rational grid. The saved root squares are at least the exact radicands, and the immediately smaller grid points are below them. Dividing by σ² gives a state-specific upper expectation Rsector. Taking min(Rglobal,Rsector) is valid because both independently bound the same expectation. It need not bound H′ on other vectors. Every final gain is at least its global-compression counterpart.

## 6. Finite physical checks and thermal use

The audit constructs six direct physical test vectors, two each on 2×2, 3×2, and 4×2 rungs, from normalized singlet pairs and their q=4 creation images. These include period-two multiple bonds, different nonzero residual shell weights, and mixed coefficient signs. The largest test has 1,101 nonzero trial configurations and 4,067 nonzero residual configurations.

All six tests independently check the full G/K/J matrices against direct physical H′ action, every q-resolved residual mass, ψ⊥r, the filtered normalization, both bounds on the actual ⟨r,H′r⟩, and the actual filtered Rayleigh quotient below the certified optimized endpoint. The 2×2 and 4×2 F/S/V/W physical contractions also agree with the prior independent geometric output. These checks are supplemental finite-model tests of the general argument. They are not the basis for extrapolating to 8×8. Direct higher actions occur only in these tiny audit fixtures, not as new production input moments.

For β>0, Jensen's inequality in the spectral measure of normalized φ gives

Tr exp(−βH′) ≥ ⟨φ,exp(−βH′)φ⟩ ≥ exp(−β⟨φ,H′φ⟩) ≥ exp[−β(ρ−δ)].

The filtered state remains an even spin singlet. It can therefore replace the original even trial in a trace lower sum containing the unchanged orthonormal odd triplet trial family. This operation does not alter the certified number of retained eigenvalues and does not require assigning the new vector the old residual. The variational principle independently gives λ1(H′)≤ρ−δ.

For N=64, the global and q-resolved improvements are respectively

| g | Global improvement | q-resolved improvement |
|---|---:|---:|
| 0.03 | 0.00000810164916752232 | 0.000008223606661653405 |
| 0.04 | 0.00004333230047791971 | 0.000044475902350273736 |
| 0.05 | 0.0001553195021060917 | 0.0001614531974343531 |
| 0.06 | 0.0004302948304396458 | 0.0004533894155280005 |
| 0.07 | 0.0009943987588343424 | 0.0010624147567235697 |
| 0.08 | 0.0020068075813080197 | 0.0021739102428210404 |
| 0.10 | 0.006080247946504525 | 0.006763181395119954 |

These decimals are displays. The accepted values are exact fractions in `results/point_replay.json`, which also contains all smaller-geometry results.

The original trial spaces have dimensions 11/29/29. The implicit filter plane has dimension at most two, and adjoining r to the original space gives dimension at most 12/30/30. The new retained object is one filtered state with q≤6 support. Its residual may have q=8 support and is not certified here. At the largest geometry the full Hilbert dimension is 4^64=2^128, which must not be confused with any trial-space dimension.

## 7. Reproduction and remaining work

Run `bash REPRODUCE.sh` in this directory or by absolute path. It verifies all frozen input hashes and runs the independent audit. Outputs are confined to this review directory. The audit is pinned to one CPU, all BLAS/OpenMP settings are one, and the inherited physical-input module tightens the address-space cap to 1 GiB. The observed complete replay takes 8–23 seconds under shared load and about 87 MiB peak RSS on this worker.

The active extracted tree has no Git metadata, so this review identifies the exact bytes through hashes rather than asserting a newly verified local commit. No producer files or remote repository state were changed.

The next admissible step is a separately reviewed combination with the existing lower-energy intervals, complete spectral tail, thermal ratios, recurrence, and finite-size bridge. Approval of the present filter does not pre-approve numerical results from that combination.
