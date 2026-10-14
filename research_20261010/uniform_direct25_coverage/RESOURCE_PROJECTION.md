# Cost projection for the MPS25 anchor

Only the own-length MPS25 anchor is included. The validated combined small-power engine took 2.329 CPU seconds at lengths 12/16/20/24, compared with 8–10 seconds for the generic 128-power engine. The unchanged matrix multiplication needs only binary powers 1, 2, 4, 8, and 16 for 25−2=23.

The projected cost is less than 3 CPU seconds and 35 MiB. The proposed hard limits are 7 CPU seconds and 100 MiB on CPU5, within the remaining original allowance of 7.36279 CPU seconds. No other anchor is included. The separate scalar calculation is limited to 30 CPU seconds and 256 MiB on CPU2.
