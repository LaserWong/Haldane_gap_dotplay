# Candidate extension of uniform-chain coverage to length 48

The exact generated candidate was awaiting a new independent review at the recorded checkpoint.

The direct finite window gives gap>=0.0053 for every integer 48<=L<=96.
Combined with the accepted n = 52 theorem, it gives gap>=0.0038 for every integer L>=48.
Bootstrap initialization remains 52, while coverage begins at 48.

The calculation uses only the accepted anchors at lengths 48 and 96.
It uses neither the provisional length-50 input nor a new physical calculation.
It makes no claim below 48 or about minimality.

Read `PROOF.md` and run `python certify.py`.
The recorded replay used about 0.49 CPU seconds and 10.6 MiB.
