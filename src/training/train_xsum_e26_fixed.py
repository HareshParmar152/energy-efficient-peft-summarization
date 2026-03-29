#!/usr/bin/env python3
"""
XSum E26 - GPT-2 QLoRA (FIXED for 4GB VRAM)
Key fixes vs previous attempt:
  - Use gpt2 (117M) instead of gpt2-medium (345M) - fits in 4GB with QLoRA
  - max_length=256 (XSum summaries are short, 23 tokens avg)
  - batch_size=1, gradient_accumulation=16 (effective batch=16)
  - CPU offload enabled
  - Aggressive memory cleanup before start
  - gradient_checkpointing=True
"""

import os
import sys
import json
import time
import gc
from datetime import datetime
from pathlib import Path

# Memory optimizations before any CUDA init
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

import torch

# Aggressive cleanup before loading anything
gc.collect()
if torch.cuda.is_available():
    torch.cuda.empty_cache()
    torch.cuda.synchronize()

from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
from codecarbon import EmissionsTracker

print("=" * 70)
print("XSum E26 - GPT-2 QLoRA (Memory-Optimized for 4GB VRAM)")
print("=" * 70)

start_time = time.time()
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Output paths
BASE_PATH = Path("E:/Pending Experiment data/XSum_Experiments")
results_dir  = BASE_PATH / "GPT2" / "results"
checkpoints_dir = BASE_PATH / "GPT2" / "checkpoints" / "E26_QLoRA"
results_dir.mkdir(parents=True, exist_ok=True)
checkpoints_dir.mkdir(parents=True, exist_ok=True)

# ── 1. Energy tracking ────────────────────────────────────────────────────────
print("\n[1/8] Starting energy tracker...")
tracker = EmissionsTracker(
    project_name="E26_XSum_GPT2_QLoRA",
    output_dir=str(results_dir),
    log_level="error",
)
tracker.start()

try:
    # ── 2. Dataset ────────────────────────────────────────────────────────────
    print("[2/8] Loading XSum dataset...")
    dataset = load_dataset("xsum")
    # Use 500 train / 100 test samples (same as other GPT-2 experiments)
    train_data = dataset["train"].select(range(500))
    test_data  = dataset["test"].select(range(100))
    print(f"      Train: {len(train_data)} | Test: {len(test_data)}")

    # ── 3. Tokenizer ──────────────────────────────────────────────────────────
    print("[3/8] Loading tokenizer (gpt2)...")
    # Use base gpt2 (117M params) - gpt2-medium (345M) OOMs on 4GB with QLoRA
    MODEL_NAME = "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"   # causal LM: pad on left

    # ── 4. Tokenize ───────────────────────────────────────────────────────────
    print("[4/8] Tokenizing dataset...")
    # XSum avg source=431 tokens, avg summary=23 tokens
    # max_length=256 covers most XSum examples after truncation
    MAX_LENGTH = 256

    def tokenize_fn(examples):
        texts = [
            f"Summarize the following article:\n{doc}\n\nSummary: {summ}{tokenizer.eos_token}"
            for doc, summ in zip(examples["document"], examples["summary"])
        ]
        enc = tokenizer(
            texts,
            truncation=True,
            max_length=MAX_LENGTH,
            padding="max_length",
        )
        enc["labels"] = enc["input_ids"].copy()
        return enc

    train_tok = train_data.map(tokenize_fn, batched=True,
                               remove_columns=train_data.column_names)
    test_tok  = test_data.map(tokenize_fn,  batched=True,
                               remove_columns=test_data.column_names)
    train_tok.set_format("torch")
    test_tok.set_format("torch")

    # ── 5. Model with 4-bit quantization ─────────────────────────────────────
    print("[5/8] Loading gpt2 with 4-bit QLoRA quantization...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,   # saves ~0.4 bits/param extra
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        low_cpu_mem_usage=True,
    )
    model = prepare_model_for_kbit_training(model)

    # ── 6. QLoRA config ───────────────────────────────────────────────────────
    print("[6/8] Applying QLoRA (r=4, alpha=8)...")
    # r=4 (smaller than default 8) to reduce memory further
    lora_config = LoraConfig(
        r=4,
        lora_alpha=8,
        target_modules=["c_attn"],   # GPT-2 attention projection
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params     = sum(p.numel() for p in model.parameters())
    trainable_pct    = (trainable_params / total_params) * 100
    print(f"      Trainable: {trainable_params:,} / {total_params:,} ({trainable_pct:.4f}%)")

    # ── 7. Training ───────────────────────────────────────────────────────────
    print("[7/8] Configuring training (2000 steps)...")
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir=str(checkpoints_dir),
        max_steps=2000,
        # batch=1, grad_accum=16 → effective batch=16 (same as other experiments)
        per_device_train_batch_size=1,
        gradient_accumulation_steps=16,
        learning_rate=3e-4,
        weight_decay=0.01,
        warmup_steps=100,
        logging_steps=100,
        save_steps=500,
        save_strategy="steps",
        save_total_limit=2,
        fp16=False,                    # QLoRA handles its own precision
        bf16=False,
        max_grad_norm=0.3,
        optim="paged_adamw_8bit",      # 8-bit optimizer saves ~2x optimizer memory
        gradient_checkpointing=True,   # trade compute for memory
        report_to="none",
        dataloader_num_workers=0,
        remove_unused_columns=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_tok,
        data_collator=data_collator,
    )

    print("\n" + "=" * 70)
    print("TRAINING STARTED - 2000 steps")
    print("=" * 70)
    train_result = trainer.train()

    # ── 8. Save & results ─────────────────────────────────────────────────────
    emissions = tracker.stop()

    print("\n[8/8] Saving model and results...")
    trainer.save_model(str(checkpoints_dir))
    tokenizer.save_pretrained(str(checkpoints_dir))

    end_time = time.time()
    duration_sec = end_time - start_time
    duration_min = duration_sec / 60

    results = {
        "experiment_id": "E26",
        "experiment_name": "E26_GPT2_QLoRA",
        "model": MODEL_NAME,
        "model_type": "gpt2",
        "method": "QLoRA",
        "dataset": "xsum",
        "status": "success",
        "timestamp": timestamp,
        "trainable_parameters": trainable_params,
        "total_parameters": total_params,
        "trainable_percentage": trainable_pct,
        "train_runtime_seconds": train_result.metrics.get("train_runtime", duration_sec),
        "train_runtime_minutes": train_result.metrics.get("train_runtime", duration_sec) / 60,
        "train_loss": train_result.metrics.get("train_loss", 0),
        "train_samples_per_second": train_result.metrics.get("train_samples_per_second", 0),
        "train_steps_per_second": train_result.metrics.get("train_steps_per_second", 0),
        "emissions_kg_co2": emissions,
        "checkpoint_dir": str(checkpoints_dir),
        "results_dir": str(results_dir),
        "max_steps": 2000,
        "batch_size": 1,
        "gradient_accumulation_steps": 16,
        "effective_batch_size": 16,
        "learning_rate": 3e-4,
        "max_length": MAX_LENGTH,
        "lora_r": 4,
        "lora_alpha": 8,
        "note": "XSum GPT-2 QLoRA - fixed for 4GB VRAM using gpt2 base (117M)"
    }

    result_file = results_dir / "E26_QLoRA_results.json"
    with open(result_file, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 70)
    print("TRAINING COMPLETE!")
    print("=" * 70)
    print(f"Duration     : {duration_min:.1f} minutes")
    print(f"Final loss   : {train_result.metrics.get('train_loss', 'N/A')}")
    print(f"CO2 emissions: {emissions:.6f} kg")
    print(f"Checkpoint   : {checkpoints_dir}")
    print(f"Results      : {result_file}")
    print("=" * 70)
    print("\nNEXT STEP: Run evaluation to get ROUGE scores")
    print("  python evaluate_xsum_e26.py")

except Exception as e:
    try:
        tracker.stop()
    except Exception:
        pass

    end_time = time.time()
    error_results = {
        "experiment_id": "E26",
        "experiment_name": "E26_GPT2_QLoRA",
        "model": "gpt2",
        "method": "QLoRA",
        "dataset": "xsum",
        "status": "failed",
        "error": str(e),
        "timestamp": timestamp,
        "duration_seconds": end_time - start_time,
        "note": "Check GPU memory - need at least 3GB free VRAM"
    }

    fail_file = results_dir / "E26_QLoRA_results_FAILED.json"
    with open(fail_file, "w") as f:
        json.dump(error_results, f, indent=2)

    print("\n" + "=" * 70)
    print("TRAINING FAILED")
    print("=" * 70)
    print(f"Error: {e}")
    print(f"Saved failure info to: {fail_file}")
    print("\nTroubleshooting tips:")
    print("  1. Restart Python / close other GPU apps to free VRAM")
    print("  2. Run: torch.cuda.empty_cache() before starting")
    print("  3. If still OOM, reduce MAX_LENGTH from 256 to 128")
    print("=" * 70)
    raise
