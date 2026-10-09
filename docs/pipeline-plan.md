# Plan: freaky fine-tune pipeline

## Context

150 labeled messages × 4 modes = 600 training examples exist in `data/pilot/`. Goal is a local fine-tuned model that takes `[mode] message` and outputs 2–4 cursed emoji. Training via LoRA on Qwen2.5-1.5B-Instruct, served via vLLM at inference.

---

## What we're building

3 scripts, no framework magic:

```
scripts/prep_data.py   → flatten JSONL → train/val splits
src/train.py           → LoRA fine-tune with trl SFTTrainer
src/infer.py           → hit vLLM endpoint, return emoji
```

---

## Step 1 — Data prep (`scripts/prep_data.py`)

**Input**: `data/pilot/pilot.jsonl` + `data/pilot/batch2.jsonl` (150 rows total)

**What it does**: each row has 4 modes → expand to 4 training examples per message → 600 total.

**Output format** (one row per example):
```json
{
  "prompt": "[freaky] Want to grab lunch today?",
  "completion": "🍌🌭🥒🫦"
}
```

**Split**: 80/20 → `data/splits/train.jsonl` (480) + `data/splits/val.jsonl` (120)

Split is stratified by mode so all 4 modes appear in val.

---

## Step 2 — System prompt design

During training AND inference, each mode gets its own system prompt:

```
You label messages with emoji that make them maximally cursed.

Mode: freaky — makes innocent messages sound suggestive
Valid emoji: 🫦 🍆 🍑 💦 🥵 😈 👅 ... (full mode pool)

Output 2–4 emoji from the valid set, space-separated. Nothing else.
```

Why mode-specific (not one unified prompt): constrains output space to the correct pool per mode, reducing hallucinated emoji.

Vocab source: `spec/vocab.v1.json` — filter by `modes` field to get each pool.

---

## Step 3 — Training (`src/train.py`)

**Model**: `Qwen/Qwen2.5-1.5B-Instruct` (HuggingFace)  
Why: strong Thai support, small, vLLM-native.

**Format**: chat template (system + user + assistant turns):
```
<system>...mode prompt...</system>
<user>[freaky] Want to grab lunch today?</user>
<assistant>🍌🌭🥒🫦</assistant>
```

**LoRA config**:
```python
LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM"
)
```

**Training args**:
```python
SFTConfig(
    num_train_epochs=10,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    warmup_ratio=0.1,
    bf16=True,          # M-series Mac: use fp16 if bf16 not supported
    output_dir="output/lora-adapter"
)
```

10 epochs because dataset is small (480 train). Watch val loss — stop if it rises.

**Output**: `output/lora-adapter/` (adapter weights only, ~30MB)

---

## Step 4 — Serving (vLLM)

After training, serve base model + adapter:

```bash
vllm serve Qwen/Qwen2.5-1.5B-Instruct \
  --enable-lora \
  --lora-modules freaky=./output/lora-adapter \
  --max-lora-rank 16
```

vLLM uses the adapter name `freaky` as the model ID in requests.

---

## Step 5 — Inference (`src/infer.py`)

CLI: `python src/infer.py --mode freaky "Want to grab lunch today?"`

Internally:
1. Build mode-specific system prompt from `spec/vocab.v1.json`
2. POST to `http://localhost:8000/v1/chat/completions` with `model="freaky"`
3. Parse response → strip whitespace → return emoji string

```python
# rough shape
def label(mode: str, message: str, base_url="http://localhost:8000") -> str:
    system = build_system_prompt(mode)   # loads vocab.v1.json, filters by mode
    payload = {
        "model": "freaky",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": f"[{mode}] {message}"}
        ],
        "max_tokens": 20,
        "temperature": 0.0
    }
    r = requests.post(f"{base_url}/v1/chat/completions", json=payload)
    return r.json()["choices"][0]["message"]["content"].strip()
```

---

## Dependencies to add to pyproject.toml

```toml
dependencies = [
    # existing...
    "trl>=0.9",
    "peft>=0.11",
    "accelerate>=0.30",
    "datasets>=2.20",
]

[project.optional-dependencies]
serve = ["vllm>=0.4"]   # separate because vllm has torch version constraints
```

Install train deps: `uv sync`  
Install serve deps: `uv sync --extra serve`

---

## Files to create

| file | purpose |
|------|---------|
| `scripts/prep_data.py` | flatten + split dataset |
| `src/train.py` | LoRA fine-tune |
| `src/infer.py` | vLLM client CLI |

## Files to modify

| file | change |
|------|--------|
| `pyproject.toml` | add trl, peft, accelerate, datasets, vllm (optional) |

---

## Verification

1. Run `python scripts/prep_data.py` → check `data/splits/train.jsonl` has 480 rows, val 120
2. Run `python src/train.py` → adapter saved to `output/lora-adapter/`
3. Start vLLM server
4. Run `python src/infer.py --mode freaky "กินข้าวกันมั้ย"` → should return 2–4 freaky emoji
5. Spot check all 4 modes on a few messages
