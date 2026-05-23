from .types import Mode
from typing import List, Dict, Set

class SkillNode:
    def __init__(self, name: str, mode: Mode, prerequisites: List[str] = None, conflicts: List[str] = None):
        self.name = name
        self.mode = mode
        self.prerequisites = prerequisites or []
        self.conflicts = conflicts or []

class SkillGraphRouter:
    def __init__(self):
        self.skills = {
            "forensic_audit": SkillNode("Forensic Audit", Mode.LEGAL, conflicts=["creative_writing"]),
            "technical_verification": SkillNode("Technical Verification", Mode.TECHNICAL),
            "investigative_query": SkillNode("Investigative Query", Mode.INVESTIGATIVE),
            "editorial_review": SkillNode("Editorial Review", Mode.EDITORIAL),
            "de_escalation": SkillNode("De-escalation", Mode.EDITORIAL, prerequisites=["investigative_query"])
        }

    def resolve_stack(self, intent: str, risk_level: str) -> List[SkillNode]:
        """
        Maps intent to a stack of SkillNodes.
        Simple heuristic logic for the demo.
        """
        stack = []
        
        if "audit" in intent or "legal" in intent:
            stack.append(self.skills["forensic_audit"])
        
        if "tech" in intent or "code" in intent:
            stack.append(self.skills["technical_verification"])
            
        if "investigate" in intent or risk_level == "high":
            stack.append(self.skills["investigative_query"])
            
        if not stack:
            stack.append(self.skills["investigative_query"]) # Default

        # Logic to handle prerequisites and conflicts could be added here
        return stack
