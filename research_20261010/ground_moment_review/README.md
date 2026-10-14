# Accepted full-ground inverse-moment certificates

Independent exact replay accepts all 21 new ground endpoints and 14 successful all-size scalar certificates. For the ordinary periodic spin-1/2 bilayer, the strongest retained lower bounds at g=.03,.04,.05,.06,.07 are respectively

**.318423498447, .236077925502, .171822115684, .107275412881, .032948924929**,

for every integer square side L≥2, with unique finite-volume ground states. The g=.05 entry retains the preceding stronger accepted certificate. The independent g=.07 x–time–y route gives .020459331271. The .08/.10 failures remain finite-grid diagnostics.

[REVIEW.md](REVIEW.md) contains the theorem, invariant-sector count, exact normalization, source provenance, transport and every integer-size bridge. [REVIEW_STATUS.json](REVIEW_STATUS.json) records accepted endpoints and scope. No new physical trial family or higher moment is used. The largest full space is 2^128, the ground trial space is 29-dimensional, and the complete retained band has 193 states.

Run `bash REPRODUCE.sh` for full replay. The direct rational-witness acceptance alone is `python audit_direct.py`. It does not need inverse-pencil positivity assumptions. All writes stay in this review directory, with one CPU and a 1.5 GiB address-space ceiling.
