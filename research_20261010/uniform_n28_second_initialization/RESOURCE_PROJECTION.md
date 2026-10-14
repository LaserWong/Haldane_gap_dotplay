# Resource projection for the MPS56 anchor

A fresh contraction of the unchanged D = 26 MPS at length 56 is projected to need less than 10 CPU seconds and less than 35 MiB.
This estimate uses the measured 8.96 s at length 60 and 15.91 s for lengths 64/68.
The previous generating calculations used 24.87201 CPU seconds, so the projected cumulative total is below 35 CPU seconds within the original 60 CPU-second budget.

The physical calculation is assigned CPU 5 with hard limits of 60 CPU seconds and 100 MiB.
The scalar calculation is assigned CPU 2 with limits of 120 CPU seconds and 256 MiB.
This work was authorized separately after the positive n = 30 result.
No n = 26 run is included.
