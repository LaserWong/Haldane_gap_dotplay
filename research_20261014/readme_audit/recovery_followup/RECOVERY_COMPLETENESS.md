# Stage32/33 and post38 recovery status

The remote records were inspected on 2026-10-14 without scientific replay or remote changes.

## Recovered files

Six exact original JSON files were recovered from reachable Git objects. Byte length, SHA256 and Git blob SHA1 were verified against known original metadata. `EXACT_RECOVERED_FILES.json` maps each original repository path to its already-present repository object. They are the post38 scientific SOURCE_PINS, three resource-review inventories/hash bindings, DOCUMENTARY_CHECKS, and EXTERNAL_HISTORY_SOURCE_MAP. These records establish provenance. The underlying proofs and scalar-output files are still needed.

The direct inventory contains no mapped Stage32/33 certificate proof or actual replay output. The mapped Stage32/33/38 PDFs are overviews. The key post38 assembly results have path, byte length and SHA256 metadata, but no equal-sized candidate among the 700 listed reachable objects, after using both ledger sizes and known-path sizes. Consequently their exact standalone bytes could not be recovered from this known-object inventory.

This does not exclude their presence inside an unresolved compressed transport object. The known inventory does not establish a complete path-to-transport-member mapping. Their presence elsewhere remains unresolved.

## Verified identities

See `EXACT_RECOVERED_FILES.json` for all six exact byte identities. Original paths are:

- `research_20261010/bilayer_numerator64_h3_assembly75748_scientific_receipt_review/SOURCE_PINS.json`
- `research_20261010/bilayer_numerator64_h3_assembly75748_resource_review/bindings/TARGET_INVENTORY_BEFORE_AFTER.json`
- `research_20261010/bilayer_numerator64_h3_assembly75748_resource_review/bindings/INITIAL_TARGET_INVENTORY.json`
- `research_20261010/bilayer_numerator64_h3_assembly75748_resource_review/bindings/HASH_BINDINGS.json`
- `research_20261010/bilayer_numerator64_h3_assembly75748_resource_review/bindings/DOCUMENTARY_CHECKS.json`
- `reproducibility/current_complete_transport/EXTERNAL_HISTORY_SOURCE_MAP.json`

The originals were recovered and verified locally. The mapping references existing repository objects rather than duplicating their bytes. Those exact originals preserve historical absolute paths and all source bytes. The mapping reports use repository-relative paths. SOURCE_PINS and inventory records corroborate expected dependencies. A documentary PASS only reports the earlier review, not a fresh replay of those dependencies.

## Missing proofs

Direct current-main reads returned NOT_FOUND for:

- `research_20261010/bilayer_g0116_0118_fixed_improved_bridge_review60/PROOF.md` (Stage33 entire-real-interval bridge)
- `research_20261010/bilayer_g0118_improved_actual_replay_review12/PROOF.md` (Stage32 actual isolated-point replay)

Neither appears as a direct original-path entry in KNOWN_BLOB_PATHS. The recovered status supplies their accepted historical summaries and seals but not full proof-file bytes. Thus ordinary-bilayer [0,.118] cannot yet be upgraded to a currently fully reconstructed certificate chain.

## Missing result files

`KEY_RESULT_PATH_MAP.json` lists eight relevant file paths, expected SHA256 values and sizes, each with no direct equal-size object candidate. In particular:

- assembly receipt: 5,242 bytes, SHA256 `e955ab8d5756c7c5499939e2cda63ea91858aba2705ab15668211086bf828ae0`
- cached comparison: 6,621 bytes, SHA256 `7838aa1e7433819c3a14aa5cb601232edd748be636f8f6363a8789896ac8453f`
- producer scalar/Ritz assembly: 32,559 bytes, SHA256 `2c14f34c74d9d662f7aad852cb356b958f655878e9eb3aea5a218b8f5c185d87`
- distinct algebra review: 14,114 bytes, SHA256 `52e39df84dd67fb3d0cf95e92e635fef5d22fca739c7c67294ac2925939c4df6`

Duplicate state/receipt paths have the same expected hashes. A hash alone cannot reconstruct their bytes, and an arbitrary reserialization of a summary would not be exact recovery.

## Overview PDFs and compressed catalog

`KNOWN_HIGH_IMPACT_PATH_MAP.json` includes the three directly mapped overview PDFs and five post38 metadata files. A subsequent explicit base64 file read successfully recovered the Stage33 PDF and verified its exact size, SHA256 and Git blob SHA1. Its extracted text corroborates the historical interval summary. The full proof remains missing. See `BASE64_RETRIEVAL_ADDENDUM.md` and `PDF_VERIFICATION.json`.

The larger compressed path catalog still returns empty content from the explicit-base64 file route. The blob route fails UTF-8 decoding, and a final generic fetch rejects the binary content rather than exposing raw API JSON. Thus the remaining blocker is large compressed-catalog retrieval via these connector representations, not binary files generally.

## Search coverage and remaining work

The search covered all 92 known original-path metadata records, the 700-object provenance inventory, upload ledgers, 599 external-history source-map entries, and the recovered post38 inventory/hash metadata. Direct proof/result mappings were not found. Further reconstruction requires the bytes of `SNAPSHOT_NORMAL_PATHS.jsonl.gz` and the transport catalogs, followed by a completeness check before member extraction. Those steps remain unfinished, so a complete transport package has not been established.
