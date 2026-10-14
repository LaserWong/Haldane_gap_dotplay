# Resource projection for the separate strengthening batch

The proposed batch contracts its own physical lengths 26..33, comprising 8 lengths, while reusing unchanged D26 powers through 16.
The prior shared batch of 20 lengths, 4..23, measured 6.783 CPU seconds and 6.825 wall seconds.
The new batch is projected to use 8–12 CPU seconds and less than 35 MiB.

The hard limits are 30 CPU seconds and 100 MiB on CPU 4.
An external 25-second wall watchdog, wait4 accounting, and post-exec checks are required.
Parent-death termination and process-group cleanup apply, with no retry.
Compilation is separate, on CPU 2, with limits of 30 CPU seconds and 512 MiB.
The cached 4..25 gap .0248 already passes.
No seals are changed.
