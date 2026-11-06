"""Repository root and writable scratch copies for the watertight auditors.

The auditor and seal12 producers write certificate JSON into a copy of the
research tree. That copy is not the sealed checkout.
"""
import os
from pathlib import Path

WATERTIGHT = Path(__file__).resolve().parent
REPO = WATERTIGHT.parents[1]

def _copy(env, name):
    raw = os.environ.get(env)
    path = Path(raw).resolve() if raw else (WATERTIGHT / "scratch" / name).resolve()
    marker = path / "research_20261010" / "uniform_smaller_second_initialization_review" / "audit_scalar.py"
    if not marker.is_file():
        raise SystemExit(
            env + " does not point at a repository copy (" + str(path) + "). "
            "Copy the repository there, or set the variable. "
            "An audit that calls seal() needs the sealed README and RESOURCE_PROJECTION bytes restored in that copy. "
            "See README.md."
        )
    return path

def orig_audit():
    """Writable copy of this repository. Producers and the original checker write here."""
    return _copy("WATERTIGHT_ORIG_AUDIT", "orig_audit")

def audit_copy():
    """Writable copy whose sealed documentation matches the review manifests.

    The patched checker is this copy after seal12/auditor_changes.diff is applied.
    Original-logic producers can use the same restored tree with the diff left unapplied.
    """
    return _copy("WATERTIGHT_AUDIT_COPY", "audit_copy")
