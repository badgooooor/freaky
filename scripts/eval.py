"""Evaluate model against handwritten_test.jsonl via the running server."""
import json
import sys
from pathlib import Path

import requests

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
TEST_PATH = Path(__file__).parent.parent / "data" / "handwritten_test.jsonl"
MODES = ["freaky", "passive_aggressive", "wrong_occasion", "unhinged"]


def load_examples() -> list[dict]:
    return [json.loads(l) for l in TEST_PATH.read_text().splitlines() if l.strip()]


def predict(mode: str, message: str) -> set[str]:
    r = requests.post(f"{BASE_URL}/label", json={"mode": mode, "message": message}, timeout=60)
    r.raise_for_status()
    raw = r.json()["emoji"]
    return set(raw.split())


def score(pred: set[str], gold: list[str]) -> dict:
    gold_set = set(gold)
    tp = len(pred & gold_set)
    return {
        "exact": pred == gold_set,
        "precision": tp / len(pred) if pred else 0.0,
        "recall": tp / len(gold_set) if gold_set else 0.0,
        "any_hit": bool(pred & gold_set),
    }


def main() -> None:
    examples = load_examples()
    print(f"Evaluating {len(examples)} examples × {len(MODES)} modes = {len(examples) * len(MODES)} calls\n")

    totals: dict[str, dict[str, float]] = {m: {"exact": 0, "precision": 0, "recall": 0, "any_hit": 0} for m in MODES}
    errors = 0

    for ex in examples:
        for mode in MODES:
            gold = ex["labels"].get(mode, [])
            if not gold:
                continue
            try:
                pred = predict(mode, ex["message"])
                s = score(pred, gold)
                for k, v in s.items():
                    totals[mode][k] += float(v)
            except Exception as e:
                print(f"  ERROR id={ex['id']} mode={mode}: {e}")
                errors += 1

    n = len(examples)
    print(f"{'mode':<22} {'exact':>6} {'precision':>10} {'recall':>8} {'any_hit':>8}")
    print("-" * 58)
    for mode in MODES:
        t = totals[mode]
        print(
            f"{mode:<22} {t['exact']/n:>6.1%} {t['precision']/n:>10.1%} {t['recall']/n:>8.1%} {t['any_hit']/n:>8.1%}"
        )

    overall = {k: sum(totals[m][k] for m in MODES) / (n * len(MODES)) for k in ("exact", "precision", "recall", "any_hit")}
    print("-" * 58)
    print(f"{'OVERALL':<22} {overall['exact']:>6.1%} {overall['precision']:>10.1%} {overall['recall']:>8.1%} {overall['any_hit']:>8.1%}")
    if errors:
        print(f"\n{errors} request(s) failed.")


if __name__ == "__main__":
    main()
