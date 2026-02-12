# File: terminal_backend.py
# Description: Universal Admin Panel (All Modules Integrated)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import platform

# --- MODULE AUTO-LOADER (Plug & Play) ---

# 1. Git Module
try:
    import git_ops
    git_available = True
    git_brain = git_ops.GitManager()
except ImportError:
    git_available = False

# 2. Hugging Face Module
try:
    import huggingface_manager
    hf_available = True
    hf_brain = huggingface_manager.ModelManager()
except ImportError:
    hf_available = False

# 3. System Health (Doctor)
try:
    import system_health
    health_available = True
    sys_doc = system_health.SystemDoctor()
except ImportError:
    health_available = False

# 4. Google Colab Bridge (NEW)
try:
    import colab_bridge
    colab_available = True
    colab_link = colab_bridge.ColabConnector()
except ImportError:
    colab_available = False

# --- FLASK APP SETUP ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin_secret_key_2026'
socketio = SocketIO(app)

current_dir = os.getcwd()
os_type = platform.system()

# --- HELPER FUNCTIONS ---
def translate_hinglish(command):
    cmd_lower = command.lower()
    
    # Logic: Folder Create
    if "folder" in cmd_lower and ("banao" in cmd_lower or "create" in cmd_lower):
        parts = command.split()
        folder_name = parts[-1] 
        return f"mkdir {folder_name}"

    # Logic: Delete File/Folder
    if "delete" in cmd_lower or "uda do" in cmd_lower:
        parts = command.split()
        target = parts[-1]
        if os_type == "Windows":
            return f"rmdir /s /q {target}"
        else:
            return f"rm -rf {target}"
            
    return command

@app.route('/')
def index():
    return render_template('terminal_ui.html')

@socketio.on('command_input')
def handle_command(raw_command):
    global current_dir
    raw_command = raw_command.strip()
    
    if not raw_command:
        return

    # --- 1. GOOGLE COLAB COMMANDS (NEW) ---
    if raw_command.lower() in ["connect colab", "colab setup", "google colab jodo"]:
        if colab_available:
            script = colab_link.get_setup_script()
            # User ko code bhejo
            emit('terminal_output', {'output': "👇 Copy this code and paste it in Google Colab Cell:"})
            emit('terminal_output', {'output': "------------------------------------------------"})
            emit('terminal_output', {'output': script})
            emit('terminal_output', {'output': "------------------------------------------------"})
        else:
            emit('terminal_output', {'output': "❌ Error: 'colab_bridge.py' file missing hai."})
        return

    # --- 2. SYSTEM HEALTH COMMANDS ---
    if raw_command.lower() in ["system status", "health check", "tabiyat kaisi hai"]:
        if health_available:
            report = sys_doc.diagnose()
            emit('terminal_output', {'output': report})
        else:
            emit('terminal_output', {'output': "❌ Error: Doctor module ('system_health.py') missing."})
        return

    # --- 3. HUGGING FACE COMMANDS ---
    if raw_command.startswith("hf "):
        if hf_available:
            parts = raw_command.split()
            if len(parts) > 2:
                if parts[1] == "login":
                    emit('terminal_output', {'output': hf_brain.login_hf(parts[2])})
                elif parts[1] == "download":
                    emit('terminal_output', {'output': hf_brain.download_model(parts[2])})
            else:
                emit('terminal_output', {'output': "Usage: hf login <token> | hf download <model_name>"})
        else:
            emit('terminal_output', {'output': "❌ Error: Hugging Face module missing."})
        return

    # --- 4. GIT COMMANDS ---
    if raw_command.lower() == "update system" and git_available:
        emit('terminal_output', {'output': git_brain.pull_updates()})
        return
        
    if raw_command.startswith("git ") and git_available:
        parts = raw_command.split()[1:]
        emit('terminal_output', {'output': git_brain.execute_git(parts)})
        return

    # --- 5. NORMAL COMMANDS (Fallback) ---
    final_command = translate_hinglish(raw_command)

    # CD Logic
    if final_command.startswith('cd '):
        try:
            target_dir = final_command[3:].strip()
            os.chdir(target_dir)
            current_dir = os.getcwd()
            emit('terminal_output', {'output': f"Directory changed to: {current_dir}"})
        except Exception as e:
            emit('terminal_output', {'output': f"Error: {str(e)}"})
        return

    # Execute
    try:
        process = subprocess.Popen(
            final_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
            stdin=subprocess.PIPE, cwd=current_dir
        )
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8', errors='ignore') + stderr.decode('utf-8', errors='ignore')
        
        if not output: output = "Command executed successfully."
        emit('terminal_output', {'output': output})
        
    except Exception as e:
        emit('terminal_output', {'output': f"Execution Error: {str(e)}"})

if __name__ == '__main__':
    print("--- 🚀 AI Admin Panel Started (With Colab Bridge) ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    
