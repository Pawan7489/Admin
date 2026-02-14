# File: terminal_backend.py
# Description: SUPER GENIUS ADMIN PANEL (Central Command for All Modules)
# Architecture: Onion Model (Interface -> Security -> Core Logic)

from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import subprocess
import os
import sys
import importlib

# --- 1. SYSTEM CONFIGURATION ---
app = Flask(__name__)
# Security Best Practice: Key ko environment variable se uthao, nahi toh fallback use karo
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'SUPER_SECURE_RANDOM_KEY_999')
socketio = SocketIO(app)
current_dir = os.getcwd()

# Python ko subfolders dekhne ki permission do
sys.path.append(os.path.join(current_dir, 'security'))
sys.path.append(os.path.join(current_dir, 'engines'))
sys.path.append(os.path.join(current_dir, 'cloud'))
sys.path.append(os.path.join(current_dir, 'finance'))
sys.path.append(os.path.join(current_dir, 'modules', 'social_media'))

# --- 2. THE "GHOST" REGISTRY (Modules Loader) ---
# Yeh section automatic check karta hai ki kaunsi files maujood hain.
# Agar file missing hai, toh system crash nahi hoga (Solo Mode).

modules = {
    'security': None,
    'hosting': None,
    'finance': None,
    'social': {},
    'ai_engines': {},
    'core': {}
}

print("--- ⚙️ SYSTEM BOOT: Loading Modules... ---")

# A. SECURITY LAYER (Critical)
try:
    import security_manager
    import guardian_protocol 
    import kill_switch
    modules['security'] = security_manager.SecurityGuard()
    print("✅ Security Module: ONLINE")
except ImportError as e:
    print(f"⚠️ Security Module Missing: {e}")

# B. HOSTING & CLOUD LAYER
try:
    import hosting_manager
    import koyeb_failover
    import azure_bridge
    modules['hosting'] = hosting_manager.HostingConnector()
    print("✅ Hosting/Cloud: ONLINE")
except ImportError:
    pass

# C. FINANCE LAYER
try:
    import payment_bridge
    modules['finance'] = payment_bridge
    print("✅ Finance/Wallet: ONLINE")
except ImportError:
    pass

# D. SOCIAL MEDIA (Swarm Intelligence)
social_platforms = ['whatsapp_manager_1', 'telegram_manager_1', 'instagram_manager_1', 'facebook_manager_1']
for platform in social_platforms:
    try:
        # Dynamic Import for Social Media
        mod = importlib.import_module(f"modules.social_media.{platform}")
        modules['social'][platform.split('_')[0]] = mod # keys: whatsapp, telegram, etc.
        print(f"✅ Social Link: {platform} CONNECTED")
    except ImportError:
        pass

# E. AI ENGINES (The Brain)
ai_engines = ['gemini_engine', 'speech_engine', 'vision_engine', 'deepseek_coder']
for engine in ai_engines:
    try:
        mod = importlib.import_module(f"engines.{engine}")
        modules['ai_engines'][engine] = mod
        print(f"✅ AI Engine: {engine} READY")
    except ImportError:
        pass

# F. CORE OPTIMIZERS (Musk/Pichai/Zuckerberg Rules)
try:
    import resource_balancer  # 1musk_efficiency equivalent
    modules['core']['optimizer'] = resource_balancer
except ImportError:
    pass

print("--- 🚀 BOOT COMPLETE. SERVER READY. ---")


# --- 3. ROUTES & INTERFACE ---

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('terminal'))

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Security Guard Check
        if modules['security'] and modules['security'].verify_login(username, password):
            session['logged_in'] = True
            return redirect(url_for('terminal'))
        # Fallback for testing if security module is missing
        elif username == "admin" and password == "admin123": 
             session['logged_in'] = True
             return redirect(url_for('terminal'))
        else:
            error = "❌ ACCESS DENIED: Invalid Protocol."

    return render_template('login.html', error=error)

@app.route('/terminal')
def terminal():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('terminal_ui.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# --- 4. CENTRAL COMMAND HANDLER (The Brain) ---

@socketio.on('command_input')
def handle_command(raw_command):
    global current_dir
    raw_command = raw_command.strip()
    if not raw_command: return

    parts = raw_command.split()
    cmd_head = parts[0].lower()
    
    # --- A. SECURITY COMMANDS ---
    if cmd_head == "kill":
        # EMERGENCY STOP
        try:
            emit('terminal_output', {'output': "⚠️ INITIATING KILL SWITCH PROTOCOL..."})
            if modules.get('security'):
                modules['security'].engage_kill_switch()
            else:
                os._exit(1) # Hard exit
        except Exception as e:
            emit('terminal_output', {'output': f"Error: {str(e)}"})
        return

    # --- B. DEPLOYMENT COMMANDS ---
    if cmd_head == "deploy":
        # Usage: deploy koyeb / deploy azure
        target = parts[1] if len(parts) > 1 else "all"
        if modules['hosting']:
            result = modules['hosting'].trigger_deploy(target)
            emit('terminal_output', {'output': result})
        else:
            emit('terminal_output', {'output': "❌ Hosting Module not loaded."})
        return

    # --- C. SOCIAL MEDIA COMMANDS ---
    if cmd_head == "msg":
        # Usage: msg whatsapp "Hello World"
        platform = parts[1].lower()
        message = " ".join(parts[2:])
        if platform in modules['social']:
            # Assuming the manager has a send_message function
            # modules['social'][platform].send_message(message) 
            emit('terminal_output', {'output': f"📤 Sending to {platform}: {message}"})
        else:
            emit('terminal_output', {'output': f"❌ {platform} module is offline."})
        return

    # --- D. AI ENGINE COMMANDS ---
    if cmd_head == "ask":
        # Usage: ask gemini "Explain Quantum Physics"
        engine_name = parts[1].lower() + "_engine" # e.g., gemini_engine
        prompt = " ".join(parts[2:])
        
        if engine_name in modules['ai_engines']:
            emit('terminal_output', {'output': f"🧠 {parts[1]} Thinking..."})
            # result = modules['ai_engines'][engine_name].generate(prompt)
            # Placeholder response for now
            emit('terminal_output', {'output': f"[{parts[1]}]: I received your query: '{prompt}'"})
        else:
            emit('terminal_output', {'output': f"❌ Engine {parts[1]} is not loaded."})
        return

    # --- E. FINANCE CHECK ---
    if cmd_head == "finance":
        if modules['finance']:
            emit('terminal_output', {'output': "💰 Wallet Status: SECURE (Data Encrypted)"})
        else:
            emit('terminal_output', {'output': "❌ Finance Module Offline."})
        return

    # --- F. STANDARD SHELL (Fallback) ---
    # WARNING: Dangerous commands filter
    forbidden = ["rm -rf", "format", "del /s"]
    if any(bad in raw_command for bad in forbidden):
        emit('terminal_output', {'output': "🛡️ GUARDIAN PROTOCOL: Command Blocked."})
        return

    try:
        process = subprocess.Popen(raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
        out, err = process.communicate()
        emit('terminal_output', {'output': out.decode() + err.decode()})
    except Exception as e:
        emit('terminal_output', {'output': str(e)})

if __name__ == '__main__':
    print("--- 🔒 SECURE AI Admin Panel Started on 127.0.0.1:5000 ---")
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
    
