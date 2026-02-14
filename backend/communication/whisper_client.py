# File: backend/communication/whisper_client.py
# Purpose: Connects A1 OS to the Whisper Node on Hugging Face.
# Strategy: "Decoupled Execution" - Processing happens in the cloud.

import requests
from gradio_client import Client

class WhisperClient:
    def __init__(self, hf_space_url):
        """
        hf_space_url: Aapka private/public Space URL (e.g., 'username/a1-whisper').
        """
        self.client = Client(hf_space_url)
        print("🎙️ [Whisper]: Connected to Hugging Face Transcription Node.")

    def transcribe_audio(self, audio_file_path):
        """
        Local audio file ko cloud par bhej kar text mangwata hai.
        """
        print(f"☁️ [Whisper]: Sending audio to Cloud Node...")
        try:
            # Gradio API call
            result = self.client.predict(
                audio_file_path,
                api_name="/predict"
            )
            print("✅ [Whisper]: Transcription successful.")
            return result
        except Exception as e:
            print(f"❌ [Error]: Transcription failed. {e}")
            return None

# --- Usage Strategy ---
# if __name__ == "__main__":
#     whisper = WhisperClient("your-username/a1-whisper-node")
#     text = whisper.transcribe_audio("meeting_record.wav")
#     print(f"📝 Transcribed Text: {text}")
