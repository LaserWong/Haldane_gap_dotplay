# Sharpness of the moment envelope

This exact assessment was awaiting independent review at the recorded checkpoint.

The Hermite/Radau bound is optimal for fixed moments in the positive-weight relaxation.
Explicit integer-count spectra fit all nine raw intervals and have positive seam traces at every integer length.
They limit further improvement based on these moments alone to 7.17e-5 at L = 26 and 3.05e-5 at L = 100.
A strict integer-count correction is proved, but is only about 1.50e-14 in the example.

These examples are abstract transfer spectra at a single temperature.
They are neither Heisenberg Hamiltonians nor counterexamples relating several temperatures.
They do not prove failure at n = 50 or 48, or minimality at n = 52.

`PROOF.md` gives the argument.
Run `python verify.py` and `python integer_correction.py` to reproduce the exact claims.
The auxiliary D = 26 outputs at lengths 96 and 100 are not used in these claims.
