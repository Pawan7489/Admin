# File: terminal_backend.py
# Description: Admin Terminal + App Store Logic (AI-PKG)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import json
import platform

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin_secret_key_2026'
socketio = SocketIO(app)

# Setup Environment
current_dir = os.getcwd()
PLUGINS_DIR = os.path.join(current_dir, "installed_apps")
if not os.path.exists(PLUGINS_DIR):
    os.makedirs(PLUGINS_DIR)

# --- AI Logic Core ---
def ai_package_manager(command):
    """
    Handles App Store commands like 'list apps' or 'install <app_name>'
    """
    cmd_parts = command.split()
    action = cmd_parts[0].lower()

    # COMMAND: list apps
    if action == "list" and "apps" in command:
        try:
            with open('store.json', 'r') as f:
                data = json.load(f)
            output = "\n--- 📦 AVAILABLE APPS IN AI STORE ---\n"
            for app_id, details in data.items():
                output += f"• {app_id} (v{details['version']}): {details['description']}\n"
            return output
        except FileNotFoundError:
            return "Error: store.json not found. Database missing."

    # COMMAND: install <app_name>
    if action == "install":
        if len(cmd_parts) < 2:
            return "Error: App name bataiye. Usage: install <app_name>"
        
        app_name = cmd_parts[1]
        
        try:
            with open('store.json', 'r') as f:
                data = json.load(f)
            
            if app_name in data:
                # Code fetch karo store se
                app_code = data[app_name]['code']
                
                # File banao 'installed_apps' folder mein
                file_path = os.path.join(PLUGINS_DIR, f"{app_name}.py")
                with open(file_path, 'w') as app_file:
                    app_file.write(app_code)
                
                return f"✅ SUCCESS: '{data[app_name]['name']}' installed successfully in /installed_apps/"
            else:
                return f"❌ Error: App '{app_name}' store mein nahi mila."
                
        except Exception as e:
            return f"Error during installation: {str(e)}"

    return None

# --- Main Command Handler ---
@socketio.on('command_input')
def handle_command(raw_command):
    global current_dir
    raw_command = raw_command.strip()
    
    if not raw_command:
        return

    # Check 1: App Store Command?
    store_response = ai_package_manager(raw_command)
    if store_response:
        emit('terminal_output', {'output': store_response})
        return

    # Check 2: Run Installed App? (e.g., "run system-monitor")
    if raw_command.startswith("run "):
        app_name = raw_command.split()[1]
        script_path = os.path.join(PLUGINS_DIR, f"{app_name}.py")
        if os.path.exists(script_path):
            raw_command = f"python {script_path}"
        else:
            emit('terminal_output', {'output': f"Error: App '{app_name}' installed nahi hai."})
            return

    # Check 3: System/Hinglish Commands (Existing Logic)
    try:
        process = subprocess.Popen(
            raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir
        )
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8', errors='ignore') + stderr.decode('utf-8', errors='ignore')
        if not output: output = "Done."
        emit('terminal_output', {'output': output})
    except Exception as e:
        emit('terminal_output', {'output': f"Error: {str(e)}"})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
        if os_type == "Windows":
            return "dir"
        else:
            return "ls -la"

    # Logic 3: Delete karne ka command
    # User: "Images folder uda do" or "delete folder Images"
    if "delete" in cmd_lower or "uda do" in cmd_lower:
        target = parts[-1]
        if os_type == "Windows":
            return f"rmdir /s /q {target}" # Dangerous command, use carefully
        else:
            return f"rm -rf {target}"

    # Agar koi Hinglish pattern match nahi hua, toh original command wapas karo
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

    # STEP 1: AI Translation Layer
    # Pehle hum Hinglish check karenge
    final_command = translate_hinglish(raw_command)

    # User ko dikhao ki AI ne kya samjha (Feedback Loop)
    if final_command != raw_command:
        emit('terminal_output', {'output': f"🤖 AI Logic: Translating '{raw_command}' -> '{final_command}'..."})

    # STEP 2: Execution Layer
    # Directory Change (Special Case)
    if final_command.startswith('cd '):
        try:
            target_dir = final_command[3:].strip()
            os.chdir(target_dir)
            current_dir = os.getcwd()
            emit('terminal_output', {'output': f"Directory changed to: {current_dir}"})
        except Exception as e:
            emit('terminal_output', {'output': f"Error: {str(e)}"})
            
    # System Command Execution
    else:
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
                output = "Done."
                
            emit('terminal_output', {'output': output})
            
        except Exception as e:
            emit('terminal_output', {'output': f"Execution Error: {str(e)}"})

if __name__ == '__main__':
    print(f"--- AI Admin Terminal Active on {os_type} ---")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
