#!/usr/bin/env python3
"""Independent stdlib-only audit; never imports or executes producer code.

Run from any directory. All acceptance comparisons are exact Fractions.
Numerical displays are non-authoritative. The small source copies preserve
archival provenance and avoid re-running any many-body eigensystem.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal, localcontext
import hashlib
import json
import os
import resource
import time

START = time.time()
resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
if hasattr(os, "sched_getaffinity"):
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
HERE = Path(__file__).resolve().parent
PACKET = HERE.parent / "spin2_scalar_improvement/frozen_ip_witness"

def read(p):
    return json.loads(p.read_text(), parse_float=str)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def display(q, precision=25):
    with localcontext() as ctx:
        ctx.prec = precision
        return str(Decimal(q.numerator) / Decimal(q.denominator))

def short_interval(q, places=12):
    s = 10**places
    n = q.numerator * s // q.denominator
    return [str(F(n, s)), str(F(n+1, s))]

def exp_negative_bounds(q):
    # Taylor's integral remainder has the sign of the first omitted term.
    # This gives lower (odd degree 79) and upper (even degree 80) for q>=0.
    assert q >= 0
    term = total = F(1)
    for k in range(1, 81):
        term *= -q / k
        total += term
        if k == 79:
            lower = total
    assert 0 < lower < total
    return lower, total

manifest = read(PACKET / "MANIFEST.json")
assert sha(PACKET / "MANIFEST.json") == "df696b5db74babc762f53743196ff7f76b766b1f7a292f5f808fb6e52adfe3be"
for name, expected in manifest["files"].items():
    assert sha(PACKET / name) == expected, name

archive_names = {
    "archive_trace_intervals.json": "trace_intervals.json",
    "archive_exploratory_order10_results.json": "exploratory_order10_results.json",
    "ARCHIVE_VALIDATION.md": "VALIDATION.md",
    "ARCHIVE_STATUS.json": "STATUS.json",
}
archive_manifest = read(HERE / "inputs/archive_manifest_sha256.json")
for copy_name, original_name in archive_names.items():
    assert sha(HERE / "inputs" / copy_name) == archive_manifest[original_name]

archive = read(HERE / "inputs/archive_trace_intervals.json")
selected = [r for r in archive if r["beta"] == "8" and r["twist"] in ("I", "P")]
assert sorted(selected, key=lambda r: (r["n"], r["twist"])) == sorted(
    read(PACKET / "copied_beta8_lower_trace_intervals.json"),
    key=lambda r: (r["n"], r["twist"])
)
assert len(selected) == 14
assert {r["n"] for r in selected} == set(range(2, 9))
assert all(F(r["a"]) == F(5951, 1250) and r["dimension"] == 5**r["n"] for r in selected)

witness = read(PACKET / "full_integer_witnesses.json")
atoms = {}
for row in witness:
    assert row["beta"] == 8 and F(row["a"]) == F(5951, 1250)
    assert len(row["counts"]) == len(row["nodes"]) == 17
    assert all(type(c) is int and c > 0 for c in row["counts"])
    atoms[row["sector"]] = list(zip(row["counts"], map(F, row["nodes"])))
assert set(atoms) == {"J", "N"}

def moment(sector, k):
    return sum(c * x**k for c, x in atoms[sector])

def trace(twist, k):
    return moment("J", k) + (3 if twist == "I" else -1) * moment("N", k)

lower_checks = []
for row in selected:
    k, twist = row["n"], row["twist"]
    actual = trace(twist, k)
    lower, upper = F(row["lower"]), F(row["upper"])
    assert lower < actual < upper
    lower_checks.append({"L": k, "twist": twist, "strict_inclusion": True,
                         "actual_rational": str(actual), "actual_display": display(actual),
                         "margin_rational": str(min(actual-lower, upper-actual)),
                         "margin_display": display(min(actual-lower, upper-actual)),
                         "interval_width": str(upper-lower)})

all_exploratory = read(HERE / "inputs/archive_exploratory_order10_results.json")
candidate = next(r for r in all_exploratory if r["a"] == "4.7608" and
                 r["beta"] == 8 and r["max_moment"] == 10)
saved_candidate = next(r for r in read(PACKET / "exploratory_moment_inputs.json")
                       if r["beta"] == 8)
assert candidate == saved_candidate
high_checks = []
for k in (9, 10):
    j = F(candidate["moments"]["J"][str(k)])
    n = F(candidate["moments"]["N"][str(k)])
    for twist, center in (("I", j+3*n), ("P", j-n)):
        actual = trace(twist, k)
        error = abs(actual-center)
        radius = F(6, 10**6) if k == 9 else F(5, 10**5)
        assert error < F(1, 10**48) < radius
        row = {"L": k, "twist": twist, "center_rational": str(center),
               "radius_rational": str(radius), "error_rational": str(error),
               "error_display": display(error), "strict_inclusion": True,
               "center_status": "Reconstructed exact J/N decimal combination; not certified physical trace"}
        if twist == "I":
            source_z = F(candidate["moments"]["Z"][str(k)])
            row.update({"original_Z_center_rational": str(source_z),
                        "reconstructed_minus_original_Z_rational": str(center-source_z),
                        "actual_error_from_original_Z_display": display(abs(actual-source_z))})
        high_checks.append(row)

alpha, gamma, r = F(103, 100), F(51, 50), F(3, 4)
assert atoms["J"][0] == (1, alpha) and atoms["N"][0] == (1, gamma)
assert all(abs(x) < r for sector in atoms.values() for _, x in sector[1:])
CJ = sum(c*x**10 for c, x in atoms["J"][1:])
CN = sum(c*x**10 for c, x in atoms["N"][1:])
finite_positivity = []
for k in range(2, 32):
    for twist in ("I", "P"):
        v = trace(twist, k)
        assert v > 0
        finite_positivity.append({"L": k, "twist": twist, "positive": True,
                                  "value_display": display(v)})
tail_i = alpha**32 + 3*gamma**32 - (CJ+3*CN)*r**22
tail_p = alpha**32 - gamma**32 - (CJ+CN)*r**22
assert tail_i > 0 and tail_p > 0

shift = F(8) * (F(476121, 100000) - F(5951, 1250))
assert shift == F(41, 12500)
rho_lower, rho_upper = exp_negative_bounds(shift)
assert rho_lower*gamma > 1 and rho_lower*alpha > 1

def lead(k):
    return alpha**k+3*gamma**k

length_checks = []
for k in (128, 256, 512, 1024):
    half = k//2
    residual = CJ+3*CN
    # Even powers give nonnegative remainders; no cancellation at these lengths.
    s_lower = lead(k) / (lead(half)+residual*r**(half-10))**2
    s_upper = (lead(k)+residual*r**(k-10)) / lead(half)**2
    if k == 128:
        # The crude r=3/4 remainder is wider than 1e-9 here. Direct rational
        # evaluation at orders 64 and 128 independently sharpens this case.
        s_exact = trace("I", k)/trace("I", half)**2
        assert s_lower <= s_exact <= s_upper
        s_lower = s_upper = s_exact
    s_floor = (s_lower.numerator*10**9)//s_lower.denominator
    s_ceiling = -((-s_upper.numerator*10**9)//s_upper.denominator)
    assert F(s_floor,10**9) <= s_lower <= s_upper <= F(s_ceiling,10**9)
    rho_k_lower, _ = exp_negative_bounds(shift*k)
    zi_lower = rho_k_lower*lead(k)
    zi_floor = F((zi_lower.numerator*10**6)//zi_lower.denominator,10**6)
    assert 1 < zi_floor <= zi_lower
    length_checks.append({"L": k,
                          "spatial_purity_interval_rational": [str(F(s_floor,10**9)),str(F(s_ceiling,10**9))],
                          "shifted_I_lower_rational": str(zi_floor),
                          "numerator_one_certificate_ceiling_rational": str(1/zi_floor**2),
                          "numerator_one_certificate_ceiling_display": display(1/zi_floor**2),
                          "N_mass_lower_display": display(3*rho_k_lower*gamma**k)})

# C is a rotation by 2pi/3. A triplet has character 0; a singlet has character 1.
c8 = next(row for row in archive if row["n"] == 8 and row["twist"] == "C" and row["beta"] == "8")
predicted_c8 = moment("J", 8)
assert predicted_c8 > F(c8["upper"])

output = {"status": "PASS_FOR_EXPLICIT_IP_INTERVAL_RELAXATION_WITH_SCOPE_CORRECTIONS",
          "frozen_manifest_sha256": sha(PACKET / "MANIFEST.json"),
          "frozen_file_hashes_verified": manifest["files"],
          "archive_source_hashes_verified": {k: sha(HERE/"inputs"/k) for k in archive_names},
          "lower_interval_checks": lower_checks,
          "prospective_interval_checks": high_checks,
          "positive_integer_multiplicities": True,
          "dimensions": {s: sum(c for c,x in a) for s,a in atoms.items()},
          "SO3_total_dimension": sum(c for c,x in atoms["J"])+3*sum(c for c,x in atoms["N"]),
          "all_length_positivity": {"finite_checks": finite_positivity,
                                    "nonleading_modulus_strict_upper": str(r),
                                    "CJ_rational": str(CJ), "CN_rational": str(CN),
                                    "tail_start": 32,
                                    "I_tail_margin_rational": str(tail_i),
                                    "P_tail_margin_rational": str(tail_p),
                                    "I_tail_margin_display": display(tail_i),
                                    "P_tail_margin_display": display(tail_p)},
          "shift_check": {"new_a": "476121/100000", "beta_delta_a": str(shift),
                          "rho_alpha_lower_display": display(rho_lower*alpha),
                          "rho_gamma_lower_display": display(rho_lower*gamma),
                          "both_shifted_leaders_above_one": True,
                          "for_every_even_L_ge2": "I>4, N_total_mass>3; numerator-one ceiling<1/16"},
          "large_length_checks": length_checks,
          "C8_failure_of_this_realization": {"predicted_display": display(predicted_c8),
                                             "archive_interval": [c8["lower"], c8["upper"]],
                                             "strictly_outside": True},
          "excluded_claims": ["No physical gap or gaplessness conclusion",
                              "No refutation of all scalar or moment methods",
                              "No joint beta/2beta physical thermal construction",
                              "No C-moment match or local transfer realization",
                              "No refutation of atom exclusion conditioned on J cutoff below 1.03",
                              "Future intervals must actually contain witness moments; membership of true traces in broader proposed boxes is insufficient"],
          "resource_limits": {"cpu_affinity_count": 1, "address_space_bytes": 1024**3,
                              "cpu_limit_seconds":120, "blas": "unused; standard library only"},
          "wall_seconds": time.time()-START,
          "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(HERE / "audit_results.json").write_text(json.dumps(output, indent=2)+"\n")
print(json.dumps({k: output[k] for k in ("status", "dimensions", "SO3_total_dimension", "large_length_checks", "wall_seconds", "peak_rss_kib")}, indent=2))
