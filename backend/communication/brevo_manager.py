# File: backend/communication/brevo_manager.py
# Purpose: Manages Contact Lists & Sends Newsletters/Updates.
# Free Tier: 300 Emails/Day.
# Logic: Syncs new users to Brevo & sends broadcast updates.

from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

class BrevoMarketingManager:
    def __init__(self, api_key):
        """
        Brevo API Key Dashboard se milegi.
        """
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key['api-key'] = api_key
        self.api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        self.email_api = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        
        # Default Sender (Aapka verified email)
        self.sender = {"name": "A1 OS Team", "email": "updates@a1-os.com"}

    def add_subscriber(self, user_email, username):
        """
        Jab koi naya user signup kare, use 'Newsletter List' mein add karo.
        """
        print(f"📣 [Brevo]: Adding {username} to subscriber list...")
        
        create_contact = sib_api_v3_sdk.CreateContact(
            email=user_email,
            attributes={"FIRSTNAME": username},
            list_ids=[2], # Brevo Dashboard mein List ID 2 = 'General Newsletter'
            update_enabled=True
        )

        try:
            self.api_instance.create_contact(create_contact)
            print(f"✅ [Brevo]: {username} subscribed successfully.")
            return True
        except ApiException as e:
            print(f"⚠️ [Brevo]: Could not add subscriber. {e}")
            return False

    def send_daily_update(self, target_email, update_content):
        """
        System Update bhejne ke liye (e.g., "Aaj humne Llama-3 add kiya").
        Note: Free tier mein daily 300 limit hai, isliye ise bulk mein loop mein chalayein.
        """
        print(f"📰 [Brevo]: Sending Daily Update to {target_email}...")
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": target_email}],
            sender=self.sender,
            subject="📢 A1 OS Daily Update",
            html_content=f"""
            <html>
                <body>
                    <h2>Hello System User,</h2>
                    <p>Here is your daily AI summary:</p>
                    <blockquote style="background: #f9f9f9; padding: 10px;">
                        {update_content}
                    </blockquote>
                    <p>Stay genius,<br>A1 OS Team</p>
                </body>
            </html>
            """
        )

        try:
            self.email_api.send_transac_email(send_smtp_email)
            print("✅ [Brevo]: Update Sent.")
            return True
        except ApiException as e:
            print(f"❌ [Error]: Update failed. {e}")
            return False

# --- Master Strategy (Automated News) ---
# if __name__ == "__main__":
#     KEY = "xkeysib-xxxxxxxx"
#     marketer = BrevoMarketingManager(KEY)
#     
#     # 1. New User Signup
#     marketer.add_subscriber("student@bansal.edu", "Rahul")
#     
#     # 2. Send Update (Loop for top 300 users)
#     # users = db.get_active_users(limit=300)
#     # for user in users:
#     #     marketer.send_daily_update(user.email, "Aaj humne naya Qwen model deploy kiya hai!")
