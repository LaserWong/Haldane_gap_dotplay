# Uniform spin-1 proof guide

Start with [the complete proof guide](PROOF_GUIDE.md). It states and derives the accepted finite-periodic result, explains the physical and signed-transfer calculations, and compares the result with the original `openai/math` theorem without changing its attribution.

Accepted scientific result at this checkpoint: unit-bilinear untwisted periodic spin-1 Heisenberg chains have a unique ground state and gap at least **31/1250 = 0.0248 for every integer L >= 2**, with the doubled-bond convention at L = 2.

The strong infinite tail uses canonical initialization n = 34 and a 68-site physical trial. A separate n = 30 initialization is certified at 0.0179. Finite coverage down to 2 is not initialization at 2. No minimum-seed, optimal-gap or infinite-volume uniqueness statement is made.

## Contents

- [PROOF_GUIDE.md](PROOF_GUIDE.md): end-to-end mathematical explanation, source references, original-paper comparison and a concise summary
- [DEPENDENCY_MAP.md](DEPENDENCY_MAP.md): proof inputs, scopes and exact accepted-manifest identities
- [EXACT_DATA.json](EXACT_DATA.json): source-preserving extraction of thermal totals, refined signed intervals, rational filters and majorants, physical trial quotients, finite purities and bootstrap states
- [SOURCE_PINS.json](SOURCE_PINS.json): consumed-file SHA-256 identities, original source Git blobs and upstream links
- [build_data.py](build_data.py): read-only extraction from pinned sources, writing only the two data files in this new directory
- [selfcheck.py](selfcheck.py): standard-library exact scalar/data consistency replay, bounded by 60 CPU seconds and 256 MiB address space
- [SELF_CHECK.json](SELF_CHECK.json): observed self-check outcome

## Verification status

The underlying all-size result was independently accepted in `../uniform_gap_0248_all_sizes_review`, manifest `5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf`.

This guide is a new explanatory deliverable. Its own independent review is pending at sealing. Its consistency checker does not count as an independent review and does not repeat the physical heat or MPS computations. Historical conditional records and the mathematically accepted length-25 result's unresolved resource-compliance anomaly are explicitly preserved.

The first guide self-check also recorded 30.21035921 process CPU seconds against its own declared 30-second limit. Its exact script and JSON output are preserved in `history/`. Strict measured 30-second compliance is not accepted, and the cause was not diagnosed. This new guide-specific event is separate from the historical length-25 exception and from the accepted all-size scientific theorem. A subsequent scalar replay uses an explicitly revised 60-second limit. It does not erase the first record.

## Reproduction

Run `python selfcheck.py` from this directory. It reads pinned sibling evidence and writes only `SELF_CHECK.json` here. To preserve the sealed file set, replay in a disposable copy with the same relative evidence layout. `build_data.py` is only needed to regenerate the data extraction and will replace `EXACT_DATA.json` and `SOURCE_PINS.json` in the copy.

No physical kernel, MPS contraction, optimization, network call, GitHub write or modification of a previously sealed artifact is performed by this package. The repository checkout used for writing this guide is an extracted tree without Git metadata.
