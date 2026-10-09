"""FastAPI server for cursed emoji labeling."""
import json
from pathlib import Path
from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

VOCAB_PATH = Path(__file__).parent.parent / "spec" / "vocab.v1.json"
MERGED_DIR = Path(__file__).parent.parent / "output" / "merged"
MODES = ["freaky", "passive_aggressive", "wrong_occasion", "unhinged"]
MODE_DESC = {
    "freaky": "makes innocent messages sound suggestive",
    "passive_aggressive": "makes messages drip with veiled hostility",
    "wrong_occasion": "adds wildly inappropriate celebration",
    "unhinged": "injects chaos, threat, or existential dread",
}

_pipe = None
_vocab_index: dict[str, list[str]] = {}


def _build_vocab_index() -> dict[str, list[str]]:
    vocab = json.loads(VOCAB_PATH.read_text())
    index: dict[str, list[str]] = {m: [] for m in MODES}
    for entry in vocab:
        for mode in entry.get("modes", []):
            if mode in index:
                index[mode].append(entry["emoji"])
    return index


def _build_system_prompt(mode: str) -> str:
    pool = " ".join(_vocab_index[mode])
    return (
        f"You label messages with emoji that make them maximally cursed.\n\n"
        f"Mode: {mode} — {MODE_DESC[mode]}\n"
        f"Valid emoji: {pool}\n\n"
        f"Output 2–4 emoji from the valid set, space-separated. Nothing else."
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _pipe, _vocab_index
    _vocab_index = _build_vocab_index()
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Loading model from {MERGED_DIR} on {device}...")
    tokenizer = AutoTokenizer.from_pretrained(str(MERGED_DIR))
    model = AutoModelForCausalLM.from_pretrained(
        str(MERGED_DIR), torch_dtype=torch.float16
    ).to(device)
    _pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=device,
        torch_dtype=torch.float16,
    )
    print("Model ready.")
    yield


app = FastAPI(lifespan=lifespan)


class LabelRequest(BaseModel):
    mode: str
    message: str


class LabelResponse(BaseModel):
    emoji: str


@app.post("/label", response_model=LabelResponse)
def label(req: LabelRequest) -> LabelResponse:
    if req.mode not in MODES:
        raise HTTPException(400, f"mode must be one of {MODES}")
    system = _build_system_prompt(req.mode)
    prompt = (
        f"<|im_start|>system\n{system}<|im_end|>\n"
        f"<|im_start|>user\n[{req.mode}] {req.message}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )
    out = _pipe(prompt, max_new_tokens=20, do_sample=False, return_full_text=False)
    raw = out[0]["generated_text"]
    valid = set(_vocab_index[req.mode])
    tokens = [t for t in raw.split() if t in valid]
    emoji = " ".join(tokens[:4])
    return LabelResponse(emoji=emoji or raw.strip())


app.mount("/", StaticFiles(directory=str(Path(__file__).parent.parent / "web"), html=True), name="web")
