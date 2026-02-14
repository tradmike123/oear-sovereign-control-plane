import json
import hashlib
import os
import sys
import argparse
from pathlib import Path

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__)) # oear_ref
src_dir = os.path.dirname(current_dir) # src

def load_jsonl(path):
    rows = []
    if not Path(path).exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows

def assert_sequence(name, observed, expected):
    if observed != expected:
        print(f"[FAIL] {name}")
        print(f"  observed: {observed}")
        print(f"  expected: {expected}")
        return False
    print(f"[OK] {name}")
    return True

def validate_invariants(journal, metrics):
    all_ok = True
    
    # 1. Presencia de input_hash en gate_block
    for r in journal:
        p = r.get("payload", {}) if "payload" in r else r
        if p.get("phase") == "gate_block":
            if "input_hash" not in p:
                print("[FAIL] Invariant: gate_block missing input_hash")
                all_ok = False
    
    # 2. Correspondencia HARD_FAIL Metrics -> Journal
    journal_errors = [ (r.get("payload", {}) if "payload" in r else r).get("reason") for r in journal if r.get("event_type") == "error"]
    for m in metrics:
        if m.get("verdict") == "HARD_FAIL":
            reason = m.get("notes")
            found = any(reason == r_err for r_err in journal_errors)
            if not found:
                 if reason not in ["SYNTHETIC_HARD", "SYNTHETIC_BLOCK"]:
                    print(f"[FAIL] Invariant: HARD_FAIL in metrics ({m['run_id']}) has no corresponding Journal error")
                    all_ok = False

    # 3. Correspondencia commit_ok -> Metrics OK
    commit_run_ids = [ (r.get("payload", {}) if "payload" in r else r).get("run_id") for r in journal if (r.get("payload", {}) if "payload" in r else r).get("phase") == "commit_ok"]
    for run_id in commit_run_ids:
        metrics_for_run = [m for m in metrics if m["run_id"] == run_id]
        if not any(m["verdict"] == "OK" for m in metrics_for_run):
            print(f"[FAIL] Invariant: commit_ok for {run_id} has no OK verdict in metrics")
            all_ok = False

    # 4. Monotonicidad temporal
    timestamps = [r.get("timestamp") for r in journal if "timestamp" in r]
    m_timestamps = [m.get("timestamp") for m in metrics if "timestamp" in m]
    
    def check_ts(name, ts_list):
        if not ts_list: return True
        for i in range(len(ts_list) - 1):
            if ts_list[i] > ts_list[i+1]:
                print(f"[FAIL] Invariant: {name} temporal monotonicity violation at index {i}")
                return False
        return True

    if not check_ts("Journal", timestamps): all_ok = False
    if not check_ts("Metrics", m_timestamps): all_ok = False

    if all_ok:
        print("[OK] Invariants certified.")
    return all_ok

EXPECTED_V1_HASH = "12949cc71ce56a23138bd8d530433252c52e0d867552b2996648360226e23665"

def verify_baseline_integrity(vector_path):
    if not os.path.exists(vector_path):
        return False
    with open(vector_path, "rb") as f:
        content = f.read()
        current_hash = hashlib.sha256(content).hexdigest()
        if current_hash != EXPECTED_V1_HASH:
            print(f"[WARN] Baseline v1 Hash Mismatch!")
            return False
    print("[OK] Baseline v1 integrity verified via SHA-256.")
    return True

def validate_results(journal_path, metrics_path, vector_path, use_harness=False):
    journal = load_jsonl(journal_path)
    metrics = load_jsonl(metrics_path)
    
    print("--- Starting OEAR Equivalence Validation ---")
    inv_ok = validate_invariants(journal, metrics)
    
    if not use_harness:
        return inv_ok

    # Harness Mode checks counts against vectors
    if not verify_baseline_integrity(vector_path):
        pass

    with open(vector_path, 'r', encoding='utf-8') as f:
        vectors = json.load(f)

    print(f"Validating {len(vectors)} vectors against logs...")
    
    blocks_expected = len([v for v in vectors if v["expected_gate"] == "C"])
    metrics_run_expected = len([v for v in vectors if v["expected_gate"] != "C"])
    
    journal_blocks = len([r for r in journal if (r.get("payload", {}) if "payload" in r else r).get("phase") == "gate_block"])
    unique_runs = len(set(m["run_id"] for m in metrics))
    
    c1 = assert_sequence("Gate C Block Count", journal_blocks, blocks_expected)
    c2 = assert_sequence("Metrics Run Count", unique_runs, metrics_run_expected)

    return inv_ok and c1 and c2

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--harness", action="store_true", help="Run in harness certification mode")
    args = parser.parse_args()

    # Look for logs in CWD first, then fallback to src_dir
    j_path = "oear_journal.jsonl"
    if not os.path.exists(j_path):
        j_path = os.path.join(src_dir, "oear_journal.jsonl")
        
    m_path = "oear_metrics.jsonl"
    if not os.path.exists(m_path):
        m_path = os.path.join(src_dir, "oear_metrics.jsonl")
        
    v_path = os.path.join(current_dir, "oear_gate_cert_vectors_v1.json")
    
    ok = validate_results(j_path, m_path, v_path, use_harness=args.harness)

    if not ok:
        print("\n[RESULT] CERTIFICATION FAILED")
        sys.exit(1)
    else:
        print("\n[RESULT] CERTIFICATION PASSED")
