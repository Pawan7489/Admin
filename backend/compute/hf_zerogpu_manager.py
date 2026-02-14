# File: backend/compute/hf_zerogpu_manager.py
# Purpose: Manages Free GPU grants on Hugging Face Spaces.
# Uses the 'spaces' library to request GPU on-the-fly.

try:
    import spaces # Hugging Face ZeroGPU Library
except ImportError:
    spaces = None

class HFZeroGPUManager:
    def __init__(self):
        self.has_gpu = spaces is not None

    def execute_heavy_task(self, task_function, *args):
        """
        Decorator pattern to wrap heavy functions.
        Agar GPU available hai (Quota grant), toh GPU use karega, nahi toh CPU.
        """
        if self.has_gpu:
            print("⚡ [HF Spaces]: Requesting ZeroGPU Grant...")
            
            @spaces.GPU(duration=120) # 2 minute GPU grant request
            def wrapped_task(*args):
                return task_function(*args)
            
            return wrapped_task(*args)
        else:
            print("⚠️ [HF Spaces]: Running on CPU (Basic Tier).")
            return task_function(*args)

# --- Usage Example ---
# def my_inference(text):
#     return model.generate(text)
#
# manager = HFZeroGPUManager()
# result = manager.execute_heavy_task(my_inference, "Hello AI")
