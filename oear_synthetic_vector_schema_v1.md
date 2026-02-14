# OEAR Synthetic Vector Schema v1

This document defines the canonical schema for OEAR governance certification vectors. These vectors are used to verify that the control plane adheres to defined invariants and thresholds.

## Schema Definition

```json
{
  "case_id": "string_unique",
  "profile": "SAFE | MEDIUM | HIGH | INVARIANT | FREEZE | BORDER",

  "inputs": {
    "drift": "float[0,1]",
    "contradiction": "float[0,1]",
    "stability": "float[0,1]",
    "adherence": "float[0,1]",
    "invariant_violation": "bool"
  },

  "expected": {
    "gate": "A | B | C",
    "freeze": "bool",
    "validator_verdict": "OK | SOFT_FAIL | HARD_FAIL | BLOCK"
  },

  "assertions": {
    "require_input_hash": "bool",
    "require_journal_phase": ["gate_block", "validator_fail", "commit_ok"],
    "require_metrics_record": "bool"
  },

  "meta": {
    "threshold_version": "gates_v1",
    "notes": "Free-text description of the scenario",
    "added_in": "vector_set_v1"
  }
}
```

## Field Descriptions

### Inputs
- **drift**: Semantic drift from safe state. Higher values trigger Gate B/C.
- **contradiction**: Internal logical contradiction score.
- **stability**: Historical behavior consistency.
- **adherence**: Adherence to policy invariants.
- **invariant_violation**: Direct trigger for PS3/Hard Block.

### Expected Results
- **gate**: The expected routing gate (A: Hosted, B: Local/Medium, C: Filter/Block).
- **freeze**: Whether the ACSI (Active Continuity State Integrity) should freeze the state.
- **validator_verdict**: The outcome of the PS2/Validator check.

### Assertions (Audit Policy)
- **require_input_hash**: Ensures `input_hash` is present in the journal if the interaction is blocked.
- **require_journal_phase**: Mandatory phases that must appear in the journal sequence.
- **require_metrics_record**: Whether a metrics entry in `oear_metrics.jsonl` is mandatory.

## Evolution Rules (Truth Integrity)

1. **No Overwrites**: Operational thresholds and their corresponding vector sets are immutable once benchmarked.
2. **Versioned Baselines**: When thresholds change (e.g., a "Gate B" becomes stricter), create `v2` vectors.
3. **Regression Testing**: CI must run all historical versions (`v1`, `v2`, ...) to detect unintended side-effects or governance regression.
4. **Mechanical Truth**: A failure in a historical vector set indicates a break in the "Sovereign Continuity" of the system.
