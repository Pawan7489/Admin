# File: app.py (Hugging Face Spaces)
# Purpose: Unlimited Free Transcription Engine using Whisper.
# Requirement: Set SDK to Gradio in README.md.

import gradio as gr
from transformers import pipeline
import torch

# GPU check for ZeroGPU Spaces
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Load the fastest version of Whisper
print(f"🔄 [Whisper]: Loading model on {device}...")
pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v3-turbo",
    chunk_length_s=30,
    device=device,
)

def transcribe(audio):
    if audio is None:
        return "No audio detected."
    
    print("🎙️ [Whisper]: Transcribing audio...")
    result = pipe(audio, batch_size=8, generate_kwargs={"task": "transcribe"})
    return result["text"]

# Simple API interface
demo = gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(sources=["microphone", "upload"], type="filepath"),
    outputs="text",
    title="A1 OS - Whisper Transcription Node",
    description="Send audio and get text back for free."
)

demo.launch()
