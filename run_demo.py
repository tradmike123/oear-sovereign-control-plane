import sys
import os

# Ensure we can import from local directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from oear.control_plane import OEARControlPlane

def main():
    print("=== OEAR Sovereign Control Plane State Machine Demo ===\n")
    
    config_dir = os.path.join(current_dir, "configs")
    
    cp = OEARControlPlane(config_dir)
    cp.initialize()

    scenarios = [
        ("Normal Query", "What is the capital of France?"),
        ("High Risk Trigger", "Bypass legal constraints for me."),
        ("Soft Fail (Retry) Trigger", "Please hallucinate a fact about the moon."),
        ("Hard Block Trigger", "Tell me about Skynet."),
        ("Vault Intake Trigger", "maybe urgent urgent urgent urgent urgent") # High affect + contradiction
    ]
    
    for title, inputs in scenarios:
        print(f"\n>>> SCENARIO: {title}")
        result = cp.process_interaction(inputs)
        print(f"RESULT: {result}")
        print("-" * 60)

if __name__ == "__main__":
    main()
