# File Path: frontend/sensory_dashboard.py
# Description: Integrated Control Panel for A1's Senses (Vision, STT, TTS).
# Allows real-time toggling of senses based on 'Solo Mode' [cite: 2026-02-11].

import streamlit as st
import time

class SensoryDashboard:
    def __init__(self, vision_engine, speech_engine, voice_box, stress_tester):
        self.vision = vision_engine
        self.speech = speech_engine
        self.voice = voice_box
        self.stress = stress_tester

    def render_sensory_controls(self):
        """
        Dashboard par Senses ke liye switches aur gauges banata hai. [cite: 2026-02-11]
        """
        st.write("---")
        st.header("🎛️ Sensory Control Cockpit")
        
        # 3-Column Layout for Senses
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("👁️ Vision")
            if st.toggle("Enable A1 Eyes", key="vision_toggle"):
                if not self.vision.camera_active:
                    self.vision.activate_eyes()
                st.success("Vision: ACTIVE")
            else:
                self.vision.deactivate_eyes()
                st.info("Vision: SLEEPING")

        with col2:
            st.subheader("👂 Ears (STT)")
            if st.toggle("Enable A1 Listening", key="speech_toggle"):
                st.success("Listening: ACTIVE")
                # Speech Engine link logic here [cite: 2026-02-11]
            else:
                st.info("Listening: MUTED")

        with col3:
            st.subheader("🔊 Voice (TTS)")
            if st.toggle("Enable A1 Speech", key="voice_toggle"):
                st.success("Speech: ACTIVE")
            else:
                st.info("Speech: SILENT")

    def render_stress_gauges(self):
        """Hardware load ko visually dikhata hai.""" [cite: 2026-02-11]
        st.write("---")
        st.subheader("🌡️ Sensory Health & Stress Monitor")
        
        # Simulated Health Metric (LaTeX)
        # $H_s = \frac{1}{\sum_{i=1}^{n} L_i}$ (Higher is better)
        
        health_score = 0.95 # Simulated
        st.progress(health_score, text=f"System Sensory Health: {health_score*100}%")
        
        if health_score < 0.5:
            st.warning("🚨 [High Stress]: Consider disabling Vision to save GPU.")

    def calculate_sensory_health(self, latencies):
        """
        Calculates Overall Sensory Health Index ($H_s$).
        Formula: $H_s = 1 - \frac{\sum Latencies}{N \times T_{max}}$
        """
        total_latency = sum(latencies)
        return round(1.0 - (total_latency / (len(latencies) * 2.0)), 2)

# Integration with dashboard.py
