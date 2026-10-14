# The October 12 recovery archive

This archive records the latest recoverable checkpoint at the October 12, 2026 pause. It adds recovered material while preserving the existing scientific files. It is not a complete Stage38 source release. The historical pause describes that checkpoint. The [current project status](../CURRENT_STATUS.json) records the subsequently authorized work.

## Recovered records

- The [later README](latest_recovered_roots/README.md), [status](latest_recovered_roots/CURRENT_STATUS.json), and [plan](latest_recovered_roots/research_20261010/PLAN.md) were retrieved from confirmed uploaded UTF-8 blobs. The [pause record](latest_recovered_roots/PAUSED_20261012_PUBLICATION.json) was reconstructed from its embedded copy and matched its frozen SHA-256.
- The [known-path inventory](KNOWN_BLOB_PATHS.json) contains 92 metadata records corresponding to 90 confirmed uploaded objects. A known path does not establish that all of its dependencies are available.
- The [object provenance](OBJECT_PROVENANCE.json) and [upload ledgers](RECOVERED_UPLOAD_LEDGERS.json) identify 700 unique confirmed Git blobs. Their exact bytes are stored as `objects/<GitSHA>.blob` with documentary mode `100644`. Original paths, file types, and modes can be restored only when their metadata is known.
- The [recovered materializer source](reconstructed/materialize.py) and [recovery receipt](reconstructed/MATERIALIZER_RECOVERY_RECEIPT.json) are available. The complete transport manifest and companion catalogs have not all been reconstructed, so these files do not yet form a complete executable recovery package.
- The surviving Stage22 baseline has its own [README](baseline_stage22_roots/README.md), [status](baseline_stage22_roots/CURRENT_STATUS.json), and [plan](baseline_stage22_roots/research_20261010/PLAN.md).

## What remains incomplete

The original publication inventory contained 13,967 changed paths and 7,310 distinct new contents. Of the uploaded objects, 693 belonged to the final snapshot. The archive retains all 700 confirmed project objects because the exact mapping of that 693-object subset was lost. The other seven objects contain historical or superseded project material.

The original upload plan left 6,617 ordinary-text files across 532 batches unuploaded. Some small records have since been recovered exactly. The historical count of 6,617 therefore does not measure the number still missing. The archive does not establish complete recovery of the Stage23–38 sources, original paths, or dependencies needed to reproduce the scientific results.

The original inventory has SHA-256 `87133c39de8f30526cea4d50138599c1db2d21e36a97640125241b48debe6a07`. The original paused-root receipt has SHA-256 `b7f52d87aebc5fd37635e3168ef9c2ad7d6dc671b9734e39c40cd50b2722ce49`.

The g=0.12 bootstrap replay had not run at this checkpoint, and the archive supplies no positive gap certificate at that coupling. Its files and scripts do not authorize new research. Later recovery findings and the current evidence boundary are summarized in the [progress record](../docs/PROGRESS.md).
