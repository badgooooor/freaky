"""LoRA fine-tune Qwen2.5-1.5B-Instruct on cursed emoji labeling task."""
import json
import logging
from pathlib import Path

import transformers
transformers.logging.set_verbosity_info()

import torch
from datasets import Dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTConfig, SFTTrainer

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
VOCAB_PATH = Path(__file__).parent.parent / "spec" / "vocab.v1.json"
SPLITS_DIR = Path(__file__).parent.parent / "data" / "splits"
OUTPUT_DIR = Path(__file__).parent.parent / "output" / "lora-adapter"

MODES = ["freaky", "passive_aggressive", "wrong_occasion", "unhinged"]


def build_vocab_index() -> dict[str, list[str]]:
    vocab = json.loads(VOCAB_PATH.read_text())
    index: dict[str, list[str]] = {m: [] for m in MODES}
    for entry in vocab:
        for mode in entry.get("modes", []):
            if mode in index:
                index[mode].append(entry["emoji"])
    return index


def build_system_prompt(mode: str, vocab_index: dict[str, list[str]]) -> str:
    pool = " ".join(vocab_index[mode])
    return (
        f"You label messages with emoji that make them maximally cursed.\n\n"
        f"Mode: {mode} — {_mode_desc(mode)}\n"
        f"Valid emoji: {pool}\n\n"
        f"Output 2–4 emoji from the valid set, space-separated. Nothing else."
    )


def _mode_desc(mode: str) -> str:
    return {
        "freaky": "makes innocent messages sound suggestive",
        "passive_aggressive": "makes messages drip with veiled hostility",
        "wrong_occasion": "adds wildly inappropriate celebration",
        "unhinged": "injects chaos, threat, or existential dread",
    }[mode]


def load_split(path: Path, tokenizer, vocab_index: dict[str, list[str]]) -> Dataset:
    rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    texts = []
    for row in rows:
        mode = row["prompt"].split("]")[0].lstrip("[")
        system = build_system_prompt(mode, vocab_index)
        chat = [
            {"role": "system", "content": system},
            {"role": "user", "content": row["prompt"]},
            {"role": "assistant", "content": row["completion"]},
        ]
        text = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=False)
        texts.append({"text": text})
    return Dataset.from_list(texts)


def main() -> None:
    vocab_index = build_vocab_index()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        device_map={"": "mps"},
    )
    model.config.use_cache = False

    train_ds = load_split(SPLITS_DIR / "train.jsonl", tokenizer, vocab_index)
    val_ds = load_split(SPLITS_DIR / "val.jsonl", tokenizer, vocab_index)
    print(f"Train: {len(train_ds)}  Val: {len(val_ds)}")

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
    )

    training_args = SFTConfig(
        output_dir=str(OUTPUT_DIR),
        num_train_epochs=4,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        fp16=False,
        bf16=False,
        use_mps_device=True,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_steps=10,
        dataset_text_field="text",
        max_length=256,
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        processing_class=tokenizer,
        peft_config=lora_config,
    )

    trainer.train()
    trainer.save_model(str(OUTPUT_DIR))
    print(f"Adapter saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
