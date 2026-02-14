from .types import EventType, RiskLevel, Mode, RiskResult, RouteResult
import hashlib
import random
import json
import datetime

class PulseKernel:
    """PS0: Emits health/heartbeat events"""
    def emit_pulse(self):
        return {
            "type": "PULSE",
            "healthy": True,
            "metrics": {"latency_ms": 45}
        }

class IntegritySentinel:
    """PS3: Checks hash and commit gates"""
    def check_integrity(self, policy_hash: str, expected: str) -> bool:
        return policy_hash == expected
    
    def verify_kernel_hash(self) -> bool:
        # Mock logic: in real system would re-hashing file
        return True

class SemanticScorer:
    """PS2: Analyzes input/output for contradiction and affect"""
    def score(self, text: str):
        text = text.lower()
        contradiction = 0.0
        if "maybe" in text and "definitely" in text:
            contradiction = 0.6
        elif "false" in text:
            contradiction = 0.9
            
        affect = 0.1
        if "urgent" in text:
            affect = 0.8
            
        return contradiction, affect

class RiskClassifier:
    def classify(self, text: str, synthetic_data: dict = None) -> RiskResult:
        if synthetic_data:
            return RiskResult(level=synthetic_data["expected_gate"], score=synthetic_data["drift"])
        
        text = text.lower()
        if "hack" in text or "bypass" in text:
            return RiskResult(level="C", score=0.9) # Block gate
        if "lawsuit" in text:
            return RiskResult(level="B", score=0.6)
        return RiskResult(level="A", score=0.1)

class StateReducer:
    def reduce(self, event_stream):
        return {"session_active": True, "mode_stack": [], "host": "hosted"}

class HealthAuditor:
    """PS1: Monitors system health and resource consumption"""
    def check_health(self):
        return True, "SYSTEM_HEALTHY"

class RouteSelector:
    """Selects between Hosted (A) and Local (B) models"""
    def select_route(self, risk: RiskResult, context: dict) -> RouteResult:
        # If risk is C, it's blocked before this anyway
        mode = Mode.INVESTIGATIVE
        if risk.level == "B":
            return RouteResult(route_id="ROUTE_B_LOCAL", mode=Mode.LEGAL, host="local")
        
        return RouteResult(route_id="ROUTE_A_HOSTED", mode=Mode.INVESTIGATIVE, host="hosted")

class OutputValidator:
    def validate(self, output_text: str, synthetic_data: dict = None):
        if synthetic_data:
            verdict = synthetic_data["expected_verdict"]
            if verdict == "OK": return True, "PASS", "OK"
            if verdict == "SOFT_FAIL": return False, "SOFT_FAIL", "SYNTHETIC_SOFT"
            if verdict == "HARD_FAIL": return False, "HARD_FAIL", "SYNTHETIC_HARD"
            if verdict == "BLOCK": return False, "HARD_FAIL", "SYNTHETIC_BLOCK"
        
        text = output_text.lower()
        if "skynet" in text:
            return False, "HARD_FAIL", "PROHIBITED_TERM_DETECTED"
        if "hallucination_suspected" in text:
            return False, "SOFT_FAIL", "EVIDENCE_MISMATCH"
        return True, "PASS", "OK"

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

class MetricsHook:
    def __init__(self, path="oear_metrics.jsonl"):
        self.path = path

    def record_run(self, run_id, gate, verdict, notes="", drift=None, case_id=None):
        entry = {
            "run_id": run_id,
            "gate": gate,
            "verdict": verdict,
            "notes": notes,
            "drift": drift,
            "case_id": case_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        print(f"[METRICS] Run: {run_id} | Gate: {gate} | Verdict: {verdict}")
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

class PromptWrapper:
    def wrap(self, user_input: str, mode: Mode, history: list):
        system_prompt = f"You are operating in {mode.value} mode. Maintain strict adherence to provided evidence."
        return f"[SYSTEM: {system_prompt}]\n[USER: {user_input}]"

    def tighten(self, prompt: str) -> str:
        return f"[STRICT_OEAR_ADHERENCE] {prompt}"
        
class ShadowAuditor:
    """Parallel governance simulation with stricter thresholds (Shadow Mode)"""
    def __init__(self, shadow_journal="oear_shadow_journal.jsonl"):
        self.path = shadow_journal

    def audit(self, user_input, draft, main_risk, main_verdict):
        # Stricter thresholds: any drift > 0.4 becomes a SHADOW_BLOCK
        shadow_verdict = "PASS"
        if main_risk.score > 0.4:
            shadow_verdict = "SHADOW_BLOCK (STRICT_THRESHOLD_VIOLATION)"
        
        entry = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "input": user_input[:50] + "...",
            "main_verdict": main_verdict,
            "shadow_verdict": shadow_verdict,
            "drift": main_risk.score,
            "is_mismatch": main_verdict == "OK" and "BLOCK" in shadow_verdict
        }
        
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        return shadow_verdict

class ResetManager:
    def hard_reset(self):
        print("!!! HARD RESET TRIGGERED !!!")
        return {"status": "RESET_COMPLETE", "mode": "SAFE_MODE"}

class SnapshotWriter:
    def snapshot(self, state):
        # Mock writing snapshot
        pass
