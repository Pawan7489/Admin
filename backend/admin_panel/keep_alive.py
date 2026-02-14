# File: backend/admin_panel/keep_alive.py
# Purpose: A simple heartbeat route to prevent Render/Vercel from sleeping.
# Connect this route to https://uptimerobot.com (Free)

from flask import Blueprint, jsonify

keep_alive_bp = Blueprint('keep_alive', __name__)

@keep_alive_bp.route('/health', methods=['GET'])
def heartbeat():
    """
    UptimeRobot is URL ko har 5 minute mein hit karega.
    Yeh server ko batata hai: "Jaagte raho!"
    """
    return jsonify({
        "status": "Alive",
        "system": "A1 OS",
        "message": "I never sleep."
    }), 200

# --- Setup Instruction ---
# 1. Render par deploy karne ke baad URL copy karein (e.g., https://a1-os.onrender.com).
# 2. UptimeRobot.com par account banayein.
# 3. New Monitor -> Type: HTTP(s) -> URL: https://a1-os.onrender.com/health
# 4. Interval: 5 minutes.
# Result: Aapka free server 24/7 chalega!
