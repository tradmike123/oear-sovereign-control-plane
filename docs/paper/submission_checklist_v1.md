# OEAR Submission Checklist: Reproducibility & Artifact Integrity

This checklist is designed to meet the high standards of the **cs.SE (Software Engineering)** research community, ensuring that the OEAR architecture is presented as a verifiable and reproducible artifact.

## 1. Artifact Completeness
- [ ] **Deterministic Harness**: Is the `run_synthetic_harness.py` executable without external dependencies (e.g., LLM API keys)?
- [ ] **Vector Set Baseline**: Does the `oear_gate_cert_vectors_v1.json` include all 23 scenarios described in the paper?
- [ ] **Cryptographic Anchor**: Is the SHA-256 hash of the baseline vector set explicitly stated and verifiable in the code (`oear_validator.py`)?
- [ ] **Forensic Trace**: Does the system generate `oear_journal.jsonl` and `oear_metrics.jsonl` upon execution?

## 2. Documentation & Methodology
- [ ] **Paper-to-Code Parity**: Do the Process Stack layers (PS0–PS3) in the paper match the class naming in `oear/processes.py`?
- [ ] **Protocol Specification**: Is the logic for Gate selection (A/B/C) and Output Validation (SOFT/HARD FAIL) formally described?
- [ ] **Reproducibility Section**: Does the paper include a dedicated section with step-by-step commands for a local build and certification?

## 3. Engineering Rigor (cs.SE Specific)
- [ ] **Quality Gates**: Is the integration with Git Hooks (`pre-commit`, `pre-push`) documented as a method to prevent governance regression?
- [ ] **Telemetry Integrity**: Does the `telemetry_dashboard.py` demonstrate how drift is measured across different commits?
- [ ] **Shadow Governance Proof**: Can the `shadow_reporter.py` generate a differential delta between two policy versions?

## 4. Submission Metadata
- [ ] **Archive Format**: Is the LaTeX source ready for arXiv (no unused packages, clean BIBTeX)?
- [ ] **License**: Is the MIT License file included in the root directory?
- [ ] **Version Tag**: Is the `OEAR-cert-baseline-v1` tag clearly identified as the bench-marking point?

---
*Status: Ready for mechanical certification audit.*
