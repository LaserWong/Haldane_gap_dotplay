#!/usr/bin/env python3
"""Exact/outward scalar replay. This alone does NOT certify physical inputs.

Uses only Python's standard library; supply decimal/rational strings, not floats.
The optional gap is conditional on the analytic transfer, recursion and even-
length interpolation hypotheses described in docs/TECHNICAL_GUIDE.md.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def rational(value):
    if isinstance(value, float) or isinstance(value, bool):
        raise ValueError("Use a rational/decimal string or an integer, not a float/bool")
    return F(value)


def up(value, digits=12):
    scale = 10 ** digits
    return F(-((-value.numerator * scale) // value.denominator), scale)


def update(u):
    if not 0 <= u < 1:
        raise ValueError("Scalar update outside 0 <= u < 1")
    return u * u / (2 * (1 - u) ** 2)


def log_lower(value, terms=40):
    """Exact strict lower bound on log(value), value > 1, positive series."""
    if value <= 1:
        raise ValueError("log_lower requires value > 1")
    exponent = 0
    while value >= 2:
        value /= 2
        exponent += 1
    def unit(v):
        z = (v - 1) / (v + 1)
        return 2 * sum((z ** (2*j+1) / F(2*j+1) for j in range(terms)), F(0))
    return exponent * unit(F(2)) + unit(value)


def replay(S, T, n, beta, max_rounds=64, digits=12):
    S, T, beta = map(rational, (S, T, beta))
    if not 0 < S <= 1 or not 0 < T <= 1:
        raise ValueError("Purity lower bounds must be in (0,1]")
    if not isinstance(n, int) or isinstance(n, bool) or n < 2 or n % 2:
        raise ValueError("n must be a positive even integer >= 2")
    if beta <= 0 or not 0 <= max_rounds <= 256 or not 1 <= digits <= 30:
        raise ValueError("Invalid beta, max_rounds or outward precision")
    p, q = up(1-S, digits), up(1-T, digits)
    result = {"status": "not_in_small_defect_region", "physical_inputs_verified": False,
              "interpretation": "Scalar acceptance only; physical/analytic hypotheses require separate verification",
              "input": {"S_lower": str(S), "T_lower": str(T), "n": n, "beta": str(beta)},
              "rounding_decimal_digits": digits, "updates": []}
    for j in range(max_rounds + 1):
        if max(p, q) <= F(1, 100):
            u = max(p, q)
            result.update(status="accepted_conditional_scalar_seed", rounds=j,
                          final_n=n, final_beta=str(beta), final_p=str(p), final_q=str(q),
                          final_common_u=str(u))
            if u:
                assert 5*u < 1 and 5*(1-3*u) > 3
                lower = log_lower(1/(5*u)) / beta
                gap = F((lower * 10**12).__floor__(), 10**12)
                result["conditional_gap_lower_rational"] = str(gap)
                result["conditional_scope"] = f"every even periodic L >= {n}, only if all analytic/physical premises hold"
            else:
                result["conditional_scope"] = "Both defects exactly zero; no finite gap estimate emitted"
            return result
        if j == max_rounds:
            return result
        v = 1 - (1-p)**2 * (1-q)
        if v >= 1:
            result.update(status="unusable_spatial_bound", failure_round=j+1)
            return result
        pn = up(update(v), digits)
        if pn >= 1:
            result.update(status="unusable_spatial_bound", failure_round=j+1,
                          attempted_p_upper=str(pn))
            return result
        v = 1 - (1-q)**2 * (1-pn)
        if v >= 1:
            result.update(status="unusable_thermal_bound", failure_round=j+1)
            return result
        qn = up(update(v), digits)
        result["updates"].append({"round": j+1, "p_upper": str(pn), "q_upper": str(qn)})
        if qn >= 1:
            result.update(status="unusable_thermal_bound", failure_round=j+1)
            return result
        p, q = pn, qn
        n, beta = 2*n, 2*beta
    raise RuntimeError("Unreachable")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--S", help="Certified spatial purity LOWER bound, as string")
    parser.add_argument("--T", help="Certified thermal purity LOWER bound, as string")
    parser.add_argument("--n", type=int)
    parser.add_argument("--beta")
    parser.add_argument("--max-rounds", type=int, default=64)
    args = parser.parse_args()
    if args.certificate:
        if any(v is not None for v in (args.S, args.T, args.n, args.beta)):
            parser.error("Use a certificate OR explicit scalar inputs")
        cert = json.loads(args.certificate.read_text())
        seed = cert["seed"]
        result = replay(seed["S_lower"], seed["T_lower"], seed["n"], seed["beta"], args.max_rounds)
        record = cert.get("bootstrap", {})
        if record.get("success"):
            if result["status"] != "accepted_conditional_scalar_seed":
                raise ValueError("Recorded successful seed did not replay")
            for field in ("rounds", "final_p", "final_q", "final_common_u"):
                if result[field] != record[field]:
                    raise ValueError(f"Recorded {field} mismatch")
            for actual, expected in zip(result["updates"], record["updates"]):
                if any(actual[k] != expected[k] for k in ("p_upper", "q_upper")):
                    raise ValueError("Recorded update mismatch")
            if len(result["updates"]) != len(record["updates"]):
                raise ValueError("Recorded update count mismatch")
            if result["final_n"] != record["seed_n_after_rounds"] or F(result["final_beta"]) != F(record["seed_beta_after_rounds"]):
                raise ValueError("Recorded scale mismatch")
            if F(record["uniform_gap_lower_rational"]) > F(result["conditional_gap_lower_rational"]):
                raise ValueError("Recorded gap bound exceeds independently replayed bound")
            result["recorded_success_scalars_match"] = True
    else:
        if any(v is None for v in (args.S, args.T, args.n, args.beta)):
            parser.error("Provide --certificate, or all of --S --T --n --beta")
        result = replay(args.S, args.T, args.n, args.beta, args.max_rounds)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
