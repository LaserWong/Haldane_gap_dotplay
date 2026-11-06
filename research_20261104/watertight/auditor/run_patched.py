# Run the PATCHED audit_scalar.py (seal12 diff) against the scratch copies.
# AUDIT_CERT/AUDIT_OUT/AUDIT_DIGITS/AUDIT_FULL_R68 via env.
# path is the pristine file name recorded for compile(). src is the patched source in the audit copy.
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from paths import orig_audit, audit_copy
path = str(orig_audit() / 'research_20261010/uniform_smaller_second_initialization_review/audit_scalar.py')
src = open(audit_copy() / 'research_20261010/uniform_smaller_second_initialization_review/audit_scalar.py').read()
src = src.replace("os.sched_setaffinity(0,{0})", "os.sched_setaffinity(0,{6})", 1)
exec(compile(src, path, 'exec'), {'__file__': path, '__name__': '__main__'})
