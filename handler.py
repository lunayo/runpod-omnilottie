import os
import sys
import runpod
import torch
from huggingface_hub import snapshot_download
from transformers import AutoProcessor
# OmniLottie modules import each other by bare name
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "OmniLottie"))
from decoder_hf import LottieDecoder
from inference_hf import build_messages, prepare_inference_input, generate_lottie, tokens_to_lottie_json

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_path = snapshot_download("OmniLottie/OmniLottie", allow_patterns=["*.json", "*.safetensors"])
model = LottieDecoder.from_pretrained(model_path, torch_dtype=torch.bfloat16).to(device).eval()

processor_path = snapshot_download("Qwen/Qwen2.5-VL-3B-Instruct", allow_patterns=["*.json", "*.txt"])
processor = AutoProcessor.from_pretrained(processor_path, padding_side="left")

def handler(event):
    input_data = event['input']
    prompt = input_data['prompt']
    try:
        inputs = prepare_inference_input(processor, build_messages("text", text_prompt=prompt), device)
        tokens = generate_lottie(model, inputs, input_data.get('max_tokens', 4096), device)
        lottie = tokens_to_lottie_json(tokens)
    except Exception as e:
        return {
            "error": f"Failed to generate the Lottie: {e}"
        }
    return {
        "lottie": lottie
    }


runpod.serverless.start({"handler": handler})
