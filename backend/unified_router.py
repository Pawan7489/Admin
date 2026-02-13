# Sub-File 84-I: The master router for age-group specific logic and voice.
# Implements 'The Bridge Rule' for distributed logic. [cite: 2026-02-11]

class UnifiedRouter:
    def __init__(self, voice_hub, logic_hub):
        self.voice = voice_hub
        self.logic = logic_hub

    def sync_experience(self, user_id, detected_group):
        print(f"🔄 [Router]: Syncing A1 Experience for: {detected_group}")
        # Automatically switch voice and reasoning depth
        persona_voice = self.voice.get_voice_for(detected_group)
        persona_logic = self.logic.get_depth_for(detected_group)
        
        return {"voice": persona_voice, "logic": persona_logic}
      
