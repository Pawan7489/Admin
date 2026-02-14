# File: backend/communication/deepgram_engine.py
# Purpose: Real-time, Ultra-fast Speech-to-Text.
# Free Tier: $200 credits (Thousands of hours of audio).
# Strategy: Use for "Live Mode" where lag is not allowed.

from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import os

class DeepgramSpeedEngine:
    def __init__(self, api_key):
        """
        API Key: console.deepgram.com se lein.
        """
        self.client = DeepgramClient(api_key)
        print("⚡ [Deepgram]: Bullet-Train STT Engine Online.")

    def transcribe_instant(self, audio_file_path):
        """
        Nova-2 model ka use karke instant transcription deta hai.
        """
        print(f"🚀 [Deepgram]: Transcribing at light speed...")
        
        try:
            with open(audio_file_path, "rb") as file:
                buffer_data = file.read()

            payload: FileSource = {
                "buffer": buffer_data,
            }

            # Nova-2 is their fastest and most accurate model
            options = PrerecordedOptions(
                model="nova-2",
                smart_format=True,
                language="en", # Hindi support bhi available hai
            )

            response = self.client.listen.prerecorded.v("1").transcribe_file(payload, options)
            
            transcript = response.results.channels[0].alternatives[0].transcript
            print("✅ [Deepgram]: Transcription Complete.")
            return transcript

        except Exception as e:
            print(f"❌ [Error]: Deepgram failed. {e}")
            return None

# --- Usage Strategy ---
# if mode == "real_time_chat":
#     text = deepgram_engine.transcribe_instant("mic_input.wav")
