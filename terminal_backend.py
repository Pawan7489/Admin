# File: terminal_backend.py
# Description: Universal Admin Panel (Meta + All Modules Integrated)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os

# --- MODULE AUTO-LOADER ---
modules = {}

# 1. Meta (Facebook/Insta/WhatsApp) - NEW
try:
    import meta_manager
    modules['meta'] = meta_manager.MetaController()
except ImportError:
    modules['meta'] = None

# 2. Telegram
try:
    import telegram_manager
    modules['tg'] = telegram_manager.TelegramBot()
except ImportError:
    pass

# 3. Other Modules (Cloudflare, DNS, WP, Git, etc.)
# (Keep previous imports logic here or assume they are loaded)
try:
    import cloudflare_manager
    modules['cloud'] = cloudflare_manager.CloudflareTunnel()
    import dns_manager
    modules['dns'] = dns_manager.DNSController()
except ImportError:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin_secret_key_2026'
socketio = SocketIO(app)
current_dir = os.getcwd()

@app.route('/')
def index():
    return render_template('terminal_ui.html')

@socketio.on('command_input')
def handle_command(raw_command):
    global current_dir
    raw_command = raw_command.strip()
    if not raw_command: return

    parts = raw_command.split()
    cmd_start = parts[0].lower()

    # --- 1. META COMMANDS (Facebook, Insta, WhatsApp) ---
    if cmd_start == "meta":
        if not modules['meta']:
            emit('terminal_output', {'output': "❌ Error: Meta module missing."})
            return

        # Setup: meta setup <Token> <PageID> <InstaID> <PhoneID>
        if parts[1] == "setup" and len(parts) == 6:
            emit('terminal_output', {'output': modules['meta'].setup(parts[2], parts[3], parts[4], parts[5])})
            return

        # Facebook: meta fb This is a test post
        if parts[1] == "fb":
            message = " ".join(parts[2:])
            emit('terminal_output', {'output': modules['meta'].post_facebook(message)})
            return

        # Instagram: meta insta <ImageURL> <Caption>
        if parts[1] == "insta":
            if len(parts) < 4:
                emit('terminal_output', {'output': "Usage: meta insta <ImageURL> <Caption>"})
            else:
                caption = " ".join(parts[3:])
                emit('terminal_output', {'output': modules['meta'].post_instagram(parts[2], caption)})
            return

        # WhatsApp: meta wa <Number> <Message>
        if parts[1] == "wa":
            if len(parts) < 4:
                emit('terminal_output', {'output': "Usage: meta wa <PhoneNo> <Message>"})
            else:
                message = " ".join(parts[3:])
                emit('terminal_output', {'output': modules['meta'].send_whatsapp(parts[2], message)})
            return

    # --- 2. TELEGRAM & OTHERS (Existing) ---
    if cmd_start == "telegram" or cmd_start == "tg":
        if modules.get('tg') and parts[1] == "send":
            emit('terminal_output', {'output': modules['tg'].send_message(" ".join(parts[2:]))})
        return

    # Fallback Shell
    try:
        process = subprocess.Popen(raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
        out, err = process.communicate()
        emit('terminal_output', {'output': out.decode() + err.decode()})
    except Exception as e:
        emit('terminal_output', {'output': str(e)})

if __name__ == '__main__':
    print("--- 🚀 AI Admin Panel: Meta Trinity Integrated ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    
