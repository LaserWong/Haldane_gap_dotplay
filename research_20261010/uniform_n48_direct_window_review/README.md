# Independent review of the direct n48 finite window

Updated 2026-10-10 23:17 UTC / 2026-10-10 19:17 America/New_York.
Status: ACCEPTED and sealed. The review establishes gap 53/10000 for every integer length 48–96 and the composed gap 19/5000 for every integer L≥48, with a unique ground state. The bootstrap initialization remains 52.

REVIEW.md gives the proof, inherited assumptions and scope. CLAIM_VERDICTS.json and results.json contain machine-readable results. independent_check.py reconstructs exact bounds from sealed sibling evidence, while adversarial_tests.py tests guards and boundary failures. INPUT_SHA256.json pins every read dependency. MANIFEST_SHA256.json seals this directory except for itself. Original files remain unchanged.

Replay python independent_check.py followed by python adversarial_tests.py from this directory. The scripts write results and input digests locally, and their resource-timing fields vary. Use a disposable copy to preserve the frozen seal. Required sibling dependencies are listed in results.json/seals_verified. No external service or contraction is used. The working snapshot has no Git metadata, and source blobs are pinned through the accepted source-scope review. The remaining action is to incorporate this scoped acceptance into an authorized publication. No further computation is required here.
