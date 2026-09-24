# freaky 🫦🔥

Cursed emoji classifier. Takes a chat message, returns emoji that make it worse.

Parody of [Desert Ant Labs' Emo](https://desertant.com/models/emo/). Built for Stupid Hackathon X (Oct 10–11 2026, Bangkok).

**Example:** `[freaky] กินข้าวกันมั้ย` → 🍜🫦🔥

## Modes

| Mode | Vibe |
|------|------|
| `freaky` | makes it weird |
| `passive_aggressive` | makes it passive aggressive |
| `wrong_occasion` | wrong emoji for the context |
| `unhinged` | chaos |

## Architecture

Two-stream classifier (mirrors Emo's design, on purpose):

- **Stream A:** hashed char n-grams (2–4) → MLP. Works standalone, no heavy deps.
- **Stream B:** frozen `intfloat/multilingual-e5-small` → small head.
- **Fusion:** concat A+B → linear → sigmoid over ~100-emoji vocab.

Thai + English, 50/50. Input: `[mode] message`.

## Repo Layout

```
spec/        SPEC.md, vocab.json
data/        raw/, processed/, splits/, handwritten_test.jsonl
scripts/     generate_messages.py, label_messages.py, clean.py, split.py
src/         features.py, model.py, train.py, decode.py
eval/        baseline.py, evaluate.py, ablation.py, human_eval_export.py
notebooks/   exploration + results
docs/        model card drafts, context dump
```

## Evaluation

Ablation table (baseline vs A vs B vs A+B) is the README centerpiece.
Metrics: precision@3, recall@3 — overall, per mode, per language.
Joke metrics (Ruin@3, HR Complaint Rate) go in the demo/model card only.

## Stack

Python 3.11 · uv · PyTorch · sentence-transformers · scikit-learn · Anthropic API

## Setup

```bash
uv sync
export ANTHROPIC_API_KEY=...
```
