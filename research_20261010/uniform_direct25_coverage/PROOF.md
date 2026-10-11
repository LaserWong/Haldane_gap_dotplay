# Direct thermal certificate for the missing odd length25

2026-10-10 22:36 EDT / 2026-10-11 02:36 UTC. Exact producer certificate; new physical25/scalar review pending.

## Result

Uniform periodic spin-one Heisenberg chain with bilinear coupling1 and shift a=700741/500000. A fresh own25-site D26 MPS trial, the existing exact even-moment trace bounds at24/26 and beta0=49/4 give a rigorous lower thermal purity at25 of.7059136371793064. Its exact exponential margin proves unique ground state and gap>=.0023.

Combining this missing odd length25 with the frozen isolated24 certificate and independently reviewed all-integer coverageL>=26 gives gap>=.0023 and unique ground state for EVERY integerL>=24. Bootstrap initialization remains30. The stronger nested bounds.0179 forL>=28,.0245 forL>=32 and.0248 forL>=34 remain intact. No startup24, minimum-size theorem, n22 computation, new thermal campaign or largerD is claimed.

This is genuinely different from the failed odd spatial-tail interpolation recorded in uniform_n24_second_coverage. That failed bound remains unchanged. The direct physical numerator here avoids its weak odd transfer-tail subtraction.

## Own odd-length MPS and normalization

The fresh norm and total energy are

    N0_25=Tr(T^25)>0,
    H0_25=25 Tr(T^23 O),
    R25=H0_25/N0_25+25a.

Here T and O are the physically audited D26 double-layer norm transfer and two-site bilinear Heisenberg insertion in audit/mps/mps_blocks.txt. H0_25/N0_25 is TOTAL energy; no per-bond quotient is substituted. The state is one D26 trial in the full3^25-dimensional Hilbert space. Its length is25, not50/48/72.

The exact shifted Rayleigh R25 is POSITIVE, approximately.004211576434633581. The direct argument does not need a negative Rayleigh quotient or Z25>1. By spectral Jensen for any normalized physical trial,

    Z25(2beta)>=exp(-2beta R25)>0.

This holds whether the shifted trial energy is positive, zero or negative. Ground uniqueness is not assumed at this step.

## Odd trace denominator from even neighbors

At beta0, use the inherited real self-adjoint history transfer X and its absolutely convergent physical trace identities for integer lengths>=4. Cauchy–Schwarz on its real eigenvalue sequence gives

    |Tr X^25|^2 <= (Tr X^24)(Tr X^26).

For example apply it to sequences lambda^12 and lambda^13, retaining the full physical multiplicities. This is valid for countable spectra and does not assume positivity of each transfer eigenvalue. The physical Z25 is strictly positive, so its squared denominator is legitimate. If Q24,Q26 are certified positive upper bounds on these even physical traces, then

    Z25(beta0)^2 <= Q24 Q26.

The existing signed degree-eight polynomial majorants and twelfth-moment packing bound supply Q24,Q26; the checker uses their safe minimum separately in the J and N sectors and includes multiplicity3 for N. All coefficients, moment intervals and signed support proofs are unchanged inherited exact certificates from the independently accepted smaller-initialization package. No25-site thermal matrix is computed.

## Purity, gap and coverage

The exact directed expression is

    C25=lower_exp(-2beta0 R25)/(Q24 Q26).

With outward100-decimal rational arithmetic the checker obtains C25>=.7059136371793064. It verifies C25>1/2 and

    C25-exp(beta0*.0023)(1-C25)>0,

with margin greater than.40342. A Gibbs purity above1/2 forces a unique largest Gibbs eigenweight and therefore a unique physical ground state; the standard ratio inequality yields the claimed gap. The union{24},{25},[26,infinity) covers every integerL>=24 without asserting purity monotonicity in size.

The frozen24 producer manifest is ef04180cedde73a09aa627c3dc75c2730472c9f425fd29bcec376678fea00240. The frozen26 producer manifest is c723bca65e315ad2c2d296a9b0cc6cf51dc67240749bd06ee812b49ec8a9e609; its independent review is b4e4bc246acb27b63bb51745c23cbd28b7b0928d5d45ad19ddfb3ffe5d6d077d. New direct25 and isolated24 acceptance must still be checked by the assigned reviewer before promotion.

## Small-power adaptation and resource gate

The generic prior contract_ground engine always built binary powers through128, unnecessary for25. contract25.cpp preserves its exact GMP matrix multiplication and trace rules but accepts ONLY25 and builds powers1,2,4,8,16. Since25-2=23=16+4+2+1, these exactly suffice. Norm is Tr(T^23 T^2), energy25Tr(T^23 O). This truncates unnecessary computation, not the physical matrices or spectrum. The existing independently inspected small-length engine already used these powers for12/16/20/24 and reported2.329CPU seconds for all four.

The original remaining contraction budget was7.36279CPU seconds. The fresh25 run was hard-capped7CPU seconds/100MiB onCPU5 and completed2.05471CPU seconds/14600KiB. All fresh producer anchors68/64/60/56/52/48/25 together total54.69192CPU seconds, below the original60 budget.

Two build-only attempts under100MiB failed with virtual-memory exhaustion, atO2 andO0. Their original stderr logs are retained. No physical contraction launched in either failed build, and they are not mislabeled anchor attempts. Parent separately authorized compilation onCPU2 with512MiB/30CPU-second caps; that build succeeded. Physical run limits remained7CPU seconds/100MiB. Scalar proof usesCPU2 with30CPU-second/256MiB limits and completes in about.6CPU seconds/~11MiB. The first scalar read before a successful build had missinganchor25.out and produced no certificate; final replay uses the completed own25 output.

Replay in a disposable copy: compile contract25.cpp with g++ -O2 -lgmpxx -lgmp under the separate build allowance; run taskset -c5 contract25 audit/mps/mps_blocks.txt25; then python certify.py. Preserve exact whitespace between input path and length25 in the command. INPUT_SHA256.json and the manifest pin all consumed files. The code imports only the inspected arithmetic/sector helper from the frozen n24 scalar package; its preloaded48 integers are not used in this25 proof. No previously sealed package, root documentation or remote repository is changed.
