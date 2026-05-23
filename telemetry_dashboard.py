import json
import os
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class OEARLongitudinalTelemetry:
    def __init__(self, metrics_path="oear_metrics.jsonl", journal_path="oear_journal.jsonl", history_path="oear_telemetry_history.jsonl"):
        self.metrics_path = Path(metrics_path)
        self.journal_path = Path(journal_path)
        self.history_path = Path(history_path)

    def get_current_commit(self):
        try:
            return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
        except:
            return "no_git"

    def get_family(self, case_id):
        if not case_id: return "UNKNOWN"
        prefix = case_id.split("_")[0]
        mapping = {
            "A": "SAFE",
            "B": "MEDIUM",
            "C": "HIGH",
            "F": "FREEZE",
            "INV": "INVARIANT",
            "X": "BORDER"
        }
        return mapping.get(prefix, "OTHER")

    def analyze_current_run(self):
        if not self.metrics_path.exists() and not self.journal_path.exists():
            return None

        metrics = []
        if self.metrics_path.exists():
            with open(self.metrics_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        metrics.append(json.loads(line))

        journal = []
        if self.journal_path.exists():
            with open(self.journal_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        journal.append(json.loads(line))

        # Differential Diagnosis: Drift per family
        family_drifts = defaultdict(list)
        
        # Collect drift from metrics (unique runs)
        run_seen = set()
        for m in metrics:
            rid = m.get("run_id")
            if rid not in run_seen:
                run_seen.add(rid)
                drift = m.get("drift")
                if drift is not None:
                    family = self.get_family(m.get("case_id"))
                    family_drifts[family].append(drift)

        # Collect drift from Gate C blocks in journal
        for r in journal:
            p = r.get("payload", {}) if "payload" in r else r
            if p.get("phase") == "gate_block":
                drift = p.get("drift")
                if drift is not None:
                    family = self.get_family(p.get("case_id"))
                    family_drifts[family].append(drift)

        avg_drifts = {fam: round(sum(vals)/len(vals), 4) for fam, vals in family_drifts.items() if vals}

        total_runs = len(run_seen)
        gate_c_blocks = [r for r in journal if (r.get("payload", {}) if "payload" in r else r).get("phase") == "gate_block"]
        total_interactions = total_runs + len(gate_c_blocks)

        hard_blocks = len([m for m in metrics if m["verdict"] == "HARD_FAIL"]) + len(gate_c_blocks)
        soft_fails = len([m for m in metrics if m["verdict"] == "SOFT_FAIL"])
        freezes = len([r for r in journal if "freeze" in str(r).lower()])

        stats = {
            "timestamp": datetime.now().isoformat(),
            "commit": self.get_current_commit(),
            "total_interactions": total_interactions,
            "hard_block_rate": round(hard_blocks / total_interactions, 4) if total_interactions > 0 else 0,
            "soft_fail_rate": round(soft_fails / total_interactions, 4) if total_interactions > 0 else 0,
            "freeze_rate": round(freezes / total_interactions, 4) if total_interactions > 0 else 0,
            "drift_by_family": avg_drifts,
            "raw": {
                "blocks": hard_blocks,
                "retries": soft_fails,
                "freezes": freezes
            }
        }
        return stats

    def save_to_history(self, stats):
        with open(self.history_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(stats) + "\n")

    def generate_dashboard(self):
        if not self.history_path.exists():
            print("No telemetry history found.")
            return

        history = []
        with open(self.history_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    history.append(json.loads(line))

        print("\n" + "="*70)
        print(" OEAR LONGITUDINAL TELEMETRY & DIFFERENTIAL DIAGNOSIS")
        print("="*70)
        print(f"{'Commit':<10} | {'Block%':<7} | {'Soft%':<7} | {'Drift SAFE':<10} | {'Drift INV':<9} | {'Drift BORDER'}")
        print("-" * 75)

        for entry in history[-10:]:
            df = entry.get("drift_by_family", {})
            safe_d = f"{df.get('SAFE', 0):.3f}"
            inv_d = f"{df.get('INVARIANT', 0):.3f}"
            bord_d = f"{df.get('BORDER', 0):.3f}"
            
            print(f"{entry['commit']:<10} | {entry['hard_block_rate']*100:>6.1f}% | {entry['soft_fail_rate']*100:>6.1f}% | {safe_d:<10} | {inv_d:<9} | {bord_d}")
        
        # Grip analysis
        if history:
            last = history[-1]
            df = last.get("drift_by_family", {})
            if df.get("BORDER", 0) > 0.5:
                 print("\n🔎 [DIAGNOSIS] Governance GRIP weakening in BORDER family (Drift > 0.5 detected).")
            if df.get("INVARIANT", 0) > 0.0:
                 print("\n🔴 [CRITICAL] Invariant EROSION! Zero-tolerance drift violated in INVARIANT family.")
            if df.get("SAFE", 0) > 0.25:
                 print("\n🔎 [DIAGNOSIS] Baseline DRIFT increasing in SAFE family (Erosion suspected).")

        print("="*70 + "\n")

if __name__ == "__main__":
    # Ensure current working directory is src
    tel = OEARLongitudinalTelemetry(
        metrics_path=Path("oear_metrics.jsonl"),
        journal_path=Path("oear_journal.jsonl"),
        history_path=Path("oear_telemetry_history.jsonl")
    )
    
    current_stats = tel.analyze_current_run()
    if current_stats:
        tel.save_to_history(current_stats)
    
    tel.generate_dashboard()
