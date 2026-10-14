# Independent joint-ratio and chain review

Updated 10 October 2026, 15:23 EDT / 19:23 UTC.

The reusable joint-ratio scalar lemma and its sealed implementation pass
independent analytic and exact-arithmetic review. See `GENERAL_LEMMA.md` and
`LEMMA_ACCEPTANCE.json`. The stable seal is `LEMMA_REVIEW_MANIFEST.json`.

The full frozen chain extension also passes independent physical, scalar and
all-integer bridge review. For every integer periodic cell count M>=2, with a
unique finite-volume ground state, the spin-one alternating chain has the following gap lower bounds.

- g=.175: at least .026579108896
- g=.18: at least .013222512347
- g=.181: at least .009728769181
- g=.182: at least .005940278341

See `CHAIN_REVIEW.md`, `results/chain_summary.json`, and the separate
`CHAIN_REVIEW_MANIFEST.json`. All 54 saved paths and 285 finite windows were
checked. These sufficient certificates apply at the listed discrete couplings. They do
not establish a continuous interval or a maximal coupling.

Run `bash REPRODUCE_LEMMA.sh` or `bash REPRODUCE_CHAIN.sh` for the separate audit.
Each script pins one CPU and a 1 GiB address-space limit. Frozen producer inputs
are preserved. The audit writes only this review's outputs. Replay updates
diagnostic timing bytes, so preserve a sealed copy if needed.

No new .09 or .10 bilayer coupling certificate is asserted here. The separate
continuous-bilayer application review uses the accepted general lemma with its
own physical-input and finite-window gates.
