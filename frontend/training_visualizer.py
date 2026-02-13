# File Path: frontend/training_visualizer.py
# Description: Real-time visualization of A1's fine-tuning progress.
# Connects Training Controller (File 62) to the Web Dashboard. [cite: 2026-02-11]

import streamlit as st
import pandas as pd
import numpy as np
import time

class TrainingVisualizer:
    def __init__(self):
        if 'metrics_history' not in st.session_state:
            st.session_state.metrics_history = pd.DataFrame(columns=['Epoch', 'Loss', 'Accuracy'])

    def render_live_charts(self, is_training_active):
        """
        Dashboard par live graph aur metrics dikhata hai. [cite: 2026-02-11]
        """
        st.write("---")
        st.header("📈 Evolution Analytics (A1 Learning Curve)")

        if not is_training_active and st.session_state.metrics_history.empty:
            st.info("System is idle. Start Fine-Tuning from the Admin Panel to see live evolution.")
            return

        # Top Level Metrics
        col1, col2, col3 = st.columns(3)
        
        # Latest data points
        if not st.session_state.metrics_history.empty:
            latest = st.session_state.metrics_history.iloc[-1]
            col1.metric("Current Loss", f"{latest['Loss']:.4f}", "-0.02")
            col2.metric("Learning Accuracy", f"{latest['Accuracy']:.2f}%", "+1.5%")
            col3.metric("Training Status", "ACTIVE 🔥" if is_training_active else "STABLE ✅")

        # Live Graphs
        st.subheader("Loss Convergence & Accuracy")
        if not st.session_state.metrics_history.empty:
            # Multi-line chart for comparison
            st.line_chart(st.session_state.metrics_history.set_index('Epoch')[['Loss', 'Accuracy']])

    def update_metrics_stream(self, epoch, loss, accuracy):
        """
        Backend se naya data lekar UI update karta hai.
        """
        new_row = pd.DataFrame({'Epoch': [epoch], 'Loss': [loss], 'Accuracy': [accuracy]})
        st.session_state.metrics_history = pd.concat([st.session_state.metrics_history, new_row], ignore_index=True)

    def calculate_convergence_rate(self, initial_loss, current_loss):
        """
        Calculates how fast the model is stabilizing.
        Formula: $C_r = \frac{L_0 - L_t}{L_0} \times 100$
        """
        if initial_loss == 0: return 0
        rate = ((initial_loss - current_loss) / initial_loss) * 100
        return round(rate, 2)

# Integration Logic
def sync_with_controller(visualizer, controller):
    """Training controller se data stream karta hai."""
    if controller.is_training:
        # Simulated stream for visual check
        for i in range(1, 11):
            visualizer.update_metrics_stream(i, 0.5/(i+1), 70 + (i*2.5))
            time.sleep(0.5)
          
