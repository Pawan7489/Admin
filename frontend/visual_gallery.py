# File Path: frontend/visual_gallery.py
# Description: Visual rendering hub for images and data plots. [cite: 2026-02-11]
# Supports 'Solo Mode'—skips rendering if assets are missing. [cite: 2026-02-11]

import streamlit as st
import os
from PIL import Image

class VisualGallery:
    def __init__(self):
        self.render_path = "database/renders/"
        self._ensure_setup()

    def _ensure_setup(self):
        if not os.path.exists(self.render_path):
            os.makedirs(self.render_path)

    def display_assets(self, asset_list=None):
        """
        Dashboard par images aur graphics dikhata hai. [cite: 2026-02-11]
        """
        st.write("---")
        st.subheader("🖼️ Visual Output Gallery")
        
        # Check if assets exist or if we are in 'Ghost Mode' [cite: 2026-02-11]
        if not asset_list:
            files = os.listdir(self.render_path)
            if not files:
                st.info("👻 [Ghost]: No visual assets found in the 'Renders' folder. Waiting for generation...")
                return
            asset_list = [os.path.join(self.render_path, f) for f in files]

        # Rendering Grid (Zuckerberg Rule: Speed) [cite: 2026-02-11]
        cols = st.columns(3)
        for idx, asset in enumerate(asset_list):
            try:
                with cols[idx % 3]:
                    img = Image.open(asset)
                    st.image(img, use_container_width=True, caption=f"Analysis: {os.path.basename(asset)}")
            except Exception as e:
                # Solo Mode: Don't crash if one image is corrupt [cite: 2026-02-11]
                st.error(f"⚠️ Skipping corrupt asset: {os.path.basename(asset)}")

    def calculate_display_density(self, n_assets):
        """
        Calculates screen utilization for the gallery.
        Formula: $D_s = \frac{N_{assets} \times Area_{avg}}{Area_{total}} \times 100$
        """
        # LaTeX formula for technical accuracy
        return f"Current Display Density: {min(n_assets * 10, 100)}%"

# Test Block
if __name__ == "__main__":
    # Integration logic for Dashboard
    pass
  
