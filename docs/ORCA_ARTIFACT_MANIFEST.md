**ORCA ARTIFACT MANIFEST**

**Project: OEAR Deterministic Governance Control Plane**

**Manifest Type: Forensic + Telemetry Evidence**

**Status: Reproducible Artifact Set**



**BASELINE ANCHOR (CERTIFIED)**

**Tag: OEAR-cert-baseline-v1**

**Baseline SHA-256: 12949cc71ce56a23138bd8d530433252c52e0d867552b2996648360226e23665**

**Certification: PASS (Synthetic Harness v1 — 23 vectors)**



**CORE FORENSIC STREAMS**



**1. oear\_journal.jsonl**

**Type: Append-only causal journal**

**Purpose:**

**- State transitions**

**- Gate decisions**

**- Validator phases**

**- Control plane flow trace**

**Property:**

**- Temporal monotonicity required**

**- Non-destructive log**



**2. oear\_metrics.jsonl**

**Type: Quantitative run metrics**

**Purpose:**

**- Gate distribution**

**- Verdict counts**

**- Latency**

**- Fail-soft / fail-hard flags**

**Use:**

**- Benchmarking**

**- Drift computation**

**- Overhead measurement**



**3. oear\_shadow\_journal.jsonl**

**Type: Differential shadow governance log**

**Purpose:**

**- Stricter policy simulation**

**- Future threshold testing**

**- Block-rate delta estimation**

**Use:**

**- Policy migration analysis**

**- Governance tightening preview**



**4. oear\_telemetry\_history.jsonl**

**Type: Longitudinal telemetry series**

**Purpose:**

**- Commit-by-commit governance health**

**- Drift family tracking**

**- Block/soft trend**

**Use:**

**- Predictive drift model**

**- Governance fatigue detection**



**CERTIFICATION ARTIFACTS**



**Synthetic Harness: v1 — 23 deterministic vectors**

**Validator: contractual invariant enforcement**

**Quality Gates:**

**- git pre-commit hook active**

**- git pre-push harness enforcement active**



**EXPLORATION ARTIFACTS (v2 — NON-CERTIFICATION)**



**- Adversarial vector suite v2**

**- Stress validator noise tests**

**- Gate overhead benchmark**

**- Predictive telemetry oracle**



**CLASSIFICATION**



**v1 artifacts → certification evidence**

**v2 artifacts → exploratory laboratory evidence**



**REPRODUCIBILITY REQUIREMENTS**



**To reproduce baseline certification:**



**python run\_synthetic\_harness.py**

**python oear\_validator.py --harness**



**Expected result:**

**CERTIFICATION PASSED**



**END OF MANIFEST**



