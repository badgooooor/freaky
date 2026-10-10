.PHONY: prep train merge serve eval publish all clean

HF_REPO ?= philavery-b/freaky

PYTHON  := uv run
SPLITS  := data/splits/train.jsonl
ADAPTER := output/lora-adapter/adapter_config.json
MERGED  := output/merged/config.json

# ── full pipeline ─────────────────────────────────────────────────────────────

all: prep train merge

# ── steps ─────────────────────────────────────────────────────────────────────

prep: $(SPLITS)

$(SPLITS): data/pilot/pilot.jsonl data/pilot/batch2.jsonl
	$(PYTHON) scripts/prep_data.py

train: $(ADAPTER)

$(ADAPTER): $(SPLITS)
	$(PYTHON) src/train.py

merge: $(MERGED)

$(MERGED): $(ADAPTER)
	$(PYTHON) scripts/merge_lora.py

# ── serve ─────────────────────────────────────────────────────────────────────

serve:
	$(PYTHON) -m uvicorn src.serve:app --host 0.0.0.0 --port 8000 --reload

eval:
	$(PYTHON) scripts/eval.py

publish:
	$(PYTHON) scripts/publish.py $(HF_REPO)

# ── housekeeping ──────────────────────────────────────────────────────────────

clean:
	rm -rf data/splits output/lora-adapter output/merged output/onnx
