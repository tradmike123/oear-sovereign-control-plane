import json
import os
import datetime
from .types import EventType, PulseEvent

class Journal:
    def __init__(self, journal_path: str):
        self.journal_path = journal_path
        # Ensure file exists
        if not os.path.exists(journal_path):
            with open(journal_path, 'w', encoding='utf-8') as f:
                pass # Create empty file

    def append(self, event_type: EventType, payload: dict, source: str = "oear_kernel"):
        """
        Appends an event to the immutable journal.
        Format: JSONL (one JSON object per line)
        """
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        entry = {
            "timestamp": timestamp,
            "event_type": event_type.value,
            "source": source,
            "payload": payload
        }
        
        # Write to disk immediately (flushing)
        with open(self.journal_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
            f.flush()
            
    def read_all(self):
        """
        Replays the journal from disk.
        """
        events = []
        if not os.path.exists(self.journal_path):
            return []
            
        with open(self.journal_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return events
