# Independent supplement: exact D26 anchors at96 and100

2026-10-10 18:58 EDT / 22:58 UTC. Anchor-only acceptance.

## Result

PASS. Freshly rebuilt D26 matrices and a sequential-power contraction independently reproduce the producer's complete norm and total-energy integers at lengths96 and100. Both periodic trial states are nonzero. For the uniform spin-1 Heisenberg chain with bilinear coefficient one and shift a=700741/500000, their shifted total Rayleigh quotients are strictly negative:

- L96: approximately -1.0101211900419775e-5;
- L100: approximately -1.051936674148218e-5.

The exact quotients and strictly positive opposite-sign integer margins are in results.json. These decimals are displays only.

This supplement accepts the two physical variational anchors for future use. It does not certify a gap, a thermal upper denominator, n48/n50 bootstrap success, a minimum seed, or failure of any alternative recipe. The original optimality review correctly excluded these anchors at its earlier cutoff and remains unchanged. Acceptance is provided only by this separate supplement.

## Physical reconstruction and conventions

The source matrices are the same periodic D26 trial family already reviewed in uniform_cooled_seed_review. Here rebuild_d26.py executes the entrywise reconstruction afresh from the integer parameter table, producing three real26x26 matrices A_s, s=-1,0,1, and the two-site physical spin-1 Heisenberg insertion. Its eleven difference blocks are byte-identical to the original audit/mps/mps_blocks.txt, whose SHA-256 is

    26da12458538967b97cb037059440d652d64593bf2044d7f5c99760444d683aa.

Direct product-basis amplitudes atL2 andL3 reproduce the independently archived norm and total-energy checks, including the two periodic bonds atL2. Thus normalization is tied to the physical spin-1 ladder coefficients, not inferred solely from agreement between long contractions.

The periodic trial amplitude is psi(s1,...,sL)=Tr(A_s1...A_sL). With T=sum_s A_s tensor A_s and the exact two-site insertion O,

    N0_L=Tr(T^L)=||psi||^2,
    H0_L=L Tr(T^(L-2)O)=<psi,H_L psi>.

Cyclic trace invariance makes the periodic state translation invariant, so multiplying a single-bond expectation byL gives the total Hamiltonian numerator, including the periodic seam. The accepted total unshifted Rayleigh quotient is H0_L/N0_L. The per-bond quotient is smaller byL; both are separately labeled in results.json.

D26 is the trial's bond dimension. The norm transfer has dimension676 and block dimensions1,8,32,80,136,162,136,80,32,8,1. The retained trial span is one-dimensional. The full physical Hilbert dimensions are3^96 and3^100. None of these dimensions is substituted for the thermal-transfer rank or an omitted spectral count.

## Independent contraction and exact signs

The producer uses binary powers in uniform_moment_optimality_assessment/contract_ground.cpp. This supplement instead uses the previously sealed independent sequential engine: it successively forms T,T^2,...,T^100 and takes ordinary traces and the physical insertion atL-2. It reads the freshly rebuilt blocks in this supplement, not the producer's proposed long answers.

Every H0_96,N0_96,H0_100,N0_100 integer agrees exactly with the producer's anchors.out. They also reproduce both exact shifted fractions in anchor_probe.json. The checker establishes N0_L>0 and

    M_L=-(500000 H0_L+700741 L N0_L)>0.

Therefore

    <H_L+aL>_psi = -M_L/(500000 N0_L)<0.

This is a variational upper bound on the physical ground energy of the shifted Hamiltonian. It guarantees an actual ground Boltzmann weight greater than1 at any positive inverse temperature. It does not prove ground-state uniqueness or a gap. A Jensen numerator using the actual Rayleigh magnitude is permissible, but a successful bootstrap also needs correctly directed upper traces and compatible scalar coordinates.

## Resource gate and executable provenance

The reconstruction ran under100MiB and took about0.945CPU seconds. An attempted local g++ compilation under the same100MiB virtual-memory ceiling reported virtual-memory exhaustion. No larger resource allowance was requested or used.

Instead, the already sealed independent sequential executable and its exact corresponding source were copied byte-for-byte from uniform_cooled_seed_review. Their hashes are checked against that review's immutable manifest. The executable was not the producer's contraction binary. The external launcher sets hard100MiB and120CPU-second limits and pins CPU5. Its inherited attempts to raise those limits are denied by the environment; LIMIT_PROBE.json verifies both increases are rejected and the smaller hard ceilings remain set.

Before the96/100 run, a fresh sequential L48 benchmark on the newly rebuilt blocks reproduced both accepted integers exactly. It consumed9.26638CPU seconds and11,072KiB peak RSS. The prior independently measured sequential-through120 run suggested less than60CPU seconds for this shorter batch. Only after the benchmark and exact comparison passed was the96/100 batch launched.

The completed batch used23.2349CPU seconds and16,956KiB peak RSS on CPU5. The measured scientific CPU work is about33.45 seconds plus a small scalar check, comfortably within the120CPU-second budget. BENCHMARK_GATE.json, benchmark48.log, anchors.log, and LIMIT_PROBE.json preserve these checks.

## Provenance and preservation

The complete producer optimality manifest `c862245e77fdf20e4e85859cbca804d888c96c11efcab2c30b5cbfedca3906cd` is verified. The independent cooled-seed and optimality review manifests are rechecked unchanged. All original long outputs, source blocks, and prior seals are read-only. No root or GitHub files were edited.

Run `bash REPRODUCE.sh` in a disposable copy. The script uses the included sealed executable, rebuilds local matrices, performs and validates the48 benchmark, runs the96/100 sequential contraction, and checks exact results under the stated hard resource ceilings. A new compiler invocation is not required. INPUT_SHA256.json records original and executable provenance; CLAIM_VERDICTS.json gives the narrow acceptance scope.
