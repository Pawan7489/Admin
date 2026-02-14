# File: backend/engines/search_orchestrator.py
# Logic: Try Tavily first (AI optimized). If fails or quota ends, hit Serper.

class SearchOrchestrator:
    def __init__(self, tavily, serper):
        self.tavily = tavily
        self.serper = serper

    def get_info(self, query):
        # 1. First Principle: Try Tavily
        result = self.tavily.search_the_web(query)
        
        if result:
            return result
            
        # 2. Solo Mode: If Tavily fails, use Serper
        print("🔄 [Orchestrator]: Tavily failed/exhausted. Switching to Serper (Google)...")
        return self.serper.search_google(query)
      
