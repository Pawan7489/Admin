# Sub-File 85-Q: UI to peek inside a snapshot without extracting it.
# Implements 'Liquid UI' experience. [cite: 2026-02-11]

class SnapshotPreviewUI:
    def peek_inside_zip(self, zip_path):
        import zipfile
        """Zip extract kiye bina uski file list aur metadata dikhata hai."""
        with zipfile.ZipFile(zip_path, 'r') as z:
            file_list = z.namelist()
        print(f"👁️ [Preview]: Snapshot contains {len(file_list)} files.")
        return file_list[:5] # Show top 5 files in UI
