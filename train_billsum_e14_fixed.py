#!/usr/bin/env python3
"""
BillSum E14 - T5 QLoRA (FIXED for 4GB VRAM)
Fixes applied (same root cause as E2):
  - prepare_model_for_kbit_training(use_gradient_checkpointing=False)
  - model.enable_input_require_grads()  <- fixes "does not require grad" error
  - gradient_checkpointing=False in TrainingArguments
  - max_source_length=512 (BillSum avg 1813 tokens causes OOM at full length)
  - r=4, alpha=8 (smaller rank = less memory)
  - paged_adamw_8bit optimizer
  - PYTORCH_CUDA_ALLOC_CONF to reduce fragmentation
"""

import os
import sys
import json
import time
import gc
from datetime import datetime
from pathlib import Path

# Memory optimizations BEFORE any CUDA init
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

import torch

# Aggressive cleanup before loading anything
gc.collect()
if torch.cuda.is_available():
    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    torch.cuda.reset_peak_memory_stats()
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Free VRAM: {torch.cuda.mem_get_info()[0] / 1e9:.2f} GB")

from datasets import load_from_disk, load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
from codecarbon import EmissionsTracker

print("=" * 70)
print("BillSum E14 - T5 QLoRA (Memory-Optimized for 4GB VRAM)")
print("=" * 70)

start_time = time.time()
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Paths
BASE_PATH       = Path("E:/Pending Experiment data/BillSum_Experiments")
results_dir     = BASE_PATH / "T5" / "results"
checkpoints_dir = BASE_PATH / "T5" / "checkpoints" / "E14_QLoRA"
results_dir.mkdir(parents=True, exist_ok=True)
checkpoints_dir.mkdir(parents=True, exist_ok=True)

MODEL_NAME        = "t5-base"
MAX_SOURCE_LENGTH = 512   # BillSum avg=1813 tokens; truncate to fit 4GB VRAM
MAX_TARGET_LENGTH = 128

# ── 1. Energy tracking ────────────────────────────────────────────────────────
print("\n[1/8] Starting energy tracker...")
tracker = EmissionsTracker(
    project_name="E14_BillSum_T5_QLoRA",
    output_dir=str(results_dir),
    log_level="error",
)
tracker.start()

try:
    # ── 2. Dataset ────────────────────────────────────────────────────────────
    print("[2/8] Loading BillSum dataset...")
    local_path = "E:/Pending Experiment data/local_datasets/billsum"
    try:
        dataset = load_from_disk(local_path)
        print(f"      Loaded from local disk: {local_path}")
    except Exception:
        print("      Local disk not found, downloading from HuggingFace...")
        dataset = load_dataset("billsum")

    train_data = dataset["train"].select(range(300))
    test_data  = dataset["test"].select(range(50))
    print(f"      Train: {len(train_data)} | Test: {len(test_data)}")

    # ── 3. Tokenizer ──────────────────────────────────────────────────────────
    print("[3/8] Loading T5 tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # ── 4. Tokenize ───────────────────────────────────────────────────────────
    print(f"[4/8] Tokenizing (max_source={MAX_SOURCE_LENGTH}, max_target={MAX_TARGET_LENGTH})...")
    print(f"      Note: BillSum avg source=1813 tokens, truncating to {MAX_SOURCE_LENGTH}")

    def tokenize_fn(examples):
        # T5 uses task prefix
        inputs = ["summarize: " + text for text in examples["text"]]
        model_inputs = tokenizer(
            inputs,
            max_length=MAX_SOURCE_LENGTH,
            truncation=True,
            padding="max_length",
        )
        labels = tokenizer(
            text_target=examples["summary"],
            max_length=MAX_TARGET_LENGTH,
            truncation=True,
            padding="max_length",
        )
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    train_tok = train_data.map(tokenize_fn, batched=True,
                               remove_columns=train_data.column_names)
    test_tok  = test_data.map(tokenize_fn,  batched=True,
                               remove_columns=test_data.column_names)

    # ── 5. Model with 4-bit quantization ─────────────────────────────────────
    print("[5/8] Loading T5 with 4-bit QLoRA quantization...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        low_cpu_mem_usage=True,
    )

    # FIX 1: disable gradient checkpointing at PEFT level
    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=False)
    # FIX 2: ensures input embeddings have grad_fn for backward pass through 4-bit layers
    model.enable_input_require_grads()

    # ── 6. QLoRA config ───────────────────────────────────────────────────────
    print("[6/8] Applying QLoRA (r=4, alpha=8)...")
    lora_config = LoraConfig(
        r=4,                    # smaller rank = less memory vs r=8
        lora_alpha=8,
        target_modules=["q", "v"],   # T5 attention projections
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.SEQ_2_SEQ_LM,
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params     = sum(p.numel() for p in model.parameters())
    trainable_pct    = (trainable_params / total_params) * 100
    print(f"      Trainable: {trainable_params:,} / {total_params:,} ({trainable_pct:.4f}%)")

    # ── 7. Training ───────────────────────────────────────────────────────────
    print("[7/8] Configuring training (2000 steps)...")
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, padding=True)

    training_args = Seq2SeqTrainingArguments(
        output_dir=str(checkpoints_dir),
        max_steps=2000,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=16,   # effective batch = 16
        learning_rate=3e-4,
        weight_decay=0.01,
        warmup_steps=100,
        logging_steps=100,
        save_steps=500,
        save_strategy="steps",
        save_total_limit=2,
        fp16=False,
        bf16=False,
        predict_with_generate=False,
        max_grad_norm=0.3,
        optim="paged_adamw_8bit",
        gradient_checkpointing=False,   # FIX 3: must be False for QLoRA seq2seq
        report_to="none",
        dataloader_num_workers=0,
        remove_unused_columns=False,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_tok,
        data_collator=data_collator,
    )

    print("\n" + "=" * 70)
    print("TRAINING STARTED - 2000 steps")
    print(f"Effective batch size: 16 (1 x 16 grad accum)")
    print(f"Source truncated to : {MAX_SOURCE_LENGTH} tokens")
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
        "experiment_id": "BILLSUM_E14",
        "experiment_name": "E14_T5_QLoRA",
        "model": MODEL_NAME,
        "model_type": "t5",
        "method": "QLoRA",
        "dataset": "billsum",
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
        "max_source_length": MAX_SOURCE_LENGTH,
        "max_target_length": MAX_TARGET_LENGTH,
        "lora_r": 4,
        "lora_alpha": 8,
        "note": "BillSum T5 QLoRA - fixed for 4GB VRAM, source truncated to 512 tokens"
    }

    result_file = results_dir / "E14_QLoRA_results.json"
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
    print("  python evaluate_billsum_e14.py")

except Exception as e:
    try:
        tracker.stop()
    except Exception:
        pass

    end_time = time.time()
    error_results = {
        "experiment_id": "BILLSUM_E14",
        "experiment_name": "E14_T5_QLoRA",
        "model": MODEL_NAME,
        "method": "QLoRA",
        "dataset": "billsum",
        "status": "failed",
        "error": str(e),
        "timestamp": timestamp,
        "duration_seconds": end_time - start_time,
        "note": "Check GPU memory - need at least 3GB free VRAM"
    }

    fail_file = results_dir / "E14_QLoRA_results_FAILED.json"
    with open(fail_file, "w") as f:
        json.dump(error_results, f, indent=2)

    print("\n" + "=" * 70)
    print("TRAINING FAILED")
    print("=" * 70)
    print(f"Error: {e}")
    print(f"Saved failure info to: {fail_file}")
    print("\nTroubleshooting tips:")
    print("  1. Restart Python / close all other GPU apps")
    print("  2. If still OOM, reduce MAX_SOURCE_LENGTH from 512 to 256")
    print("  3. Ensure no other training scripts are running")
    print("=" * 70)
    raise
