# Latest recoverable Haldane project checkpoint

Research is PAUSED. This is an additive recovery archive, not a complete Stage38 source release. Existing main scientific files are preserved.

## Human-readable entry points

- [Latest recovered README](latest_recovered_roots/README.md), [CURRENT_STATUS](latest_recovered_roots/CURRENT_STATUS.json), [PLAN](latest_recovered_roots/research_20261010/PLAN.md), and [pause record](latest_recovered_roots/PAUSED_20261012_PUBLICATION.json). The triplet was fetched from confirmed uploaded UTF-8 blobs; the pause record was reconstructed from its embedded copy and matched its frozen SHA256.
- [Known original paths](KNOWN_BLOB_PATHS.json):92 metadata records;90 corresponding objects were confirmed uploaded. A listed path is not evidence that all its dependencies are present.
- [Object provenance](OBJECT_PROVENANCE.json) and [upload ledgers](RECOVERED_UPLOAD_LEDGERS.json):700 unique confirmed Git blobs, stored as `objects/<GitSHA>.blob` with documentary mode100644. These are exact raw bytes; original file types/modes/paths must be restored only when their metadata is known.
- [Exact recovered materializer source](reconstructed/materialize.py) and [recovery receipt](reconstructed/MATERIALIZER_RECOVERY_RECEIPT.json). The companion complete transport manifest and catalogs are not all locally reconstructed, so this is not claimed as a complete runnable package.
- [Baseline Stage22 README](baseline_stage22_roots/README.md), [status](baseline_stage22_roots/CURRENT_STATUS.json), and [plan](baseline_stage22_roots/research_20261010/PLAN.md).

## Completeness statement

The original publication inventory had13,967 changed paths and7,310 unique new contents.693 uploaded objects were relevant to that final snapshot; all700 confirmed uploaded project objects are preserved here because the exact693 subset map was lost. The extra7 are historical/superseded project contents, not unrelated files.

The original unuploaded ordinary-text count was6,617 across532 batches. Some small records have since been recovered exactly, so6,617 is not an audited current missing-file count. No claim is made that all Stage23–38 source files, original paths, or scientific reproduction dependencies have been recovered. The original inventory SHA256 is87133c39de8f30526cea4d50138599c1db2d21e36a97640125241b48debe6a07; original paused-root receipt SHA256 isb7f52d87aebc5fd37635e3168ef9c2ad7d6dc671b9734e39c40cd50b2722ce49.

The g=.12 bootstrap replay was not run; no new .12 gap certificate is asserted. No new research is started by this archive or its scripts.
