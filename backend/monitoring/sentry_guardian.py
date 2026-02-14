# File: backend/monitoring/sentry_guardian.py
# Purpose: Real-time Error Tracking & Performance Monitoring.
# Free Tier: Developer Plan (5k events/month - Perfect for us).
# Strategy: "Silent Watchman" - Reports crashes before users do.

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

class SentryGuardian:
    def __init__(self, dsn_url):
        """
        dsn_url: Sentry.io Dashboard se milega (Client Key).
        """
        print("🚨 [Sentry]: Activating Guardian Protocol...")
        
        sentry_sdk.init(
            dsn=dsn_url,
            integrations=[FlaskIntegration()], # Humara Admin Panel Flask/Gradio par hai
            
            # Performance Monitoring (Free tier limits apply)
            traces_sample_rate=1.0,
            
            # Sensitive data filter (Privacy)
            send_default_pii=False 
        )
        print("✅ [Sentry]: System Monitoring Active. Reporting all glitches.")

    def manual_capture(self, message, level="info"):
        """
        Zaroori nahi ki code phate tabhi report ho. 
        Aap manually bhi updates bhej sakte hain.
        """
        with sentry_sdk.configure_scope() as scope:
            scope.set_level(level)
            sentry_sdk.capture_message(message)

# --- Integration Logic (In your main app.py) ---
# guardian = SentryGuardian("https://xxxxxx@sentry.io/xxxxxx")
#
# try:
#     # Aapka heavy AI logic
#     1 / 0 # Forceful Error for testing
# except Exception as e:
#     # Sentry isse automatically pakad lega, par aap extra info bhi de sakte hain
#     print(f"Crash detected! Reporting to Admin via Sentry...")
