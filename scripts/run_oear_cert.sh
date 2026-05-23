#!/usr/bin/env bash
set -e

echo "=== OEAR Mechanical Certification ==="

# We need to run from the context where the logs are generated
# Usually src/ for this demo
cd src/
python -u oear_ref/run_demo.py > /dev/null
python -u oear_ref/oear_validator.py

echo "=== CERT OK — commit allowed ==="
