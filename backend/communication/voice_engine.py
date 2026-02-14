# File: backend/communication/voice_engine.py
# Purpose: The "Ears" of A1 OS. Handles Voice Commands & NLP.
# Free Tier: Meta's Wit.ai is 100% Free.
# Strategy: Convert voice to Intent + Entities for "Hands-Free" control.

from wit import Wit
import speech_recognition as sr # For local audio capture

class VoiceEngine:
    def __init__(self, access_token):
        """
        Access Token: wit.ai dashboard se lein.
        """
        self.client = Wit(access_token)
        print("👂 [Wit.ai]: Voice Recognition System Online. Listening...")

    def listen_and_process(self):
        """
        Microphone se awaaz sunta hai aur Wit.ai ko bhejta hai.
        """
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 [A1 OS]: Speak now...")
            audio = recognizer.listen(source)

        try:
            # Audio ko text aur intent mein badalne ke liye Wit.ai ko bhejna
            # Note: Wit.ai audio files (.wav) bhi accept karta hai
            voice_data = recognizer.recognize_google(audio) # Initial STT
            print(f"🗣️ [User]: {voice_data}")
            
            # NLP Processing (Intent nikalna)
            resp = self.client.message(voice_data)
            return self._parse_intent(resp)
            
        except Exception as e:
            print(f"❌ [Error]: Could not process voice. {e}")
            return None

    def _parse_intent(self, response):
        """
        Wit.ai ke response mein se 'Main Goal' nikalta hai.
        """
        intents = response.get('intents', [])
        entities = response.get('entities', {})
        
        if intents:
            intent_name = intents[0]['name']
            confidence = intents[0]['confidence']
            print(f"🎯 [Intent]: {intent_name} ({confidence*100:.1f}%)")
            return {"intent": intent_name, "entities": entities}
        
        print("❓ [Wit.ai]: Intent not clear.")
        return None

# --- Master Logic: Linking Voice to Action ---
# if __name__ == "__main__":
#     WIT_TOKEN = "your_server_access_token"
#     ears = VoiceEngine(WIT_TOKEN)
#     
#     command = ears.listen_and_process()
#     
#     if command and command['intent'] == 'create_folder':
#         folder_name = command['entities'].get('folder_name:folder_name')[0]['value']
#         # Code to create folder... [cite: 2026-02-11]
