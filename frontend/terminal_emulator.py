# File Path: frontend/terminal_emulator.py
# Description: Captures system logs and streams them to the Web UI. [cite: 2026-02-12]
# Ensures transparency by showing what's happening under the 'Onion Layers'.

import streamlit as st
import sys
import io
import time

class VisualTerminal:
    def __init__(self):
        # Buffer to catch all print statements
        if 'terminal_log' not in st.session_state:
            st.session_state.terminal_log = "🚀 [A1 OS]: System Terminal Initialized...\n"
        
        self.log_container = st.empty()

    def capture_output(self, func, *args, **kwargs):
        """
        Kisi bhi function ke output ko terminal window mein dikhata hai. [cite: 2026-02-11]
        """
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        try:
            # Function execute ho raha hai [cite: 2026-02-11]
            result = func(*args, **kwargs)
            output = new_stdout.getvalue()
            self.update_log(output)
            return result
        finally:
            sys.stdout = old_stdout

    def update_log(self, new_text):
        """Log buffer mein naya text add karta hai."""
        if new_text.strip():
            timestamp = time.strftime("%H:%M:%S")
            st.session_state.terminal_log += f"[{timestamp}] {new_text}\n"

    def render_ui(self):
        """Web dashboard par terminal window banata hai."""
        st.write("---")
        st.subheader("📟 Real-Time System Terminal")
        
        # Terminal-style CSS [cite: 2026-02-11]
        st.markdown(
            f"""
            <div style="
                background-color: #1e1e1e;
                color: #00ff00;
                padding: 15px;
                border-radius: 5px;
                height: 300px;
                overflow-y: scroll;
                font-family: 'Courier New', Courier, monospace;
                white-space: pre-wrap;
                font-size: 14px;
                border: 1px solid #333;
            ">
                {st.session_state.terminal_log}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("Clear Terminal"):
            st.session_state.terminal_log = "🧹 [System]: Logs cleared.\n"
            st.rerun()

# Logic for Latency calculation
# Formula: $L_t = T_{display} - T_{log}$
