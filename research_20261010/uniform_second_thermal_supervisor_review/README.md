# Independent thermal-campaign supervisor review

Updated 2026-10-10 23:40 UTC / 19:40 America/New_York.

The engineering review accepts the supervisor subject to one authorized persistent state directory. Explicit launch authorization is still required. The design has a wall stop at 2026-10-11T06:00:00Z, a 21600-second aggregate CPU limit, and at most two single-core worker trees with 256 MiB each. Supervisor overhead is charged separately. No thermal commands were executed by this review.

`REVIEW.md` and `test_results.json` give the checks. `SNAPSHOT_SHA256.json` records source hashes, and `producer_manifest.json` pins the frozen source. Runtime fixtures require explicit authorization, write only local fixture files, and do not launch the campaign. Earlier source and review seals remain unchanged.

The sole authorized state path is `/workspace/shared/haldane_active/research_20261010/uniform_second_thermal_campaign_run`. An alternate path, copied or reset ledger, or second campaign is outside this authorization. A new budget decision must precede any such change.
