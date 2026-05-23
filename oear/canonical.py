import json
import hashlib
import os
from .types import PolicyConfig

class PolicyKernel:
    def __init__(self, config_path: str, hash_path: str):
        self.config_path = config_path
        self.hash_path = hash_path
        self.policy: PolicyConfig = None
        self.raw_data: dict = {}
        # We don't verify on init, we verify on explicit load
    
    def load(self):
        """
        Loads the Canonical Policy Kernel from disk.
        MUST verify SHA256 against the authorized signature file.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Policy Kernel not found at {self.config_path}")
            
        with open(self.config_path, 'r', encoding='utf-8') as f:
            file_content = f.read() # Read as raw string for hashing
            
        # 1. Compute Hash
        computed_hash = hashlib.sha256(file_content.encode('utf-8')).hexdigest()
        
        # 2. Verify against Authoritative Hash
        if not os.path.exists(self.hash_path):
             raise FileNotFoundError(f"Policy Hash not found at {self.hash_path}")

        with open(self.hash_path, 'r', encoding='utf-8') as f:
            expected_hash = f.read().strip()
            
        if computed_hash != expected_hash:
            raise ValueError(f"CRITICAL INTEGRITY FAILURE: Policy Kernel hash mismatch.\nComputed: {computed_hash}\nExpected: {expected_hash}")
            
        # 3. Parse and Interpret
        self.raw_data = json.loads(file_content)
        
        # Extract fields for typed object
        # Note: mapping directly to PolicyConfig
        self.policy = PolicyConfig(
            schema_version=self.raw_data.get("schema_version"),
            invariants=self.raw_data.get("invariants", []),
            change_control=self.raw_data.get("change_control", {}),
            compatibility=self.raw_data.get("compatibility", {})
        )
        
        print(f"[OEAR] Policy Kernel v{self.policy.schema_version} loaded. Integrity OK.")
        return self.policy
