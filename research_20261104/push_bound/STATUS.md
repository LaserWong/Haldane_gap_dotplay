# Task B: push the certified uniform gap lower bound (all L >= 2)

All numbers are exact rationals. "CERTIFIED" means the checker ACCEPTED: the scalar checker first, then the ORIGINAL all-sizes `audit.py` for all L>=2.
Producers (`produce_fast.py`, `chain_scan.py`) are untrusted search tools. Only checker acceptance counts.

## Best certified results
| Logic | Gap | W | Grid B | Scalar checker | Scalar check CPU | Folder |
|---|---|---|---|---|---|---|
| ORIGINAL, strictly unmodified resource limits (60 s CPU cap) | **250023/10000000 = 0.0250023** | 15 | 10^3016 | original audit_scalar.py via run_orig_logic.py | 18.7 s | certs/orig_W15 |
| ORIGINAL, CPU cap 60 -> 590 s (resource-only substitution) | 50009/2000000 = 0.0250045 | 16 | 10^5632 | run_orig_logic_cpu.py | 74 s | certs/orig_W16 |
| **ORIGINAL, CPU cap 60 -> 590 s (resource-only substitution)** | **250057/10000000 = 0.0250057** | 17 | 10^10000 | run_orig_logic_cpu.py | 330 s | certs/orig_W17 |
| FULL (patched seal12 checker) | 126049/5000000 = 0.0252098 | 15 | 10^3016 | run_patched.py | ~78 s wall | certs/full_W15 |
| FULL | 252121/10000000 = 0.0252121 | 16 | 10^5632 | run_patched.py | 85 s | certs/full_W16 |
| **FULL** | **63033/2500000 = 0.0252132** | 17 | 10^10000 | run_patched.py | 353 s | certs/full_W17 |

Each row's gap is the largest that passes on a 1e-7 grid at that W; the next grid point fails (asymptotic closure).
Previous values were 1/40 (original logic) and 0.025179 (FULL).

## The CPU-limit substitution (labelled, not hidden)
- The original `audit_scalar.py` sets `RLIMIT_CPU=(60,60)`. At W>=16 it was SIGKILLed at 60 s (`certs/orig_W16/2_scalar_check_ORIGINAL_cpu60_KILLED.log`).
- `run_orig_logic_cpu.py` is `watertight/auditor/run_orig_logic.py` plus ONE count-asserted substitution: that limit becomes CPU_LIMIT=590.
- No arithmetic or acceptance line changes. The 256 MB address-space cap is kept.
- If you want zero source changes beyond the earlier file name / affinity / grid substitutions, the best ORIGINAL result is 0.0250023 (W=15).

## Producer speedup (untrusted side only)
- `produce_fast.py` swaps the checker's binary-search q-th root for a Newton integer root that gives the same floor.
- It also bisects ell on a coarse grid, then re-asserts the forcing at the full grid.
- Its W=16 certificate is byte-identical (JSON-equal) to the slow producer's.

## Commands (run from runs/watertight/auditor)
ORIGINAL W=17:
  env -u AUDIT_FULL_R68 AUDIT_DIGITS=10000 W=17 GAP_LO=50009/2000000 GAP_HI=2501/100000 RES=1/10000000 AUDIT_CERT=certificate_orig_W17.json python3 ../../push_bound/produce_fast.py
  ../../push_bound/check_only.sh ORIG orig_W17 250057/10000000 10000
  (= CPU_LIMIT=590 DIGITS=10000 python3 run_orig_logic_cpu.py scalar orig_W17 ; produce_allsizes_orig.py ; run_orig_logic.py allsizes orig_W17 250057/10000000)
FULL W=17:
  AUDIT_FULL_R68=1 AUDIT_DIGITS=10000 W=17 GAP_LO=252121/10000000 GAP_HI=25222/1000000 RES=1/10000000 AUDIT_CERT=certificate_full_W17.json python3 ../../push_bound/produce_fast.py
  ../../push_bound/check_only.sh FULL full_W17 63033/2500000 10000
W=15/16: certify.sh MODE TAG GAP W DIGITS (slow producer + checkers).
Runtimes:
- W=17 producer: 11 s (ORIG) / 18 s (FULL).
- W=17 checker: 330 s CPU (ORIG) / 353 s CPU (FULL, 453 s wall).
- all-sizes audit: about 3 s.

## Not done / limits
- W=18: the producer finds ORIG 125031/5000000 = 0.0250062 and FULL 126069/5000000 = 0.0252138 (certs/*_W18/1_producer.log, 19500 digits). These are **NOT CERTIFIED**.
  - The checker would need about 1400 s CPU, extrapolated from its d^2.2 scaling.
  - The box kills any process after about 600 s CPU ("CPU Watchdog Timeout (hard)" in dmesg). That also killed the first-pass scans in scan/*_W17-19.
  - Making the checker itself faster would change checker code, so I did not do it.
- Ceiling extrapolation (ESTIMATE from the W=15..18 sequence, not a proof): about 0.0250067 (ORIGINAL) and about 0.0252144 (FULL). Further gains are at most about 1e-6.
