# File: app.py (For Hugging Face Spaces)
# Purpose: The Inference Engine using Gradio.
# Connects to your trained model from the Hub.

import gradio as gr
import torch
from transformers import pipeline

# --- ZeroGPU Logic (Optional) ---
# Agar aap ZeroGPU Space use kar rahe hain, toh yeh decorator GPU assign karega
try:
    import spaces
    @spaces.GPU
    def gpu_decorator(func):
        return func
except ImportError:
    # Agar CPU space hai, toh decorator kuch nahi karega
    def gpu_decorator(func):
        return func

# --- Model Loader ---
# Yahan hum wo model load karenge jo Colab ne train karke Hub par push kiya hai
MODEL_ID = "username/A1-OS-FineTuned-Llama3" # Colab se push kiya hua model

print(f"🔄 [Engine]: Loading {MODEL_ID} into memory...")
try:
    # Pipeline automatically CPU/GPU detect karega
    pipe = pipeline("text-generation", model=MODEL_ID, device_map="auto")
    print("✅ [Engine]: Model Loaded Successfully!")
except Exception as e:
    print(f"❌ [Error]: Model Load Failed. {e}")
    pipe = None

# --- Inference Function ---
@gpu_decorator
def generate_response(prompt, history):
    if pipe is None:
        return "System Error: Model not loaded."
    
    # Generation Logic
    messages = [{"role": "user", "content": prompt}]
    result = pipe(messages, max_new_tokens=512)
    return result[0]['generated_text'][-1]['content']

# --- The Interface (Face of A1 OS) ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 A1 OS | Neural Interface")
    
    chatbot = gr.ChatInterface(
        fn=generate_response,
        chatbot=gr.Chatbot(height=600),
        textbox=gr.Textbox(placeholder="Ask me anything...", container=False, scale=7),
        title="Super Genius AI",
        description="Running on Hugging Face Spaces (Powered by A1 OS Swarm)",
        theme="soft",
        examples=["Write a Python script", "Explain Quantum Physics", "Plan a trip to Bhopal"],
        cache_examples=False,
    )

if __name__ == "__main__":
    demo.launch()
  
