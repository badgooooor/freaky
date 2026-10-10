# freaky 🫦🔥

Provocative and cursed emoji classifier. Takes a chat message, returns emoji that make it worse.

Built for Stupid Hackathon X (Oct 10–11 2026, Bangkok).

**Model:** [philavery-b/freaky](https://huggingface.co/philavery-b/freaky)

**Example:** `[freaky] กินข้าวกันมั้ย` → 🍜🫦🔥

## Modes

| Mode | Vibe |
|------|------|
| `freaky` | makes it weird |
| `passive_aggressive` | makes it passive aggressive |
| `wrong_occasion` | wrong emoji for the context |
| `unhinged` | chaos |

## Architecture

LoRA fine-tune on `Qwen/Qwen2.5-1.5B-Instruct`.

- Input: `[mode] message` (Thai + English)
- Output: 2–4 emoji from mode-specific vocab pool
- Adapter: r=16, targets q/k/v/o projections
- Trained on ~600 examples (pilot + synthetic), 2 epochs

## Repo Layout

```
spec/        vocab.v1.json
data/        pilot/, splits/, handwritten_test.jsonl, synthetic_v1.jsonl
scripts/     prep_data.py, merge_lora.py, eval.py, publish.py
src/         train.py, serve.py, infer.py
web/         demo UI
docs/        pipeline plan, model card drafts
```

## Pipeline

```bash
make prep     # flatten + split data → data/splits/
make train    # LoRA fine-tune → output/lora-adapter/
make merge    # merge adapter into base → output/merged/
make serve    # FastAPI server on :8000
make eval     # run eval against handwritten_test.jsonl
make publish  # push to HF (philavery-b/freaky)
```

## Stack

Python 3.11 · uv · PyTorch · transformers · peft · trl · FastAPI

## Setup

```bash
uv sync
uv run src/infer.py --mode freaky "กินข้าวกันมั้ย"
```
