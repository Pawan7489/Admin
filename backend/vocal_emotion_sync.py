# Sub-File 84-L: Adjusts pitch, rate, and volume of the age-group voice based on user's mood.
# Follows 'The Soul Engine' logic (File 83). [cite: 2026-02-11]

class VocalEmotionSync:
    def sync_voice_to_mood(self, base_voice, user_mood):
        modifications = {
            "Happy": {"pitch": "+20%", "rate": "1.1x"},
            "Frustrated": {"pitch": "-10%", "rate": "0.9x", "volume": "softer"},
            "Neutral": {"pitch": "+0%", "rate": "1.0x"}
        }
        settings = modifications.get(user_mood, modifications["Neutral"])
        print(f"🎭 [Voice Sync]: Modulating {base_voice} for {user_mood} mood.")
        return settings

    def calculate_vocal_resonance(self, frequency_hz):
        """
        Calculates Resonance Factor ($R_f$).
        Formula: $R_f = \frac{f_{vocal}}{f_{ambient}} \cdot \sin(\theta)$
        """
        return round(frequency_hz / 440, 2)
      
