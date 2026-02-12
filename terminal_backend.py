# File: terminal_backend.py
# Description: Universal Admin Panel (WP + Blogger + All Previous Modules)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import platform

# --- MODULE AUTO-LOADER ---
# Hum check karenge ki files maujood hain ya nahi

modules = {}

# 1. WordPress
try:
    import wordpress_manager
    modules['wp'] = wordpress_manager.WordPressBot()
except ImportError:
    modules['wp'] = None

# 2. Blogger
try:
    import blogger_manager
    modules['blogger'] = blogger_manager.BloggerBot()
except ImportError:
    modules['blogger'] = None

# 3. Kaggle
try:
    import kaggle_manager
    modules['kaggle'] = kaggle_manager.KaggleBot()
except ImportError:
    modules['kaggle'] = None

# 4. Git
try:
    import git_ops
    modules['git'] = git_ops.GitManager()
except ImportError:
    modules['git'] = None

# 5. Hugging Face
try:
    import huggingface_manager
    modules['hf'] = huggingface_manager.ModelManager()
except ImportError:
    modules['hf'] = None

# 6. System Health
try:
    import system_health
    modules['health'] = system_health.SystemDoctor()
except ImportError:
    modules['health'] = None

# 7. Colab Bridge
try:
    import colab_bridge
    modules['colab'] = colab_bridge.ColabConnector()
except ImportError:
    modules['colab'] = None


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

    # --- 1. WORDPRESS COMMANDS ---
    if cmd_start == "wp":
        if not modules['wp']:
            emit('terminal_output', {'output': "❌ Error: WordPress module missing."})
            return
        
        # wp setup <url> <user> <pass>
        if parts[1] == "setup" and len(parts) == 5:
            emit('terminal_output', {'output': modules['wp'].setup(parts[2], parts[3], parts[4])})
            return
        
        # wp post <title> <content>
        if parts[1] == "post":
            # Simple content parsing (Title needs quotes logic in future, simple split for now)
            # Usage: wp post MyTitle This is my content
            if len(parts) < 4:
                emit('terminal_output', {'output': "Usage: wp post <Title_No_Spaces> <Content>"})
            else:
                emit('terminal_output', {'output': modules['wp'].create_post(parts[2], " ".join(parts[3:]))})
            return

    # --- 2. BLOGGER COMMANDS ---
    if cmd_start == "blogger":
        if not modules['blogger']:
            emit('terminal_output', {'output': "❌ Error: Blogger module missing."})
            return

        # blogger setup <json_file> <blog_id>
        if parts[1] == "setup" and len(parts) == 4:
            emit('terminal_output', {'output': modules['blogger'].setup(parts[2], parts[3])})
            return

        # blogger post <title> <content>
        if parts[1] == "post":
            emit('terminal_output', {'output': modules['blogger'].create_post(parts[2], " ".join(parts[3:]))})
            return

    # --- 3. EXISTING MODULE COMMANDS (Git, HF, Colab, Health, Kaggle) ---
    
    # Kaggle
    if cmd_start == "kaggle" and modules['kaggle']:
        if parts[1] == "download": 
            emit('terminal_output', {'output': modules['kaggle'].download_dataset(parts[2])})
            return

    # Colab
    if raw_command.lower() == "connect colab" and modules['colab']:
        emit('terminal_output', {'output': modules['colab'].get_setup_script()})
        return

    # Health
    if raw_command.lower() == "system status" and modules['health']:
        emit('terminal_output', {'output': modules['health'].diagnose()})
        return

    # Git
    if cmd_start == "git" and modules['git']:
        emit('terminal_output', {'output': modules['git'].execute_git(parts[1:])})
        return

    # Fallback System Command
    try:
        process = subprocess.Popen(raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
        out, err = process.communicate()
        emit('terminal_output', {'output': out.decode() + err.decode()})
    except Exception as e:
        emit('terminal_output', {'output': str(e)})

if __name__ == '__main__':
    print("--- 🚀 AI Admin Panel: CMS Integrated (WP + Blogger) ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    
