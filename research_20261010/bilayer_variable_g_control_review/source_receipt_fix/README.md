# Receipt-binding source revision

Parent-authorized source-only patch. No producer numerical or metadata validation was run. This is not a passed production gate.

The base evidence is ../bilayer_incremental_control_gate, manifest SHA256 1bad844f7945081ddae5a86a2167ef40e2510ef49434678d422c588023ed6a1d. That package remains immutable. Original gate charged 27/30 with soft cap 27. Separately authorized continuation charged 10/10. Its FAILED_FINAL_VALIDATION.json retains the incomplete one-second attempt charged within the continuation's two-second supervisor/metadata reserve. No refund or remaining test authority is inferred.

Relative to the base, committed startup in engine.py now requires a complete accepted attempt, binds canonical payload SHA256 directly to attempt.output_sha256 as well as envelope/receipt hashes, and checks payload kind, integral id, exact planned range, and all 24 canonical signed integer strings. Adoption additionally rejects noncanonical normalized output bytes, making the output-byte and canonical-payload digest conventions identical. physical_session.py, session_supervisor.py and production_supervisor.py are byte-identical copies from base.

The copied physical dispatcher already includes the conservative full remaining-work wall forecast (all pending/retry worker allowances, ten seconds per worker, controller/session overhead, at least one day independent-review reserve), mandatory pins, new-format final normalization and accepted m0/m1/m2 gate. Physical runtime, address-space partition and full accepted controls remain unvalidated producer-side. No production launch is authorized.

The independent reviewer should test recomputed-envelope corruption, changed kind/range/noncanonical values/incomplete attempts, fresh 2945-record synthetic reconstruction, recovery/fault controls, and the separately authorized vacuum integration profile. No raw prior evidence is rebound to this revision.
