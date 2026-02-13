# File Path: backend/onion_wrapper.py
# Description: Implements the 'Ball-in-Ball' Rule (Nested Encapsulation).
# Ensures that direct access to the Core is impossible.

import json
import os

class OnionWrapper:
    def __init__(self, core_module, security_module, validation_module):
        """
        Initializes the nested layers.
        Core is at the center, wrapped by Validation, then Security.
        """
        self._core = core_module
        self._security = security_module
        self._validation = validation_module

    def process_request(self, user_intent, data=None):
        """
        The Interface Layer (Outer Ball) entry point.
        Requests must peel through every layer successfully.
        """
        print("🧅 [Onion]: Request received at Interface Layer. Peeling layers...")

        # LAYER 1: Security Layer (Second Outer Ball)
        security_check = self._security.verify_ethical_compliance(user_intent)
        if not security_check.get("is_safe"):
            return f"❌ Access Denied at Security Layer: {security_check.get('reason')}"
        print("✅ [Layer 1]: Security Layer passed.")

        # LAYER 2: Validation Layer (Inner Wrapping)
        # Checks if the intent is valid and data is correct
        validation_check = self._validation.validate_input(user_intent)
        if not validation_check.get("valid"):
            return f"❌ Access Denied at Validation Layer: {validation_check.get('reason')}"
        print("✅ [Layer 2]: Validation Layer passed.")

        # LAYER 3: The Core (The Inner Ball)
        # Direct access is only possible after Layer 1 and 2 are clear.
        print("🎯 [Layer 3]: Accessing the Core Logic...")
        result = self._core.execute(user_intent, data)
        
        return {
            "status": "Success",
            "layers_peeled": 3,
            "core_output": result
        }

# Mock Validation Module for demonstration
class ValidationLayer:
    def validate_input(self, text):
        if len(text) < 3:
            return {"valid": False, "reason": "Input too short for processing."}
        return {"valid": True}

# Test block
if __name__ == "__main__":
    # In real system, these would be the actual modules from File 01, 13, etc.
    from core_engine import AI_CORE
    from guardian_protocol import GuardianShield
    
    shield = GuardianShield()
    validator = ValidationLayer()
    
    onion = OnionWrapper(AI_CORE, shield, validator)
    
    # Testing a safe request
    response = onion.process_request("Ek naya storage folder banao")
    print(response)
      
