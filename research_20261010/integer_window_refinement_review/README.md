Updated: 2026-10-10 18:13 EDT (America/New_York) / 22:13 UTC.

# Independent direct time-first window review

Status: analytic lemma and exact complete paths accepted. Physical inputs are inherited from independently reviewed, hash-matched records.

- g=.21: gap >= .107424972, all integer M>=2
- g=.22: gap >= .071581253, all integer M>=2
- g=.225: gap >= .051807500, all integer M>=2
- g=.25: gap >= .01, only every integer 2<=M<=16; no new all-size certificate

All certified ground states in these scopes are unique. Strong exchange is one. No continuous-coupling interval or uniform g=1 chain claim is made.

See `PROOF.md` for the full operator proof, exact beta/basepoints and scope restrictions. `audit.py` is independent of producer code; `audit.json` contains exact acceptance results and adversarial/toy counts. `REPRODUCE.sh` checks frozen input hashes and repeats the scalar audit using CPU8 and a 1GiB address-space limit. `clean_replay` is the independent-directory repeat.

One producer prose-only decimal overstatement, .542 for a .541671301... lower endpoint, is explicitly corrected in `PRODUCER_PROSE_ERRATUM.json`; the original producer proof and manifest are preserved unchanged. The numerical certificate itself was correct.

Next useful research step: improve physical numerator/denominator inputs or develop stronger continuation inequalities at g=.25. A finite-window repair alone does not imply a complete bootstrap. No additional compute is pending in this audit.
