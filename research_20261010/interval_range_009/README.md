# Extend the continuous bilayer range to .09

Updated 2026-10-10 17:19 America/New_York (EDT) / 21:19 UTC.
Exact producer certificate; independent new-interval review still required.

Seven adjoining closed intervals certify every real g in [.085,.09] and every
integer square side L >= 2 at gap >= .005788366954. Joining the unchanged,
independently reviewed [0,.085] package gives 56 intervals covering [0,.09]
and preserves its uniform gap >= .001945771244.

- Largest seed: 128 physical spins, full Hilbert dimension 2^128
- Largest numerator: one retained state from a 43-dimensional search
- Smaller denominator retained states: 49 and 97; total available trial spaces 59 and 125
- Exact affine numerator and fixed-center denominator inputs throughout each interval
- 41 finite windows, 42 short-size rows, analytic large-L tail, multiedge L=2 conventions preserved
- No enlarged-state residual, q=8 support, physical-gap monotonicity, or point interpolation

See PROOF.md, coverage_summary.json, numerator_matrix_polynomial.json, and
replay_result.json. The original exact source geometries and all prior review
seals are bound in INPUT_SHA256.json and INHERITED_SEALS.json.

Run from the repository root:

    bash research_20261010/interval_range_009/REPRODUCE.sh

Reproduction verifies immutable inputs and replays all saved vectors without
an eigensolver. It does not overwrite the frozen package. Candidate generation
is in certify.py; its bounded beta proposals and two subdivided coarse failures
are recorded in coverage_summary.json. Generation took ~8.6 seconds, initial
replay ~9.6 seconds, each under 85 MiB, with one CPU and a 1 GiB cap.
All new work is confined here. Earlier certificates and repository root files
are untouched; no GitHub changes are included.
