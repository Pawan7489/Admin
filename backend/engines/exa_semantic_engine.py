# File: backend/engines/exa_semantic_engine.py
# Purpose: Deep Semantic Research for A1 OS.
# Free Tier: 1,000 Requests/Month.
# Strategy: Use for high-quality source finding (Neural Search).

from exa_py import Exa

class ExaSemanticEngine:
    def __init__(self, api_key):
        """
        API Key: dashboard.exa.ai se lein.
        """
        self.exa = Exa(api_key)
        print("🧠 [Exa.ai]: Semantic Search Engine Active. Searching by meaning, not keywords.")

    def deep_research(self, query):
        """
        Neural search ka use karke high-quality results nikalta hai.
        """
        print(f"🧬 [Exa]: Performing neural crawl for: '{query}'...")
        
        try:
            # Exa automatically query ko vector mein badalta hai
            result = self.exa.search(
                query,
                num_results=5,
                use_autoprompt=True, # AI query ko behtar banata hai
                highlights=True # Text ke zaroori hisse nikalna
            )
            
            context = ""
            for res in result.results:
                context += f"\nTitle: {res.title}\nURL: {res.url}\nHighlight: {res.highlights[0] if res.highlights else 'No summary'}\n"
            
            print(f"✅ [Exa]: High-quality sources retrieved.")
            return context
            
        except Exception as e:
            print(f"❌ [Error]: Exa Search failed. {e}")
            return None

# --- Usage Strategy ---
# if "Research" in user_intent:
#     exa_engine.deep_research(user_query)
