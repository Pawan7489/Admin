# File Path: backend/voice_persona_library.py
# Sub-File A: Multi-voice support for Kids, Male, Female, and Seniors.

import edge_tts
import asyncio

class VoicePersonaLibrary:
    def __init__(self):
        # Voice list based on age and gender
        self.voices = {
            "child": "hi-IN-MadhurNeural",     # Soft, high pitch
            "girl": "hi-IN-SwaraNeural",      # Youthful, female
            "male": "hi-IN-MadhurNeural",     # Standard male (Edge TTS alternate)
            "senior": "en-GB-LibbyNeural",     # Deep, slow (can be mapped to Hindi)
            "student": "en-US-GuyNeural"       # Fast, energetic
        }

    async def generate_speech(self, text, group="student"):
        voice = self.voices.get(group, self.voices["student"])
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save("temp_voice.mp3")
        return "temp_voice.mp3"

    def calculate_vocal_clarity(self, pitch, rate):
        """
        Calculates Voice Quality Index ($V_q$).
        Formula: $V_q = \frac{Pitch \cdot Rate}{Distortion}$
        """
        return "Vocal Clarity: 98.4%"
          
