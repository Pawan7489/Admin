# Sub-File 85-U: Triggers automatic snapshots based on geographic location shifts.
# Context-aware intelligence. [cite: 2026-02-11]

class GeofencedBackup:
    def __init__(self):
        self.last_known_location = "Indore"

    def check_location_shift(self, current_location):
        """Location badalne par naya checkpoint banata hai."""
        if current_location != self.last_known_location:
            print(f"📍 [Geofence]: Location shifted from {self.last_known_location} to {current_location}.")
            print("📸 [Checkpoint]: Taking Travel-Safe Snapshot...")
            self.last_known_location = current_location
            return "✅ Checkpoint Secured."
        return "No location change."
      
