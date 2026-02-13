# Sub-File 85-F: Links snapshots to specific user age-groups and personas.
# Follows 'Demographic Logic' (File 84-D). [cite: 2026-02-11]

class AgeRestoreBridge:
    def map_snapshot_to_persona(self, metadata):
        """Snapshot ke meta-data se age-group aur voice settings extract karta hai."""
        group = metadata.get("age_group", "student")
        voice = metadata.get("voice_id", "hi-IN-MadhurNeural")
        print(f"🎭 [Restore Bridge]: Re-aligning A1 to '{group}' persona.")
        return {"group": group, "voice": voice}
      
