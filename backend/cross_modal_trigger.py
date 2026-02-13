# File Path: backend/cross_modal_trigger.py
# Description: Automatically links different data types (Image -> Text -> Voice). [cite: 2026-02-11]
# Orchestrates multiple models to work as a single "Super Genius" unit. [cite: 2026-02-11]

import os
import json
from datetime import datetime

class CrossModalEngine:
    def __init__(self, text_engine, voice_engine, vision_engine=None):
        """
        Initializes the triggers between different AI modalities.
        """
        self.text_engine = text_engine
        self.voice_engine = voice_engine
        self.vision_engine = vision_engine
        self.trigger_log = "database/cross_modal_log.json"
        self._ensure_setup()

    def _ensure_setup(self):
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists(self.trigger_log):
            with open(self.trigger_log, 'w') as f:
                json.dump({}, f)

    def process_image_input(self, image_path):
        """
        When an image is detected, automatically triggers Text and Voice models. [cite: 2026-02-11]
        """
        print(f"👁️ [Cross-Modal]: Image detected at {image_path}. Triggering Analysis...")
        
        # Step 1: Vision/Text Analysis (Simulation)
        # In a real setup, vision_engine would analyze the image.
        description = f"Analyzed image at {image_path}: A complex electronic circuit detected."
        
        # Step 2: Automatic Text Explanation [cite: 2026-02-11]
        explanation = self.text_engine.process_intent(f"Explain this: {description}")
        
        # Step 3: Automatic Voice Narration [cite: 2026-02-11]
        narration_status = self.voice_engine.execute_ghost_stub("Voice_Narration")
        
        self._log_trigger("Image_to_Speech", image_path, description)
        
        return {
            "vision_output": description,
            "text_explanation": explanation,
            "voice_status": narration_status
        }

    def _log_trigger(self, trigger_type, source, result):
        """Logs the cross-modal activity for the system registry."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "type": trigger_type,
            "source": source,
            "result": result
        }
        
        try:
            with open(self.trigger_log, 'r') as f:
                history = json.load(f)
        except:
            history = {}
            
        history[timestamp] = entry
        with open(self.trigger_log, 'w') as f:
            json.dump(history, f, indent=4)

# Test Block (Standalone Simulation)
if __name__ == "__main__":
    # Mocking existing modules for the trigger
    class MockEngine:
        def process_intent(self, t): return f"Logic: {t}"
        def execute_ghost_stub(self, m): return f"Ghost {m} Standby"

    cm_engine = CrossModalEngine(MockEngine(), MockEngine())
    print(cm_engine.process_image_input("uploads/circuit_board.jpg"))
  
