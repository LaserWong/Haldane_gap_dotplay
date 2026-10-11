# Accepted positive-transfer near-uniform certificates

All integer periodic cell counts M >= 2, with 2M physical spin-one sites and designated unit exchange:

- g in [19999/20001, 20001/19999]: gap >= .02.
- g in [99993/100007, 100007/99993]: gap >= .015.
- g in [199983/200017, 200017/199983]: gap >= .01.
- g in [99991/100009, 100009/99991]: gap >= .005.

Each includes a unique finite-volume ground state. Four additional odd-cell-start certificates at15/17 also passed. PROOF.md gives their exact intervals, all assumptions and coverage. The previous interval reviews and the uniform all-physical-length .0248 theorem are unchanged.

Independent600-bit directed arithmetic validates all eight paths, including the late defect around3.78e-83. All70 windows and183 source-manifest members pass;22 adversarial corruptions are rejected. The new checker cost .5683 CPU seconds /15,300 KiB. No physical computation was performed.

The accepted physical thermal/MPS inputs are inherited and pinned. Preliminary60-digit failures remain scoped diagnostics. Reproduce with `python audit.py` in a disposable copy; all required inputs are in snapshot.
