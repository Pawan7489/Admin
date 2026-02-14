# File: backend/engines/serper_google_engine.py
# Purpose: Google Search Backup using Serper.dev.
# Free Tier: 2,500 Queries.
# Strategy: "The Second Eye" - High accuracy Google results fallback.

import requests
import json

class SerperGoogleEngine:
    def __init__(self, api_key):
        """
        API Key: serper.dev dashboard se lein.
        """
        self.api_key = api_key
        self.url = "https://google.serper.dev/search"
        self.headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        print("🌐 [Serper]: Google Search API Ready (Backup Eye).")

    def search_google(self, query):
        """
        Google se real-time data nikaalta hai.
        """
        print(f"🕵️ [Serper]: Querying Google for: '{query}'...")
        
        payload = json.dumps({"q": query})
        
        try:
            response = requests.post(self.url, headers=self.headers, data=payload)
            response.raise_for_status()
            data = response.json()
            
            # Google's Knowledge Graph ya Top Snippets nikalna
            results = data.get('organic', [])
            answer_box = data.get('answerBox', {}).get('answer', "No direct answer.")
            
            # Top 3 results ko context ke liye process karna
            context = ""
            for i, res in enumerate(results[:3]):
                context += f"\n[{i+1}] {res['title']}: {res['snippet']} (Link: {res['link']})"
            
            print(f"✅ [Serper]: Retrieved {len(results[:3])} Google results.")
            return {
                "quick_answer": answer_box,
                "context": context
            }
            
        except Exception as e:
            print(f"❌ [Error]: Serper Search failed. {e}")
            return None

# --- Usage Strategy: The Failover Router ---
# if tavily_fail:
#     serper_engine.search_google(user_query)
