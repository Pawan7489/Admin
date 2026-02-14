import os
from groq import Groq
from dotenv import load_dotenv

# Musk Rule: Minimalist and Efficient
load_dotenv("config.env")

class GroqBrain:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            # Solo Mode: Don't crash, just alert
            print("⚠️ Groq API Key missing in config.env. Skipping Groq Module...")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)
            self.model = "llama3-8b-8192" # Speed & Intelligence balance

    def think(self, prompt):
        if not self.client:
            return "Error: Groq module not active."

        try:
            # Internal Critique Simulation: Requesting clean response
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Super Genius AI. Respond concisely in Hinglish."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1024,
                stream=False
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"System Error: {str(e)}"

# Integration Test
if __name__ == "__main__":
    brain = GroqBrain()
    print(brain.think("Ek naya folder banane ka Python code batao."))
  
