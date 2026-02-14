from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import datetime

@dataclass
class RiskResult:
    level: str  # "A", "B", "C"
    score: float = 0.0

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class RouteResult:
    route_id: str
    mode: "Mode"
    host: str = "hosted"

class EventType(Enum):
    USER_INPUT = "user_input"
    MODEL_OUTPUT = "model_output"
    SYSTEM_INTERNAL = "system_internal"
    ERROR = "error"
    STATE_CHANGE = "state_change"

@dataclass
class PulseEvent:
    timestamp: str
    event_type: EventType
    payload: Dict[str, Any]
    source: str = "oear_kernel"

@dataclass
class TraceDelta:
    session_id: str
    timestamp_utc: str
    changes: List[Dict[str, Any]] = field(default_factory=list)
    validations: List[str] = field(default_factory=list)
    next_actions: List[str] = field(default_factory=list)

@dataclass
class PolicyConfig:
    schema_version: str
    invariants: List[str]
    change_control: Dict[str, Any]
    compatibility: Dict[str, Any]

@dataclass
class VaultItem:
    content: str
    contradiction_score: float
    affect_intensity: float
    timestamp: str
    status: str = "pending_review"

class Mode(Enum):
    INVESTIGATIVE = "investigative"
    LEGAL = "legal"
    TECHNICAL = "technical"
    EDITORIAL = "editorial"
    DEFAULT = "default"

@dataclass
class ModeStack:
    base_mode: Mode
    secondary_modes: List[Mode] = field(default_factory=list)

class SystemState(Enum):
    BOOT = "BOOT"
    LOAD_CANON = "LOAD_CANON"
    REBUILD_STATE = "REBUILD_STATE"
    INTEGRITY_GATE = "INTEGRITY_GATE"
    SOFT_RESYNC = "SOFT_RESYNC"
    PULSE_PS0 = "PULSE_PS0"
    HEALTH_PS1 = "HEALTH_PS1"
    SCORE_PS2 = "SCORE_PS2"
    VAULT_INTAKE = "VAULT_INTAKE"
    ROUTE_SELECT = "ROUTE_SELECT"
    ROUTE_A = "ROUTE_A"
    ROUTE_B = "ROUTE_B"
    BUILD_WRAPPER = "BUILD_WRAPPER"
    LLM_CALL = "LLM_CALL"
    VALIDATE_OUTPUT = "VALIDATE_OUTPUT"
    COMMIT = "COMMIT"
    RETRY_SOFT = "RETRY_SOFT"
    HARD_BLOCK = "HARD_BLOCK"
    DONE = "DONE"
