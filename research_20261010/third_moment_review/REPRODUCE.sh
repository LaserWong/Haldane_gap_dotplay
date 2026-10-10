#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python verify_manifest.py
python verify_inputs.py
python run_limited.py python audit_geometry.py >logs/geometry_driver.log 2>&1
python run_limited.py python audit_matrices.py >logs/matrix_and_rayleigh.log 2>&1
python run_limited.py python audit_physical.py >logs/physical.log 2>&1
python run_limited.py python audit_scalar.py >logs/scalar.log 2>&1
python run_limited.py python test_adversarial.py >logs/adversarial.log 2>&1
python verify_inputs.py
cat logs/{geometry_driver,matrix_and_rayleigh,physical,scalar,adversarial}.log
