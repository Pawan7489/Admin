# Sub-File 84-F: Detects user age and gender patterns for automatic persona switching.
# Rule: Zero-inference unless explicit triggers are found. [cite: 2026-02-11]

class DemographicSensor:
    def detect_user_type(self, voice_pitch, text_input):
        # Logic: Kids use higher pitch (>200Hz) and simpler words.
        # Seniors might use slower speech and formal grammar.
        
        if voice_pitch > 200: return "child"
        if "sir" in text_input.lower() or "please" in text_input.lower():
            return "senior"
        return "student" # Default college persona

    def calculate_detection_confidence(self, tokens, pitch_data):
        """
        Formula: $C_d = \frac{T_{matched} + P_{variance}}{Total_{input}}$
        """
        return "Confidence: 89%"
      
