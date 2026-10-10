Updated 2026-10-10 17:25 America/New_York (EDT) / 21:25 UTC.

# Independent .09 continuous-interval review

The ordinary spin-1/2 square bilayer is certified for all real g in [0,.09] and every integer square side L>=2, with unique finite-volume ground state and uniform gap at least .001945771244. The new [.085,.09] extension alone has bound .005788366954.

- REVIEW.md: theorem, independent argument, physical normalization, scope and limitations.
- REVIEW_STATUS.json: final acceptance and test counts.
- results/SUMMARY.json: per-interval exact outcomes, finite windows and resource data.
- results/numerator_operator.json: independently assembled affine physical matrices and positive Gram pivots.
- results/inherited_basepoint_ledger.json: same-base partition-function identities.
- results/odd_endpoint_checks.json: every smaller-patch odd-mode interval certificate.
- results/adversarial_rejections.json: deliberately corrupted certificates rejected.
- PRODUCER_FREEZE.json and snapshot/: exact frozen candidate.
- PINS.json: mandatory producer, physical and previous continuous review hashes.
- MANIFEST_SHA256.json: immutable review contents.

Run ./REPRODUCE.sh from this directory. It verifies immutable inputs, runs only independent exact auditors with one CPU and 1 GiB cap, writes into a fresh replay_unsealed directory and verifies the immutable seal again. No eigensolver, producer Python module, sparse physical recomputation, root write, Git operation or network access is needed. Python and NumPy are required. A replay ordinarily takes a few minutes, principally the adversarial checks.

Next use: parent may incorporate this sealed theorem into the project overview, preserving separate labels for the single-point .09 bound and this continuous-interval bound. Any extension beyond .09 needs fresh interval certificates and independent acceptance.
