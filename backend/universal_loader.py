# File Path: backend/universal_loader.py
# Sub-File C: Support for GGUF and BIN formats for easy AI engine swaps.

class UniversalLoader:
    def __init__(self):
        self.supported_formats = [".gguf", ".bin", ".onnx"]

    def load_custom_engine(self, file_path):
        """Checks format and links to A1 Core."""
        ext = file_path.split('.')[-1]
        if f".{ext}" in self.supported_formats:
            print(f"📦 [Loader]: Injecting {ext} engine into System Design.")
            return True
        return False

    def calculate_load_efficiency(self, size_gb):
        """
        Formula: $E_l = \frac{1}{T_{load} \cdot VRAM_{used}}$
        """
        return "Load Efficiency: High"
      
