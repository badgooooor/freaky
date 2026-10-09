"""Merge LoRA adapter into base model and save full weights."""
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
ADAPTER_DIR = Path(__file__).parent.parent / "output" / "lora-adapter"
OUT_DIR = Path(__file__).parent.parent / "output" / "merged"


def main() -> None:
    print("Loading base model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16)

    print("Applying adapter...")
    model = PeftModel.from_pretrained(model, str(ADAPTER_DIR))

    print("Merging weights...")
    model = model.merge_and_unload()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(OUT_DIR), safe_serialization=True)
    tokenizer.save_pretrained(str(OUT_DIR))
    print(f"Saved merged model → {OUT_DIR}")


if __name__ == "__main__":
    main()
