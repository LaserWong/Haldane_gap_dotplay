# Supervisor launch gate

This package defines a launch gate and does not launch a campaign. It uses a persistent 21600 CPU-second ledger, two worker trees on CPU0/1, and a 256 MiB address-space ceiling for each tree. Supervisor overhead is capped and charged separately. The hard campaign wall stop is 2026-10-11T06:00:00Z, before the user's research stop at 2026-10-14T00:00:00Z.

Each attempt pre-reserves a worst-case process-count bound that includes metadata and failures. The reservation is 122 seconds for each process with a 120-second limit. Successful terminal wait4 measurements refund unused allowance. Unknown attempts remain fully charged. No budget reset or automatic restart is permitted after a terminal state.

A private process-lifetime and memory hook ensures descendant cleanup even if the watchdog or supervisor crashes. Safeguards include an exclusive campaign lock, a reserve-before-launch startup gate, persistent exact statuses, full-group cleanup before reuse, and certificate validation for the current invocation. The frozen runner 4a2828… remains unchanged. See PROOF.md and tests.json.

Only scheduling fixtures and metadata integration were run. No thermal campaign was launched. Independent review and root authorization are required before --launch.
