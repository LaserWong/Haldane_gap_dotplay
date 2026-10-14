# Exact m4 local fixture

The exact sparse physical comparison for 4×2 and 5×2 was completed and frozen 2026-10-11 00:23 UTC / 2026-10-10 20:23 EDT. See PROOF.md for normalization, all terms, bounds and limitations. The producer output is preserved. Independent review was pending at this freeze. The calculation does not include a full-size contraction or establish a new gap.

Run `bash REPRODUCE.sh /absolute/path/to/new-output-directory` only with an approved small-fixture budget. It compiles separately and does not overwrite frozen output. `MANIFEST_SHA256.json` seals source, executable, outputs and documentation. `INPUT_SHA256.json` pins the previously accepted plan/review. This exported working tree has no .git metadata, so no new commit is asserted.

