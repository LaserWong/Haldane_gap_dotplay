# g = 0.10 diagnostics independent review

2026-10-10 17:41 EDT / 21:41 UTC.

PASS: three rational weighted-polynomial ground lower improvements; endpoint-weighted degree-five class brackets; fixed 43D numerator bracket; independent conditional-grid replay. No g = 0.10 gap proof.

- `REVIEW.md`: proof, global-ground/even-sector separation, scope, diagnostic interpretation and adversarial tests
- `review_exact.py` / `exact_result.json`: independent geometry, M0…M5, rational witness, span and LDL replay
- `review_scan.py` / `scan_result.json`: independent bounded conditional sensitivity replay
- `REVIEW_STATUS.json`: machine-readable verdict
- `MANIFEST_SHA256.json`: review seal
- `REPRODUCE.sh`: read-only source replay to a fresh temporary directory

Source freeze: `64aef0cf10637f509afd325ab230f8a74a97775b961657d1c5962e6c61be04bb`.

The 8×4 denominator ground interval is the principal bottleneck in these bounded tests. Polynomial endpoint improvements alone still yield zero successful startup proposals. Neither finite-grid failure nor a fixed-space optimum is a universal no-go theorem.
