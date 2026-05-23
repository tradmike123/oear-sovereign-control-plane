import os
import sys
import subprocess
import argparse

def run_command(cmd, description):
    print(f"\n>>> {description}...")
    try:
        # Use shell=True for Windows compatibility with scripts
        result = subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILED: {description}")
        return False

def main():
    parser = argparse.ArgumentParser(description="OEAR Sovereign Control Center")
    parser.add_argument("action", choices=["certify", "dashboard", "shadow", "demo", "install"], 
                        help="Action to perform")
    
    args = parser.parse_args()

    if args.action == "certify":
        # Cleanup existing logs for fresh certification
        for log in ["oear_journal.jsonl", "oear_metrics.jsonl", "oear_shadow_journal.jsonl"]:
            if os.path.exists(log):
                os.remove(log)
        
        # Run harness + validator
        if run_command("python run_synthetic_harness.py", "Executing Synthetic Harness"):
            run_command("python oear_validator.py --harness", "OEAR Mechanical Certification")
    
    elif args.action == "dashboard":
        run_command("python telemetry_dashboard.py", "Generating Longitudinal Dashboard")
    
    elif args.action == "shadow":
        run_command("python shadow_reporter.py", "Generating Shadow Audit Differential Report")
    
    elif args.action == "demo":
        run_command("python run_demo.py", "Executing OEAR Core Demo")
        
    elif args.action == "install":
        run_command("python install_gates.py", "Installing OEAR Quality Gates (Hooks)")

if __name__ == "__main__":
    main()
