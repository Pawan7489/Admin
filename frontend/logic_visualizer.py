# File Path: frontend/logic_visualizer.py
# Description: Visualizes the command's journey through Onion Layers. [cite: 2026-02-11]
# Maps the 'Hidden Reasoning Path' for the Admin. [cite: 2026-02-11]

import streamlit as st
import time

class LogicVisualizer:
    def __init__(self):
        self.layers = ["Interface", "Security Shield", "Validation", "Core Logic"]

    def render_flow(self, current_stage, status_report):
        """
        Dashboard par live logic tree dikhata hai. [cite: 2026-02-11]
        """
        st.write("---")
        st.subheader("🗺️ Logic Flow Path (Onion Peeling)")
        
        # Creating a visual horizontal flow
        cols = st.columns(len(self.layers))
        
        for i, layer in enumerate(self.layers):
            with cols[i]:
                # Dynamic highlighting based on progress
                if i < current_stage:
                    st.success(f"✔️ {layer}")
                elif i == current_stage:
                    st.warning(f"🟡 {layer}")
                    st.caption("Processing...")
                else:
                    st.info(f"⚪ {layer}")
            
            # Drawing arrows between columns
            if i < len(self.layers) - 1:
                st.write("      →")

        # Detailed Reasoning Log [cite: 2026-02-11]
        with st.expander("🔍 View Deep Reasoning Path"):
            st.json(status_report)

    def calculate_transparency_index(self, steps_visible, total_steps):
        """
        Calculates how 'Open' the AI's thinking is.
        Formula: $T_i = \frac{S_{visible}}{S_{total}} \times 100$
        """
        index = (steps_visible / total_steps) * 100
        return f"Transparency Index: {round(index, 2)}%"

# Test Block
if __name__ == "__main__":
    # Integration for Dashboard.py
    pass
  
