# Stage23–38 recovered-claim audit, 2026-10-14

## Bottom line

The recovered documents record a strongest ordinary-bilayer continuous certificate of gap ≥ 0.004499695659 for every real g in [0,0.118], and gap ≥ 0.005 on [0.108,0.118], with a unique finite-volume ground state for every integer square side L≥2. They also preserve the stronger bound 0.01 on [0.108,0.115] and at the isolated point g=0.116. These are historical independently accepted exact-certificate claims, not newly reverified theorems in this audit. The present repository explicitly does not establish complete Stage23–38 source/evidence recovery.

The post-Stage38 handoff records accepted fixed-preparation H³ and Ritz results. The g=0.12 bootstrap replay remains SOURCE_ONLY/NOTRUN, with incomplete controls/entrypoint/admission and no new gap certificate. The older Stage38 frozen statement “no accepted H³ scalar/Ritz” is true at its earlier boundary; the later handoff supersedes that operational fact without modifying the frozen snapshot.

No research computation, compiler, scientific replay, or remote write was run for this audit. The user's new explicit resume governs current work; the October 12 pause and October 14 00:00 UTC deadline in historical files are not a newly imposed current stop instruction.

## Primary documentary evidence actually read

- `AGENTS.md`
- `CURRENT_STATUS.json` (current recovery wrapper)
- `research_20261010/PLAN.md` (current recovery wrapper)
- `recovery_20261012/README.md`
- `recovery_20261012/KNOWN_BLOB_PATHS.json`
- `recovery_20261012/latest_recovered_roots/README.md`
- `recovery_20261012/latest_recovered_roots/CURRENT_STATUS.json`
- `research_20261010/MODELS_AND_NORMALIZATION.md`

The recovered README has 132,695 bytes and SHA256 `e022c6e8aa6292a8c2b7c0e5f5ee0ab9ba24330d29af1e250fcf6602627240f8`; the recovered status has 1,151,776 bytes and SHA256 `234be47d8c379ae4a4ec3ba3a276eb56302bfe21bf439ae95fa4f2f6394533ad`. Both match the known-object metadata. The file API returned empty content for the large status file; the blob API supplied its full JSON. This is an API retrieval limitation, not an empty source file.

## Model and normalization

Ordinary square bilayer: spin 1/2, rung exchange 1, no crossed interlayer bonds or field,

H_L = sum_r S_(r,1)·S_(r,2) + g sum_(r,mu=x,y) [S_(r,1)·S_(r+e_mu,1) + S_(r,2)·S_(r+e_mu,2)].

There are 2L² spins, L² rungs, and periodic positive-direction edges counted with multiplicity. Thus L=2 has parallel bonds. Claims cover all integer square L≥2, including odd L; they do not assert arbitrary rectangular aspect ratios. H′=H+3L²/4; for rectangular N-rung seeds H′=H+3N/4. Energy shifts do not change the gap. N16/N32/N64 denote 16/32/64 rungs, hence 32/64/128 physical spins and full Hilbert dimensions 2^32/2^64/2^128.

Uniform spin-1 chain uses unit nearest-neighbor antiferromagnetic exchange and periodic boundaries. Alternating-chain Hamiltonian is sum_(j=1)^M [S_(2j−1)·S_(2j)+g S_(2j)·S_(2j+1)], with 2M spin-1 sites, M≥2, strong exchange 1, H′=H+2M. Its g=1 point is uniform; its g=.2/.225 certificates are not uniform-chain certificates. Completely frustrated bilayer results involve crossed bonds and must remain separate from ordinary bilayer.

## Stage-by-stage claim ledger

All ordinary-bilayer positive rows below have the Hamiltonian, boundary convention, uniqueness and all-integer-square-size scope stated above. “Accepted” below means explicitly recorded as accepted in recovered historical documents, not freshly reproduced here.

| Stage | Recorded mathematical progress | Evidence class / limits |
|---|---|---|
| 23 | Preserves uniform spin-1 gap .0248 for all integer L≥2; bilayer [0,.108]/.004499695659 and [0,.10825]/.000586405978; near-uniform alternating-chain intervals | Uniform result combines L2/L3 analytic anchors, L4–25 strengthened and L26–33 finite exact certificates, n34 tail. Initialization n30 gives .0179; n32 .0245; n34 .0248. Coverage onset 2 is not seed size 2 or minimum-seed proof. Stage23 Krylov/exporter work had no actual new g=.11 gap yet. |
| 24 | g=.11 gap .000131518777; alternate route .000094038987 | Actual exact endpoint + 25 finite windows, 2 tails, L2–7 bridge. Full N32 m0–m4 export: 2,945 chunks ×24 signed fields, independently reassembled G/K/J. Six independent small-system fixtures and 19 same-kernel large-system samples; no second independent complete N32 contraction. |
| 25 | [0,.11] gap .0001 | New [.10825,.11] bridge has 14 closed pieces; joined total102. Preserves stronger previous subintervals and .11 point. Whole-interval certificate, not endpoint interpolation. |
| 26 | No new positive gap | Exact exclusion only for specified g=.1105/.111/.112/.115, beta10, target10^-6, ≤24 square cycles, fixed 2D denominator/57D numerator recipe. No physical gap closure or all-temperature/minimum-dimension claim. |
| 27 | [0,.112] gap .004499695659; [.108,.112] gap .01 | 118-piece strong join. Implicit filtered state leaves old57D family; uses rigorous variance lower bound, not exact variance or physical norm substitution. One numerator retained state, individual filter plane ≤2D; enlarged family ≤58D. |
| 28 | No new positive gap | Mixed-X/robust3D and finite temperature/parameter diagnostics. Unknown X not exact; robust upper is a fixed worst-completion surrogate, not actual physical 3D optimum. Selected lower-path failures do not exclude all beta or trial families. |
| 29 | [0,.115] gap .004499695659; [.108,.115] gap .01 | 142/56 pieces. Complete N64 H² accepted, seven exact blocks independently matched, signed q8 retained algebraically without q8 enumeration. This stage's positive Jlo bridge does not use the newly computed full H². |
| 30 | [0,.116] gap .004499695659; [.108,.116] gap .005; isolated .116 gap .01 | 150/64 pieces; new bridge8 pieces,46 windows,8 tails, actually uses accepted complete N64 H². Parity/r3 and restricted-family diagnostics add no .12/.125/.13 gap. |
| 31 | No new positive gap | g=.118 fixed-scheme exact conditional targets/exclusions;58D augmented denominator improves bounds but fixed numerator/beta10 scheme remains obstructed. Not general impossibility. |
| 32 | Isolated g=.118 gap1/200 | Complete16 physical variance includes q8,16-column preparation embedded in21 mixed-q columns. Independent actual beta10 replay:6 windows,tail256,L2–7. Initial conditional-monotonic transfer and later actual replay are separate steps. No continuous extension yet. |
| 33 | [0,.118] gap .004499695659; [.108,.118] gap .005 | New [.116,.118] bridge16 closed leaves,83 finite windows,16 tails,L2–7.166/80-piece joins.13 tails start128,3 start256. Exact endpoint matching and within-leaf bounds; not isolated-point interpolation. |
| 34 | No new .12 gap | Improved physical bounds,48 odd low states, conditional H³/Ritz target. Four beta10 lower paths exhaust at32. Latest sufficient numerator gain7869587/26843545600; necessary gain strictly >15739173/53687091200. Conditional targets are not attainability or measured H³. |
| 35 | Pilot controls/samples only | N64 sample32 q4 and128 q6 supports, not complete39,711/7,028,847. N32 old norm comparison covers16/129 samples. Selected-vector4×2 matrix check is not whole16D independent matrix acceptance. No full H³/Ritz/gap. |
| 36 | Calibration scientific controls accepted, cost gate failed | 305 sample targets;8 signed fields+6 controls;37,800 local checks. Ten jobs pass but forecasts exceed13k/26k budgets; FAILED_NO_RETRY. No full N64 H³. |
| 37 | First full-native attempt resource failure, separate control diagnosis accepted | q4[0,12288) partial log unaccepted; no q6/checker/full H³. Control112 seven phases/20 descendants pass; recorder terminal CPU unknown. No new gap. |
| 38 frozen | Complete native fields accepted, scalar assembly initially failed twice | All39,711 q4 +7,028,847 q6 origins,440 chunks,8 signed fields,6 controls agree between native implementations. First assembly MemoryError before worker; second H² assertion from wrong default right-vector. Corrected source accepted, not launched at frozen boundary. No scalar/Ritz yet at that boundary. |
| Post38 handoff | Complete fixed-preparation H³ and Ritz accepted | Separate assembly75748, scientific and qualified resource reviews accepted. Bootstrap .12 remains source-only NOTRUN; no new gap. Exact scalar values are not reproduced in the handoff summary read here, so do not invent them. |

## Dimensional and certification cautions

Stage33 preparations16/58/57 correspond to full spaces2^32/2^64/2^128, not those full spaces' dimensions. Ground16 variance is complete/exact; ground32 uses a conservative complete second-moment upper bound with q10 diagonal terms retained, not an exact full H² matrix. N64 H²/sector data are accepted full physical quantities for the fixed preparation. Retained thermal counts49/97/1 are distinct from preparation dimensions;49/97 equal one even ground contribution plus3N odd levels and need not be the first globally ordered49/97 levels. MPS bond dimension26 belongs to the uniform-chain representation and is not a bilayer linear dimension.

Finite-temperature floating searches/failed grids are diagnostics only. Exact rational/interval/PSD certificate claims require their full physical-input, missing-spectrum/tail, finite-window and large-size bridge premises. Low variational residual alone does not establish the full gap. Historical scientific acceptance does not erase FAILED_ACCOUNTING_TERMINAL, missing receipts, unknown tails or worker overruns.

## Actual availability versus referenced-but-missing paths

Direct main-branch reads on2026-10-14 returned NOT_FOUND for:

- `research_20261010/overview_stage24/README.md`
- `research_20261010/overview_stage33/README.md`
- `research_20261010/overview_stage38/README.md`
- `research_20261010/bilayer_g011_krylov_all_size_review_c12/PROOF.md`
- `research_20261010/bilayer_filtered_backward_bridge_review24/PROOF.md`
- `research_20261010/bilayer_sharp_filter_continuous_review_completion/PROOF.md`
- `research_20261010/bilayer_haldane_poststage38_pause_handoff/PAUSED_HANDOFF.md`

This establishes missing original paths, not proof that their bytes are absent from all unidentified recovered objects. The recovery index states700 confirmed project blobs preserved, while the relevant final-snapshot subset was693 and its exact map was lost.92 known-path metadata records correspond to90 confirmed uploaded objects. Original pending text count6,617 across532 batches is historical, not the current missing-file count. Complete transport manifest/catalog recovery is not established; recovered materializer source alone is not a complete runnable reconstruction.

Known metadata maps the Stage33 overview PDF to `recovery_20261012/objects/83892297f52130ffcafce07314e5e72af2211c21.blob`. Its direct file read reached binary content but the UTF-8 decoder failed; its PDF contents have not been inspected in this audit. Other mapped PDFs cover Stage24–38 but summaries are not full proof dependencies. Large recovered SOURCE_PINS and inventories likewise document dependencies without establishing every dependency's availability.

The two available local archival ZIPs contain1150 and60 members respectively and no `research_20261010` or Stage23–38 paths. They do not supply the later missing proofs. No ZIP extraction or full mathematical reexecution was needed.

## Recommended README wording and next documentation step

Use a distinct section “历史记录中的 Stage23–38 进展（证据恢复不完整，尚未在当前仓库重新复核）”. Report the above scientific frontier there, anchored to the verified recovered README and status paths, while keeping baseline fully available results separate. Do not link unavailable original paths as if they open; list them explicitly as recovery targets. Do not label700 recovered blobs a complete release, declare .12 certified, or present old cost charges as measured CPU. Post38 cumulative retained charge75,748 plus historical pilot240 is distinct from assembly measured components3.033131 CPU seconds with unknown coordinator terminal tail.

For a genuinely self-contained Stage23–38 reproduction, next locate/map missing proofs, CSVs, exact inputs, manifests and review receipts; verify byte hashes and complete dependency closure; only then rerun bounded checks. Until then documentation can accurately preserve all historical result claims without falsely promoting them to freshly verified complete-repository certificates.
