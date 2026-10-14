# Accepted near-uniform certificates from the positive transfer

The certificates cover every integer periodic cell count M >= 2, with 2M physical spin-one sites and the designated unit exchange:

- g in [19999/20001, 20001/19999]: gap >= .02.
- g in [99993/100007, 100007/99993]: gap >= .015.
- g in [199983/200017, 200017/199983]: gap >= .01.
- g in [99991/100009, 100009/99991]: gap >= .005.

Each certificate includes a unique finite-volume ground state. Four additional certificates with odd-cell starts at 15/17 also passed. PROOF.md gives their exact intervals, assumptions and coverage. The previous interval reviews and the uniform all-physical-length .0248 theorem remain unchanged.

Independent 600-bit directed arithmetic validates all eight paths, including the late defect around 3.78e-83. All 70 windows and 183 source-manifest members pass, and 22 adversarial corruptions are rejected. The new checker used .5683 CPU seconds and 15,300 KiB. No physical computation was performed.

The accepted physical thermal/MPS inputs are inherited and pinned. Preliminary 60-digit failures remain scoped diagnostics. Reproduce the audit with `python audit.py` in a disposable copy. All required inputs are in snapshot.
