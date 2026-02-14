# File: backend/nervous_system/groq_speed_engine.py
# Purpose: Fetches answers in milliseconds using Groq's LPU (Language Processing Unit).
# Strategy: "The Speed King" - First responder for all queries.

import os
from groq import Groq

class GroqSpeedEngine:
    def __init__(self, api_key):
        """
        Groq Client initialize karta hai.
        api_key: Groq Console se mila hua free key.
        """
        self.client = Groq(api_key=api_key)
        self.model = "llama3-8b-8192" # Super fast & efficient

    def get_instant_response(self, user_query):
        """
        User query ko process karke turant jawab deta hai.
        """
        print(f"⚡ [Groq]: Processing query at light speed: '{user_query}'...")
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are A1 OS, a super-intelligent AI. Answer briefly and accurately."
                    },
                    {
                        "role": "user",
                        "content": user_query,
                    }
                ],
                model=self.model,
                temperature=0.5,
                max_tokens=1024,
            )
            
            response = chat_completion.choices[0].message.content
            print("✅ [Groq]: Response received in milliseconds.")
            return response
            
        except Exception as e:
            print(f"❌ [Error]: Groq API failed. {str(e)}")
            return None

# --- Usage ---
# groq = GroqSpeedEngine("gsk_xxxxxxxx")
# print(groq.get_instant_response("What is the capital of India?"))
