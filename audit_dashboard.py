import json
import os
import glob

def run_audit():
    print("=== OEAR Audit Dashboard ===")
    
    # 1. Journal Summary
    journal_path = "oear_journal.jsonl"
    if os.path.exists(journal_path):
        with open(journal_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"Total Journal Events: {len(lines)}")
            # Count by type
            counts = {}
            for line in lines:
                evt = json.loads(line)
                etype = evt.get("event_type")
                counts[etype] = counts.get(etype, 0) + 1
            print(f"Event Distribution: {counts}")
    else:
        print("Journal not found.")

    # 2. Vault Summary
    vault_path = "oear_vault.jsonl"
    if os.path.exists(vault_path):
        with open(vault_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"Items in Deferred Vault: {len(lines)}")
            for line in lines:
                item = json.loads(line)
                print(f" - [{item['timestamp']}] Conflict: {item['contradiction_score']} Snippet: {item['content_snippet']}")
    else:
         print("Vault is empty.")

    # 3. Traces
    trace_files = glob.glob("traces/*.json")
    print(f"Total TRACE Deltas: {len(trace_files)}")
    
    print("\n--- End of Audit ---")

if __name__ == "__main__":
    run_audit()
