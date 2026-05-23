import json
import os
import datetime
from .types import TraceDelta

class ContinuitySubstrate:
    def __init__(self, trace_dir: str):
        self.trace_dir = trace_dir
        if not os.path.exists(trace_dir):
            os.makedirs(trace_dir)

    def emit_trace(self, session_id: str, changes: list, validations: list):
        """
        6.1 TRACE Delta Format (Recommended)
        """
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        trace = TraceDelta(
            session_id=session_id,
            timestamp_utc=timestamp,
            changes=changes,
            validations=validations,
            next_actions=[]
        )
        
        filename = f"trace_{session_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.trace_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(trace.__dict__, f, indent=2)
            
        return filepath

    def create_compendium(self, session_id: str):
        """
        Periodic compendia as curated state.
        """
        # In a real system, this would aggregate TRACE deltas
        pass
