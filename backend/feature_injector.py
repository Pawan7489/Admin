# Sub-File 84-M: Allows real-time 'Drag & Drop' of new features and tools.
# Implements 'Universal Hot-Swapping' instruction. [cite: 2026-02-11]

import importlib
import os

class FeatureInjector:
    def __init__(self, registry):
        self.registry = registry # Link to File 45

    def inject_new_tool(self, file_path):
        """Naye script ko AI ke 'Skill Registry' mein live add karta hai."""
        file_name = os.path.basename(file_path)
        if file_name.endswith(".py"):
            # Dynamic Import Logic
            module_name = file_name.replace(".py", "")
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            new_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(new_module)
            
            # Registering the new power [cite: 2026-02-11]
            self.registry[module_name] = {"type": "Plugin", "status": "Active"}
            return f"🚀 [Injection]: New Skill '{module_name}' added smoothly!"
        return "❌ [Error]: Invalid file format. Drop a .py or GGUF folder."

    def calculate_injection_latency(self, start_time, end_time):
        """
        Formula: $L_{inj} = T_{exec} - T_{drop}$
        """
        return f"Latency: {round(end_time - start_time, 4)}s"
      
