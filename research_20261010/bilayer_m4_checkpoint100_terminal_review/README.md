# Terminal checkpoint-100 review

Sealed 2026-10-11 01:53 EDT /05:53 UTC.

## Result

The terminal evidence and accounting passed review. The production lifecycle failed its gate pending a separately reviewed repair for incomplete process identity. The accepted initial 100 snapshot remains intact. There is no 400 checkpoint, q6 sample, full moment result or gap claim. No new scientific worker or fork test was launched by this review.

Producer export `bilayer_m4_checkpoint100_terminal`, manifest `2d89c43b510c5fd40f8032c827ea21f8739a06dc3064ad3e4c89a7ff3d992c44`: all 1036 files independently hashed and copied. Job `c2c9f79a9d55bbc0867f3ef38103d54cb98fc44c185adc280360ca25a969fd01`. Accepted 100 checkpoint `01d7a5098422a5dcb210fff8c77782e57099ff439e9e49b4b323cba06aea2418`.

## Checkpoint integrity and failed startup

All 1021 previously accepted scientific/checkpoint/session/event files selected for comparison are byte-identical, including every raw output, attempt, normalized result and commit. Their exact 24-field receipt chains were accepted in `bilayer_m4_checkpoint100_review` seal 01bebdec.... Coverage remains q0=1, q2=496, q4=1456, q6=0. Worker charge 492 includes 192 retired reservations plus 300 for this generation. No new scientific receipt or attempt appeared after 100.

The 100→400 token has exactly the required job, checkpoint digest, explicit approval and cap 400. The old outer process used that authority to begin another supervisor startup, but stopped before another inner reservation/controller/native worker. The token authorized the stage but did not establish completion of 400 chunks. No 400 token or FULL_MOMENTS marker exists.

## Observer failure

The sole new event is 6edab5e1bf540b7e5cd6e9899204e294fab492211965c57edffbdb48224d5291. PID 112, PPid 9, start 5752939, expected supervisor. Both sampled executable paths are the pinned Python 3.12 and both argv arrays are empty. CPU soft/hard limits 3/20, address-space soft/hard limits 64/128 MiB, affinity 6 are all correct for that startup role.

The frozen classifier deterministically maps the missing second argv element to an empty script string, matching neither the expected supervisor nor inherited outer command. It raises unexpected_stable_executable_or_command. This source interpretation was independently reproduced on the preserved tuple. Equal samples with incomplete command-line identity do not establish an unexpected executable. Why the argv reads were empty is not established by the tuple. The proposed remedy must handle bounded incomplete identity without marking it verified, while keeping resource enforcement and genuine identified-limit checks active. No pending repair source is included or accepted here.

The terminal cumulative map is now available. Its 99 observed native chunks 1–99 each have correct pinned executable/command/range, CPU3/3, AS128/128 and affinity 6, with stable PID/start identity. One supervisor, one controller and the external watchdog also have valid tuples. The short vacuum worker 0 was not observed by sampling, which is an explicit limitation, not missing numerical coverage. All 100 numerical receipts still exist.

## Terminal idle and resources

Both existing lifetime LOCK and OUTER_LOCK were independently acquired exclusively and held during this audit. The terminal outer receipt, complete 100 attempts and unchanged inner reaping receipt agree. The review relied on these matching locks and receipts rather than an empty scan of an unrelated PID namespace.

Terminal outer wait4 tree CPU 16.546556, self CPU 2.843112, wall 676.113218 including the approval wait, peak sampled combined RSS 59,121,664. Final self CPU slightly exceeds the earlier ledger update timestamp, while remaining far below the prepaid 100 cap. No failed-startup CPU is refunded. Startup is covered by the existing 20-second contingency inside the outer 120 reservation.

Control ledger 716 = prior 711 plus the approved 5-second terminal metadata export. Worker ledger 492. Total 1208. The original 220 startup failure, the later 463-control/192-worker history and every export remain charged. Some old stopped jobs retain reserved labels in subordinate rows. These labels describe already charged reservations and cannot authorize reuse.

## Resource forecast and proposed restart

The producer's 1383 control figure is 716+29*23 and excludes a fresh launcher. Adding the necessary 220 gives 1603, above this source's 1600 pool. Therefore the old job cannot simply be relaunched under its old budget. Its already-used reservations cannot be reused.

A separate design authorization proposed the following partition for a clean generation. The unchanged 21600 total =16800 standard +1800 controls +3000 retries. All 716 controls and all 492 retired workers would carry. Retries left 2508. Planned clean control 716+220+30*23=1626, leaving 174. This arithmetic is recorded as a pending proposal, not source/launch acceptance. Fresh source/pins, independent review and new explicit launch authority are required. Existing numerical accumulators are not silently rebound to a new identity.

## Audit budget

The previously reserved 400-checkpoint allowance was redirected to this terminal review. It provided 8 CPU seconds, split as 6 child+2 parent, and remains fully charged at 8/8. Actual metadata child .822083 CPU and guard .122951. No descendants remained. The accepted 100 review and all prior ledgers/seals are unchanged. Metadata preparation/sealing stays within the remaining parent allowance.
