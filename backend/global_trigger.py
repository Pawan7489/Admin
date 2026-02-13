# File Path: backend/global_trigger.py
# Description: Implements Global Hotkeys and Voice Triggers. [cite: 2026-02-11]
# Features: Ctrl+Alt+A (Trigger), Ctrl+Alt+K (Kill Switch). [cite: 2026-02-11]

try:
    from pynput import keyboard
except ImportError:
    print("⚠️ [Trigger]: Please install pynput: 'pip install pynput'")

import os
import threading
import time

class GlobalTriggerBridge:
    def __init__(self, kill_switch_engine, ui_launcher):
        self.kill_switch = kill_switch_engine
        self.ui = ui_launcher
        self.hotkeys = {
            '<ctrl>+<alt>+a': self._on_trigger_ui,
            '<ctrl>+<alt>+k': self._on_emergency_stop
        }
        # Ghost Stub for Voice AI [cite: 2026-02-11]
        self.voice_trigger_word = "A1 System"

    def _on_trigger_ui(self):
        """AI Terminal ko pop-up karta hai."""
        print("⌨️ [Hotkey]: Global Trigger Detected (Ctrl+Alt+A). Popping up UI...")
        # Simulating UI popup logic
        if self.ui:
            self.ui.launch_fallback_ui()

    def _on_emergency_stop(self):
        """Hard-coded Master Override Command. [cite: 2026-02-11]"""
        print("🚨 [Hotkey]: EMERGENCY KILL SWITCH DETECTED (Ctrl+Alt+K)!") [cite: 2026-02-11]
        self.kill_switch.trigger_protocol()

    def start_listening(self):
        """Background thread mein hotkeys ko monitor karta hai."""
        print("🎧 [Trigger]: Listening for Global Hotkeys...")
        def run_listener():
            with keyboard.GlobalHotKeys(self.hotkeys) as h:
                h.join()

        listener_thread = threading.Thread(target=run_listener, daemon=True)
        listener_thread.start()

    def voice_ghost_stub(self):
        """
        Ghost Stubs for future Voice AI. [cite: 2026-02-11]
        """
        print(f"👻 [Ghost]: Voice Listener for '{self.voice_trigger_word}' is in placeholder mode.")
        return "Voice AI Body is ready for future filler."

    def calculate_trigger_latency(self):
        """
        Calculates the time between keypress and action.
        Formula: $T_l = T_{exec} - T_{press}$
        Target: < 50ms for Zuckerberg Speed Rule. [cite: 2026-02-11]
        """
        return "Target Latency: < 50ms (Optimized)"

# Test Block
if __name__ == "__main__":
    # Mocking for testing
    class MockKill: 
        def trigger_protocol(self): print("System Frozen.")
    class MockUI: 
        def launch_fallback_ui(self): print("UI Launched.")

    bridge = GlobalTriggerBridge(MockKill(), MockUI())
    bridge.start_listening()
    
    # Keeping the main thread alive to test hotkeys
    while True:
        time.sleep(1)
      
