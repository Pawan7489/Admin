# File Path: backend/ui_generator.py
# Description: Implements 'Interface Insurance'. [cite: 2026-02-11]
# Automatically generates a fallback UI on localhost:7860 if the main UI is offline.

import os
import threading
import time

class InterfaceInsurance:
    def __init__(self, intent_engine):
        self.engine = intent_engine
        self.fallback_port = 7860
        self.ui_type = "Gradio" # As per Master Plan [cite: 2026-02-11]

    def launch_fallback_ui(self):
        """
        Gradio ka upyog karke ek simple auto-generated UI banata hai. [cite: 2026-02-11]
        Ye tab kaam aata hai jab aap 'Black Code Screen' se bachna chahte hain.
        """
        try:
            import gradio as gr
        except ImportError:
            return "❌ Error: Gradio library not found. Please run 'pip install gradio'."

        print(f"🛠️ [Interface Insurance]: Generating Fallback UI on port {self.fallback_port}...") [cite: 2026-02-11]

        def a1_terminal_proxy(user_input):
            # Seedha Intent Engine se baat karta hai [cite: 2026-02-11]
            response = self.engine.process_intent(user_input)
            return response

        # Simple Interface for A1 OS
        with gr.Blocks(title="A1 OS - Fallback Interface") as demo:
            gr.Markdown(f"# 🤖 A1 CORE - INTERFACE INSURANCE")
            gr.Markdown("### Main UI not detected. Fallback Mode Active.")
            
            with gr.Row():
                with gr.Column(scale=4):
                    user_msg = gr.Textbox(label="Enter Hinglish Command", placeholder="e.g., 'Ek naya folder banao'")
                    submit_btn = gr.Button("Execute Command", variant="primary")
                
                with gr.Column(scale=1):
                    # Solo Mode Indicators [cite: 2026-02-11]
                    gr.Label("SOLO MODE: ACTIVE")
                    gr.Label("SECURE BRIDGE: CONNECTED")

            output = gr.Textbox(label="A1 Terminal Output", interactive=False)
            
            submit_btn.click(fn=a1_terminal_proxy, inputs=user_msg, outputs=output)

        # Launching in a separate thread to not block the main OS
        thread = threading.Thread(target=demo.launch, kwargs={"server_port": self.fallback_port, "share": False, "prevent_thread_lock": True})
        thread.start()
        print(f"✅ [Interface Insurance]: Fallback UI is live at http://localhost:{self.fallback_port}") [cite: 2026-02-11]

    def monitor_main_ui(self, main_ui_status):
        """
        Agar main UI (Flask) fail hota hai, toh ye fallback trigger karta hai. [cite: 2026-02-11]
        """
        if not main_ui_status:
            print("⚠️ [Interface Insurance]: Main UI detected as OFFLINE. Triggering Fallback UI...")
            self.launch_fallback_ui()

# Test Block (Standalone)
if __name__ == "__main__":
    # Mocking Intent Engine for testing
    class MockEngine:
        def process_intent(self, text): return f"Intent '{text}' received via Fallback UI."
    
    insurance = InterfaceInsurance(MockEngine())
    insurance.launch_fallback_ui()
    # Keeping script alive for testing
    while True: time.sleep(1)
          
