# Independent direct25 thermal certificate and coverage composition

2026-10-11 02:40UTC /2026-10-10 22:40 America/New_York.

## Mathematical verdict and separate resource exception

MATHEMATICAL RESULT ACCEPTED: the unit-bilinear untwisted periodic spin-one Heisenberg chain has a unique ground state and gap≥23/10000=.0023 for every integer L≥24. This package supplies the missing individual length25; it joins the separately accepted isolated24 certificate and the tail for every integer L≥26. Canonical bootstrap initialization remains30. The stronger nested bounds .0179 from28, .0245 from32 and .0248 from34 remain unchanged. No minimum or below24 claim follows.

RESOURCE COMPLIANCE IS NOT ACCEPTED. The independent25 contraction reports25.9614 process CPU seconds despite a requested/asserted15-second external CPU limit. The source uses clock()/CLOCKS_PER_SEC, not wall time. This anomaly was reported before sealing; no rerun was made. RESOURCE_ANOMALY.json preserves the limits, logs and missing runtime measurements. The exact mathematical evidence and the resource-control failure are distinct findings. This package must not be described as a successful15-second resource gate.

## 1. Fresh physical25-site anchor

The fixed real D26 tensors were independently reconstructed entrywise, including the physical spin-one nearest-neighbor insertion and charge-difference block decomposition. The rebuilt blocks exactly match the previously independently verified physical original. Direct amplitude checks at lengths2 and3 again verify norm and TOTAL periodic energy conventions. Periodic amplitudes Tr(A_s1...A_sL) define legitimate states for odd L as well as even L; no bipartite transformation or even-size extrapolation is used.

The reviewer reuses its inspected sequential GMP power implementation, distinct from the producer's binary/small-power implementation. All exact25-site norm and energy integers match. The norm is strictly positive. H0_25=25 Tr(T^23 O) is already the TOTAL Hamiltonian numerator, so

    Etrial25=H0_25/N0_25+25(700741/500000).

Its exact value is POSITIVE, approximately.0042115764. It is not a negative-energy anchor and does not imply Z25(2beta)>1. The positive energy is fully retained in the numerator bound below. No48-,50- or52-site energy is substituted for this25-site trial. D26 is bond dimension, the trial span is one-dimensional and the physical Hilbert dimension is3^25.

Producer manifestabd4e0f0a315ef9878129c56ee884d797707687f07361c83f1cb140f0ebee9fa is fully verified. Exact norm, total-energy identity, rebuilt blocks and source/executable pins are checked by audit.py.

## 2. Physical thermal numerator

Let H' be the shifted physical25-site Hamiltonian. The variational principle gives its ground energy E0≤Etrial25. Consequently for beta>0,

    Z25(2beta)=Tr exp(−2beta H') ≥ exp(−2beta E0)
              ≥ exp(−2beta Etrial25).

This uses neither ground uniqueness nor negativity of Etrial25. Equivalently one may use Jensen on the normalized trial state. Here Etrial25>0, so the retained numerator is below1. The reviewer bounds exp(2beta Etrial25) above by exact directed Taylor arithmetic, then takes its reciprocal to obtain a valid lower bound for exp(−2beta Etrial25). The producer's saved lower endpoint is at most this independently computed endpoint.

## 3. Odd denominator from even physical traces

The source-verified self-adjoint spatial transfer identity is Z_L(beta)=Tr X_beta^L for every integer L≥4, including the untwisted odd physical chain. With real eigenvalues lambda_i, absolute convergence follows from finite even moments. Cauchy–Schwarz gives

    0<Z25(beta) ≤ sum_i |lambda_i|^25
      ≤ sqrt[(sum_i |lambda_i|^24)(sum_i |lambda_i|^26)]
      = sqrt[Z24(beta) Z26(beta)].

Even powers ensure the last two sums are the physical traces despite signed subleading eigenvalues. Thus Z25(beta)^2≤Q24 Q26 for any certified physical upper bounds Q24,Q26. The argument does not replace an odd numerator by an unsigned trace and does not require the spatial transfer spectrum to be nonnegative.

The Q values are reconstructed as J+3N, taking the minimum of accepted signed polynomial and exact packing upper bounds at24 and26. All four polynomial bounds were independently proved on their full signed support intervals in core review54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f. Negative coefficients use lower moment endpoints and positive coefficients use upper endpoints; N multiplicity3 remains present.

The full physical thermal review792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94 is verified in full. Its18-case provenance table explicitly maps all locally reproduced beta49/4 I/P integer totals and exact error intervals to the refined signed moment intervals. audit.py compares that entire signed-moment mapping exactly to the current certificate. Thus no printed-only thermal premise remains hidden in Q24,Q26.

## 4. Purity, gap and complete coverage

Combining numerator and denominator,

    T25(beta) ≥ exp(−2beta Etrial25)/(Q24 Q26).

At beta49/4 the certified lower purity is approximately.7059136372. Exact rational arithmetic verifies C>1/2 and

    C−exp[(49/4)(23/10000)](1−C)>0,

with margin approximately.40342356. A Gibbs purity>1/2 implies its largest weight exceeds1/2, so the ground state is unique. The first-excited to ground weight ratio is at most(1−C)/C; the displayed exponential inequality proves the gap. Uniqueness is a conclusion, not an input to the variational bound.

Independent isolated24 review9d31eeb0dc44f24047943a4ad4dd06e4f8f82aced5ca321857a1aaedf82b8282 gives the same gap at24. Independent parity-prefix reviewb4e4bc246acb27b63bb51745c23cbd28b7b0928d5d45ad19ddfb3ffe5d6d077d supplies every integer≥26. The union{24},{25},[26,infinity) is every integer≥24. No monotonicity of finite-volume physical gaps is assumed. The earlier failed25 parity bound remains a truthful diagnostic of that weaker recipe and is not contradicted by this different successful numerator estimate.

## 5. Tests, execution and the unresolved timing anomaly

Seven adversarial tests reject a false negative-anchor assumption, replacing the numerator by1, reversing its exponential sign, confusing one-bond/total energy, omitting N multiplicity, relabeling coverage24 as initialization24 and dropping25 from the union. A signed-spectrum rational fixture also checks the Cauchy–Schwarz direction.

The scalar audit reports.716CPU seconds/14280KiB onCPU4 within its30CPU-second/256MiB budget. The physical rebuild reports1.435CPU seconds; the contraction reports25.9614CPU seconds/8568KiB onCPU5. Its wrapper sets and asserts RLIMIT_CPU=(15,15), RLIMIT_AS=100MiB and tests that Python cannot raise them before exec. The C++ source later attempts larger limits without logging return values. Runtime post-exec limits, external wait4 user/system CPU and actual thread count were not retained. The executable is unchanged from the sealed independent engine; it is not setuid. Read-only shell observations show ordinary uid1000 and no effective capabilities, but do not establish the finished child's runtime state.

The cause of the reported CPU-limit anomaly is unresolved. The25.9614 value must not be silently relabeled wall time, and requested15-second compliance must not be asserted. Root and the finite-prefix producer were warned, further reviewer physical execution was paused, and no investigation rerun occurred. The logged exact output still matches the separately produced integer result and has a complete physical derivation. Preserve this resource exception alongside the mathematical acceptance.

Replay the cheap mathematical audit only in a disposable copy with pinned dependencies: python audit.py. Do not repeat physical execution merely to investigate timing without a separately reviewed resource plan. All prior seals and producer/root files remain unchanged.
