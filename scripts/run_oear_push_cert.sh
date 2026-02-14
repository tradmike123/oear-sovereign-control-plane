#!/usr/bin/env bash
set -e

echo "=== OEAR Synthetic Harness Certification (Pre-Push) ==="

# 1. Run Harness
python -u src/oear_ref/run_synthetic_harness.py

# 2. Run Validator in Harness mode
python -u src/oear_ref/oear_validator.py --harness

# 3. Update and Display Longitudinal Telemetry
python -u src/oear_ref/telemetry_dashboard.py

echo "=== CERT OK — push allowed ==="
