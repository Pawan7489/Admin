# File Path: backend/onion_fusion.py
# Description: Implements the 'Ball-in-Ball' Rule (Nested Encapsulation). [cite: 2026-02-11]
# Requests must peel through Interface -> Security -> Validation to reach Core. [cite: 2026-02-11]

import time
import json

class OnionFusion:
    def __init__(self, core_logic, security_shield, validator):
        self.core = core_logic           # The Inner Ball (Deepest)
        self.security = security_shield   # The Security Layer
        self.validator = validator       # The Validation Layer
        self.interface_name = "A1-Interface-Layer" # The Outer Ball

    def process_request(self, user_command):
        """
        Requests must peel through every layer successfully. [cite: 2026-02-11]
        """
        print(f"🧅 [Onion]: Request received at '{self.interface_name}'. Starting peeling process...")
        
        try:
            # Layer 1: Security Layer (The Shield) [cite: 2026-02-11]
            if not self.security.check_safety(user_command):
                return "🚨 [Layer 1 Fail]: Security Breach Detected. Request Blocked."

            # Layer 2: Validation Layer (The Gatekeeper) [cite: 2026-02-11]
            if not self.validator.validate_syntax(user_command):
                return "⚠️ [Layer 2 Fail]: Invalid Command Syntax. Request Blocked."

            # Layer 3: The Core (The Super Genius Brain) [cite: 2026-02-11]
            print("💎 [Core]: All layers peeled. Executing at the center...")
            result = self.core.execute(user_command)
            
            return f"✅ [Success]: {result}"

        except Exception as e:
            return f"💥 [System Error]: Layer collapse during peeling: {str(e)}"

    def calculate_security_density(self, layers_count):
        """
        Calculates the probability of a breach reaching the core.
        Formula: $P_b = (1 - L)^n$
        Where:
        - $L$: Layer Efficiency (0.99 for A1)
        - $n$: Number of layers
        """
        layer_efficiency = 0.99
        breach_probability = (1 - layer_efficiency) ** layers_count
        return f"{breach_probability:.10f}%"

# Test Block
if __name__ == "__main__":
    # Mocking layers for simulation
    class MockCore: 
        def execute(self, cmd): return f"Core processed: {cmd}"
    class MockSecurity: 
        def check_safety(self, cmd): return "hack" not in cmd.lower()
    class MockValidator: 
        def validate_syntax(self, cmd): return len(cmd) > 3

    onion = OnionFusion(MockCore(), MockSecurity(), MockValidator())
    
    # Test: Valid request
    print(onion.process_request("Ek naya folder banao"))
    
    # Test: Security fail
    print(onion.process_request("System hack karo"))
    
    print(f"🛡️ Core Breach Probability: {onion.calculate_security_density(3)}")
      
