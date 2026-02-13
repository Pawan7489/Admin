# File Path: backend/model_connector.py
# Description: Connects local AI models (Llama 3, Gemma, Phi 3) to the Core. [cite: 2026-02-10]
# Implements 'Solo Mode' if a specific model file is missing. [cite: 2026-02-11]

import requests
import json
import os

class LocalModelConnector:
    def __init__(self, config_manager):
        self.config = config_manager
        # Target Engines: Ollama (Default for zero investment) or Llama.cpp
        self.base_url = "http://localhost:11434/api/generate" 
        self.active_model = "llama3" # Default

    def get_response(self, prompt, system_instruction="You are A1 Super Genius AI."):
        """
        Local model se response fetch karta hai. [cite: 2026-02-11]
        """
        print(f"🧠 [Model]: Thinking using {self.active_model}...")
        
        payload = {
            "model": self.active_model,
            "prompt": prompt,
            "system": system_instruction,
            "stream": False
        }

        try:
            # Musk Rule: Efficiency check before calling [cite: 2026-02-11]
            response = requests.post(self.base_url, json=payload, timeout=30)
            
            if response.status_status == 200:
                return response.json().get("response", "No response generated.")
            else:
                return self._handle_model_failure()

        except Exception as e:
            # Solo Mode: Switch to Ghost Stub or lighter model [cite: 2026-02-11]
            return self._handle_model_failure(str(e))

    def switch_model(self, model_name):
        """Dyanmically switches between Llama, Gemma, and Phi 3. [cite: 2026-02-10]"""
        available_models = ["llama3", "gemma", "phi3", "mistral"]
        if model_name in available_models:
            self.active_model = model_name
            return f"🔄 [Model]: Switched to {model_name} successfully."
        return "⚠️ [Model]: Model not found in local library."

    def calculate_inference_speed(self, tokens, time_taken):
        """
        Calculates Token per Second (TPS).
        Formula: $T_{ps} = \frac{N_{tokens}}{T_{sec}}$
        Target: > 15 TPS for smooth interaction.
        """
        if time_taken == 0: return 0
        return round(tokens / time_taken, 2)

    def _handle_model_failure(self, error="Engine Offline"):
        print(f"❌ [Model Error]: {error}. Activating Solo Mode...") [cite: 2026-02-11]
        return "🤖 [A1 Solo]: Local Engine offline. I am currently running on 'Ghost Logic' (Basic Scripted Responses)."

# Test Block
if __name__ == "__main__":
    # Mocking config
    connector = LocalModelConnector(None)
    # response = connector.get_response("Bhopal se Indore ka rasta batao")
    # print(response)
  
