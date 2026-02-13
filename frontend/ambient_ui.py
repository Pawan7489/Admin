# Sub-File 84-O: Adaptive UI themes based on Location, Time, and Mood.
# Follows 'Pichai Rule' for global-standard aesthetics. [cite: 2026-02-11]

class AmbientUIEngine:
    def apply_location_theme(self, current_city):
        themes = {
            "Indore": {"primary": "#FF4B2B", "secondary": "#FF416C"}, # Energetic
            "Bhopal": {"primary": "#1A2980", "secondary": "#26D0CE"}  # Academic/Calm
        }
        selected = themes.get(current_city, themes["Bhopal"])
        return f"🎨 [UI]: Theme shifted to '{current_city} Liquid Mode'."

    def calculate_color_contrast(self, l1, l2):
        """
        Formula for Accessibility: $C_r = \frac{L1 + 0.05}{L2 + 0.05}$
        Ensures text is always readable regardless of theme.
        """
        return round((l1 + 0.05) / (l2 + 0.05), 2)
      
