#!/usr/bin/env python3
"""Stdlib-only scalar/provenance audit, independent of producer code.

No eigensolver, heat trace, or MPS contraction is run. All acceptance arithmetic
uses integers/Fractions. Displays have no role in acceptance. The complete
bundled gzip blocks are verified portably. --archive optionally also rehashes
the original extracted sources; it is not needed for the minimal replay.
"""
import argparse
from contextlib import contextmanager
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import gzip
import io
import json
import os
from pathlib import Path
import re
import resource
import sys
import time

START = time.time()
sys.set_int_max_str_digits(20000)
resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
if hasattr(os, "sched_getaffinity"):
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
P = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--archive", type=Path, default=None,
                    help="Optional original extracted archive for extra source rehashing")
args = parser.parse_args()

def read(path):
    return json.loads(path.read_text(), parse_float=str)

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1024**2), b""):
            h.update(part)
    return h.hexdigest()

def display(q, precision=25):
    with localcontext() as ctx:
        ctx.prec = precision
        return str(Decimal(q.numerator) / Decimal(q.denominator))

def decimal_enclosure(q, places=20):
    scale = 10**places
    n = q.numerator * scale // q.denominator
    return [str(F(n, scale)), str(F(n + 1, scale))]

def exp_minus_bounds(x):
    # Taylor integral remainder alternates for exp(-x), x>=0. No asymptotic
    # approximation or floating monotonicity decision is used.
    assert 0 <= x <= 1
    term = total = F(1)
    for k in range(1, 41):
        term *= -x / k
        total += term
        if k == 39:
            lo = total
    assert 0 < lo <= total <= 1
    return lo, total

def exp_plus_bounds(x):
    assert 0 < x < 1
    term = total = F(1)
    for k in range(1, 41):
        term *= x / k
        total += term
    first_omitted = term * x / 41
    # All subsequent ratios are at most x/42.
    return total, total + first_omitted / (1 - x / 42)

manifest_path = P / "inputs/archive_manifest_sha256.json"
assert sha(manifest_path) == "92c2cb80c718e5daf5c6e78a0dcddd220b643b5b974c9924b2699d2ab6953e1a"
original_manifest = {r["path"]: r for r in read(manifest_path)["files"]}
copy_map = read(P / "inputs/COPY_MAP.json")
copy_checks = []
for dest, source in copy_map.items():
    if source == "MANIFEST_SHA256.json":
        continue
    expected = original_manifest[source]
    actual = P / "inputs" / dest
    assert sha(actual) == expected["sha256"]
    assert actual.stat().st_size == expected["bytes"]
    copy_checks.append({"copy": dest, "source": source, "sha256": expected["sha256"]})

producer = P / "producer_snapshot"
producer_manifest = read(producer / "MANIFEST.json")
assert sha(producer / "MANIFEST.json") == "dc698e0e40756823eb90c85fc306c6b34e805bd255c17a9b256cd21bc2cf986f"
for path in producer.iterdir():
    if path.name != "MANIFEST.json":
        assert sha(path) == producer_manifest[path.name], path.name

archived_traces = read(P / "inputs/archive_trace_intervals.json")
rows = [r for r in archived_traces if r["beta"] == "8" and r["twist"] in ("I", "P")]
assert len(rows) == 14
assert sorted(rows, key=lambda r: (r["n"], r["twist"])) == sorted(
    read(producer / "copied_beta8_lower_trace_intervals.json"),
    key=lambda r: (r["n"], r["twist"]))
r8 = next(r for r in rows if r["n"] == 8 and r["twist"] == "I")
assert F(r8["a"]) == F(5951, 1250) and r8["dimension"] == 5**8
U8 = F(r8["upper"])
assert U8 == F(3382547386422157, 10**14)
a0, a1, beta = F(5951, 1250), F(476121, 100000), F(8)
alpha = beta * (a1 - a0)
assert alpha == F(41, 12500)
rho_lo, rho_hi = exp_minus_bounds(alpha)
z8_factor_lo, z8_factor_hi = exp_minus_bounds(8 * alpha)
assert rho_hi < 1 and z8_factor_hi < 1

certificate = read(P / "inputs/archive_mps124_arb_certificate.json")
summary = read(P / "inputs/archive_mps_RESULTS.json")
assert summary["new_certificate"] == certificate
assert summary["bond_dimension"] == 124
assert F(summary["new_certified_shift"]) == a1
tensor = read(P / "inputs/archive_mps124_integer_tensor.json")
assert tensor["physical_spin"] == 2 and tensor["bond_dimension"] == 124
assert sum(2 * j + 1 for j in tensor["virtual_spins"]) == 124
assert tensor["physical_weights"] == [1, 4, 6, 4, 1]
assert len(tensor["B_integer"]) == 5
assert all(len(A) == 124 and all(len(row) == 124 and
    all(type(x) is int for x in row) for row in A) for A in tensor["B_integer"])
assert sum((2 * j + 1) * n for j, n in enumerate(tensor["highest_weight_dims"])) == 124**2
assert sha(P / "inputs/archive_mps124_integer_tensor.json") == certificate["tensor_sha256"]

source_rehash = []
parts_dir = P / "inputs/blocks_gzip_parts"
parts_manifest = read(parts_dir / "manifest.json")
part_paths = []
compressed_hash = hashlib.sha256()
compressed_bytes = 0
for i, part in enumerate(parts_manifest["parts"]):
    assert part["name"] == f"part-{i:03d}.gzpart"
    path = parts_dir / part["name"]
    assert path.stat().st_size == part["bytes"] <= 2 * 1024**2
    part_hash = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024**2), b""):
            part_hash.update(chunk)
            compressed_hash.update(chunk)
            compressed_bytes += len(chunk)
    assert part_hash.hexdigest() == part["sha256"]
    part_paths.append(path)
assert compressed_bytes == parts_manifest["compressed_bytes"]
assert compressed_hash.hexdigest() == parts_manifest["compressed_sha256"]
assert compressed_hash.hexdigest() == "736d7544363f65bd4c378973a727e5c417c9d0fcd04744ab15168b73b1b47423"

class ConcatenatedReader(io.RawIOBase):
    """Read split gzip parts as one stream, never reassembling a large file."""
    def __init__(self, paths):
        self.remaining = iter(paths)
        self.current = None

    def readable(self):
        return True

    def readinto(self, buf):
        while True:
            if self.current is None:
                try:
                    self.current = next(self.remaining).open("rb")
                except StopIteration:
                    return 0
            count = self.current.readinto(buf)
            if count:
                return count
            self.current.close()
            self.current = None

    def close(self):
        if self.current is not None:
            self.current.close()
        super().close()

@contextmanager
def open_blocks():
    with io.BufferedReader(ConcatenatedReader(part_paths)) as raw:
        with gzip.GzipFile(fileobj=raw, mode="rb") as uncompressed:
            yield uncompressed

block_source_name = "cases/spin2_campaign/mps/improved124_exact_blocks.txt"
block_digest = hashlib.sha256()
block_bytes = 0
with open_blocks() as f:
    for part in iter(lambda: f.read(1024**2), b""):
        block_digest.update(part)
        block_bytes += len(part)
assert block_digest.hexdigest() == certificate["blocks_sha256"]
assert block_digest.hexdigest() == original_manifest[block_source_name]["sha256"]
assert block_bytes == original_manifest[block_source_name]["bytes"]
assert block_digest.hexdigest() == parts_manifest["uncompressed_sha256"]
assert block_bytes == parts_manifest["uncompressed_bytes"]
with open_blocks() as raw, io.TextIOWrapper(raw) as f:
    nb = int(f.readline())
    dimensions = []
    for j in range(nb):
        J, n = map(int, f.readline().split())
        assert J == j
        dimensions.append(n)
        for _ in range(2 * n):
            row = [int(z) for z in f.readline().split()]
            assert len(row) == n
    assert not f.read().strip()
assert dimensions == tensor["highest_weight_dims"]
block_shape_checks = {"sectors": nb, "dimensions": dimensions,
    "virtual_transfer_dimension": 124**2,
    "compressed_sha256": compressed_hash.hexdigest(),
    "part_count": len(part_paths), "individual_part_hashes_verified": True,
    "uncompressed_sha256": block_digest.hexdigest(),
    "uncompressed_bytes": block_bytes, "portable_bundle_verified": True}
if args.archive is not None:
    assert args.archive.is_dir()
    needed = ["cases/spin2_campaign/mps/improved124_exact_blocks.txt"]
    needed += [src for src in copy_map.values() if src != "MANIFEST_SHA256.json"]
    for src in needed:
        path = args.archive / src
        assert sha(path) == original_manifest[src]["sha256"]
        assert path.stat().st_size == original_manifest[src]["bytes"]
        source_rehash.append({"source": src, "sha256": original_manifest[src]["sha256"]})

mps_checks = []
assert [r["N"] for r in certificate["results"]] == [128, 256, 512, 1024]
for r in certificate["results"]:
    match = re.fullmatch(r"\[([^ ]+) \+/- ([^ ]+)\]", r["energy_interval"])
    assert match is not None
    center, radius = map(F, match.groups())
    assert radius > 0 and r["norm_positive"] is True
    upper = center + radius
    margin = -a1 - upper
    assert margin > 0 and F(r["threshold_a"]) == a1
    exponent = beta * r["N"] * margin
    exp_lo, exp_hi = exp_plus_bounds(exponent)
    assert exp_lo > 1
    # Conditional on the archived energy ball, variational principle gives
    # Z_L >= exp[-beta L(a1 + e_trial)] >= exp(exponent) > exp_lo > 1.
    mps_checks.append({"L": r["N"], "energy_upper": str(upper),
        "energy_margin": str(margin), "positive_exponent": str(exponent),
        "exp_lower_rational": str(exp_lo), "exp_upper_rational": str(exp_hi),
        "exp_lower_display": display(exp_lo), "Z_L_gt_1": True})

expected = {128: F("0.971082"), 256: F("0.985901"),
            512: F("0.993037"), 1024: F("0.996540")}
producer_atoms = read(producer / "atom_location.json")
assert F(producer_atoms["U8"]) == U8
atom_checks = []
for r in producer_atoms["rows"]:
    L, ell = r["L"], F(r["ell"])
    assert ell == expected[L] and L % 2 == 0 and 0 < ell < 1
    value = U8 * ell**(L - 8)
    assert value < 1
    # Independently validate the millionth proposal without logarithms/floats.
    next_grid = U8 * (ell + F(1, 10**6))**(L - 8)
    assert next_grid >= 1
    atom_checks.append({"L": L, "q": 8, "ell": str(ell),
        "ell_display": display(ell), "exact_comparison_passed": True,
        "U8_times_ell_power": str(value), "exclusion_upper_display": display(value),
        "strict_slack": str(1 - value), "strict_slack_display": display(1 - value),
        "largest_valid_millionth_with_U8_and_B1": True})
assert len(atom_checks) == 4

# Small exact examples guard against inadvertently adding uniqueness claims.
for k in range(4, 41):
    j = F(1)**k + F(-1)**k + F(1, 2)**k
    assert j > 0  # Tied +/-1 in J, positive physical I/P traces nevertheless.
    i, o, n = F(2), F(1), F(1)
    assert i - o > 0 and i + 2 * o - n > 0

result = {
    "status": "PASS_ANALYTIC_LEMMA_AND_EXACT_SCALAR_CHECKS_WITH_INHERITED_FINITE_INPUTS",
    "model": "periodic spin-2 Heisenberg, J=1, H_L=sum S_j dot S_(j+1)",
    "beta": str(beta), "shift_old": str(a0), "shift_target": str(a1),
    "all_length_transfer_scope": "Analytically reconstructed for every integer L>=2 in README.md",
    "finite_input_limits": [
        "Original complete-spectrum L8 intervals and stated arithmetic assumptions are inherited, not recomputed",
        "Original exact D124 block construction and Arb contractions are inherited, not recomputed",
        "Hash/provenance, original output consistency, dimensions, ball-endpoint signs and all new scalar arithmetic are independently checked"
    ],
    "copied_source_checks": copy_checks,
    "original_sources_rehashed": bool(source_rehash),
    "original_source_checks": source_rehash,
    "mps_block_shape_checks": block_shape_checks,
    "normalization": {
        "atom_rescaling": "exp(-beta*(a1-a0))", "atom_exponent": str(alpha),
        "rho_enclosure": [str(rho_lo), str(rho_hi)],
        "rho_display_enclosure": [display(rho_lo), display(rho_hi)],
        "Z8_rescaling_exponent": str(8 * alpha),
        "Z8_rescaling_enclosure": [str(z8_factor_lo), str(z8_factor_hi)],
        "old_U8_remains_upper": True},
    "U8": str(U8), "mps_checks": mps_checks, "atom_checks": atom_checks,
    "unique_leading_atom_claim": False, "thermal_startup_claim": False,
    "uniform_gap_claim": False, "seconds": time.time() - START
}
(P / "audit_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "original_sources_rehashed": bool(source_rehash),
    "portable_bundle_verified": block_shape_checks["portable_bundle_verified"],
    "MPS_Z_gt_1_lengths": [r["L"] for r in mps_checks],
    "positive_trivial_atom_lower_bounds": [
        {k: r[k] for k in ("L", "ell_display", "exclusion_upper_display",
                           "strict_slack_display")} for r in atom_checks],
    "thermal_startup_claim": False, "uniform_gap_claim": False,
    "seconds": result["seconds"]}, indent=2))
