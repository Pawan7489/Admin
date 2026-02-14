# File: backend/communication/speech_engine_pro.py
# Purpose: High-Quality Voice Synthesis (Hybrid Mode).
# Free Tier: ElevenLabs (10k chars/mo) + gTTS (Unlimited Free).
# Strategy: "Musk Rule" - Use expensive resources only when necessary.

import os
from elevenlabs import generate, save, set_api_key
from gtts import gTTS

class SpeechEnginePro:
    def __init__(self, eleven_key):
        """
        eleven_key: elevenlabs.io dashboard se milega.
        """
        self.api_key = eleven_key
        set_api_key(self.api_key)
        self.output_dir = "./temp/voice_outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        print("🗣️ [ElevenLabs]: Premium Voice Engine Connected.")

    def speak(self, text, priority="low"):
        """
        Priority-based voice generation.
        'high' -> ElevenLabs (Realistic)
        'low'  -> gTTS (Robot-like but Free)
        """
        filename = f"{self.output_dir}/speech_{hash(text)}.mp3"

        if priority == "high":
            print(f"💎 [Premium Voice]: Generating realistic speech for: '{text[:20]}...'")
            try:
                audio = generate(
                    text=text,
                    voice="Adam", # "Adam" or "Bella" are popular choices
                    model="eleven_multilingual_v2"
                )
                save(audio, filename)
                print("✅ [Success]: Premium Audio Saved.")
                return filename
            except Exception as e:
                print(f"⚠️ [ElevenLabs]: Quota full or error: {e}. Falling back to free voice...")
                priority = "low" # Auto-fallback if premium fails

        if priority == "low":
            print(f"🤖 [Basic Voice]: Using Free TTS for: '{text[:20]}...'")
            tts = gTTS(text=text, lang='hi') # Hinglish/Hindi support
            tts.save(filename)
            print("✅ [Success]: Basic Audio Saved.")
            return filename

# --- Master Control Logic ---
# if __name__ == "__main__":
#     engine = SpeechEnginePro("your_elevenlabs_key")
#     
#     # Scenario 1: Welcome Message (High Priority)
#     engine.speak("Welcome back, Master. All systems are online.", priority="high")
#     
#     # Scenario 2: Routine Log (Low Priority)
#     engine.speak("Backup completed successfully at 3:00 AM.", priority="low")
