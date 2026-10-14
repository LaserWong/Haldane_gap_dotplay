# Stage 20 research overview

This separate snapshot preserves every stage 19 scientific record and all historical certificates. The final scope combines independently accepted proof exposition, near-uniform interval certificates, structural transfer lemmas, and explicitly limited implementation reviews.

## Accepted uniform theorem and proof guide

For the untwisted periodic spin-one Heisenberg Hamiltonian with unit bilinear exchange, every integer length L≥2 has a unique finite-volume ground state and gap at least 31/1250 = .0248. At L=2 the periodic Hamiltonian contains the doubled bond. The strongest proof uses the n34 tail. The smallest separately successful genuine initialization is n30 at .0179. Neither all-size coverage nor these successful initializations establish a minimum seed.

The [self-contained proof guide](../uniform_proof_guide/PROOF_GUIDE.md) and its [independent review](../uniform_proof_guide_review/REVIEW.md) explain the exact scalar correspondence, all eighteen physically reproduced thermal premises, finite prefix, and original-framework attribution. This is accepted exposition of the existing theorem, with no new physical computation or gap row. In particular, L24 uses parity-resolved S24/T48 and a physical MPS48 anchor, rather than an own-length MPS24 contraction. Finite-volume uniqueness does not by itself establish uniqueness of all infinite-volume ground states.

The original first and second theorem bounds are (4/105) log(80/79) on even L≥60 and log(20)/784 on even L≥2304. On the common scopes, .0248 is approximately 51.7538 and 6.49030 times these lower bounds. These are comparisons of certified lower bounds, not estimates of the true gap. Original initializations were n60 and n36. The original work already used certified matrix-polynomial thermal traces.

The guide's first self-check reported 30.21035921 CPU seconds against 30 seconds. Strict measured compliance for that attempt is not accepted. The final recorded self-check used 25.746380744 CPU seconds under its 60-second limit. The independent reviewer inspected that source and record and separately replayed the exact scalar mathematics. It did not claim an external wait4 or post-exec resource-limit record for the guide self-check. The historical direct25 reviewer resource anomaly and earlier 58D producer resource caveat remain preserved.

## Stronger positive-cell intervals

The [final positive-transfer numerical review](../uniform_alternating_positive_transfer_review/PROOF.md) accepts eight exact certificates for the same periodic alternating spin-one model and every integer M≥2. Every row gives a unique finite-volume ground state. The four main cell 16 / physical 32 certificates, using their own physical MPS64 anchor, are listed below.

| Entire closed g interval | Gap lower bound |
| --- | --- |
| [19999/20001, 20001/19999] | .020 |
| [99993/100007, 100007/99993] | .015 |
| [199983/200017, 200017/199983] | .010 |
| [99991/100009, 100009/99991] | .005 |

Four additional accepted certificates demonstrate odd cell starts. The following hold for every g in the entire [(1−r)/(1+r), (1+r)/(1−r)].

- Cell 17 / physical 34, own MPS68, r=69/1000000 gives .015. r=89/1000000 gives .005.
- Cell 15 / physical 30, own MPS60, r=1/25000 gives .015. r=7/100000 gives .005.

See the [eight-row exact dataset](stage20_positive_cell_certificates.csv) and [new frontier figure](stage20_positive_cell_frontier.png). All 70 integer windows, finite Weyl bridges, coupling/temperature rescaling, own-anchor matches and late 120-digit closure are independently checked. Preliminary 60-digit failures remain diagnostics rather than no-go results. No new physical calculation or optimal-radius claim is made. The uniform .0248 theorem for every integer physical L≥2 is unchanged. These cell-based results have physical length 2M.

## Earlier near-uniform alternating intervals, retained

The [independent robustness proof](../uniform_alternating_robustness_review/PROOF.md) accepts the periodic alternating spin-one Hamiltonian H_M(g)=Σ_j[S_(2j−1)·S_(2j)+g S_(2j)·S_(2j+1)] for every integer cell count M≥2. The designated first bond coefficient is one on both sides of g=1. There are 2M physical sites and physical Hilbert dimension 3^(2M)=9^M.

- Throughout the entire closed [19999/20001, 20001/19999], the gap≥3/200=.015 and the ground state is unique.
- Throughout the entire wider closed [12499/12501, 12501/12499], the gap≥1/200=.005 and the ground state is unique.

Both nested records are retained in [the exact interval dataset](stage20_near_uniform_certificates.csv) and [the scope figure](stage20_near_uniform_intervals.png). No optimal neighborhood, true-gap estimate, or thermodynamic phase label is asserted.

The proof independently constructs a real symmetric two-spin cell-history kernel. Uniform untwisted Gibbs translation symmetry, Golden–Thompson, and a scalar spectral-measure bound control the coupling loss quadratically. It does not assume that a product of self-adjoint transfer operators is self-adjoint. Normalized β=49/4 corresponds to physical τ=β/c, c=(1+g)/2. Initialization is cell 16, or physical 32, with the inherited physical MPS64 anchor (bond dimension 26, one trial vector). All odd and even cell windows are checked through closures at cell 256/512. The extensive Weyl estimate is used only for the finite bridge M=2…15. Previously accepted physical thermal and MPS inputs remain explicit inherited premises. This proof performs no new physical contraction or heat calculation.

## Stronger cell-transfer lemma, separately accepted

The [positive-cell review](../uniform_alternating_positive_cell_review/PROOF.md) proves that, for spin one, every finite g≥0 and finite β>0, the exact physical cell transfer is the positive trace-class operator A_g A_g*, where A_g maps L²(μ_g) to L²(μ_1). The raw measures have masses μ_g(Ω)=exp(3βg) and μ_1(Ω)=exp(3β). The proof treats the adjoints, convergence and physical trace identity explicitly.

For every integer cell base n≥2, including odd n, and every n≤M≤2n, it gives T(M,β)≥S(n,β)^(2−M/n) T(2n,β)^(M/(2n))≥min(S√T,T). No inverse-purity threshold is needed for this interpolation. Later numerical recurrence domains still apply. This structural review alone supplies no new numerical interval. Cell-based uniform statements cover even physical lengths unless separately extended. It does not change the already accepted all-integer-physical-length .0248 theorem or claim arbitrary cell potentials or half-odd-integer spins.

## Prior accepted bilayer covers

Both nested all-integer-square-size results remain. Here, 86 closed pieces cover [0,.108] with gap at least .004499695659, and 88 closed pieces cover [0,.10825] with gap at least .000586405978. Each holds for every integer L≥2 with a unique finite-volume ground state. New local compiler fixtures or finite samples cannot change these gap records.

## Whole-moment implementation. Accepted fixture and sample scope

The [independent pipeline review](../bilayer_whole_m4_pipeline_review/REVIEW.md) accepts complete m0–m4 algebra and all fifteen signed terms, with six complete dense spin-derived physical fixtures on 4×2/5×2 tori. The review separately verifies producer provenance for 512 q6 and 128 q4 targets per cold/repeated phase and an independently replayed exact 64-q6 checkpoint. These are bounded sample sums, not complete 8×4 physical moments. No new energy endpoint or gap follows.

The independent small-fixture reference reconstructs local operators from four-spin swaps and includes complete high sectors, including q10 nonzero on 5×2. Physical 8×4 geometry is 32 rungs, 64 spatial neighbor edges per layer, 128 intralayer physical bonds, and Hilbert dimension 4^32=2^64. The fixture/sample coupling is fixed at g=11/100. Here H′=Q+(g/2)(C+C†+D), Q is the sum of rung triplet projectors, and T=200H′=200Q+11(C+C†+D). Moment normalization divides unnormalized T moments by ||ψ||²200^k. The coefficient endpoint c0=2^48 is explicit. Checked integer action intermediates and GMP scalar sums have distinct roles.

An independent sample stopped at its internal soft limit before the repeated phase and before final q4 aggregate totals. Those are not claimed independently reproduced. The producer's general descendant detector is unverified because its expected proc children path is absent. Direct-child CPU/wall/wait4 evidence is retained. Producer compilation CPU was not recorded, and early fixture launches lack source/executable hashes. Those historical provenance limitations are not upgraded by the later review. The repaired independent review process-tree observer passed explicit descendant and cleanup tests. Review reservations remain 90/90 seconds, actual aggregate wait4 CPU 49.784555 seconds, including failed and capped builds. No reservations were refunded.

Full production admission remains blocked pending hardening, complete cost validation and separate authorization. The empirical cold tenfold envelope is approximately 15065 CPU seconds, exceeding 10800. The smaller repeated estimate cannot substitute for a validated cache/setup schedule. These cost screens are scoped planning evidence, not intrinsic impossibility results. Active 24-field/control hardening and any production launch are excluded from this snapshot.

## Sealed partial hardening finding

A separate [read-only 22-field component finding](../bilayer_lazy_chunk_hardening_review/PARTIAL22_FINDING.md) preserves producer evidence without any independent runtime replay or new review CPU reservation. Full production remains blocked because receipt output digests are not enforced during adoption, controller death can leave a worker alive without stale-run reconciliation, aggregate/deadline/reservation forecasting is missing, and a fixed CAP−2 soft margin remains. Variable-g fields are absent. The separate active 24-field/control package is not included in this finding. A sealed finding of these limitations is not production admission.

## Reproduction and provenance

[Prior frozen stage 19 overview](../overview_stage19/README.md). The stage 20 builder pins its complete immutable manifest and retains all prior CSV bytes and scientific JSON values. Exact source hashes and independent review manifests are checked before rendering. The reproduction script first hydrates the existing lossless [stage 11 evidence package](../../reproducibility/stage11_exact_evidence/README.md), then checks source seals, corruption guards, and byte-identical PNG/PDF exports. No producer physical campaign is rerun by the overview.
