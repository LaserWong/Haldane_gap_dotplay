# Stage33 PDF retrieval and remaining catalog access

The Stage33 overview PDF was recovered on 2026-10-14 through a file read with explicit `encoding: base64`. This corrects the earlier report that binary repository files could not be retrieved.

The recovered file has 23,854 bytes, Git blob SHA1 `83892297f52130ffcafce07314e5e72af2211c21`, and SHA256 `929ffb3feb1f598f33374c27cbfadd1374a418362d8d831f39f9c4831f7faa7e`. All three match the known metadata.

Its original repository path is `research_20261010/overview_stage33/stage33_uniform_bridge.pdf`. The existing recovery object is `recovery_20261012/objects/83892297f52130ffcafce07314e5e72af2211c21.blob`. [PDF_VERIFICATION.json](PDF_VERIFICATION.json) records the byte checks and extracted text.

The text confirms the reported lower bound .004499695659 on [0,.118] over 166 pieces and .005 on [.108,.118] over 80 pieces. It also preserves .01 on [.108,.115] and at the isolated point .116. The new bridge has 16 leaves of width 1/8000, 83 finite windows, 16 infinite tails and the L2–7 short-size bridge. Thirteen tails start at 128 and three at 256. The figure retains the failure of the coarse whole-leaf lower bound at 64. These are historical summary statements in an overview figure. The full exact certificate and its missing dependencies were not recovered from this PDF.

## Compressed path catalog

The original catalog `reproducibility/current_complete_transport/SNAPSHOT_NORMAL_PATHS.jsonl.gz` maps to `recovery_20261012/objects/be98c1d71af5abe1dafdf67d75efdc920187ceff.blob`. Its expected size is 1,424,615 bytes and its expected SHA256 is `c78a8c32099c374af7860ab3aeaa08af98eb4cf70cfee5fc5dcc00b295a696c7`.

The explicit-base64 file read reported success, base64 encoding and the correct blob hash, but returned an empty content string. The explicit-base64 blob read still attempted UTF-8 decoding and failed on gzip byte `0x8b` at position 1. A final generic fetch of the Git blobs API representation returned HTTP 400 with the message `GitHub Fetch only accepts UTF-8 text`, rather than raw JSON containing base64 data.

No compressed bytes were obtained or decompressed through these routes. The remaining access problem concerns this large compressed catalog. No broader transport search, scientific recomputation or remote edit was performed in this recovery check. Stage32/33 proof and result reconstruction remains incomplete.
