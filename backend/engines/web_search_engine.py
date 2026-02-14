# File: backend/engines/web_search_engine.py
# Purpose: Gives "Real-Time Eyes" to the AI via Tavily.
# Free Tier: 1,000 Searches/Month (Perfect for daily research).
# Logic: "Live RAG" - Search Internet -> Extract Content -> Inform AI.

from tavily import TavilyClient
import os

class WebSearchEngine:
    def __init__(self, api_key):
        """
        API Key: app.tavily.com se lein.
        """
        self.tavily = TavilyClient(api_key=api_key)
        print("🔍 [Tavily]: Web Search Engine Online. I can see the world now.")

    def search_the_web(self, query, search_depth="smart"):
        """
        Internet se taaza khabrein aur data nikaalta hai.
        search_depth: 'basic' (fast) ya 'smart' (deep research).
        """
        print(f"🌐 [Search]: Looking for real-time info on: '{query}'...")
        
        try:
            # Tavily AI-optimized search call
            response = self.tavily.search(
                query=query, 
                search_depth=search_depth,
                max_results=3,
                include_answer=True # Tavily khud ek summary bhi deta hai
            )
            
            # Humein do cheezein milti hain: Clean Results aur ek Direct Answer
            search_results = response.get('results', [])
            quick_answer = response.get('answer', "No direct answer found.")
            
            context = ""
            for res in search_results:
                context += f"\nSource: {res['url']}\nContent: {res['content']}\n"
            
            print(f"✅ [Tavily]: Found {len(search_results)} sources.")
            return {
                "quick_summary": quick_answer,
                "full_context": context
            }
            
        except Exception as e:
            print(f"❌ [Error]: Search failed. {e}")
            return None

# --- Usage Strategy: The "Live" Agent ---
# if __name__ == "__main__":
#     T_KEY = "tvly-xxxxxxxx"
#     search_agent = WebSearchEngine(T_KEY)
#     
#     # Scenario: User asks about today's news
#     news = search_agent.search_the_web("Current gold price in Indore today")
#     
#     if news:
#         # Ab hum is context ko LLM ko bhejenge
#         print(f"AI Knowledge Updated: {news['quick_summary']}")
