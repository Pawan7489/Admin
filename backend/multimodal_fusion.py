# File Path: backend/multimodal_fusion.py
# Description: Synchronizes Vision, Speech, and Core Logic for seamless interaction.
# Rule: Trigger Text + Voice automatically when Vision detects a known object. [cite: 2026-02-11]

import time
import threading

class MultimodalFusion:
    def __init__(self, vision, voice, orchestrator):
        self.vision = vision           # File 67
        self.voice = voice             # File 68
        self.orchestrator = orchestrator # File 50
        self.fusion_active = False

    def start_unified_flow(self):
        """
        Vision aur Voice ko ek saath sync mein chalta hai. [cite: 2026-02-11]
        """
        self.fusion_active = True
        print("🔗 [Fusion]: Multimodal Bridge is now LIVE.")
        
        # Background loop for 'Auto-Sense'
        threading.Thread(target=self._auto_sense_loop, daemon=True).start()

    def _auto_sense_loop(self):
        while self.fusion_active:
            # Step 1: Vision se latest scan lena [cite: 2026-02-11]
            if self.vision.camera_active:
                # Simulated: Detecting an object like a 'Circuit'
                detected_object = "Circuit Diagram (Bansal College Lab)" 
                
                print(f"👁️‍🗨️ [Fusion]: Vision detected: {detected_object}")
                
                # Step 2: Auto-trigger Brain to explain [cite: 2026-02-11]
                explanation = self.orchestrator.process_user_request(
                    f"Explain this detected object: {detected_object}"
                )
                
                # Step 3: Auto-trigger Voice to narrate [cite: 2026-02-11]
                self.voice.speak(explanation)
                
                # Cooldown to avoid talking non-stop
                time.sleep(15)
            
            time.sleep(2)

    def calculate_fusion_sync_index(self, v_latency, a_latency):
        """
        Calculates how 'In-Sync' the senses are ($S_{idx}$).
        Formula: $S_{idx} = 1 - \frac{|L_v - L_a|}{L_v + L_a}$
        """
        if (v_latency + a_latency) == 0: return 1.0
        sync_index = 1 - (abs(v_latency - a_latency) / (v_latency + a_latency))
        return round(sync_index, 2)

    def deactivate(self):
        self.fusion_active = False
        print("🔌 [Fusion]: Multimodal Bridge deactivated.")

# Test Block
if __name__ == "__main__":
    # Integration logic for Master Orchestrator
    pass
  
