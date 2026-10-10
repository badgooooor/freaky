"""Flatten pilot JSONL data into train/val splits."""
import json
import random
from pathlib import Path
from collections import defaultdict

MODES = ["freaky", "passive_aggressive", "wrong_occasion", "unhinged"]
SEED = 42
TRAIN_RATIO = 0.8

DATA_DIR = Path(__file__).parent.parent / "data"
INPUTS = [
    DATA_DIR / "pilot" / "pilot.jsonl",
    DATA_DIR / "pilot" / "batch2.jsonl",
    DATA_DIR / "synthetic_v1.jsonl",
]
OUT_DIR = DATA_DIR / "splits"


def load_examples() -> list[dict]:
    examples = []
    for path in INPUTS:
        with open(path) as f:
            for line in f:
                row = json.loads(line)
                for mode in MODES:
                    emoji_list = row["labels"].get(mode, [])
                    if not emoji_list:
                        continue
                    examples.append({
                        "prompt": f"[{mode}] {row['message']}",
                        "completion": " ".join(emoji_list),
                        "_mode": mode,
                    })
    return examples


def stratified_split(examples: list[dict]) -> tuple[list[dict], list[dict]]:
    by_mode: dict[str, list[dict]] = defaultdict(list)
    for ex in examples:
        by_mode[ex["_mode"]].append(ex)

    train, val = [], []
    rng = random.Random(SEED)
    for mode_examples in by_mode.values():
        rng.shuffle(mode_examples)
        n_train = round(len(mode_examples) * TRAIN_RATIO)
        train.extend(mode_examples[:n_train])
        val.extend(mode_examples[n_train:])

    rng.shuffle(train)
    rng.shuffle(val)
    return train, val


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for row in rows:
            out = {"prompt": row["prompt"], "completion": row["completion"]}
            f.write(json.dumps(out, ensure_ascii=False) + "\n")


def main() -> None:
    examples = load_examples()
    print(f"Total examples: {len(examples)}")

    train, val = stratified_split(examples)
    print(f"Train: {len(train)}  Val: {len(val)}")

    write_jsonl(OUT_DIR / "train.jsonl", train)
    write_jsonl(OUT_DIR / "val.jsonl", val)
    print(f"Wrote splits to {OUT_DIR}/")


if __name__ == "__main__":
    main()
