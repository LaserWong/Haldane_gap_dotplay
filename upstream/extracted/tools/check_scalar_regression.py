#!/usr/bin/env python3
"""Compare the new generic scalar engine against three existing exact records."""
from fractions import Fraction as F
import json
from pathlib import Path
from bootstrap_scalar import replay

ROOT = Path(__file__).resolve().parents[1]
checks = []
for name, filename, expected in [
    ("blbq_eta_m005", "order12_success_certificate.json", "accepted_conditional_scalar_seed"),
    ("blbq_eta_m01", "order12_partial_certificate.json", "unusable_thermal_bound"),
    ("blbq_eta_m08", "order12_partial_certificate.json", "unusable_spatial_bound"),
]:
    cert = json.loads((ROOT/"cases"/name/"moments"/filename).read_text())
    seed, saved = cert["seed"], cert["bootstrap"]
    actual = replay(seed["S_lower"], seed["T_lower"], seed["n"], seed["beta"])
    assert actual["status"] == expected
    if name == "blbq_eta_m005":
        assert actual["rounds"] == saved["rounds"] == 6
        assert actual["conditional_gap_lower_rational"] == saved["uniform_gap_lower_rational"]
        assert actual["final_n"] == 3840 and F(actual["final_beta"]) == 1440
    if name == "blbq_eta_m08":
        assert F(actual["attempted_p_upper"]) == F(saved["p"])
    for a, b in zip(actual["updates"], saved["updates"]):
        assert a["p_upper"] == b["p_upper"] and a["q_upper"] == b["q_upper"]
    assert len(actual["updates"]) == len(saved["updates"])
    checks.append({"case": name, "status": "PASS", "scalar_outcome": expected})
assert replay("7/8", "7/8", 60, "20")["status"] == "accepted_conditional_scalar_seed"
for values in [("1.1", "0.9", 60, "1"), ("0.9", "0.9", 3, "1"),
               ("0.9", "0.9", 60, "0"), (0.9, "0.9", 60, "1")]:
    try:
        replay(*values)
    except ValueError:
        pass
    else:
        raise AssertionError(f"Invalid inputs accepted: {values}")
print(json.dumps({"status": "PASS", "checks": checks,
                  "symmetric_sufficient_seed": "PASS", "invalid_inputs_rejected": 4}, indent=2))
