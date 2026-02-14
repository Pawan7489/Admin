# File: backend/engines/gemini_engine.py
# Purpose: Integrates Gemini 1.5 Pro/Flash for High-Context Reasoning.
# Free Tier: Uses Google AI Studio's Free API (Rate limited, but powerful).
# Special Feature: Handles 1M+ tokens context (The "Infinite Memory" feel).

import google.generativeai as genai
import os

class GeminiEngine:
    def __init__(self, api_key):
        """
        API Key: Google AI Studio (aistudio.google.com) se lein.
        """
        genai.configure(api_key=api_key)
        # 1.5 Flash: Speed ke liye | 1.5 Pro: Bhaari dimaag ke liye
        self.model_flash = genai.GenerativeModel('gemini-1.5-flash')
        self.model_pro = genai.GenerativeModel('gemini-1.5-pro')
        print("🤖 [Gemini]: Connection established with Google's Cloud Brain.")

    def analyze_complex_data(self, prompt, use_pro=False):
        """
        Gemini ki badi context window ka use karta hai.
        Agar 'Pro' mode on hai, toh deep reasoning karega.
        """
        model = self.model_pro if use_pro else self.model_flash
        mode_name = "Pro" if use_pro else "Flash"
        
        print(f"🧠 [Gemini {mode_name}]: Thinking...")
        
        try:
            response = model.generate_content(prompt)
            print(f"✅ [Gemini]: Answer generated.")
            return response.text
        except Exception as e:
            print(f"❌ [Error]: Gemini API error. {e}")
            return None

    def multimodal_insight(self, image_path, prompt):
        """
        Vision Capability: Image dekh kar logic batata hai. [cite: 2026-02-11]
        """
        # (Pseudo-code for image processing)
        # img = genai.upload_file(image_path)
        # response = self.model_flash.generate_content([img, prompt])
        pass

# --- Usage Strategy ---
# if __name__ == "__main__":
#     MY_KEY = "AIzaSy..." # Your API Key
#     gemini = GeminiEngine(MY_KEY)
#     
#     # Scenario: Poore project ke 100 files ka code ek sath analyze karna
#     answer = gemini.analyze_complex_data("Explain the entire architecture of A1 OS based on these files...", use_pro=True)
