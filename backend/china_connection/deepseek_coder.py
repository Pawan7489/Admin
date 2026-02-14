# File: backend/china_connection/deepseek_coder.py
# Purpose: Uses DeepSeek-R1 for superior coding capabilities (GPT-4 Level).
# Optimization: Loads in 4-bit to run on Free Google Colab/Kaggle GPUs.

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

class DeepSeekCoder:
    def __init__(self):
        self.model_id = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B" # Efficient & Powerful
        self.tokenizer = None
        self.model = None
        self._load_model()

    def _load_model(self):
        """DeepSeek ko 4-bit mode mein load karta hai (Free Tier Friendly)."""
        print("🇨🇳 [DeepSeek]: Loading the World's Best Open-Source Coder...")
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
        )

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                quantization_config=bnb_config,
                device_map="auto"
            )
            print("✅ [DeepSeek]: System Online. Ready to write code.")
        except Exception as e:
            print(f"❌ [Error]: DeepSeek Load Failed. {e}")

    def generate_code(self, prompt):
        """Complex Coding Tasks ko handle karta hai."""
        if not self.model:
            return "Model not loaded."

        print(f"👨‍💻 [DeepSeek]: Analyzing logic for: {prompt[:50]}...")
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = self.model.generate(**inputs, max_new_tokens=1024)
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# --- Usage ---
# coder = DeepSeekCoder()
# print(coder.generate_code("Write a Python script for a Snake Game."))
