# File: backend/communication/pusher_manager.py
# Purpose: Instant Live Updates without page refresh.
# Free Tier: 200,000 messages/day (Sandbox Plan).
# Strategy: "Pichai Rule" - Offload heavy WebSocket traffic to Pusher.

import pusher

class PusherManager:
    def __init__(self, app_id, key, secret, cluster):
        """
        Pusher Dashboard se credentials lein.
        """
        self.pusher_client = pusher.Pusher(
            app_id=app_id,
            key=key,
            secret=secret,
            cluster=cluster,
            ssl=True
        )
        print("📡 [Pusher]: Real-time Broadcast Channel is Online.")

    def trigger_live_msg(self, channel_name, event_name, message_data):
        """
        Server se Frontend ko instant signal bhejta hai.
        Example: AI ne reply generate kiya aur turant UI par dikh gaya.
        """
        try:
            # First Principles: Minimal payload for maximum speed
            self.pusher_client.trigger(channel_name, event_name, {'message': message_data})
            return True
        except Exception as e:
            print(f"⚠️ [Pusher Error]: Broadcast failed. {e}")
            return False

# --- Usage Strategy: The Live Dashboard ---
# if ai_engine.status == "generating":
#     pusher_manager.trigger_live_msg('a1-chat-channel', 'typing-event', 'AI is thinking...')
