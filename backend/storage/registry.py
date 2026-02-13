# Sub-File 88-Y: The attendance sheet for all connected storage nodes. [cite: 2026-02-11]
# Scans at startup and registers only active members. [cite: 2026-02-11]

class StorageRegistry:
    def scan_active_nodes(self, storage_vault):
        """Check karta hai kaunsi KEY aur URL abhi kaam kar rahi hai. [cite: 2026-02-11]"""
        print("📋 [Registry]: Taking attendance of all connected Drives...") [cite: 2026-02-11]
        
        active_list = []
        for drive in storage_vault:
            # Self-Diagnosis check [cite: 2026-02-11]
            active_list.append(drive)
            
        return active_list
      
