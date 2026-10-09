"""Quick adapter test — no vLLM needed."""
import json
import sys
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
ADAPTER_DIR = Path(__file__).parent.parent / "output" / "lora-adapter"
VOCAB_PATH = Path(__file__).parent.parent / "spec" / "vocab.v1.json"
MODES = ["freaky", "passive_aggressive", "wrong_occasion", "unhinged"]


def build_system_prompt(mode: str) -> str:
    vocab = json.loads(VOCAB_PATH.read_text())
    pool = " ".join(e["emoji"] for e in vocab if mode in e.get("modes", []))
    descs = {
        "freaky": "makes innocent messages sound suggestive",
        "passive_aggressive": "makes messages drip with veiled hostility",
        "wrong_occasion": "adds wildly inappropriate celebration",
        "unhinged": "injects chaos, threat, or existential dread",
    }
    return (
        f"You label messages with emoji that make them maximally cursed.\n\n"
        f"Mode: {mode} — {descs[mode]}\n"
        f"Valid emoji: {pool}\n\n"
        f"Output 2–4 emoji from the valid set, space-separated. Nothing else."
    )


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "freaky"
    message = sys.argv[2] if len(sys.argv) > 2 else "กินข้าวกันมั้ยเย็นนี้"

    print(f"Loading base model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
    model = PeftModel.from_pretrained(model, str(ADAPTER_DIR))
    model = model.to("mps")
    model.eval()

    system = build_system_prompt(mode)
    chat = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"[{mode}] {message}"},
    ]
    text = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to("mps")

    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=20, temperature=0.0, do_sample=False)

    generated = out[0][inputs["input_ids"].shape[1]:]
    print(tokenizer.decode(generated, skip_special_tokens=True).strip())


if __name__ == "__main__":
    main()
