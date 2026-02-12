# File: terminal_backend.py
# Description: Admin Panel Core (Integrated with Git, HuggingFace, and System Health)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import platform

# --- MODULES AUTO-DETECTION (Plug & Play) ---
# Ye code check karega ki aapne file folder me daali hai ya nahi.
# Agar file milegi, to feature ON ho jayega. Agar nahi, to OFF.

# 1. Git Module
try:
    import git_ops
    git_available = True
    git_brain = git_ops.GitManager()
except ImportError:
    git_available = False
    print("⚠️  Warning: 'git_ops.py' nahi mila. Git commands kaam nahi karenge.")

# 2. Hugging Face Module
try:
    import huggingface_manager
    hf_available = True
    hf_brain = huggingface_manager.ModelManager()
except ImportError:
    hf_available = False
    print("⚠️  Warning: 'huggingface_manager.py' nahi mila. AI Models download nahi honge.")

# 3. System Health Module (NEW)
try:
    import system_health
    health_available = True
    sys_doc = system_health.SystemDoctor()
except ImportError:
    health_available = False
    print("⚠️  Warning: 'system_health.py' nahi mila. Doctor checkup fail.")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin_secret_key_2026'
socketio = SocketIO(app)

# Current Directory Setup
current_dir = os.getcwd()
os_type = platform.system()

# --- HELPER: Hinglish Translator ---
def translate_hinglish(command):
    cmd_lower = command.lower()
    
    # Logic: Folder Banane ka command
    if "folder" in cmd_lower and ("banao" in cmd_lower or "create" in cmd_lower):
        parts = command.split()
        folder_name = parts[-1] 
        return f"mkdir {folder_name}"

    # Logic: Delete karne ka command
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

    # --- 1. SYSTEM HEALTH COMMANDS (Doctor) ---
    if raw_command.lower() in ["system status", "health check", "tabiyat kaisi hai", "check system"]:
        if health_available:
            # Doctor module se report mango
            report = sys_doc.diagnose()
            emit('terminal_output', {'output': report})
        else:
            emit('terminal_output', {'output': "❌ Error: 'system_health.py' file missing hai."})
        return

    # --- 2. HUGGING FACE COMMANDS (AI Brain) ---
    if raw_command.startswith("hf "):
        if not hf_available:
            emit('terminal_output', {'output': "❌ Error: Hugging Face module missing."})
            return
            
        parts = raw_command.split()
        if parts[1] == "login" and len(parts) > 2:
            token = parts[2]
            emit('terminal_output', {'output': hf_brain.login_hf(token)})
        elif parts[1] == "download" and len(parts) > 2:
            model_name = parts[2]
            emit('terminal_output', {'output': hf_brain.download_model(model_name)})
        else:
            emit('terminal_output', {'output': "Usage: hf login <token> OR hf download <model_name>"})
        return

    # --- 3. GIT COMMANDS (Memory) ---
    if raw_command.lower() == "update system" or raw_command.lower() == "code update karo":
        if git_available:
            emit('terminal_output', {'output': "🔄 Pulling latest code from GitHub..."})
            emit('terminal_output', {'output': git_brain.pull_updates()})
        else:
            emit('terminal_output', {'output': "❌ Git module not loaded."})
        return

    if raw_command.startswith("git ") and git_available:
        parts = raw_command.split()[1:]
        emit('terminal_output', {'output': git_brain.execute_git(parts)})
        return

    # --- 4. NORMAL SYSTEM COMMANDS (Shell) ---
    
    # Hinglish Translation
    final_command = translate_hinglish(raw_command)
    
    # Directory Change (cd) logic
    if final_command.startswith('cd '):
        try:
            target_dir = final_command[3:].strip()
            os.chdir(target_dir)
            current_dir = os.getcwd()
            emit('terminal_output', {'output': f"Directory changed to: {current_dir}"})
        except Exception as e:
            emit('terminal_output', {'output': f"Error: {str(e)}"})
        return

    # Execute Command
    try:
        process = subprocess.Popen(
            final_command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            stdin=subprocess.PIPE,
            cwd=current_dir
        )
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8', errors='ignore') + stderr.decode('utf-8', errors='ignore')
        
        if not output:
            output = "Command executed."
            
        emit('terminal_output', {'output': output})
        
    except Exception as e:
        emit('terminal_output', {'output': f"Execution Error: {str(e)}"})

if __name__ == '__main__':
    print("--- 🚀 AI Admin Panel Started (Monitoring Mode) ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
