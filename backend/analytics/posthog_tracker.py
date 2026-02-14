# File: backend/analytics/posthog_tracker.py
# Purpose: Tracking User Behavior & AI Performance.
# Free Tier: 1 Million Events/Month.
# Strategy: "Zuckerberg Rule" - Data-driven iterations.

from posthog import Posthog
import os

class PostHogTracker:
    def __init__(self, api_key, host="https://us.i.posthog.com"):
        """
        API Key: app.posthog.com se lein.
        """
        self.posthog = Posthog(api_key, host=host)
        print("📈 [PostHog]: Analytics Spy Glass is Active.")

    def track_ai_interaction(self, user_id, intent, engine_used, processing_time):
        """
        Jab bhi AI koi jawab deta hai, ye event record hota hai.
        """
        self.posthog.capture(user_id, 'ai_command_processed', {
            'intent': intent,
            'engine': engine_used,
            'latency_sec': processing_time,
            'location_context': 'Indore-Bhopal-Mesh'
        })
        print(f"📊 [PostHog]: Event captured for user {user_id}")

    def track_feedback(self, user_id, rating, feedback_text=None):
        """
        RLHF (Human-in-the-Loop) feedback ko track karta hai. [cite: 2026-02-11]
        """
        self.posthog.capture(user_id, 'user_feedback', {
            'rating': rating,
            'comment': feedback_text
        })

# --- Usage Logic ---
# tracker = PostHogTracker("phc_xxxxxx")
# tracker.track_ai_interaction("user_001", "create_folder", "Groq", 0.5)
