# File Path: backend/voice_box.py
# Description: Converts AI responses into human-like speech. [cite: 2026-02-11]
# Supports offline mode and local Hinglish synthesis.

import pyttsx3
import threading
import os

class VoiceBox:
    def __init__(self):
        print("🔊 [Voice Box]: Initializing A1 Speech Synthesis...")
        # Offline Engine initialization
        try:
            self.engine = pyttsx3.init()
            self._configure_voice()
        except Exception as e:
            print(f"⚠️ [Solo Mode]: Audio driver error. Voice Box entering 'Ghost Mode'.") [cite: 2026-02-11]
            self.engine = None

    def _configure_voice(self):
        """Voice speed aur accent set karta hai."""
        voices = self.engine.getProperty('voices')
        # Selecting a clear voice (usually index 1 is female/softer for AI)
        self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        self.engine.setProperty('rate', 175) # Speaking speed

    def speak(self, text):
        """
        Text ko awaaz mein badalta hai. [cite: 2026-02-11]
        """
        if not self.engine:
            return "🔊 [Ghost]: Speech skipped (No audio driver)."

        print(f"📢 [A1 Speaking]: {text}")
        
        # Non-blocking speech using threading [cite: 2026-02-11]
        def run_speech():
            self.engine.say(text)
            self.engine.runAndWait()

        threading.Thread(target=run_speech, daemon=True).start()

    def calculate_audio_latency(self, char_count, time_to_start):
        """
        Calculates Synthesis Latency ($L_a$).
        Formula: $L_a = \frac{T_{start}}{N_{chars}}$
        """
        if char_count == 0: return 0
        return round(time_to_start / char_count, 4)

    def stop_speech(self):
        """Emergency Stop for the Voice Box.""" [cite: 2026-02-11]
        if self.engine:
            self.engine.stop()

# Test Block
if __name__ == "__main__":
    speaker = VoiceBox()
    speaker.speak("Bhai, A1 OS ab bol sakta hai. Hum Indore se Bhopal tak saath hain!")
  
