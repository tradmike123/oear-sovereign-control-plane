from .types import VaultItem
import json
import datetime
import uuid

class DeferredVault:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        
    def triage(self, content: str, contradiction_score: float, affect_intensity: float) -> str:
        """
        Decision engine: if ambigous or risky, store for later.
        Returns 'STORED' or 'IMMEDIATE'
        """
        # Example naive threshold
        if contradiction_score > 0.7 or (contradiction_score > 0.4 and affect_intensity > 0.8):
            self._store_item(content, contradiction_score, affect_intensity)
            return "STORED"
        
        return "IMMEDIATE"

    def _store_item(self, content, c_score, a_score):
        pk = str(uuid.uuid4())
        item = {
            "id": pk,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "contradiction_score": c_score,
            "affect_intensity": a_score,
            "content_snippet": content[:200], # truncated for metadata
            "status": "pending_review"
        }
        
        # In a real system, full content would be blob-stored. Here inline.
        item["full_content"] = content
        
        with open(self.storage_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(item) + '\n')
            
    def get_pending(self):
        items = []
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        items.append(json.loads(line))
        except FileNotFoundError:
            pass
        return items
