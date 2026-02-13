# File Path: server.py (Root Directory)
# Description: The Ultimate Central Hub for A1 OS (Flask + WebSockets)
# Ye file automatic backend, templates aur static folders ko connect kar legi.

import os
import sys
import subprocess
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# ==========================================
# 1. PATH CONFIGURATION (Auto-Linking)
# ==========================================
# Ye system ko batata hai ki saari logic 'backend' folder me hai
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(backend_dir)

# ==========================================
# 2. MODULE AUTO-LOADER (Plug & Play)
# ==========================================
modules = {}

# Backend folder se modules load karne ki koshish
def load_module(module_name, class_name, key):
    try:
        mod = __import__(module_name)
        modules[key] = getattr(mod, class_name)()
        print(f"✅ Loaded: {module_name}")
    except (ImportError, AttributeError) as e:
        modules[key] = None
        print(f"⚠️ Skipped: {module_name} (Not found or error)")

print("\n--- 🔄 SCANNING BACKEND FOLDER ---")
# Loading our created boxes from backend/ folder
load_module('engine_manager', 'EngineRegistry', 'engine')
load_module('storage_manager', 'StorageRegistry', 'storage')
load_module('hosting_manager', 'HostingConnector', 'host')
load_module('domain_registry', 'DomainController', 'domain')
load_module('meta_manager', 'MetaController', 'meta')
load_module('plugin_store', 'PluginMarketplace', 'plugin')

# Load AI Council separately (if exists)
try:
    import ai_council
    modules['council'] = ai_council.CouncilOfExperts()
    council_active = True
    print("✅ Loaded: ai_council (Security Active)")
except ImportError:
    council_active = False
    print("⚠️ Skipped: ai_council")
print("----------------------------------\n")

# ==========================================
# 3. SERVER SETUP (Flask + SocketIO)
# ==========================================
# Auto-connects templates/ and static/ folders
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = 'A1_MASTER_KEY_ULTRA_SECURE_2026'
socketio = SocketIO(app, cors_allowed_origins="*")
current_dir = os.getcwd()

# ==========================================
# 4. WEB ROUTES
# ==========================================
@app.route('/')
def home():
    """Serves the main A1 OS Graphical Interface from templates/index.html"""
    return render_template('index.html')

# ==========================================
# 5. WEBSOCKET REAL-TIME BRIDGE
# ==========================================
@socketio.on('connect')
def handle_connect():
    print("🟢 SYSTEM LINKED: A new Admin Session started.")

@socketio.on('command_input')
def handle_command(raw_command):
    global current_dir
    raw_command = raw_command.strip()
    if not raw_command: return

    # --- EMERGENCY PROTOCOL ---
    if raw_command == 'SYSTEM_FREEZE_PROTOCOL_ACTIVATE':
        print("🚨 KILL SWITCH ACTIVATED BY ADMIN!")
        emit('terminal_output', {'output': "🛑 [CRITICAL] System processes halted. Network offline."})
        return

    # --- AI COUNCIL AUDIT (If exists) ---
    if council_active:
        audit = modules['council'].audit_intent(raw_command)
        if not audit.get('approved', True):
            emit('terminal_output', {'output': f"❌ BLOCKED BY SECURITY: {audit.get('reason', 'Unknown Error')}"})
            return

    # --- INTENT ROUTER (Module Execution) ---
    parts = raw_command.split()
    cmd = parts[0].lower()

    try:
        # Storage Box Commands
        if cmd == "storage" and modules.get('storage'):
            if parts[1] == "list": emit('terminal_output', {'output': modules['storage'].list_storage()})
            elif parts[1] == "add": emit('terminal_output', {'output': modules['storage'].add_storage(parts[2], parts[3], " ".join(parts[4:]))})
            return
            
        # Engine Hub Commands
        if cmd == "engine" and modules.get('engine'):
            if parts[1] == "list": emit('terminal_output', {'output': modules['engine'].list_engines()})
            elif parts[1] == "start": emit('terminal_output', {'output': modules['engine'].start_engine(parts[2])})
            return

        # Hosting Commands
        if cmd == "hosting" and modules.get('host'):
            if parts[1] == "list": emit('terminal_output', {'output': modules['host'].list_hosting()})
            return

        # Fallback: Normal Terminal Command Execution
        process = subprocess.Popen(raw_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
        out, err = process.communicate()
        output_text = out.decode() + err.decode()
        if not output_text.strip(): output_text = "Task Completed Successfully."
        
        emit('terminal_output', {'output': output_text})

    except Exception as e:
        emit('terminal_output', {'output': f"⚠️ Execution Error: {str(e)}"})


# ==========================================
# 6. SYSTEM STARTUP
# ==========================================
if __name__ == '__main__':
    print("="*50)
    print(" 🚀 A1 OS MASTER SERVER INITIALIZING...")
    print("="*50)
    print(f" 📂 Working Directory: {current_dir}")
    print(" 🌐 Server running at: http://127.0.0.1:5000")
    print("="*50)
    
    # Run the server securely on localhost
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
          
