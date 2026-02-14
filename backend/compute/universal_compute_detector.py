# File: backend/compute/universal_compute_detector.py
# Purpose: Detects the current Cloud Environment (Colab/Kaggle/Lightning/Local).
# Sets paths for Input/Output automatically so code never breaks.

import os
import sys

class UniversalComputeDetector:
    def __init__(self):
        self.env_type = self._detect_environment()
        self.paths = self._configure_paths()

    def _detect_environment(self):
        """System Environment Variables check karke platform batata hai."""
        if 'COLAB_GPU' in os.environ:
            return "Google_Colab"
        elif 'KAGGLE_KERNEL_RUN_TYPE' in os.environ:
            return "Kaggle_Kernel"
        elif 'LIGHTNING_CLOUD_URL' in os.environ:
            return "Lightning_Studio"
        elif 'SPACE_ID' in os.environ: # Hugging Face Spaces
            return "HF_Space"
        else:
            return "Local_Machine"

    def _configure_paths(self):
        """Platform ke hisab se storage paths set karta hai."""
        paths = {"input": "./input", "output": "./output", "temp": "./temp"}
        
        if self.env_type == "Google_Colab":
            paths["input"] = "/content/drive/MyDrive/A1_OS/Input"
            paths["output"] = "/content/drive/MyDrive/A1_OS/Output"
            print("☁️ [Compute]: Detected Colab. Linking Google Drive...")
            
        elif self.env_type == "Kaggle_Kernel":
            paths["input"] = "/kaggle/input"
            paths["output"] = "/kaggle/working"
            print("☁️ [Compute]: Detected Kaggle. Optimizing for P100 GPU...")
            
        elif self.env_type == "Lightning_Studio":
            paths["input"] = "/teamspace/studios/this_studio/input"
            print("⚡ [Compute]: Detected Lightning AI. High-Speed Storage Active.")
            
        return paths

    def get_status(self):
        return f"Environment: {self.env_type} | Storage: {self.paths['output']}"

# --- Usage ---
# detector = UniversalComputeDetector()
# print(detector.get_status())
