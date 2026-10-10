# Stage9 provenance and immutable scope

This extraction starts from the entire sealed stage8 dataset. All209 prior gap records are retained byte-equivalently as JSON values, and all56 interval pieces are copied byte-for-byte in their CSV. Existing alternatives,207 historical chain routes, reference AKLT and all prior diagnostic rows remain.

ACCEPTED_REVIEW_SEALS.json pins immutable manifests. overview_data.json records direct source SHA-256 values, exact fractions and JSON pointers; the verifier checks every pinned manifest entry and every extracted gap. New diagnostics preserve their exact verdict objects and enforce no-gap/no-startup typing. New sources are the chain_above02 independent review, longitudinal and momentum independent reviews, and the scoped g=.10 diagnostics review. Source integrity is not a fresh spectral-proof audit.

All work is confined to overview_stage9. The extracted project has no Git metadata; no branch or publication is inferred. No root files, prior sealed packages, or GitHub state are written. common.py uses one available CPU (CPU0 if available) and1GiB address space, with numerical libraries limited to one thread.

REPRODUCE.sh checks the final manifest, scientific scope invariants and corruption guards, rerenders all12 PNG/PDF figures in a temporary directory, compares bytes, and checks the final manifest again. Frozen files cannot be regenerated in place; use --output-dir for rendering. Pending mutable branches are not pinned as accepted scientific evidence.
