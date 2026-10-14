# Exact Stage 11 evidence

This package stores the large Stage 11 evidence files without loss. The scientific producer and independent-review manifests retain their original hashes and filenames. No original evidence is discarded or altered.

From a fresh repository checkout, run this command before source-manifest checks or scientific replay:

```sh
python3 reproducibility/stage11_exact_evidence/materialize.py --repo-root .
```

Python 3.9 or newer and its standard library are sufficient. No network, credentials, extra package, or additional download is used. Restoration needs about 362 MB for the 18 exact target files, plus up to about 96 MB of temporary disk space. The implementation streams bounded chunks instead of retaining a large cache in RAM.

The mapping is `MANIFEST.json`. It preserves 18 original paths using nine unique raw contents. Their combined original size is 361,508,926 bytes. Deduplicated deterministic gzip streams occupy 67,012,477 bytes in 21 content-addressed transport parts. Each part is at most 4 MiB. The threshold is 1 MiB and applies only to new paths. Existing remote files are unchanged.

For each content object, the materializer checks every part's byte count and SHA-256, the reconstructed gzip stream's byte count and SHA-256, and the decompressed file's exact byte count and SHA-256. Only then does it atomically create each original path. Existing matching files are retained. Existing differing files or symlinks cause an error, never an overwrite. Producer and review copies are restored separately with their original modes.

The 68,118,456-byte fused-current `cells.txt` is included once in compressed form and restored at both its producer and review paths. Its raw SHA-256 is `822810ccc816dd225718dc52dc4adfdf491a95d68457ca84a7ab183cabc38f9e`.

After restoration, every prior raw-content verification command can run unchanged. To check the materialized files and transport integrity without creating missing files:

```sh
python3 reproducibility/stage11_exact_evidence/materialize.py --repo-root . --verify-only
```

For a clean-checkout restoration, original-seal replay, idempotence, and corruption-guard test:

```sh
python3 reproducibility/stage11_exact_evidence/selftest.py --repo-root .
```

The `.gzpart` files are ordered pieces of one gzip stream per unique raw object, not independent gzip members. Their order and hashes are specified in `MANIFEST.json`. This packaging is a transport/storage choice, with no change to any mathematical claim, numerical certificate, or raw source seal.
