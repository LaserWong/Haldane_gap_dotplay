# Recovered Stage 23–38 results

## Results and evidence

The strongest continuous ordinary-bilayer certificate in the recovered documents gives gap ≥ 0.004499695659 for every real g in [0,0.118], and gap ≥ 0.005 on [0.108,0.118], with a unique finite-volume ground state for every integer square side L≥2. They also preserve the stronger bound 0.01 on [0.108,0.115] and at the isolated point g=0.116. These exact-certificate claims were independently accepted in the historical records. The current recovery is incomplete, and this audit did not reverify their full proofs.

The post-Stage38 handoff records accepted fixed-preparation H³ and Ritz results. The g=0.12 bootstrap replay remains SOURCE_ONLY/NOTRUN, with incomplete controls, entrypoint and run-admission checks and no new gap certificate. The frozen Stage38 record predates that acceptance. The later handoff updates the status while preserving the earlier snapshot.

This document review ran no compiler or scientific replay and made no remote changes. The October 12 pause and October 14 00:00 UTC deadline describe the historical work period. The subsequent request to resume superseded them.

## Sources reviewed

- `AGENTS.md`
- `CURRENT_STATUS.json` (current recovery wrapper)
- `research_20261010/PLAN.md` (current recovery wrapper)
- `recovery_20261012/README.md`
- `recovery_20261012/KNOWN_BLOB_PATHS.json`
- `recovery_20261012/latest_recovered_roots/README.md`
- `recovery_20261012/latest_recovered_roots/CURRENT_STATUS.json`
- `research_20261010/MODELS_AND_NORMALIZATION.md`

The recovered README has 132,695 bytes and SHA256 `e022c6e8aa6292a8c2b7c0e5f5ee0ab9ba24330d29af1e250fcf6602627240f8`. The recovered status has 1,151,776 bytes and SHA256 `234be47d8c379ae4a4ec3ba3a276eb56302bfe21bf439ae95fa4f2f6394533ad`. Both match the known-object metadata. The file API returned empty content for the large status file. The blob API supplied its full JSON. This is an API retrieval limitation, not an empty source file.

## Model and normalization

Ordinary square bilayer: spin 1/2, rung exchange 1, no crossed interlayer bonds or field,

H_L = sum_r S_(r,1)·S_(r,2) + g sum_(r,mu=x,y) [S_(r,1)·S_(r+e_mu,1) + S_(r,2)·S_(r+e_mu,2)].

There are 2L² spins, L² rungs, and periodic positive-direction edges counted with multiplicity. Thus L=2 has parallel bonds. Claims cover all integer square L≥2, including odd L. They do not assert arbitrary rectangular aspect ratios. H′=H+3L²/4. For rectangular N-rung seeds H′=H+3N/4. Energy shifts do not change the gap. N16/N32/N64 denote 16/32/64 rungs, hence 32/64/128 physical spins and full Hilbert dimensions 2^32/2^64/2^128.

Uniform spin-1 chain uses unit nearest-neighbor antiferromagnetic exchange and periodic boundaries. Alternating-chain Hamiltonian is sum_(j=1)^M [S_(2j−1)·S_(2j)+g S_(2j)·S_(2j+1)], with 2M spin-1 sites, M≥2, strong exchange 1, H′=H+2M. Its g=1 point is uniform. Its g=.2/.225 certificates are not uniform-chain certificates. Fully frustrated bilayer results involve crossed bonds and must remain separate from ordinary bilayer.

## Historical results by stage

The positive ordinary-bilayer results below use the Hamiltonian and boundary convention above and include a unique ground state for every integer square side L≥2. Acceptance refers to the recovered historical reviews.

| Stage | Recorded result | Evidence and scope |
|---|---|---|
| 23 | Uniform spin-1 gap .0248 for all integer L≥2. Ordinary bilayer bounds .004499695659 on [0,.108] and .000586405978 on [0,.10825]. Near-uniform alternating-chain intervals. | The uniform result joins analytic L2/L3 anchors, strengthened L4–25 certificates, finite exact L26–33 certificates and the n34 tail. The n30, n32 and n34 initializations give .0179, .0245 and .0248. Coverage from L=2 does not imply a seed of size 2 or a minimum-seed theorem. The Stage23 Krylov/exporter work had not yet produced a new g=.11 gap. |
| 24 | At g=.11, gap .000131518777, with .000094038987 from an alternative route. | The exact endpoint is joined to 25 finite windows, 2 tails and an L2–7 bridge. The complete N32 m0–m4 export has 2,945 chunks of 24 signed fields, with independently reassembled G/K/J. Checks cover six independent small-system fixtures and 19 same-kernel large-system samples. No second independent complete N32 contraction was recorded. |
| 25 | Gap .0001 on [0,.11]. | The new [.10825,.11] bridge has 14 closed pieces, giving 102 pieces in the combined interval. Earlier stronger subinterval and .11-point bounds are preserved. The certificate covers the whole interval without endpoint interpolation. |
| 26 | No new positive gap. | Exact exclusions cover g=.1105/.111/.112/.115 at β=10, target 10^-6, at most 24 square cycles, and the fixed 2D-denominator/57D-numerator construction. They do not establish physical gap closure, an all-temperature obstruction or a minimum dimension. |
| 27 | Gap .004499695659 on [0,.112] and .01 on [.108,.112]. | The stronger interval uses 118 pieces. An implicit filtered state extends beyond the old 57D family and uses a rigorous variance lower bound. The argument does not substitute an exact variance or a physical norm. It retains one numerator state, with each filter plane at most 2D and the enlarged family at most 58D. |
| 28 | No new positive gap. | Mixed-X and robust-3D diagnostics cover finite temperature and parameter ranges. X remains unknown. The robust upper bound uses a fixed worst completion rather than the actual physical 3D optimum. Failures of selected lower-bound paths do not exclude all temperatures or trial families. |
| 29 | Gap .004499695659 on [0,.115] and .01 on [.108,.115]. | The joins have 142/56 pieces. The complete N64 H² was accepted after seven exact blocks matched independently. Signed q8 contributions were retained algebraically without enumerating q8. This stage's positive Jlo bridge does not use the newly computed full H². |
| 30 | Gap .004499695659 on [0,.116], .005 on [.108,.116], and .01 at isolated g=.116. | The joins have 150/64 pieces. The new 8-piece bridge uses 46 windows, 8 tails and the accepted complete N64 H². Parity/r3 and restricted-family diagnostics add no gap at .12/.125/.13. |
| 31 | No new positive gap. | At g=.118, exact conditional targets and exclusions concern the fixed scheme. A 58D augmented denominator improves the bounds, but the fixed-numerator, β=10 scheme remains obstructed. The result is not a general impossibility theorem. |
| 32 | Gap 1/200 at isolated g=.118. | The complete physical variance for the 16-column preparation includes q8. The preparation is embedded in 21 mixed-q columns. An independent actual replay at β=10 covers 6 windows, a tail from 256 and L2–7. The initial conditional-monotonic transfer and subsequent actual replay are separate results. No continuous extension was established at this stage. |
| 33 | Gap .004499695659 on [0,.118] and .005 on [.108,.118]. | The new [.116,.118] bridge has 16 closed leaves, 83 finite windows, 16 tails and L2–7 coverage. The combined intervals have 166/80 pieces. Thirteen tails start at 128 and three at 256. Exact endpoint matching and within-leaf bounds establish the interval result without interpolation from isolated points. |
| 34 | No new gap at .12. | Improved physical bounds include 48 odd low states and a conditional H³/Ritz target. Four β=10 lower-bound paths are exhausted at 32. The latest sufficient numerator gain is 7869587/26843545600, and the necessary gain is strictly greater than 15739173/53687091200. These targets establish neither attainability nor a measured H³. |
| 35 | Pilot controls and samples only. | N64 samples cover 32 q4 and 128 q6 supports out of the complete 39,711/7,028,847. The N32 old-norm comparison covers 16/129 samples. A selected-vector 4×2 matrix check does not accept the entire 16D matrix independently. No full H³, Ritz or gap result was established. |
| 36 | Scientific calibration controls accepted, resource forecast rejected. | The checks cover 305 sample targets, 8 signed fields, 6 controls and 37,800 local checks. Ten jobs pass, but forecasts exceed the 13k/26k budgets. The status is FAILED_NO_RETRY, with no full N64 H³. |
| 37 | The first full-native attempt failed its resource requirements. A separate control diagnosis was accepted. | The partial q4[0,12288) log was not accepted. There is no q6, checker or full H³ result. Control112 passed seven phases and 20 descendants, but the recorder's terminal CPU usage is unknown. No new gap was established. |
| 38 frozen | Complete native fields accepted. Scalar assembly failed twice. | All 39,711 q4 and 7,028,847 q6 origins, 440 chunks, 8 signed fields and 6 controls agree between the native implementations. The first assembly raised MemoryError before a worker started. The second failed an H² assertion because the default right vector was wrong. Corrected source was accepted but had not been launched at the frozen cutoff, so no scalar or Ritz result was yet available. |
| Post38 handoff | Complete fixed-preparation H³ and Ritz results accepted. | Assembly 75748 received scientific acceptance and a qualified resource review. The .12 bootstrap remains SOURCE_ONLY/NOTRUN, without a new gap. The handoff summary reviewed here does not give the exact scalar values. |

## Dimensions and certificate assumptions

Stage33 preparations 16/58/57 correspond to full spaces 2^32/2^64/2^128, with preparation dimensions distinct from the full Hilbert dimensions. The N16 ground-state variance is complete and exact. N32 uses a conservative complete second-moment upper bound with q10 diagonal terms retained, not an exact full H² matrix. N64 H²/sector data are accepted full physical quantities for the fixed preparation. Retained thermal counts 49/97/1 are distinct from preparation dimensions. 49/97 equal one even ground contribution plus 3N odd levels and need not be the first globally ordered 49/97 levels. MPS bond dimension 26 belongs to the uniform-chain representation and is not a bilayer linear dimension.

Finite-temperature floating searches/failed grids are diagnostics only. Exact rational/interval/PSD certificate claims require their full physical-input, missing-spectrum/tail, finite-window and large-size bridge premises. Low variational residual alone does not establish the full gap. Historical scientific acceptance does not erase FAILED_ACCOUNTING_TERMINAL, missing receipts, unknown tails or worker overruns.

## Available files and missing dependencies

Direct main-branch reads on 2026-10-14 returned NOT_FOUND for:

- `research_20261010/overview_stage24/README.md`
- `research_20261010/overview_stage33/README.md`
- `research_20261010/overview_stage38/README.md`
- `research_20261010/bilayer_g011_krylov_all_size_review_c12/PROOF.md`
- `research_20261010/bilayer_filtered_backward_bridge_review24/PROOF.md`
- `research_20261010/bilayer_sharp_filter_continuous_review_completion/PROOF.md`
- `research_20261010/bilayer_haldane_poststage38_pause_handoff/PAUSED_HANDOFF.md`

This establishes missing original paths, not proof that their bytes are absent from all unidentified recovered objects. The recovery index records 700 confirmed project blobs. The relevant final-snapshot subset contained 693 objects, but its exact mapping was lost. The 92 known-path metadata records correspond to 90 confirmed uploaded objects. The original queue of 6,617 text files across 532 batches is historical and does not give the current missing-file count. The transport manifests and catalogs remain incompletely recovered. Materializer source alone does not provide a runnable reconstruction.

The Stage33 overview PDF was subsequently recovered through an explicit base64 file read. Its 23,854 bytes match Git blob SHA1 `83892297f52130ffcafce07314e5e72af2211c21` and SHA256 `929ffb3feb1f598f33374c27cbfadd1374a418362d8d831f39f9c4831f7faa7e`. The extracted text corroborates the interval claims, 166/80-piece joins, 16 leaves of width 1/8000, 83 finite windows, 16 tails and L2–7 bridge. The PDF is an overview, so the underlying proof dependencies remain incomplete. The [retrieval addendum](recovery_followup/BASE64_RETRIEVAL_ADDENDUM.md) and [verification record](recovery_followup/PDF_VERIFICATION.json) document this correction. Other mapped PDFs cover Stage24–38. SOURCE_PINS and inventories identify dependencies without establishing that all their bytes are available.

The two available local archival ZIPs contain 1150 and 60 members respectively and no `research_20261010` or Stage23–38 paths. They do not supply the later missing proofs. No ZIP extraction or full mathematical reexecution was needed.

## Remaining recovery work

The recovered README and status support reporting the historical Stage23–38 results separately from the baseline certificates. Missing original paths remain recovery targets. The 700 recovered blobs do not establish a complete release, and no g=.12 gap certificate is recorded. Post38 cumulative retained charge 75,748 plus historical pilot 240 is distinct from assembly measured components 3.033131 CPU seconds with unknown coordinator terminal tail.

A self-contained Stage23–38 reproduction still needs the missing proofs, CSVs, exact inputs, manifests and review receipts. Their hashes and complete dependencies must be checked before rerunning the certificates.
