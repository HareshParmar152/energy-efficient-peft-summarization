#!/usr/bin/env python3
"""
Evaluate BillSum E14 - T5 QLoRA
Run this AFTER train_billsum_e14_fixed.py completes successfully
"""

import os
import json
import gc
from pathlib import Path

import torch
from datasets import load_from_disk, load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel
import evaluate

print("=" * 70)
print("EVALUATION: BillSum E14 - T5 QLoRA")
print("=" * 70)

CHECKPOINT_DIR = Path("E:/Pending Experiment data/BillSum_Experiments/T5/checkpoints/E14_QLoRA")
RESULTS_DIR    = Path("E:/Pending Experiment data/BillSum_Experiments/T5/results")
BASE_MODEL     = "t5-base"
MAX_SOURCE     = 512
MAX_TARGET     = 128
NUM_TEST       = 50

# ── Load model ────────────────────────────────────────────────────────────────
print("\n[1/5] Loading tokenizer and model from checkpoint...")
tokenizer = AutoTokenizer.from_pretrained(str(CHECKPOINT_DIR))

model = AutoModelForSeq2SeqLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float16,
    device_map="auto",
    low_cpu_mem_usage=True,
)
model = PeftModel.from_pretrained(model, str(CHECKPOINT_DIR))
model.eval()

# ── Load dataset ──────────────────────────────────────────────────────────────
print("[2/5] Loading BillSum test set...")
local_path = "E:/Pending Experiment data/local_datasets/billsum"
try:
    dataset = load_from_disk(local_path)
except Exception:
    dataset = load_dataset("billsum")

test_data = dataset["test"].select(range(NUM_TEST))

# ── Generate summaries ────────────────────────────────────────────────────────
print(f"[3/5] Generating summaries for {NUM_TEST} examples...")
predictions = []
references  = []

for i, example in enumerate(test_data):
    if i % 10 == 0:
        print(f"      Progress: {i}/{NUM_TEST}")

    # T5 uses task prefix
    input_text = "summarize: " + example["text"]
    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        max_length=MAX_SOURCE,
        truncation=True,
        padding=True,
    ).to(model.device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=MAX_TARGET,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3,
        )

    summary = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
    predictions.append(summary if summary else "no summary generated")
    references.append(example["summary"])

    if i % 25 == 0:
        gc.collect()
        torch.cuda.empty_cache()

# ── Compute ROUGE ─────────────────────────────────────────────────────────────
print("[4/5] Computing ROUGE scores...")
rouge = evaluate.load("rouge")
scores = rouge.compute(predictions=predictions, references=references)

rouge1 = round(scores["rouge1"], 4)
rouge2 = round(scores["rouge2"], 4)
rougeL = round(scores["rougeL"], 4)

print(f"\n  ROUGE-1 : {rouge1}")
print(f"  ROUGE-2 : {rouge2}")
print(f"  ROUGE-L : {rougeL}")

# ── Save results ──────────────────────────────────────────────────────────────
print("\n[5/5] Saving evaluation results...")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
eval_results = {
    "experiment_id": "BILLSUM_E14",
    "dataset": "BillSum",
    "model": BASE_MODEL,
    "method": "QLoRA",
    "status": "Complete",
    "ROUGE-1": rouge1,
    "ROUGE-2": rouge2,
    "ROUGE-L": rougeL,
    "num_test_samples": NUM_TEST,
    "checkpoint": str(CHECKPOINT_DIR),
    "note": "Source truncated to 512 tokens (BillSum avg 1813 tokens)"
}

out_file = RESULTS_DIR / "E14_QLoRA_evaluation.json"
with open(out_file, "w") as f:
    json.dump(eval_results, f, indent=2)

print("\n" + "=" * 70)
print("EVALUATION COMPLETE")
print("=" * 70)
print(f"  ROUGE-1 : {rouge1}")
print(f"  ROUGE-2 : {rouge2}")
print(f"  ROUGE-L : {rougeL}")
print(f"\nResults saved to: {out_file}")
print("=" * 70)
print("\nUpdate Experiment_Results.csv with these scores for BILLSUM_E14")
