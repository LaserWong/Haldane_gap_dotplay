# Independent review of the joint-aware spin-one chain extension

Updated 10 October 2026, 15:23 America/New_York (EDT) / 19:23 UTC.

## Verdict

The periodic spin-one alternating chain with strong exchange one has these
independently verified lower bounds, for every integer cell count M>=2:

| Weak exchange g | Uniform gap lower bound | Unique finite-volume ground |
|---|---:|---|
| 7/40 = .175 | .026579108896 | Yes |
| 9/50 = .18 | .013222512347 | Yes |
| 181/1000 = .181 | .009728769181 | Yes |
| 91/500 = .182 | .005940278341 | Yes |

These are discrete sufficient certificates. They do not establish a continuous
coupling interval, a maximal certifiable coupling, the actual physical gap, or
an infinite-volume ground-state uniqueness assertion. Failed bounded scans at
other couplings are not all-temperature or all-order obstructions.

The complete producer manifest SHA-256 is
`bc1b7bcc23f7f217c558a77790c0c45a8763ae40c1d8b20b5ca3b50d18d16370`.
All 43 producer files are preserved byte-for-byte in `chain_snapshot/`. The
external 27 input hashes and 21 files of the prior independent frontier review
are verified before any mathematical computation. No frozen file is changed.

## 1. Physical model and exact first moments

The Hamiltonian is

    H_M(g) = sum_i S_(i,0) dot S_(i,1)
             + g sum_i S_(i-1,1) dot S_(i,0),

with spin one and periodic cell indices. It contains 2M physical spins and
full Hilbert dimension 9^M. The periodic weak-bond multiset has M entries;
at M=2 both physically distinct bonds are retained. The cell, not an individual
microscopic spin, is the unit of doubling and interpolation.

The physical local dimer kernel is inherited from the sealed independently
reconstructed spin-one kernel. Its code hash is
`30c997e6e56135af60cd989ab22e31a8957346dc3ff2235ae8ac6b2c62916a19`.
It reconstructs the physical spin operators and their rational dimer-basis
matrix elements, including Gram weights (3,2,2,2,1,2,6,2,1).

For M=8 this review independently reassembles the two-by-two Gram, strong first
moment, and weak first moment. The implementation constructs a returning-support
action dictionary for each ket, independently of the producer's matrix assembly.
Every saved entry agrees, all matrices are symmetric, and the Gram determinant
is strictly positive. The integer coefficient proposal is accepted only after
its exact positive metric norm and Rayleigh quotient are recomputed.

The two trial vectors have common support 43,294 inside the full 43,046,721-
dimensional space. The combination search is two-dimensional, the retained
Rayleigh contribution is one state, and neither number is an MPS bond dimension.
No largest-patch residual, isolation, energy lower bound or complete trace upper
bound is needed. Matrix elements returning to the support determine a Rayleigh
quotient exactly; omitted outputs are not called a residual certificate.

The same independent action reconstruction verifies the M=6 and M=7 short-
bridge first moments at support dimensions 2,434 and 365. Their affine Rayleigh
quotients are reevaluated at each actual coupling.

## 2. Complete M=4 ground and full-spectrum tail

At each accepted coupling, the inherited independent physical checker is run
on the frozen small-patch trial, with its actual coupling checked explicitly.
It reconstructs the entire H-applied vector, exact metric norm, Rayleigh
quotient and residual square. All 1,099 trial configurations and all 1,107
reached configurations are accounted for; the physical space has dimension
6,561. The weak-bond multiset and full residual are checked independently of
the saved producer scalar results.

The exact rational local matrix

    g V + a(h_i+h_j) + b I

has 81 strictly positive LDL pivots across every magnetization block. With
alpha=1-2a>0, summing the local comparison yields

    H_M >= -2M + alpha sum_i h_i - Mb.

The isolated-dimer levels are 0,1,3 with multiplicities 1,3,5. The complete
reference count is rebuilt by convolution; it sums to 9^4. This comparison
proves a full-space second-level cutoff, and the complete trial residual then
proves the unique-ground Temple interval. The review checks every separation
and variance condition.

For the actual saved ground Rayleigh rho4 and lower endpoint e_minus, the
independently bounded shifted trace is evaluated as an explicit sum over all
nonzero reference bins:

    Q4(beta) <= exp[beta(rho4-e_minus)]
      + sum_(e>0) multiplicity(e)
          exp[-beta(-8-4b+alpha e-rho4)].

This is the complete spectral tail, not a selected low-state trace. Summing
individual bins instead of reusing the producer's power polynomial provides
a separate implementation of the same min-max bound.

## 3. Independent exponential and ratio arithmetic

The audit imports no new producer mathematical module and never calls the
producer's exponential function. Its own exact interval exponential reduces
to absolute argument at most 1/16, uses 110 Taylor terms with an explicit
geometric remainder, and rounds outward to 384 binary bits after every square.
Negative exponents use outward reciprocal intervals.

Every stored small trace upper endpoint is at least this independent upper
bound. Using only the independently checked rho8 and rho4 gives

    J >= exp[-2 beta(rho8-2rho4)] / Q4(beta)^4,
    C >= exp[-2 beta(rho8-2rho4)] / Q4(2 beta)^2.

The saved 12-decimal lower ratios lie below these independent rigorous ratios.
All subsequent 12-decimal purification updates are reproduced exactly.
Square-root enclosures are independently recomputed at 70 decimal digits;
each producer's saved 50-decimal inverse-purity root witness is also verified
by exact integer/rational squaring.

## 4. Time-first cycles, joint transport, and canonical states

The separately sealed general lemma review is `LEMMA_ACCEPTANCE.json`, with
manifest `LEMMA_REVIEW_MANIFEST.json`. It proves the same-base identity

    S_actual^2 T_actual = a_actual^2 b_actual.

At an even base, time-first lower endpoints a,b give separate simultaneous
bounds S>=a sqrt(b), T>=a^2 b, and the independent joint lower endpoint
K=a^2 b. The product of the first two rounded bounds can be much smaller than
K. This audit preserves K as a separate quantity in each relevant row.

Starting with the physical n=4 seed at beta, the initial time-first startup
produces a,b at exactly (8,2 beta). Each additional time-first cycle doubles
both coordinates. Every intermediate state is converted for its own finite
window before the next cycle. When canonical continuation begins, its first
spatial update uses G(K), not G(S^2 T), followed by the valid thermal update.
Later canonical cycles conservatively use their new component product.

The selected paths have these exact labels:

| g | Initial beta | Additional time-first cycles | Canonical cycles | Canonical conversion (cells,beta) | Asymptotic onset | Final beta |
|---|---:|---:|---:|---|---:|---:|
| .175 | 111/5 | 3 | 1 | (64,1776/5) | 128 | 3552/5 |
| .18 | 114/5 | 3 | 2 | (64,1824/5) | 256 | 7296/5 |
| .181 | 231/10 | 3 | 2 | (64,1848/5) | 256 | 7392/5 |
| .182 | 469/20 | 4 | 1 | (128,3752/5) | 256 | 7504/5 |

The numbers of additional cycles exclude the initial physical startup.
Conversion changes edge order without changing its base. No time coordinate
is silently relabeled as a spatial length. All 54 saved scalar paths, not
just the four selected paths, are independently reproduced.

## 5. Every integer finite bridge and the terminal theorem

Every saved finite window is checked with its actual cells, inverse temperature,
component endpoints, separate joint endpoint, inverse-dominant-weight root,
absolute tail ratio, thermal lower bound, and exact exponential gap test.
All 285 windows across the saved alternatives pass. The accepted selected
finite windows are:

| g | [8,16] | [16,32] | [32,64] | [64,128] | [128,256] |
|---|---:|---:|---:|---:|---:|
| .175 | .026579108896 | .027064580555 | .027938643319 | .028694527166 | not needed |
| .18 | .013336452251 | .013222512347 | .014108759667 | .014748312144 | .014142877743 |
| .181 | .010569709793 | .009805419826 | .010526884112 | .011129976216 | .010532307541 |
| .182 | .007720429617 | .005940278341 | .006214580622 | .006762052691 | .007111597416 |

The intervals contain every integer, including odd cells, by the previously
reviewed signed-transfer theorem. Each next window starts where its predecessor
ends. A later successful bootstrap is never substituted for a missing earlier
window.

At the final canonical state the common defect satisfies 0<u<=1/100. The
inherited all-integer asymptotic theorem is accepted only after the independent
rational exponential test

    exp(beta_final gap) 5u < 1.

The respective asymptotic gap endpoints are .026593870571, .013330661856,
.009728769181, and .006117337305. The .181 overall certificate is limited by
its asymptotic endpoint; the other three are limited by an earlier finite
window. Reporting only the terminal bootstrap gap would therefore overstate
three of the four all-size results.

For M=2,...,7 the same new local LDL comparison provides
lambda2>=-2M+alpha-Mb. The trial Rayleigh upper energy is -2M for the product
state, or the independently reevaluated M=6/M=7 trial when lower. Every
cutoff-minus-Rayleigh value is strictly positive. Their minimum values are
respectively greater than .060886447122, .037789730996, .033146995125, and
.028522820458. They exceed each corresponding final accepted bound.

The six short sizes, consecutive finite windows beginning at M=8, and the
asymptotic all-integer theorem consequently cover every integer M>=2.

## 6. Reproduction, resources, and integrity

Run `bash REPRODUCE_CHAIN.sh` from this directory. It reruns only the independent
audit and writes this review's results; no producer package is rerun or edited.
Keep a copy of the sealed review if preserving timing/resource bytes matters,
because diagnostic run times will change on replay.

The accepted run took 29.98 seconds, peaked at 40,328 KiB RSS, pinned itself to
one permitted CPU, and imposed a 1 GiB address-space cap. It ran no many-body
eigensolver and rebuilt no large residual support. The extracted workspace has
no Git metadata, and this review makes no remote-publication claim.

Machine-readable results:

- `results/chain_summary.json`: accepted gaps, scope, seals and resources.
- `results/chain_review_*.json`: every exact physical check, scalar path, window
  and positive exponential margin.
- `results/chain_first_moments.json`: independent returning-support moment checks.
- `results/chain_audit_input_sha256.json`: consumed immutable sources.
- `PRODUCER_CHAIN_MANIFEST.json` and `chain_snapshot/`: frozen producer bytes.
- `CHAIN_REVIEW_MANIFEST.json`: this complete external review's seal.
