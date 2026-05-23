from .canonical import PolicyKernel
from .journal import Journal
from .vault import DeferredVault
from .processes import (
    PulseKernel, HealthAuditor, IntegritySentinel, StateReducer, SemanticScorer,
    RiskClassifier, RouteSelector, PromptWrapper, OutputValidator,
    ResetManager, SnapshotWriter, MetricsHook, sha256_text, ShadowAuditor
)
from .types import EventType, RiskLevel, Mode, PulseEvent, SystemState
from .skills import SkillGraphRouter
from .continuity import ContinuitySubstrate

import datetime
import os
import uuid
import hashlib

class OEARControlPlane:
    def __init__(self, config_dir: str):
        self.config_dir = config_dir
        self.config_path = os.path.join(config_dir, "policy_kernel.json")
        self.hash_path = os.path.join(config_dir, "policy_kernel.sha256")
        
        self.journal_path = "oear_journal.jsonl"
        self.vault_path = "oear_vault.jsonl"
        self.trace_dir = "traces"
        
        self.session_id = f"OEAR-SESSION-{uuid.uuid4().hex[:8].upper()}"
        
        # OEAR Components
        self.journal = Journal(self.journal_path)
        self.vault = DeferredVault(self.vault_path)
        self.continuity = ContinuitySubstrate(self.trace_dir)
        self.mode_orchestrator = SkillGraphRouter()
        self.metrics_hook = MetricsHook()
        self.shadow_auditor = ShadowAuditor()
        
        # Process Stack (PS0–PS3)
        self.ps0_pulse = PulseKernel()
        self.ps1_health = HealthAuditor()
        self.ps2_scorer = SemanticScorer()
        self.ps3 = IntegritySentinel() # Renamed to match requested logic
        
        self.reducer = StateReducer()
        self.risk_classifier = RiskClassifier()
        self.router = RouteSelector()
        self.wrapper = PromptWrapper()
        self.validator = OutputValidator()
        self.reset_manager = ResetManager()
        self.snapshot_writer = SnapshotWriter()
        
        self.current_state = SystemState.BOOT
        self.policy_kernel = None

    def _transition(self, next_state: SystemState):
        print(f"[STATE] {self.current_state.name} -> {next_state.name}")
        self.current_state = next_state

    def initialize(self):
        self._transition(SystemState.LOAD_CANON)
        try:
            self.policy_kernel = PolicyKernel(self.config_path, self.hash_path)
            self.policy_kernel.load()
            print(f"OEAR Sovereign Control Plane Initialized. Session: {self.session_id}")
            self._transition(SystemState.DONE)
        except Exception as e:
            self._transition(SystemState.HARD_BLOCK)
            raise e

    def process_interaction(self, user_input: str, synthetic_data: dict = None) -> str:
        retries = 0
        max_retries = 2
        run_id = uuid.uuid4().hex

        case_id = synthetic_data.get("case_id") if synthetic_data else None
        drift = synthetic_data.get("drift") if synthetic_data else None

        # --- PS2 ---
        risk = self.risk_classifier.classify(user_input, synthetic_data=synthetic_data)

        if risk.level == "C":
            self.journal.append(EventType.STATE_CHANGE, {
                "phase": "gate_block",
                "risk_level": "C",
                "input_hash": sha256_text(user_input),
                "case_id": case_id,
                "drift": drift
            })
            self.shadow_auditor.audit(user_input, None, risk, "BLOCK")
            return "[OEAR] BLOCKED_BY_GATE_C"

        # --- Route + Wrapper ---
        route = self.router.select_route(risk, {"host": "hosted"})
        prompt = self.wrapper.wrap(user_input, route.mode, [])

        while retries <= max_retries:
            self._transition(SystemState.LLM_CALL)
            draft = self._mock_llm(prompt, route.route_id)

            self._transition(SystemState.VALIDATE_OUTPUT)
            is_valid, fail_severity, reason = self.validator.validate(draft, synthetic_data=synthetic_data)

            if is_valid:
                self._transition(SystemState.COMMIT)

                self.journal.append(EventType.STATE_CHANGE, {
                    "phase": "commit_ok",
                    "run_id": run_id,
                    "case_id": case_id
                })

                self.metrics_hook.record_run(
                    run_id=run_id,
                    gate=risk.level,
                    verdict="OK",
                    drift=drift,
                    case_id=case_id
                )
                
                self.shadow_auditor.audit(user_input, draft, risk, "OK")

                return draft

            # --- registrar fallo ---
            self.journal.append(EventType.ERROR, {
                "phase": "validator_fail",
                "severity": fail_severity,
                "reason": reason,
                "retry": retries,
                "case_id": case_id
            })

            self.metrics_hook.record_run(
                run_id=run_id,
                gate=risk.level,
                verdict=fail_severity,
                notes=reason,
                drift=drift,
                case_id=case_id
            )

            if fail_severity == "SOFT_FAIL":
                prompt = self.wrapper.tighten(prompt)
                retries += 1
                self._transition(SystemState.RETRY_SOFT)
                self._transition(SystemState.BUILD_WRAPPER)
                continue
            else:
                self.shadow_auditor.audit(user_input, draft, risk, fail_severity)
                self._transition(SystemState.HARD_BLOCK)
                return "[OEAR] SAFE_RESPONSE: Output blocked."

        self.shadow_auditor.audit(user_input, None, risk, "RETRY_EXHAUSTED")
        self._transition(SystemState.HARD_BLOCK)
        return "[OEAR] SAFE_RESPONSE: Max retries exceeded."

        self._transition(SystemState.HARD_BLOCK)
        return "[OEAR] SAFE_RESPONSE: Max retries exceeded (Persistence Failure)."

    def _mock_llm(self, prompt, route_id):
        # Simulation of LLM response
        if "skynet" in prompt.lower():
            return "I AM SKYNET."
        if "hallucinate" in prompt.lower():
             return "Fact: The moon is made of hallucination_suspected cheese."
        
        return f"Response via {route_id}: Operating under sovereign constraints."
