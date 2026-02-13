# File Path: server.py (Root Directory)
# Description: The Final Integrated Hub linking all 25 Modules. [cite: 2026-02-11]
# Implements: Solo Mode, Onion Architecture, Intent Core, & Kill Switch. [cite: 2026-02-11]

import os
import sys
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# 1. DISTRIBUTED PATH LINKING (Bridge Rule) [cite: 2026-02-11]
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(backend_path)

# 2. MODULE INITIALIZATION (Solo Mode & Ghost Protocol) [cite: 2026-02-11]
try:
    from master_registry import MasterBlueprint
    from system_health import SystemDoctor
    from guardian_protocol import GuardianShield
    from onion_wrapper import OnionWrapper, ValidationLayer
    from intent_parser import IntentEngine
    from internal_critique import CritiqueEngine
    from kill_switch import EmergencyKillSwitch
    from logic_version_control import TimeTravelManager
    from relevance_engine import RelevanceEngine
    from config_manager import ConfigManager
    
    # Initializing Core Components
    config = ConfigManager()
    blueprint = MasterBlueprint()
    doctor = SystemDoctor()
    shield = GuardianShield()
    critique = CritiqueEngine()
    kill_protocol = EmergencyKillSwitch()
    
    # Linking Modules for Intent Engine [cite: 2026-02-11]
    active_mods = blueprint.scan_distributed_units()
    intent_core = IntentEngine(active_mods)
    
    # Wrapping in Onion Architecture (Ball-in-Ball) [cite: 2026-02-11]
    validator = ValidationLayer()
    onion_system = OnionWrapper(intent_core, shield, validator)
    
    BOOT_SUCCESS = True
except ImportError as e:
    print(f"⚠️ [Solo Mode]: Missing non-essential module: {e}. Continuing...") [cite: 2026-02-11]
    BOOT_SUCCESS = False

# 3. SERVER SETUP
app = Flask(__name__, template_folder="templates", static_folder="static")
socketio = SocketIO(app, cors_allowed_origins="*")

# 4. STARTUP PROTOCOL: 5-Second Self-Diagnosis [cite: 2026-02-11]
def run_startup_diagnosis():
    print("\n" + "="*50)
    print("🚀 A1 CORE ENGINE: INITIALIZING STARTUP PROTOCOL...") [cite: 2026-02-11]
    health = doctor.run_full_diagnosis()
    time.sleep(2) # Simulated 5-second check [cite: 2026-02-11]
    
    if not health['is_safe']:
        print(f"🛑 [CRITICAL]: {health['warnings']}") [cite: 2026-02-11]
    else:
        print("✅ SYSTEM DIAGNOSIS: 100% HEALTHY.") [cite: 2026-02-11]
    print("="*50 + "\n")

# 5. ROUTES & SOCKET EVENTS
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command_input')
def handle_intent(command):
    """Processes Hinglish Intent via the Onion Security Layers. [cite: 2026-02-11]"""
    
    # A. Emergency Kill Switch Check [cite: 2026-02-11]
    if "system freeze" in command.lower() or "kill" in command.lower():
        emit('terminal_output', {'output': "🚨 KILL SWITCH TRIGGERED! LOCKING SYSTEM..."})
        kill_protocol.trigger_protocol()
        return

    # B. Internal Critique: Generating Reasoning Path [cite: 2026-02-11]
    emit('terminal_output', {'output': "🧠 AI is thinking (Internal Critique)..."})
    audit = critique.finalize_execution(command, "Onion_Processing")
    
    # C. Onion Processing (Security & Validation) [cite: 2026-02-11]
    result = onion_system.process_request(command)
    
    # D. RLHF Feedback Slot [cite: 2026-02-11]
    output_message = f"{result['core_output']}\n\n[Rate this: 👍 Good Job | 👎 Bad]"
    emit('terminal_output', {'output': output_message})

# 6. RUN
if __name__ == '__main__':
    if BOOT_SUCCESS:
        run_startup_diagnosis()
        socketio.run(app, host='127.0.0.1', port=5000, debug=True)
        
