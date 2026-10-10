# Independent frontier-point review above g=0.10

Updated 2026-10-10 18:39 EDT / 22:39 UTC.

Accepted for every integer square L>=2, with a unique finite-volume ground state:

- g=.1001: gap >= .054499712024
- g=.1005: gap >= .049244008353
- g=.101: gap >= .040917096762
- g=.1015: gap >= .029199965244
- g=.102: gap >= .016509932002

These are discrete points. The physical legality domain near 0.120382423 is separately checked; it does not imply gap certification there.

PROOF.md explains the new-coupling physical bounds, exact fixed-z=.1 odd-family reconstruction, complete residual and counted tails, short-size bridges and scalar closure. The frozen point fixed_center labels require the explicit metadata erratum retained in snapshot; all numerical polynomials independently match z=.1.

PROVENANCE.json pins accepted structural identities. audit.json records physical margins and all-size results. REPRODUCE.sh checks seals and repeats the audit in a clean directory with CPU 4/600CPU-second/700MiB caps. No producer code, large physical computation or remote write is used.
