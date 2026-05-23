import hashlib
from .types import EventType, RiskLevel, SystemState

def oear_step_implementation(user_input, oear_cp):
    """
    Implementation of the OEAR 'hilo' (thread) logic as per pseudocódigo.
    This demonstrates the core logic loop of a single governing step.
    """
    
    # 1) Reducir eventos -> estado
    # oear_cp.reducer.reduce() performs the event sourcing translation
    event_log = oear_cp.journal.read_all()
    state = oear_cp.reducer.reduce(event_log)
    
    # 2) Clasificar riesgo del input
    # risk classifies social/legal/identity risk without censorship
    risk = oear_cp.risk_classifier.classify(user_input)
    
    # 3) Gate de ruta
    # route = "B" (Local) if high risk on hosted, else "A" 
    route = oear_cp.router.select_route(risk, {"host": "hosted"})
    
    # 4) Construir wrapper (contexto mínimo + invariantes + tarea + formato)
    # Determined by MOE (Skill Graph)
    skill_stack = oear_cp.mode_orchestrator.resolve_stack(user_input, risk.name.lower())
    wrapper = oear_cp.wrapper.wrap(user_input, skill_stack[0].mode, [])
    
    # 5) Ejecutar LLM (subrutina)
    draft = oear_cp._mock_llm(user_input, route, skill_stack[0].mode)
    
    # 6) Validar salida
    is_valid, fail_type, reason = oear_cp.validator.validate(draft, [])
    
    if fail_type == "SOFT_FAIL":
        # retry logic: tighten_wrapper
        print(f"[OEAR] SOFT_FAIL: {reason}. Tightening wrapper and retrying...")
        wrapper = "[STRICT CONTEXT] " + wrapper 
        draft = oear_cp._mock_llm(user_input, route, skill_stack[0].mode)
        is_valid, fail_type, reason = oear_cp.validator.validate(draft, [])
        
    if fail_type == "HARD_FAIL":
        # log_event("PS3_PERMISSION_BLOCK")
        oear_cp.journal.append(EventType.ERROR, {"type": "PS3_PERMISSION_BLOCK", "reason": reason})
        return "[OEAR] SAFE_RESPONSE: Output blocked due to policy constraints."

    # 7) Registrar eventos + actualizar estado
    content_hash = hashlib.sha256(draft.encode()).hexdigest()
    oear_cp.journal.append(EventType.MODEL_OUTPUT, {"summary_hash": content_hash})
    
    return draft
