"""Push merged model to Hugging Face Hub."""
import argparse
from pathlib import Path

from transformers import AutoModelForCausalLM, AutoTokenizer

MERGED_DIR = Path(__file__).parent.parent / "output" / "merged"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_id", help="e.g. yuttakhanbaingen/freaky-qwen2.5-1.5b")
    parser.add_argument("--private", action="store_true")
    args = parser.parse_args()

    print(f"Loading merged model from {MERGED_DIR}...")
    tokenizer = AutoTokenizer.from_pretrained(str(MERGED_DIR))
    model = AutoModelForCausalLM.from_pretrained(str(MERGED_DIR))

    print(f"Pushing to {args.repo_id}...")
    model.push_to_hub(args.repo_id, private=args.private)
    tokenizer.push_to_hub(args.repo_id, private=args.private)
    print("Done.")


if __name__ == "__main__":
    main()
