# File: backend/security/gatekeeper_clerk.py
# Purpose: Validates User Identity using Clerk JWT.
# Strategy: "The Bouncer" - No token, no entry to the AI Brain.
# Requirement: pip install python-jose[cryptography]

from jose import jwt
import requests

class ClerkGatekeeper:
    def __init__(self, frontend_api_url, clerk_secret_key):
        self.clerk_secret = clerk_secret_key
        # Clerk provides a JWKS (JSON Web Key Set) to verify tokens
        self.jwks_url = f"{frontend_api_url}/.well-known/jwks.json"

    def verify_user(self, token):
        """
        Token check karta hai ki kya user login hai?
        """
        print("🛡️ [Gatekeeper]: Checking user ID card...")
        
        try:
            # Clerk se public keys mangwana
            jwks = requests.get(self.jwks_url).json()
            
            # Token decode aur verify karna
            # Note: Production mein yahan 'audience' aur 'issuer' check zaroori hai
            payload = jwt.decode(token, jwks, algorithms=['RS256'], options={"verify_aud": False})
            
            user_id = payload.get('sub')
            print(f"✅ [Gatekeeper]: Welcome, User {user_id}. Access Granted.")
            return user_id
            
        except Exception as e:
            print(f"❌ [Security Alert]: Invalid Token or Hacker detected! {e}")
            return None

# --- Usage Strategy (Middleware) ---
# token = request.headers.get('Authorization').split(" ")[1]
# user = gatekeeper.verify_user(token)
# if not user:
#     abort(401) # Kick them out
