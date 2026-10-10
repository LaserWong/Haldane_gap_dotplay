#!/usr/bin/env python3
"""Run existing finite-input postprocessing audits in one isolated temporary copy.

No full physical eigensolver or MPS optimization is scheduled. Some existing
audits verify cached trace/energy intervals rather than regenerate those inputs.
Logs are printed as summaries, or saved with --output DIRECTORY.
"""
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
JOBS = {
    "blbq_m005": ["blbq_eta_m005/audit/audit_success.py"],
    "blbq_m01": ["blbq_eta_m01/audit/audit_partial.py"],
    "blbq_m08": ["blbq_eta_m08/audit/audit_partial.py"],
    "blbq_m025": ["blbq_eta_m025/audit/certify_b6_thermal_obstruction.py"],
    "spin2": ["spin2_campaign/audit/audit_low_beta.py", "spin2_campaign/stronger_bootstrap/certify_scalars.py"],
    "haldane_reference": ["haldane_reference_audit/bootstrap_scalar_checks.py", "haldane_reference_audit/published_scalar_enclosures.py"],
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--case", choices=list(JOBS)+["all"], default="all")
    p.add_argument("--output", type=Path, help="Optional new log directory; never under cases/")
    p.add_argument("--timeout", type=int, default=240, help="Maximum seconds per selected audit")
    args = p.parse_args()
    out = args.output.resolve() if args.output else None
    if out and (out == ROOT/"cases" or ROOT/"cases" in out.parents):
        p.error("Do not write audit logs into preserved case sources")
    if out:
        out.mkdir(parents=True, exist_ok=True)
    versions = {}
    for name in ("numpy", "scipy", "sympy", "mpmath", "python-flint", "torch"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = "not installed"
    report = {"python": sys.version, "packages": versions, "scope": "Cached finite-input postprocessing; no full spectra or new Arb contractions recomputed", "checks": []}
    selected = list(JOBS) if args.case == "all" else [args.case]
    with tempfile.TemporaryDirectory(prefix="spin_bootstrap_audit_") as tmp:
        dst = Path(tmp)/"cases"
        shutil.copytree(ROOT/"cases", dst)
        env = os.environ.copy()
        # Prevent stale per-machine overrides from pointing outside this copy.
        env.pop("BLBQ_SPECTRA", None)
        env.pop("SPIN2_BUNDLE_ROOT", None)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["OPENBLAS_NUM_THREADS"] = "1"
        env["OMP_NUM_THREADS"] = "1"
        for case in selected:
            for script in JOBS[case]:
                start = time.monotonic()
                print(f"Running {script}", flush=True)
                try:
                    r = subprocess.run([sys.executable, str(dst/script)], cwd=dst,
                                       env=env, capture_output=True, text=True, timeout=args.timeout)
                    code, stdout, stderr = r.returncode, r.stdout, r.stderr
                except subprocess.TimeoutExpired as exc:
                    code = 124
                    stdout = exc.stdout or ""
                    stderr = exc.stderr or ""
                    stdout = stdout.decode(errors="replace") if isinstance(stdout, bytes) else stdout
                    stderr = stderr.decode(errors="replace") if isinstance(stderr, bytes) else stderr
                    stderr += "\nAudit timeout; no PASS claimed."
                row = {"case": case, "script": script, "exit_code": code,
                       "status": "PASS" if code == 0 else "FAIL",
                       "seconds": round(time.monotonic()-start, 3)}
                log = stdout + ("\nSTDERR:\n"+stderr if stderr else "")
                if out:
                    filename = script.replace("/", "__")+".log"
                    (out/filename).write_text(log)
                    row["log"] = filename
                if code:
                    print(log[-3000:], flush=True)
                report["checks"].append(row)
                print(row["status"], row["seconds"], "seconds", flush=True)
    report["status"] = "PASS" if all(x["status"] == "PASS" for x in report["checks"]) else "FAIL"
    if out:
        (out/"audit_run.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
