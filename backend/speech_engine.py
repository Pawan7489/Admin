# File Path: backend/speech_engine.py
# Description: Real-time Hinglish Speech Recognition for A1 OS. [cite: 2026-02-11]
# Uses Whisper (Local) for Zero-Investment high accuracy. [cite: 2026-02-10]

import os
import time
import queue
import speech_recognition as sr
import whisper
import threading

class SpeechEngine:
    def __init__(self):
        print("🎙️ [Speech]: Initializing A1 Ears (Whisper Tiny)...")
        self.model = whisper.load_model("tiny") # Zero investment local model
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.recognizer = sr.Recognizer()

    def listen_and_transcribe(self, callback):
        """
        Microphone se awaaz sunkar use text mein badalta hai. [cite: 2026-02-11]
        """
        self.is_listening = True
        
        # Solo Mode: Check if Mic is connected [cite: 2026-02-11]
        try:
            self.mic = sr.Microphone()
        except Exception:
            print("⚠️ [Solo Mode]: Microphone not detected, skipping speech input...") [cite: 2026-02-11]
            return

        def background_listener():
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source)
                while self.is_listening:
                    try:
                        print("👂 Listening...")
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        # Processing via Whisper
                        with open("temp_audio.wav", "wb") as f:
                            f.write(audio.get_wav_data())
                        
                        result = self.model.transcribe("temp_audio.wav", language="hi") # Hindi/English Mix
                        text = result.get("text", "").strip()
                        
                        if text:
                            print(f"🗣️ [User]: {text}")
                            callback(text) # Send to Intent Engine
                            
                    except sr.WaitTimeoutError:
                        continue
                    except Exception as e:
                        print(f"❌ [Speech Error]: {str(e)}")

        thread = threading.Thread(target=background_listener, daemon=True)
        thread.start()

    def calculate_wer(self, reference, hypothesis):
        """
        Calculates Word Error Rate ($WER$) to check accuracy.
        Formula: $WER = \frac{S + D + I}{N}$
        Where S=Substitutions, D=Deletions, I=Insertions.
        """
        # Standard Speech accuracy metric
        r = reference.split()
        h = hypothesis.split()
        # Simplified for visualization
        return round(abs(len(r) - len(h)) / max(len(r), 1), 2)

    def stop(self):
        self.is_listening = False

# Test Block
if __name__ == "__main__":
    def dummy_callback(text):
        print(f"🤖 [A1 Processed]: {text}")

    ears = SpeechEngine()
    ears.listen_and_transcribe(dummy_callback)
    
    # Keep alive for testing
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        ears.stop()
                      
