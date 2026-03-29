#!/usr/bin/env python3
"""
Evaluate XSum E26 - GPT-2 QLoRA
Generates ROUGE-1, ROUGE-2, ROUGE-L scores
Run this AFTER train_xsum_e26_fixed.py completes successfully
"""

import os
import json
import gc
from pathlib import Path

import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import evaluate

print("=" * 70)
print("EVALUATION: XSum E26 - GPT-2 QLoRA")
print("=" * 70)

CHECKPOINT_DIR = Path("E:/Pending Experiment data/XSum_Experiments/GPT2/checkpoints/E26_QLoRA")
RESULTS_DIR    = Path("E:/Pending Experiment data/XSum_Experiments/GPT2/results")
BASE_MODEL     = "gpt2"
MAX_LENGTH     = 256
NUM_TEST       = 100   # evaluate on 100 test samples

# ── Load model ────────────────────────────────────────────────────────────────
print("\n[1/5] Loading tokenizer and model from checkpoint...")
tokenizer = AutoTokenizer.from_pretrained(str(CHECKPOINT_DIR))
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "left"

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float16,
    device_map="auto",
    low_cpu_mem_usage=True,
)
model = PeftModel.from_pretrained(model, str(CHECKPOINT_DIR))
model.eval()

# ── Load dataset ──────────────────────────────────────────────────────────────
print("[2/5] Loading XSum test set...")
dataset = load_dataset("xsum")
test_data = dataset["test"].select(range(NUM_TEST))

# ── Generate summaries ────────────────────────────────────────────────────────
print(f"[3/5] Generating summaries for {NUM_TEST} examples...")
predictions = []
references  = []

for i, example in enumerate(test_data):
    if i % 20 == 0:
        print(f"      Progress: {i}/{NUM_TEST}")

    prompt = f"Summarize the following article:\n{example['document']}\n\nSummary:"
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_LENGTH - 50,   # leave room for generated summary
    ).to(model.device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=50,        # XSum summaries avg 23 tokens
            num_beams=2,
            early_stopping=True,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    # Decode only the newly generated tokens
    generated = output_ids[0][inputs["input_ids"].shape[1]:]
    summary = tokenizer.decode(generated, skip_special_tokens=True).strip()

    predictions.append(summary if summary else "no summary generated")
    references.append(example["summary"])

    # Periodic memory cleanup
    if i % 50 == 0:
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
eval_results = {
    "experiment_id": "XSUM_E26",
    "dataset": "XSum",
    "model": BASE_MODEL,
    "method": "QLoRA",
    "status": "Complete",
    "ROUGE-1": rouge1,
    "ROUGE-2": rouge2,
    "ROUGE-L": rougeL,
    "num_test_samples": NUM_TEST,
    "checkpoint": str(CHECKPOINT_DIR),
}

out_file = RESULTS_DIR / "E26_QLoRA_evaluation.json"
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
print("\nUpdate Experiment_Results.csv with these scores for XSUM_E26")
