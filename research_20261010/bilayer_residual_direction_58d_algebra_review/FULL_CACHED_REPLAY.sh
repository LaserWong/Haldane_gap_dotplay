#!/bin/bash
# Requires a new authorization; the environment flag itself does not authorize work.
set -euo pipefail
[ "${SEPARATELY_AUTHORIZED_CACHED_REPLAY:-}" = YES ] || { echo 'A new60CPU-second/256MiB cached-review authorization is required.' >&2; exit 2; }
echo 'Copy this sealed review to a fresh directory at the same repository depth, verify dependencies, then run: /usr/bin/python3 measure.py fresh_metrics.json 256 60 /usr/bin/python3 audit.py'
echo 'Do not overwrite the frozen original audit.json. No physical contractions are required.'
