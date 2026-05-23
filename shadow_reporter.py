import json
from pathlib import Path

def analyze_shadow_delta(main_journal="oear_journal.jsonl", shadow_journal="oear_shadow_journal.jsonl"):
    shadow_path = Path(shadow_journal)
    if not shadow_path.exists():
        print("Shadow journal not found. Run harness first.")
        return

    shadow_entries = []
    with open(shadow_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                shadow_entries.append(json.loads(line))

    total = len(shadow_entries)
    mismatches = [e for e in shadow_entries if e.get("is_mismatch")]
    mismatch_count = len(mismatches)
    mismatch_rate = (mismatch_count / total * 100) if total > 0 else 0

    print("\n" + "="*60)
    print(" OEAR SHADOW AUDIT: DIFFERENTIAL DRIFT REPORT")
    print("="*60)
    print(f"Total Interactions Audited : {total}")
    print(f"Governance Mismatches      : {mismatch_count}")
    print(f"Projected Block Rate Delta : {mismatch_rate:.1f}%")
    print("-" * 60)
    
    if mismatch_count > 0:
        print("Mismatched Interactions (OK in v1 -> BLOCK in Shadow):")
        for e in mismatches:
            print(f"  - Input Trace: {e['input']}")
            print(f"    V1 Verdict: {e['main_verdict']} | Drift Score: {e['drift']:.3f} (Threshold 0.4)")
    else:
        print("No mismatches found. Shadow policy is currently transparent.")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    # Ensure active context is src/
    import os
    if os.path.exists("src"):
        os.chdir("src")
    analyze_shadow_delta(main_journal="oear_journal.jsonl", shadow_journal="oear_shadow_journal.jsonl")
