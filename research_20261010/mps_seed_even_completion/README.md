# Separate all-temperature tests at n18 and n22

Separate exact tests exclude the specified recipes at every temperature for n18 and n22, using either three or four retained states. The proof does not assume monotonicity with seed size. These conclusions apply
only to the fixed archived D26 single-Rayleigh numerator at 2n and the existing
thermal-first / delayed joint-aware canonical recipes. They do not exclude
new finite-window interpolation lemmas or other uses of the same data.

The denominator states are psi (Sz0), the staggered normalized raising
source (Sz1), its global spin flip (Sz-1), and optionally the separately
contracted staggered Sz source (Sz0, momentum pi). Translation makes the last
state orthogonal to psi. The sealed source integers verify nonzero norms and
identical transverse/longitudinal norm and energy at both n18 and 22.
No total-spin assumption about these two sizes is needed.

The original producer source contractions already contain n18/n22. The
reviewer's sealed ordinary ground contractions contain lengths 36 and 44,
which the original producer ground sample omitted. Their exact hash is
recorded as an input. No new physical contraction was performed.

Scalar Jensen gives Z_n(beta)>=exp(-beta alpha0)[1+m exp(-beta g)], with
m=2 or 3. The fixed numerator at 2n yields the same J/C upper envelopes as
mps_excited_seed_witnesses/PROOF.md. Exact hot and cold tails plus a closed-box
cover exclude the specified recipes. Every possible whole-cycle delay is
checked until its optimistic continuation fails. No finite replay limit is
silently accepted as an exclusion. All signs use outward rational arithmetic.

The local search dimension is zero (fixed vectors), the retained span dimension
is 3 or 4, and individual MPS bonds are 26/52. The full physical Hilbert spaces
have dimensions 3^18 and 3^22, with 3^36 and 3^44 for the numerator lengths.
No larger physical support or full spectrum is constructed.

The run used 3.04 CPU seconds and 10.75 MiB on one core. To reproduce, copy this directory
and both dependency directories mps_excited_seed_witnesses and
mps_excited_seed_review to a new parent, then run
`taskset -c 2 python3 verify_sizes.py` from the copied directory. Output files
are rewritten, so replay must not run inside this freeze.

Inputs, exact histories, and hashes are in results.json. The summary is in summary.json.
Independent review remains separate.
