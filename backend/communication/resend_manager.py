# File: backend/communication/resend_manager.py
# Purpose: Sends OTPs & Welcome Emails using Resend API.
# Free Tier: 3,000 Emails/Month (100/day).
# Logic: "Fire and Forget" - API call karo aur bhul jao.

import resend
import random
import os

class ResendEmailManager:
    def __init__(self, api_key):
        """
        Resend API Key Dashboard se milegi.
        """
        resend.api_key = api_key
        # Testing ke liye Resend ek default domain deta hai (e.g., onboarding@resend.dev)
        # Production mein apna domain verify karwana padega (e.g., support@a1-os.com)
        self.sender_email = "onboarding@resend.dev" 

    def generate_otp(self):
        """6-digit random number banata hai."""
        return str(random.randint(100000, 999999))

    def send_verification_otp(self, user_email):
        """
        User ko login/signup ke waqt OTP bhejta hai.
        """
        otp_code = self.generate_otp()
        
        print(f"📧 [Resend]: Sending OTP to {user_email}...")
        
        try:
            params = {
                "from": self.sender_email,
                "to": [user_email],
                "subject": "🔐 A1 OS Verification Code",
                "html": f"""
                <div style="font-family: sans-serif; text-align: center;">
                    <h2>Welcome to A1 OS</h2>
                    <p>Your verification code is:</p>
                    <h1 style="color: #007bff; letter-spacing: 5px;">{otp_code}</h1>
                    <p>This code expires in 10 minutes.</p>
                </div>
                """
            }
            
            email = resend.Emails.send(params)
            print(f"✅ [Resend]: OTP Sent! ID: {email['id']}")
            return otp_code  # Yeh OTP hum database (Redis) mein save karenge verification ke liye
            
        except Exception as e:
            print(f"❌ [Error]: Email failed. {e}")
            return None

    def send_welcome_email(self, user_email, username):
        """
        Jab user successfully register ho jaye, tab sundar sa welcome mail bhejo.
        """
        try:
            params = {
                "from": self.sender_email,
                "to": [user_email],
                "subject": "🚀 Welcome to the Future!",
                "html": f"""
                <div style="font-family: sans-serif; padding: 20px;">
                    <h1>Hello {username},</h1>
                    <p>Welcome to <strong>A1 OS</strong> - The Zero Investment AI Ecosystem.</p>
                    <p>We are thrilled to have you on board.</p>
                    <br>
                    <a href="https://a1-os-admin.onrender.com" style="background-color: #000; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Go to Dashboard</a>
                </div>
                """
            }
            resend.Emails.send(params)
            print(f"🎉 [Resend]: Welcome email sent to {username}.")
            return True
            
        except Exception as e:
            print(f"❌ [Error]: Welcome email failed. {e}")
            return False

# --- Usage Strategy ---
# if __name__ == "__main__":
#     # Resend Dashboard se API Key lein
#     API_KEY = "re_123456789"
#     
#     mailer = ResendEmailManager(API_KEY)
#     
#     # Scenario 1: User Login
#     otp = mailer.send_verification_otp("user@example.com")
#     
#     # Scenario 2: Save OTP in Redis (File 92) for 5 mins
#     # redis.set(f"otp:{user_email}", otp, ex=300)
