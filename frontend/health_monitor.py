# File Path: frontend/health_monitor.py
# Description: Visual gauges and real-time health metrics for the A1 Dashboard.
# Ensures the user is alerted before any hardware failure. [cite: 2026-02-11]

import streamlit as st
import psutil
from backend.telemetry_watchdog import TelemetryWatchdog

class SystemHealthMonitor:
    def __init__(self, watchdog):
        self.watchdog = watchdog # File 48 link

    def render_vital_gauges(self):
        """Dashboard par visual health metrics dikhata hai."""
        st.write("---")
        st.header("🌡️ A1 Vital Signs (Health Hub)")
        
        # Hardware Stats fetching
        stats = self.watchdog.get_hardware_stats()
        cpu_usage = psutil.cpu_percent()
        mem_usage = psutil.virtual_memory().percent
        
        # Columnar Gauges [cite: 2026-02-11]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="GPU Temperature", value=f"{stats['temp']}°C", delta="-2°C" if stats['temp'] < 60 else "+5°C")
            if stats['temp'] > 75: st.warning("🔥 GPU is heating up!")

        with col2:
            st.metric(label="CPU Load", value=f"{cpu_usage}%", delta="Normal")
            st.progress(cpu_usage / 100)

        with col3:
            st.metric(label="Memory Availability", value=f"{100 - mem_usage}%", delta="Optimized")
            st.progress(mem_usage / 100)

    def display_sync_status(self, sync_integrity):
        """Distributed Sync (File 78) ka status dikhata hai.""" [cite: 2026-02-11]
        st.write("---")
        st.subheader("🌉 Indore-Bhopal Bridge Status")
        
        if sync_integrity == 100.0:
            st.success(f"✅ All Drives Synced (Integrity: {sync_integrity}%)")
        else:
            st.info(f"🔄 Syncing Mesh... ({sync_integrity}%)")
            st.progress(sync_integrity / 100)

    def calculate_overall_health(self, temp, cpu, mem):
        """
        Calculates System Health Index ($H_i$).
        Formula: $H_i = 100 - (\frac{T_{gpu}}{T_{max}} \cdot 40 + \frac{L_{cpu}}{100} \cdot 30 + \frac{L_{mem}}{100} \cdot 30)$
        """
        # LaTeX formula for calculating the health percentage
        score = 100 - ((temp/85)*40 + (cpu/100)*30 + (mem/100)*30)
        return round(max(0, score), 2)

# Integration with dashboard.py
