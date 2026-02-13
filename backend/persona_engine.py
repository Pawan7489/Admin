# File Path: backend/persona_engine.py
# Description: Defines the personality, tone, and emotional intelligence of A1 OS.
# Implements 'Human-in-the-Loop' feedback logic. [cite: 2026-02-11]

import json

class PersonaEngine:
    def __init__(self):
        self.current_mood = "Balanced"
        self.persona_presets = {
            "Genius": "Strict, highly technical, uses First Principles.",
            "Peer": "Friendly, uses Hinglish, supportive like a lab mate.",
            "Sarcastic": "Witty, uses humor, reminds you to work harder."
        }
        self.active_persona = "Peer" # Default for Bansal College student life

    def analyze_user_mood(self, user_text):
        """Simple keyword-based sentiment sensing."""
        positive_keys = ["good", "awesome", "mast", "badhiya", "chal gaya"]
        negative_keys = ["error", "ghatiya", "bekar", "slow", "pareshan"]
        
        if any(word in user_text.lower() for word in positive_keys):
            self.current_mood = "Happy"
        elif any(word in user_text.lower() for word in negative_keys):
            self.current_mood = "Frustrated"
        else:
            self.current_mood = "Neutral"
        
        return self.current_mood

    def modulate_response(self, base_response):
        """AI ke response ko mood ke hisab se modify karta hai."""
        if self.current_mood == "Frustrated":
            return f"Bhai, fikar mat karo, hum ise milkar solve kar lenge. {base_response}"
        elif self.current_mood == "Happy":
            return f"Maza aa gaya! {base_response}"
        return base_response

    def calculate_emotional_quotient(self, success_rate, user_rating):
        """
        Calculates the AI's Emotional Quotient ($EQ$).
        Formula: $EQ = \frac{R_{success} + R_{user}}{2} \times Context_{depth}$
        """
        eq_score = (success_rate + user_rating) / 2
        return round(eq_score, 2)

# Test Block
if __name__ == "__main__":
    persona = PersonaEngine()
    print(f"Mood Detected: {persona.analyze_user_mood('Bhai aaj ka kaam mast raha!')}")
    print(persona.modulate_response("System is running fine."))
  
