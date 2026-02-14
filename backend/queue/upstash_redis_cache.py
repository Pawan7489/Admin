# File: backend/queue/upstash_redis_cache.py
# Purpose: Caching common queries to save GPU computation.
# Logic: Check Cache -> If Found (Return) -> Else (Ask AI & Save).

from upstash_redis import Redis
import json

class UpstashCacheManager:
    def __init__(self, url, token):
        """
        Upstash Console se REST URL aur Token lein.
        """
        self.redis = Redis(url=url, token=token)

    def get_cached_response(self, query):
        """
        Check karta hai ki kya ye sawal pehle pucha gaya tha?
        """
        # Query ko key banate hain (Spaces remove karke)
        key = f"query:{hash(query)}"
        
        data = self.redis.get(key)
        if data:
            print("⚡ [Redis]: Cache Hit! Serving instant answer.")
            return data # String wapas karega
        return None

    def save_response(self, query, response):
        """
        AI ke jawab ko future ke liye save karta hai.
        TTL (Time To Live): 24 ghante (86400 seconds) baad delete ho jayega.
        """
        key = f"query:{hash(query)}"
        print(f"💾 [Redis]: Caching answer for future speed.")
        self.redis.set(key, response, ex=86400)

# --- Usage Strategy ---
# if cache_manager.get_cached_response(user_input):
#     return cache_result
# else:
#     ai_result = model.generate(user_input)
#     cache_manager.save_response(user_input, ai_result)
