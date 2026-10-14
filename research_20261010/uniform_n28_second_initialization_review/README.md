# Accepted .0179 bound from L28

Updated 2026-10-11 02:29 UTC / 2026-10-10 22:29 America/New_York.

The review accepts a unique ground state and gap≥.0179 for every integer periodic length L≥28 in the unit-bilinear spin-1 Heisenberg model. The new exact window 28..56 joins the accepted tail from 30. Bootstrap initialization remains 30, and the stronger .0245 bound from 32 and .0248 bound from 34 remain valid.

The independent physical D26/MPS56 contraction and exact signed-transfer replay pass. Fresh auxiliary anchors at 48/52 are included without gap claims at 24/26. The particular n28 continuation fails later, which leaves other constructions open. Floating scans remain proposals only.

`PROOF.md`, `results.json`, `anchor_results.json`, and `adversarial_results.json` contain the evidence. In a disposable copy, run `python check_anchors.py`, `python audit_bridge.py`, and `python adversarial_tests.py`. No new thermal calculation or producer-source import is required.
