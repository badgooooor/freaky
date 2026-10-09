"""CLI client for cursed emoji labeling via vLLM endpoint."""
import argparse
import json
from pathlib import Path

import requests

VOCAB_PATH = Path(__file__).parent.parent / "spec" / "vocab.v1.json"
MODES = ["freaky", "passive_aggressive", "wrong_occasion", "unhinged"]


def build_vocab_index() -> dict[str, list[str]]:
    vocab = json.loads(VOCAB_PATH.read_text())
    index: dict[str, list[str]] = {m: [] for m in MODES}
    for entry in vocab:
        for mode in entry.get("modes", []):
            if mode in index:
                index[mode].append(entry["emoji"])
    return index


def _mode_desc(mode: str) -> str:
    return {
        "freaky": "makes innocent messages sound suggestive",
        "passive_aggressive": "makes messages drip with veiled hostility",
        "wrong_occasion": "adds wildly inappropriate celebration",
        "unhinged": "injects chaos, threat, or existential dread",
    }[mode]


def build_system_prompt(mode: str, vocab_index: dict[str, list[str]]) -> str:
    pool = " ".join(vocab_index[mode])
    return (
        f"You label messages with emoji that make them maximally cursed.\n\n"
        f"Mode: {mode} — {_mode_desc(mode)}\n"
        f"Valid emoji: {pool}\n\n"
        f"Output 2–4 emoji from the valid set, space-separated. Nothing else."
    )


def label(mode: str, message: str, base_url: str = "http://localhost:8000") -> str:
    vocab_index = build_vocab_index()
    system = build_system_prompt(mode, vocab_index)
    payload = {
        "model": "freaky",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": f"[{mode}] {message}"},
        ],
        "max_tokens": 20,
        "temperature": 0.0,
    }
    r = requests.post(f"{base_url}/v1/chat/completions", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Label a message with cursed emoji.")
    parser.add_argument("--mode", choices=MODES, required=True)
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("message")
    args = parser.parse_args()

    result = label(args.mode, args.message, args.base_url)
    print(result)


if __name__ == "__main__":
    main()
