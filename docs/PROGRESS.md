# Results and research history

Updated 2026-10-14. Model definitions and the main conclusions are in the [project overview](../README.md). This record retains weaker bounds when they identify a distinct calculation, as well as failed searches and incomplete calculations that constrain future work.

## Uniform spin-1 chain

All entries use unit bilinear exchange and periodic bonds. Every range includes all integer lengths within it. Uniqueness refers to the full finite-volume ground state. The initialization length identifies the seed of a tail argument, which can exceed the smallest length covered after finite-size bridging.

| Construction | Length range | Gap lower bound |
| --- | --- | --- |
| Strengthened finite prefix and n34 tail | L≥2 | .0248 |
| Earlier all-size splice | L≥2 | .0023 |
| Finite window 28–56 and n30 tail | L≥28 | .0179 |
| n32 initialization, β=49/4, MPS64 anchor | L≥32 | .0245 |
| n34 initialization, β=49/4, MPS68 anchor | L≥34 | .0248 |
| All 18 second-set inputs independently reproduced, refined signed moments | L≥36 | .0214 |
| Earlier filter using the same reproduced inputs | L≥36 | .0046 |
| Direct finite windows joined to the n52 theorem | L≥48 | .0038 |
| Direct finite windows at β=21/2 | 48≤L≤96 | .0053 |
| n52 initialization with an exact Hermite envelope | L≥52 | .0038 |
| n54 generalized sector powers | L≥54 | .0025 |
| n56 quadratic-tail cooling | L≥56 | .0068 |
| Improved n60 construction | L≥60 | .0102 |
| Original nine Appendix A inputs, exact D26 contractions and integer interpolation | L≥1920 | .005908566393 |

The all-size .0248 proof was already present in Stage19, preserved by the Stage22 baseline, at `research_20261010/uniform_gap_0248_all_sizes_review/PROOF.md`, dated 2026-10-11 02:56 UTC. The Stage23 overview repeated this result. The second set of 18 inputs underwent physical-moment, error, and signed-moment checks. Agreement of integer totals alone would not establish those properties.

## Alternating spin-1 chain

### Discrete weak-bond couplings

Each row covers every integer cell count M≥2 unless a finite range is stated. The chain has 2M physical sites. Discrete coupling values do not imply a certificate between them.

| g | Gap lower bound | Construction or scope |
| --- | --- | --- |
| .05 | .116303868802 | Early certificate, reproduced on 2026-10-14 |
| .1 | .118954972866 | Dimer-seed construction |
| .125 | .068202652189 | Dimer-seed construction |
| .15 | .017013326349 | Depth 4 |
| .16 | .004358246531 | Dimer-seed construction |
| .161 | .001952374069 | Dimer-seed construction |
| .16125 | .001075806295 | Dimer-seed construction |
| .1615 | .039815121561 | Temperature-first recurrence |
| .1625 | .037716426713 | Temperature-first recurrence |
| .175 | .026579108896 | Joint heat-trace ratio |
| .18 | .112949677804 | Counted low band in the smaller seed |
| .185 | .096048414952 | Counted low band |
| .19 | .078956697835 | Counted low band |
| .195 | .061526095375 | Counted low band |
| .2 | .043446395688 | Counted low band |
| .21 | .101607534008 | Earlier bound |
| .22 | .065580452251 | Earlier bound |
| .225 | .045509923956 | Earlier bound |
| .21 | .107424972 | 67-dimensional small-seed reference and direct integer windows |
| .22 | .071581253 | Same construction |
| .225 | .051807500 | Same construction |
| .25 | .01 | Direct integer windows, only 2≤M≤16 |

The M4 counting reference contains the vacuum, 12 single-triplet configurations, and 54 double-triplet configurations, giving dimension 67. All 20 single-quintet configurations remain in the complement and must be counted there.

### Closed intervals near g=1

All intervals cover M≥2. The first bond coefficient remains 1 on both sides of g=1, including the rescaling required for g>1.

| Construction | Closed interval | Gap lower bound |
| --- | --- | --- |
| Full H² variance | [4999249/5000751,5000751/4999249] | .020 |
| Full H² variance | [9997911/10002089,10002089/9997911] | .015 |
| Full H² variance | [399901/400099,400099/399901] | .010 |
| Full H² variance | [399891/400109,400109/399891] | .005 |
| B² and exact finite bridge | [9998709/10001291,10001291/9998709] | .020 |
| B² and exact finite bridge | [1249773/1250227,1250227/1249773] | .015 |
| B² and exact finite bridge | [9997841/10002159,10002159/9997841] | .010 |
| B² and exact finite bridge | [156213/156287,156287/156213] | .005 |
| Positive cell-transfer certificate | [19999/20001,20001/19999] | .020 |
| Positive cell-transfer certificate | [99993/100007,100007/99993] | .015 |
| Positive cell-transfer certificate | [199983/200017,200017/199983] | .010 |
| Positive cell-transfer certificate | [99991/100009,100009/99991] | .005 |
| Earlier alternating-bond interval | [19999/20001,20001/19999] | .015 |
| Earlier wider interval | [12499/12501,12501/12499] | .005 |

The B² analysis gave Gibbs bounds κ32≤.136 and κ64≤.157. Full H² variance control improved these to κ32≤.0969 and κ64≤.119, using total variances approximately .0002629779063 and .0004964120744. The energy estimate first establishes F>1/2 before selecting the small-infidelity branch. An MPS trial state is not itself a Gibbs state.

## Ordinary square bilayer

### Surviving baseline at fixed couplings

Every entry in this table covers each integer square side L≥2. The 4×4, 8×4, and 8×8 rung seeds contain 32, 64, and 128 physical spins. Earlier bounds are retained for comparison with their original outputs.

| g | Gap lower bound | Construction |
| --- | --- | --- |
| .01 | .072950533962 | Early route with largest seed 32 spins, physical dimension 2^32, search dimension 377 |
| .01 | .168921021674 | Improved baseline |
| .02 | .057308457817 | Baseline |
| .03 | .011205710127059 | Smaller-seed route after eight scalar iterations |
| .03 | .341601445704 | 4×4 / 8×4 / 8×8 rung seeds |
| .04 | .272402896810 | Same seeds |
| .05 | .203655275044 | Same seeds |
| .06 | .164746706191 | Temperature-first steps followed by the standard recurrence |
| .07 | .093479385120 | Temperature-first recurrence |
| .08 | .023243965748 | Complete moments and implicit filtered vector |
| .085 | .027887084487 | Joint heat-trace ratio and repeated temperature-first cycles |
| .09 | .027330086079 | Exact third moment, 43-dimensional search, one numerator state |
| .10 | .038976038275 | Earlier bound |
| .10 | .055807148827 | Full residual inputs and two-dimensional direct integer windows |
| .1001 | .054499712024 | Physical reconstruction at fixed z=.1 and direct windows |
| .1005 | .049244008353 | Same construction |
| .101 | .040917096762 | Same construction |
| .1015 | .029199965244 | Same construction |
| .102 | .016509932002 | Same construction |
| .105 | .031673112867 | New 16/43-dimensional denominator-ground searches and full residuals |
| .106 | .020945510446 | Baseline endpoint certificate |
| .1065 | .021451810876 | Baseline endpoint certificate |
| .10675 | .018514632200 | Baseline endpoint certificate |
| .107 | .015448308603 | Baseline endpoint certificate |
| .1075 | .012576432653 | Baseline endpoint certificate |
| .108 | .006236941481 | Baseline endpoint certificate |
| .10825 | .001585809758 | Baseline endpoint certificate |

### Surviving continuous intervals

These bounds hold throughout the closed intervals and for every integer square L≥2. Interval certificates control the interiors as well as the endpoints.

| Closed interval | Gap lower bound | Construction |
| --- | --- | --- |
| [0,.078] | .001945771244 | Early splice |
| [.07,.078] | .002006633957 | Additional interval |
| [0,.082] | .001945771244 | Only ground-state contributions retained in each seed |
| [0,.085] | .001945771244 | Added low excited band in the smaller denominator seed |
| [0,.09] | .001945771244 | Continuous extension of a fixed 43-dimensional numerator trial state |
| [.085,.09] | .005788366954 | Additional interval |
| [.09,.10] | .008761649092 | Additional interval |
| [0,.10] | .004499695659 | Direct-window replay on 66 physical intervals |
| [.10,.102] | .013574634391 | Eight additional closed pieces |
| [0,.102] | .004499695659 | Complete 74-piece cover |
| [.102,.105] | .017785998829 | Six-piece extension with new full residuals |
| [0,.105] | .004499695659 | Complete 80-piece cover |
| [.105,.106] | .020881493369 | Continuous extension |
| [.106,.1065] | .019955613868 | Continuous extension |
| [.1065,.108] | .005329481750 | Continuous extension |
| [.108,.10825] | .000586405978 | Continuous extension |
| [0,.108] | .004499695659 | Complete 86-piece cover |
| [0,.10825] | .000586405978 | Complete 88-piece cover |

At g=.11, Stage22 established .020227124817 only for L=2–32. Its component windows gave .066142574905 for L=8–16 and .020227124817 for L=16–32. The older proposed all-size values .000137393606 and .000212810132 depended on unproved ground-lower improvements .0002743 and .0002847. They remain conditional targets. Stage24 later obtained an accepted all-size result by a different route.

## Other models and controlled comparisons

At J=.3 in the perturbed fully frustrated bilayer, direct bonds are J+ε and crossed bonds are J. The following bounds cover all square L≥2.

| Parameter range | Gap lower bound | Preparation |
| --- | --- | --- |
| ε=.005 | .038983227177 | Fixed-coupling certificate |
| 0≤ε≤.00475 | .008090283176 | Single product trial state |
| 0≤ε≤.0085 | >.001703099464 | Piecewise fixed trial states |
| 0≤ε≤.00855 | >.000768515509 | Piecewise fixed trial states |

Floating-point checks gave gaps approximately .4 and .8 for the unperturbed 2×2 and 4×2 systems at J=.3, and approximately .16 for 2×2 at J=.32. At J=1/3 the ground-state degeneracy is 2. The stored value approximately .6666667 is the separation above that degenerate band. At J=.35 the singlet product still has zero residual, but is an excited state.

| ε at J=.3 | Approximate 2×2 gap | Approximate 4×2 gap |
| --- | --- | --- |
| .005 | .369984020939 | .789973866547 |
| .01 | .340040407779 | .779851413466 |
| .02 | .281030177572 | .759030103134 |

These floating-point values do not certify continuous parameter intervals or larger sizes.

For a general perturbation of disjoint cells, spectral width w=.03 gives all-M≥2 bounds .1535504099 and, by a correlated route, .1667512861. At w=.04 a short-size bridge gives .0968387421. The width w need not equal a Heisenberg coupling g. The scalar seed at w=.047846 has no complete short-size bridge.

The large-D g=.015 correlated scalar output was approximately .0187550008 only for L≥32. The old directory description does not establish independent acceptance. A spin-1 bilayer scan succeeded at g=.005 and sampled failures at g=.01, but neither establishes an independently accepted all-size certificate.

For the ordinary single-layer spin-1/2 4×4 lattice, the approximate gap .578598335765 did not satisfy the specified small-seed purity test. In the large-D fixed-width 2×2→4×2 test, samples at g=.05 and β=5.75–11 passed, while samples at g=.1 failed. This is a strip calculation. A 64-site experiment at g=.02 used 34,881 configurations and 3,224,129 configurations in one Hamiltonian action, without an accepted seed. A commuting spin-1 square-lattice control model has exact gap 1, with a different interaction structure.

## What the unsuccessful searches exclude

The ground-only dimer-tail construction fails at all temperatures for the ordinary bilayer at g=.03. Later constructions succeed by retaining a low band and improving the tail estimate. At g=.04 and .05, the 2×2→4×2→4×4 geometry fails for all temperatures in six fixed direction orders. Larger seeds succeed. The exclusion therefore leaves other geometries, adaptive ordering, and improved inequalities open.

For the alternating chain, the older spatial-first scheme fails at g=.1615, where a later temperature-first construction succeeds. At g=.25, the old M8 two-dimensional numerator and first-window obstruction apply to that preparation. The finite M=2–16 result does not close the infinite-size tail.

The fixed 2D/57D bilayer recipe excluded at g=.1105–.115 was later surpassed by a filtered physical state outside that family. The fixed D26, single-Rayleigh, and specified-recurrence obstructions at small uniform-chain seeds coexist with the all-size .0248 certificate. Likewise, the specified-order n2 all-temperature obstructions for uniform spin 1, 2, and 3 do not establish a universal minimum seed size. The general one-dimensional defect-domain result uses u≤1/40 and entry constant 5.

A small residual alone does not identify the ground state, as the fully frustrated J=.35 example illustrates. Ground-state or low-spectrum branch identification is part of the certificate. Algorithmic exclusions do not establish a physical gap closure or a phase transition.

## Stage11–22 development

The stages below describe historical calculations. Their production and pause states do not describe current running processes.

| Stage | Contribution and limitations |
| --- | --- |
| 11 | Direct integer windows strengthened alternating-chain bounds at .21/.22/.225. M8 work included 4D and 9/13/17D pair/block spaces. Uniform-chain n54/n56/n60 cooling, MPS spin currents, and small-seed obstructions were studied. The .25 result remained finite-size. Inherited rounded vectors were not exact singlet or translation eigenstates. The value .4238202243 was a trial-energy improvement. Exclusions of specified time-first families did not establish a universal minimum seed. |
| 12 | Exact Hermite envelopes enabled uniform-chain n52 initialization with L≥52/.0038. Two-dimensional interval work reached .10 and extended to .102. Nine heat traces remained inherited inputs. The original paper's even-length scope was not reinterpreted as an odd-length theorem. |
| 13 | New full residuals, uniform-chain direct windows, and fixed-recipe diagnostics were obtained. The .0053 bound covered L=48–96. The L≥48/.0038 result additionally used the n52 tail. Full q8 norms and cross terms were required. A truncated Ritz matrix could not replace them. |
| 14 | Conditional theorems, finite-size tools, and heat-trace implementation work progressed. Unmet hypotheses and unsuccessful numerical grids yielded no unconditional all-size gap. |
| 15 | Complete physical matrices, ground-state endpoints, and some heat traces were accepted. Partial coverage and endpoint improvements were recorded separately from complete bootstrap success. |
| 16 | Square-symmetric direct windows and recurrences gave the .106/.1065 points and interval extensions. Square reflection did not establish arbitrary-rectangle x/y purity exchange. Positivity conditions required exact checks. |
| 17 | New points .10675/.107/.1075/.108/.10825 and the [0,.10825] cover were obtained. Fixed pair-product variance floors were proved. The β=19/2 failure at .1085 applied to that temperature. The variance floor at .11 and z=−11/400 applied to those fixed parameters. |
| 18 | All 18 second-set heat-trace inputs were physically reproduced, giving the uniform-chain L≥36/.0214 bound. Complete 58D matrices passed mathematical review. Totals from 2,428 checkpoints did not replace physical and error checks. The 58D endpoint resources remained UNVERIFIED, with earlier overruns retained. |
| 19 | Actual initializations n30/.0179, n32/.0245, and n34/.0248 were obtained and joined to short sizes for L≥2/.0248. L24 used parity/MPS48. The Direct25 resource review remained NOT ACCEPTED despite mathematical acceptance. |
| 20 | Positive cell transfer gave near-uniform alternating intervals and a self-contained uniform-chain proof guide. The positivity of A A* was essential. A product of self-adjoint operators need not be self-adjoint. Whole-m4 work passed small-physical and local replays, without a complete 8×4 high-moment result. There was no g=.9 certificate. |
| 21 | Independent B² inputs and Gibbs κ bounds strengthened the near-uniform intervals. Variable-g small fixtures and controls passed. The restricted-cell proposal did not obtain resource acceptance, and the controls were not a completed production calculation. |
| 22 | Full H² variances strengthened four intervals. The initial100 run produced a partial chain and terminal audit. Its 100 checkpoints did not supply complete m0/m1/m2 or m4. The historical charge of 1208 was retained. |

Spin-2 work accepted 255 L3/L4 symmetry representatives, the complete L4 heat trace, and its error budget. Under matched compilation conditions, the I/C columns were faster by approximately 8.1/3.0 times. The full L10 I/P/C calculation was still estimated at 847–1034 core-hours, failed the scalar-start screen, and was not launched. A rational-spectrum counterexample from finite moments refuted only the specified I/P information combined with numerator 1. It did not satisfy the C moments. All-length positivity and localization of the principal spectral point continued to depend on inherited inputs. Uniqueness, isolation of that point, and a successful thermal-purity initialization were not established.

## Stage23–38 and the later handoff

Acceptance in this section means acceptance recorded at the time in the recovered history. It does not mean that the complete calculation has been reconstructed and rerun today. Positive ordinary-bilayer bounds retain the Hamiltonian and normalization in the overview, a unique finite-volume ground state, and all integer square sides L≥2.

| Stage | Results and remaining restrictions |
| --- | --- |
| 23 | Retained the uniform-chain .0248 result, bilayer [0,.108] and [0,.10825] intervals, and near-uniform alternating intervals. The uniform result already belonged to the baseline. Krylov/exporter work had not yet produced a new g=.11 bound. |
| 24 | At g=.11, obtained .000131518777 and an alternative valid .000094038987 route. The calculation used actual endpoints, 25 finite windows, two tails, and an L=2–7 bridge. N32 m0–m4 comprised 2,945×24 signed fields independently reassembled into G/K/J. Six independent small physical fixtures and 19 large same-kernel samples were checked. A second independent complete N32 contraction was not performed. |
| 25 | Established .0001 throughout [0,.11]. Fourteen new pieces on [.10825,.11] joined the earlier 88 to give 102 pieces. Stronger subinterval bounds were retained. |
| 26 | Excluded the fixed 2D denominator/57D numerator recipe at g=.1105/.111/.112/.115, β=10, target 10^-6, and at most 24 square cycles. No new positive gap resulted. |
| 27 | Established .004499695659 on [0,.112] and .01 on [.108,.112], using a 118-piece splice. The numerator ψ−τ(H′−μ)ψ leaves the original 57D family. Its construction uses a strict lower bound on the full variance, rather than an exact variance or norm. Each fixed-vector plane has dimension at most 2, the extended family at most 58, and only one numerator state is retained. |
| 28 | Studied mixed-X, conservative 3D, and temperature diagnostics without a new gap. Four enclosures of the same unknown X did not recover its exact value. The robust upper bound belonged to a fixed worst-completion Temple surrogate. It was not an upper bound on the physical 3D optimum. Failure of 23 specified paths left other temperatures and trial families open. |
| 29 | Established .004499695659 on [0,.115] and .01 on [.108,.115], with 142/56 pieces. The individual points .113/.114/.115 each gave .01. Seven blocks of the complete N64 H² calculation passed independent checks, retaining q8 through signed algebra. The positive Jlo bridge in this stage did not use the new complete H² input. |
| 30 | Established .004499695659 on [0,.116], .005 on [.108,.116], and .01 at the isolated point .116. The covers contained 150/64 pieces. The new eight-piece bridge used 46 windows, eight tails, and the complete N64 H² input. r3/parity and .12/.125/.13 diagnostics gave no new gap. |
| 31 | Improved the 58D augmented denominator and obtained conditional targets and exclusions at .118. Ground-only repair with the fixed numerator and β=10 remained insufficient. The failed review, equivalent-decimal schema correction, and resource exceptions remain part of the record. |
| 32 | Established the isolated-point result g=.118 with gap≥1/200=.005. The complete16 physical variance includes q8, with the 16 preparation columns embedded in 21 mixed-q columns. Conditional transfer was followed by an independently checked actual β=10 replay using six windows, a tail beginning at 256, and L=2–7. Continuous extension had not yet been established. |
| 33 | Established .004499695659 on [0,.118] and .005 on [.108,.118], with 166/80 pieces. The new [.116,.118] bridge contains 16 closed leaves of width 1/8000, 83 finite windows, 16 tails, and L=2–7. Thirteen tails begin at 128 and three at 256. Interior bounds and endpoint joins are both required. |
| 34 | Improved g=.12 physical bounds, 48 odd low states, and conditional H³/Ritz targets. Four β=10 lower paths were exhausted at 32. Necessary numerator gain is strictly greater than 15739173/53687091200. The sufficient gain is 7869587/26843545600. Neither gain was achieved by this stage. Conditional targets T≤approximately .288818450706901697 or normalized H′³≤approximately −.145765369881870095 apply only to the fixed preparation. |
| 35 | H³ pilot240 passed small-physical controls and samples. N64 covered only 32 q4 and 128 q6 supports, compared with the complete counts 39,711 and 7,028,847. The old N32 norm check sampled 16/129. A one-vector 4×2 test did not independently accept the entire 16D matrix. |
| 36 | Calibration passed scientific controls over 305 samples, eight fields, six controls, and 37,800 local checks. Ten jobs passed, but predicted costs exceeded 13k/26k and the final cost gate returned FAILED_NO_RETRY. The failure concerned resources, with no complete H³ result. |
| 37 | The first full-native attempt failed its resource requirements. Separate control112 diagnostics passed seven stages and 20 descendants. The q4[0,12288) log was an unaccepted partial result, without q6, a checker, or full H³. The terminal accounting tail remained unknown. |
| 38 freeze | Two implementations agreed on all 39,711 q4 and 7,028,847 q6 origins, 440 chunks, eight signed fields, and six controls. Full native fields were accepted. Scalar assembly failed twice, first with MemoryError before the worker and then at an H² assertion exposing the wrong default right vector. Corrected source was accepted but had not run at the freeze. |
| Post38 handoff | assembly75748 subsequently completed the fixed-preparation full H³ and Ritz calculation and passed scientific and qualified resource reviews. The .12 bootstrap still had SOURCE_ONLY/NOTRUN status, with controls, entry checks, and admission unfinished. No new gap certificate followed. |

The Stage38 freeze and post38 handoff refer to different times. The later success does not erase the two earlier assembly failures. The handoff summary does not supply every exact scalar, so missing values have not been reconstructed from prose. The ground16 variance is complete and exact. The ground32 calculation uses a conservative complete second-moment upper bound containing q10 diagonal terms, rather than an exact complete H² matrix. N64 H² and sector inputs describe complete physical quantities for the fixed preparation, not the full 2^128 spectrum.

Resource and mathematical acceptance remain separate. The 32-rung m3/m4 run has status FAILED_ACCOUNTING_TERMINAL and a retained charge of 22,983. In Stage26, the target worker used 20.407048 against a component limit of 20, despite a total below 24. The post38 cumulative charge is 75,748, with the earlier pilot240 listed separately. The measured assembly component used 3.033131 CPU seconds, excluding an unknown coordinator terminal tail. A reserve of .25 is neither a measured duration nor a proved end-to-end upper bound. Missing receipts, overruns, source rejections, and retries remain recorded after later scientific success.

## Evidence recovery

The surviving Stage22 baseline has original commit `d17eadfb655c35eb325245d8660737b761db6b28` and tree `faebf2327efd955fbe212d65bced3c975f9ed782`. Its scientific files, proofs, data, and audit entry points remain available. The [baseline roots](../recovery_20261012/baseline_stage22_roots/README.md) identify their provenance. The [later recovered README](../recovery_20261012/latest_recovered_roots/README.md) and [historical status](../recovery_20261012/latest_recovered_roots/CURRENT_STATUS.json) describe Stage23–38 and the handoff, including dependencies that have not been restored.

The recovered README has 132,695 bytes and SHA-256 `e022c6e8aa6292a8c2b7c0e5f5ee0ab9ba24330d29af1e250fcf6602627240f8`. The historical status has 1,151,776 bytes and SHA-256 `234be47d8c379ae4a4ec3ba3a276eb56302bfe21bf439ae95fa4f2f6394533ad`. A file-interface read once returned empty content for a large file. A later object-interface read retrieved its complete JSON, so the earlier response did not establish that the source was empty.

The recovery inventory contains 700 confirmed uploaded objects. The final relevant subset originally contained 693, but its full mapping has not been recovered. Known-path metadata contains 92 entries for 90 confirmed objects. The historical plan to upload 6,617 text files in 532 batches does not measure the exact number now missing. Existing materializer source is insufficient without its catalogs and dependencies.

The bounded follow-up examined the 92 path records, 700 objects, and 599 external-history mappings. Six original source-binding JSON files were recovered and checked by size, SHA-256, and Git blob identity. Eight key result paths had no same-size candidate among the known objects. This search does not exclude their presence inside an unresolved compressed transport object. Details appear in the [recovery audit](../research_20261014/readme_audit/recovery_followup/RECOVERY_COMPLETENESS.md).

The Stage33 overview PDF was subsequently retrieved through explicit base64 and verified as 23,854 bytes, Git blob `83892297f52130ffcafce07314e5e72af2211c21`, and SHA-256 `929ffb3feb1f598f33374c27cbfadd1374a418362d8d831f39f9c4831f7faa7e`. Its extracted text confirms the 166/80-piece covers, the preserved [.108,.115]/.01 and isolated .116/.01 bounds, and the 16-leaf, 83-window, 16-tail bridge. The [retrieval addendum](../research_20261014/readme_audit/recovery_followup/BASE64_RETRIEVAL_ADDENDUM.md) documents this correction. The PDF corroborates the historical result while the full proofs and dependencies remain missing.

Direct reads on 2026-10-14 did not find the following original paths. They are listed as recovery targets rather than links.

- `research_20261010/overview_stage24/README.md`
- `research_20261010/overview_stage33/README.md`
- `research_20261010/overview_stage38/README.md`
- `research_20261010/bilayer_g011_krylov_all_size_review_c12/PROOF.md`
- `research_20261010/bilayer_filtered_backward_bridge_review24/PROOF.md`
- `research_20261010/bilayer_sharp_filter_continuous_review_completion/PROOF.md`
- `research_20261010/bilayer_haldane_poststage38_pause_handoff/PAUSED_HANDOFF.md`

The original checkpoint ZIPs contain 1,150 and 60 entries. Neither includes `research_20261010` or Stage23–38 directories. Their contents therefore cannot fill the later gaps. Failure to find an original path does not establish absence from every unidentified object.

## Checks performed on 2026-10-14

The existing independent verifiers were run in copies of the original checkpoints. Both ZIP CRC checks passed, and hashes matched for 1,149 checkpoint files and 59 extension files. The 1,149 original manifest files were checked again after replay and remained unchanged.

The original 625-dimensional benchmark reproduced integer moments of orders 0–200, inertia counts 0/1/4/9/9, and heat-trace checks at β=1 and 2. Its saved generic scalar gap lower bound is .055688426272. This is a separate benchmark, not the gap bound for the uniform spin-1 model.

The alternating-chain replay used g=1/20, M=2/4, physical dimensions 81/6561, and one retained vector per seed. Exact Hamiltonian actions and residuals, full-space Weyl completeness bounds, Temple enclosures, the full spectral tail, and the saved scalar bootstrap passed. Among β=6/8/10/12/16/20, β=10 gave the strongest bound, reproducing .116303868802. Matrix actions used conserved magnetization sectors, with Weyl bounds controlling the full space. The full many-body spectrum was not enumerated.

This work reran an existing independent verifier. It did not create a second verifier or discover a new bound. Hand-derived transfer assumptions, all-integer interpolation, and every short-size bridge were not reproved. Ordinary and fully frustrated bilayers, large-D, the uniform-chain Appendix A, Stage38, and the g=.12 bootstrap were not rerun. Their status follows the surviving evidence or the explicitly identified recovered history.

The [baseline audit](../research_20261014/readme_audit/baseline_audit.md), [later-history audit](../research_20261014/readme_audit/recovered_audit.md), and [replay scope](../research_20261014/readme_audit/replay/AUDIT_SCOPE.json) give the detailed checks. Portable entry points and input hashes are in the [replay instructions](../research_20261014/readme_audit/replay/README.md).

## Current work and scope

Work resumed at the user's explicit request on 2026-10-14 at 17:36:22 UTC. The in-place English documentation revision follows the evidence audit and bounded reruns. The [current status](../CURRENT_STATUS.json) records the active scope. Historical `PAUSED.json` files, archived running states, and old deadlines retain their original meaning. They do not override the current instruction. Raw code, data, certificates, and manifests are unchanged. Documentation may be edited even when a historical manifest records its previous hash.

The completed audit read the project rules, normalization, Stage22 baseline, and recovered later history, and cross-checked the main proof files. No long numerical production was added. The recorded gap bounds are existing results rather than new theorems proved on this date. No overall completion percentage is assigned because there is no defined total against which to measure it. Exact rational and interval calculations are not proof-assistant formalizations, and a lower bound need not equal the physical gap or exhaust the certifiable range.

## Next research steps

Recover the Stage23–38 proofs, exact inputs, interval CSV files, manifests, and review receipts, beginning with the .118 interval certificate and known object mappings. Check original bytes and close the dependency set before attempting replay. Overview files and source checks alone do not establish an executable calculation.

Once the dependencies are available, run bounded, recoverable regression checks in a copy and retain commands, environment records, outputs, and failures. Avoid repeating expensive calculations that already passed unless a specific dependency requires it. For g=.12, first reconstruct the accepted fixed-preparation H³/Ritz outputs and bootstrap inputs, then complete the controls, entry checks, and resource admission. If the missing material cannot be recovered, prepare a limited reconstruction plan before calculating.

Every long calculation requires an explicit budget, recovery points, and stopping conditions. The historical automatic reports remain inactive. New scope or pause instructions take precedence over the old research schedule. New results should update the overview with their model, normalization, coupling and size ranges, and evidence. Preserve the underlying numerical records and distinguish revised documentation from the historical files identified by earlier hashes.
