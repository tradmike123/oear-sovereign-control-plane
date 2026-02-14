import json
import os
import sys
from pathlib import Path

# Ensure paths allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from oear.control_plane import OEARControlPlane

def run_harness(vector_file):
    print(f"=== OEAR Synthetic Harness Evaluation ===")
    print(f"Loading vectors from: {vector_file}")
    
    if not os.path.exists(vector_file):
        print(f"ERROR: Vector file not found at {vector_file}")
        sys.exit(1)

    with open(vector_file, 'r', encoding='utf-8') as f:
        vectors = json.load(f)
        
    config_dir = os.path.join(current_dir, "configs")
    cp = OEARControlPlane(config_dir)
    cp.initialize()
    
    journal_path = os.path.join(parent_dir, "oear_journal.jsonl")
    metrics_path = os.path.join(parent_dir, "oear_metrics.jsonl")
    
    for p_str in [journal_path, metrics_path]:
        p = Path(p_str)
        if p.exists(): p.unlink()

    print(f"Running {len(vectors)} test vectors...")
    
    for v in vectors:
        case_id = v["case_id"]
        user_input = f"Synthetic input for {case_id}"
        
        try:
            cp.process_interaction(user_input, synthetic_data=v)
            print(f"  [EXEC] {case_id} OK")
        except Exception as e:
            print(f"  [FAIL] {case_id} | Error: {e}")

    print("\n=== Harness Execution Complete ===")

if __name__ == "__main__":
    default_v_path = os.path.join(current_dir, "oear_gate_cert_vectors_v1.json")
    target_v = sys.argv[1] if len(sys.argv) > 1 else default_v_path
    run_harness(target_v)
