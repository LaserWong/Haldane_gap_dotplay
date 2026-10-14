# Independent continuous bilayer certificate through g = .10

The ordinary bilayer has a unique finite-volume ground state and a gap of at least .001945771244 for every real coupling 0≤g≤.10 and every integer periodic square side L≥2.
The extension on [.09,.10] alone has the stronger lower bound .008761649092.

`REVIEW.md` gives the proof, limitations, provenance, and dimensions.
`REVIEW_STATUS.json` records the machine-readable acceptance.
Run `bash REPRODUCE.sh` for a fresh exact audit and corruption tests.
The immutable manifest excludes fresh replay directories.

The proof uses explicitly pinned accepted physical residuals and earlier interval proofs.
The checker runs neither a certificate-generator module nor an eigensolver.
