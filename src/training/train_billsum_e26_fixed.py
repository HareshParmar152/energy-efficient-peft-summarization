#!/usr/bin/env python3
"""
BillSum E26 - GPT-2 QLoRA (FIXED for 4GB VRAM + CUDA assert)
Fixes vs previous attempt:
  - Use gpt2 base (117M) instead of gpt2-medium (345M) - avoids OOM
  - max_length=512 with proper label masking (fixes CUDA device-side assert)
  - batch_size=1, gradient_accumulation=16
  - paged_adamw_8bit optimizer
  - gradient_checkpointing=True
  - Aggressive memory cleanup before start
  - labels set to -100 for padding tokens (critical fix)
"""

import os
import gc
import json
import time
from datetime import datetime
from pathlib import Path

os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

import torch

gc.collect()
if torch.cuda.is_available():
    torch.cuda.empty_cache()
    torch.cuda.synchronize()

from datasets import load_from_disk, load_dataset
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

print("=" * 80)
print("TRAINING: BillSum E26 - GPT-2 QLoRA (FIXED)")
print("=" * 80)

start_time = time.time()
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

BASE_PATH = Path("E:/Pending Experiment data/BillSum_Experiments")
results_dir = BASE_PATH / "GPT2" / "results"
checkpoints_dir = BASE_PATH / "GPT2" / "checkpoints" / "E26_QLoRA"
results_dir.mkdir(parents=True, exist_ok=True)
checkpoints_dir.mkdir(parents=True, exist_ok=True)

print("\n[1/8] Starting energy tracker...")
tracker = EmissionsTracker(
    project_name="E26_BillSum_GPT2_QLoRA",
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
        print("      Loaded from local disk.")
    except Exception:
        print("      Local not found, downloading...")
        dataset = load_dataset("billsum")

    # 250 train / 25 test - smallest subset for hardest experiment
    train_data = dataset["train"].select(range(250))
    test_data  = dataset["test"].select(range(25))
    print(f"      Train: {len(train_data)} | Test: {len(test_data)}")

    # ── 3. Tokenizer ──────────────────────────────────────────────────────────
    print("[3/8] Loading tokenizer (gpt2 base)...")
    # Use gpt2 base (117M) - gpt2-medium (345M) OOMs on 4GB with QLoRA
    MODEL_NAME = "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"

    # ── 4. Tokenize ───────────────────────────────────────────────────────────
    print("[4/8] Tokenizing dataset...")
    # BillSum avg source=1813 tokens - truncate to 512 (GPT-2 max context)
    MAX_LENGTH = 512

    def tokenize_fn(examples):
        texts = [
            f"Summarize: {text}\n\nSummary: {summary}{tokenizer.eos_token}"
            for text, summary in zip(examples["text"], examples["summary"])
        ]
        enc = tokenizer(
            texts,
            truncation=True,
            max_length=MAX_LENGTH,
            padding="max_length",
        )
        # CRITICAL FIX: mask padding tokens in labels to avoid CUDA assert
        # -100 tells the loss function to ignore these positions
        labels = []
        for ids, attn in zip(enc["input_ids"], enc["attention_mask"]):
            label_row = [
                token_id if mask == 1 else -100
                for token_id, mask in zip(ids, attn)
            ]
            labels.append(label_row)
        enc["labels"] = labels
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
        bnb_4bit_use_double_quant=True,
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
    lora_config = LoraConfig(
        r=4,
        lora_alpha=8,
        target_modules=["c_attn"],
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
    # Use default DataCollatorForLanguageModeling - labels already set above
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir=str(checkpoints_dir),
        max_steps=2000,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=16,
        learning_rate=3e-4,
        weight_decay=0.01,
        warmup_steps=100,
        logging_steps=100,
        save_steps=500,
        save_strategy="steps",
        save_total_limit=2,
        fp16=False,
        bf16=False,
        max_grad_norm=0.3,
        optim="paged_adamw_8bit",
        gradient_checkpointing=True,
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

    print("\n" + "=" * 80)
    print("TRAINING STARTED - 2000 steps")
    print("=" * 80)
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
        "max_length": MAX_LENGTH,
        "lora_r": 4,
        "lora_alpha": 8,
        "note": "BillSum GPT-2 QLoRA fixed: gpt2 base (117M), label masking for padding"
    }

    result_file = results_dir / "E26_results.json"
    with open(result_file, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 80)
    print("TRAINING COMPLETE!")
    print("=" * 80)
    print(f"Duration     : {duration_min:.1f} minutes")
    print(f"Final loss   : {train_result.metrics.get('train_loss', 'N/A')}")
    print(f"CO2 emissions: {emissions:.6f} kg")
    print(f"Checkpoint   : {checkpoints_dir}")
    print(f"Results      : {result_file}")
    print("=" * 80)
    print("\nNEXT STEP: Run evaluation")
    print("  python evaluate_billsum_e26.py")

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
        "dataset": "billsum",
        "status": "failed",
        "error": str(e),
        "timestamp": timestamp,
        "duration_seconds": end_time - start_time,
    }

    fail_file = results_dir / "E26_results_FAILED.json"
    with open(fail_file, "w") as f:
        json.dump(error_results, f, indent=2)

    print("\n" + "=" * 80)
    print("TRAINING FAILED")
    print("=" * 80)
    print(f"Error: {e}")
    print(f"Saved failure info to: {fail_file}")
    print("\nTroubleshooting:")
    print("  1. Restart computer to fully clear GPU state")
    print("  2. Ensure no other GPU processes are running")
    print("  3. Try: torch.cuda.empty_cache() before starting")
    print("=" * 80)
    raise
