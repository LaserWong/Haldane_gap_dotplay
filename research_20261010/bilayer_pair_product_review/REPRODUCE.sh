#!/bin/sh
set -eu
cd "$(dirname "$0")"
python verify_seal.py
taskset -c 6 python verify.py
