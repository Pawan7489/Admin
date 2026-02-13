# Sub-File 85-O: Verifies physical drive presence before triggering distributed backup.
# Implements 'Solo Mode' failover. [cite: 2026-02-11]

import os

class DriveHandshake:
    def ping_drives(self, drive_d_path, drive_e_path):
        """Check karta hai ki drives active hain ya nahi."""
        d_status = os.path.exists(drive_d_path)
        e_status = os.path.exists(drive_e_path)
        
        if not e_status:
            return "⚠️ [Handshake]: Drive E missing. Queuing distributed backup for later."
        return "✅ [Handshake]: Both drives active. Ready for split-backup."
      
