# Exact positive-cell robustness certificates

2026-10-11 03:31 UTC. Producer exact scalar certificates, independent scalar/composition review required. The new positive cell/history and window lemmas have separate independent structural acceptance, manifest abb8e04fa7478e939d18c831a3a4b201c0ec6baf9b8e3e494b5b867a4347f872. Prior accepted near-uniform intervals are unchanged.

## Results

Let eta=(1-g)/(1+g), c=(1+g)/2, and keep the designated exchange one in H_M(g). Every row below is a producer certificate of a unique ground state and the listed physical-unit gap for EVERY integer cell number M>=2 throughout |eta|<=r. Equivalently, g belongs to the exact closed interval [(1-r)/(1+r),(1+r)/(1-r)].

| Physical uniform seed | Cell seed | Radius r | Gap D | Small-cell Weyl lower bound, display |
|---|---|---|---|---|
| 32 | 16 | 1/20000 | 1/50 = .02 | .02029898505074746 |
| 32 | 16 | 7/100000 | 3/200 = .015 | .01849870509064366 |
| 32 | 16 | 17/200000 | 1/100 = .01 | .01714854237389822 |
| 32 | 16 | 9/100000 | 1/200 = .005 | .01669849713525783 |
| 34 | 17 | 69/1000000 | 3/200 = .015 | .01817474594252997 |
| 34 | 17 | 89/1000000 | 1/200 = .005 | .01625455334475232 |
| 30 | 15 | 1/25000 | 3/200 = .015 | .02143914243430263 |
| 30 | 15 | 7/100000 | 1/200 = .005 | .01891867569270151 |

The first four rows are the strongest nested interval/gap summaries among these eight chosen tests. Their g intervals are respectively

- [19999/20001, 20001/19999], gap .02;
- [99993/100007, 100007/99993], gap .015;
- [199983/200017, 200017/199983], gap .01;
- [99991/100009, 100009/99991], gap .005.

The widest interval is approximately [.9998200161985421, 1.0001800162014581]. Exact fractions define the theorem. No optimality or all-method threshold is claimed. The old accepted .015 result on radius1/20000 and .005 result on radius1/12500 remain valid historical/weaker results; their files and review seals are read-only dependencies and were verified unchanged.

The n30 and n34 rows explicitly test odd CELL starts15 and17, with the correct independent physical MPS60 and68 anchors. They do not claim odd PHYSICAL-length alternating chains. The alternating model always has 2M physical spins.

## Fixed physical inputs

All three uniform seeds are the already accepted n30/n32/n34 rows of uniform_smaller_second_initialization/certificate.json, review manifest54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f. They use all18 uniform physical thermal inputs at beta0=49/4, lengths4 through12, each with I and P seam, and shift a=700741/500000 per physical site. Their signed moment/sector support and long-length consequences are unchanged.

Each row uses its own already accepted periodic D26 MPS at physical length2n, respectively60,64,68. The exact shifted TOTAL energies R_2n=H0_2n/N0_2n+2na are negative and recorded in certificate.json. There is no extra factor2n on H0/N0. These are one-dimensional linear trial spans with bond dimension26, norm-transfer dimension676 and physical Hilbert dimensions3^60,3^64,3^68, respectively. No new physical trace, state, contraction, Hamiltonian matrix, diagonalization, support direction, or thermal campaign is used.

One-site translation fixes the trial and reverses its staggered expectation, so the alternating-chain shifted Rayleigh is exactly c R_2n. With actual beta=beta0/c the MPS Boltzmann contribution is unchanged. The thermal input temperature itself remains49/4 in the normalized model. Doubled-temperature numerators arise variationally, not from a new physical beta49/2 thermal job.

## New analytic steps and seed transport

POSITIVE_CELL_TRANSFER.md supplies the direct Gram operator construction with nonnegative history measures at couplings1 andg, the distinct domain/range measures for A_g, the chronological cell factorization, shift, trace-class control, and all integer M>=2 identity. The independent structural review checks it separately.

The previously accepted finite untwisted trace comparison gives, at fixed physical L and normalized beta,

    1 <= Z_eta,L(beta)/Z_0,L(beta) <= exp[A_L],
    A_L=(9/8)(beta L r)^2.

It is based on the centered local spectrum, translation-odd B_L, zero uniform Gibbs expectation, Golden–Thompson and a scalar spectral-measure bound. No corresponding zero-expectation claim is made for the pi seam. The original I/P traces are used only inside the accepted UNIFORM seed.

For a uniform physical seed n with lower endpoints S0,T0 at beta0, the perturbed cell base m=n/2 therefore has

    S >= S0 exp(-2A_n),
    T >= T0 exp(-8A_n),
    actual beta=beta0/c.

All loss is applied at these finite sizes. Subsequent bootstrap steps use the actual perturbed positive cell operator.

## All-cell window, sequential recurrence and terminal test

For any integer cell base m>=2, the positive-transfer proof gives

    T(M,beta) >= S^(2-M/m) T^(M/(2m)) >= min(S sqrt(T),T),
    m<=M<=2m.

This is derived from positive-spectrum power monotonicity for the numerator and Hölder interpolation for the denominator, not by deleting a sign penalty from an old formula. It neither requires even m nor K=S^2T>1/2. The separate legal-domain conditions of the sequential update remain in force:

    S_new=G(S^2T), T_new=G(T^2 S_new),
    G(x)=1-(1-x)^2/(2x^2).

Every input and usable output is checked in (0,1], and lengths and normalized temperatures double together. For each row, each integer-cell window has C=min(S sqrt(T),T) and passes

    C-exp[2^j beta0(1+r)D](1-C)>0.

The worst actual beta is 2^j beta0(1+r), because1/c=1+eta<=1+r. At common defect u<=.01, the exact test5u exp[2^j beta0(1+r)D]<1 closes the infinite tail. The structural note explicitly proves that the conservative five-defect closure also holds at odd cell bases. All source/window/terminal endpoints and margins are rational records in certificate.json.

For the four main n32 rows the respective closure cell bases are4096,2048,16384,1024. Each earlier window overlaps its successor, so every integer M>=16 is covered. Each row separately records its exact closure and window list; no fixed-temperature or size relabeling is used.

## Finite small-cell bridge

The accepted uniform all-size gap31/1250 is used only at physical lengths4,6,...,n-2. Since ||B_L||<=3L/2, Weyl gives

    gap(H_M(g)) >= [31/1250-3(n-2)r]/(1+r), 2<=M<n/2.

The exact positive margins above each target are saved. Thus small cells2..14,2..15,2..16 are covered for n30,n32,n34, respectively. This finite use of an extensive perturbation norm is not extended to infinity. Original finite thermal/MPS provenance, including the physical24 parity/MPS48 construction, is left intact.

## Arithmetic, preliminary failures and resource budget

check_scalar.py uses Fraction arithmetic, a120-decimal-place outward grid, exact integer-square-root enclosures, positive Taylor exponentials with a geometric next-term remainder, argument halving and outward repeated squaring. It validates every source manifest member where the source uses the simple file/hash map, in addition to pinning the manifest digests. It does not import any physical contraction code.

A floating-only older width design exited with ZeroDivisionError when a computed purity rounded to1; it produced no accepted result. An early exact script stopped at an overstrong all-pass assertion, also without accepting a result. A subsequent60-digit mixed-result run is preserved in preliminary_certificate.json and preliminary_scalar.log. Its last endpoints saturated at a1e-60 defect floor for two proposed pairs. That is a finite-precision limitation of those sufficient checks, not an obstruction to the actual model. The final120-digit run retained the n30 radius1/25000,.015 target and verified it; the n34 .015 proposal was conservatively narrowed from7/100000 to69/1000000. No success is inferred for the larger unverified n34 pair.

The final measured run uses less than one process CPU second and about15 MiB RSS; exact measurements are in certificate.json and check_scalar.log. All preliminary scalar activity, including the earlier successful120-digit replay, is conservatively charged4CPU seconds. Thus the cumulative charge plus final measured run is below5CPU seconds, within the authorized30CPU-second/256MiB budget. Each scalar process has a hard limit of at most30CPU seconds and256MiB address space. No new physical work, root-file edit, remote action, or modification of an accepted seal occurred.

Reproduction should use a disposable copy because the script writes certificate/resource records. This is an exact-arithmetic producer certificate requiring independent review, not a formal proof-assistant result.
