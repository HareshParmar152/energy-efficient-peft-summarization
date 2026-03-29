#!/usr/bin/env python3
"""
Train BillSum E26 (GPT-2 QLoRA)
Complete with research data collection: energy, time, parameters, metrics
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

import torch
from datasets import load_from_disk
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
from codecarbon import EmissionsTracker

print("="*80)
print("TRAINING: BillSum E26 (GPT-2 QLoRA)")
print("WARNING: This is the HARDEST experiment")
print("="*80)

start_time = time.time()
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

BASE_PATH = Path("E:/Pending Experiment data/BillSum_Experiments")
results_dir = BASE_PATH / "GPT2" / "results"
checkpoints_dir = BASE_PATH / "GPT2" / "checkpoints" / "E26_QLoRA"
results_dir.mkdir(parents=True, exist_ok=True)
checkpoints_dir.mkdir(parents=True, exist_ok=True)

print("\n1. Starting energy tracking...")
tracker = EmissionsTracker(
    project_name="E26_BillSum_GPT2_QLoRA",
    output_dir=str(results_dir),
    log_level="error"
)
tracker.start()

try:
    print("\n2. Loading BillSum dataset...")
    dataset = load_from_disk("E:/Pending Experiment data/local_datasets/billsum")
    train_dataset = dataset["train"].select(range(250))  # Smallest for hardest experiment
    test_dataset = dataset["test"].select(range(25))
    print(f"   Train samples: {len(train_dataset)}")
    print(f"   Test samples: {len(test_dataset)}")

    print("\n3. Loading GPT-2 model with 4-bit quantization...")
    model_name = "gpt2-medium"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token

    def tokenize_function(examples):
        texts = [f"Summarize: {text}\n\nSummary: {summary}" 
                 for text, summary in zip(examples["text"], examples["summary"])]
        return tokenizer(texts, truncation=True, max_length=512, padding="max_length")

    print("\n4. Tokenizing dataset...")
    train_dataset = train_dataset.map(tokenize_function, batched=True, remove_columns=train_dataset.column_names)
    test_dataset = test_dataset.map(tokenize_function, batched=True, remove_columns=test_dataset.column_names)

    print("\n5. Loading model with 4-bit quantization...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto"
    )
    
    model = prepare_model_for_kbit_training(model)

    print("\n6. Applying QLoRA configuration...")
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["c_attn"],
        lora_dropout=0.1,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    trainable_percentage = (trainable_params / total_params) * 100

    print(f"\n   Trainable params: {trainable_params:,}")
    print(f"   Total params: {total_params:,}")
    print(f"   Trainable %: {trainable_percentage:.4f}%")

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    print("\n7. Setting up training arguments...")
    training_args = TrainingArguments(
        output_dir=str(checkpoints_dir),
        max_steps=2000,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=16,
        learning_rate=3e-4,
        weight_decay=0.01,
        warmup_steps=50,
        logging_steps=50,
        save_steps=500,
        save_strategy="steps",
        fp16=False,
        max_grad_norm=0.3,
        save_total_limit=2,
        report_to="none",
        dataloader_num_workers=0,
        optim="paged_adamw_8bit",
        gradient_checkpointing=True,
    )

    print("\n8. Creating trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator,
    )

    print("\n9. Starting training (2000 steps)...")
    print("="*80)
    train_result = trainer.train()
    
    emissions = tracker.stop()
    
    print("\n10. Saving model...")
    trainer.save_model(str(checkpoints_dir))
    tokenizer.save_pretrained(str(checkpoints_dir))
    
    end_time = time.time()
    duration_seconds = end_time - start_time
    duration_minutes = duration_seconds / 60
    
    print("\n11. Saving results...")
    results = {
        "experiment_id": "E26",
        "experiment_name": "E26_GPT2_QLoRA",
        "model": model_name,
        "model_type": "gpt2",
        "method": "QLoRA",
        "dataset": "billsum",
        "status": "success",
        "timestamp": timestamp,
        "trainable_parameters": trainable_params,
        "total_parameters": total_params,
        "trainable_percentage": trainable_percentage,
        "train_runtime_seconds": train_result.metrics.get("train_runtime", duration_seconds),
        "train_runtime_minutes": train_result.metrics.get("train_runtime", duration_seconds) / 60,
        "train_loss": train_result.metrics.get("train_loss", 0),
        "train_samples_per_second": train_result.metrics.get("train_samples_per_second", 0),
        "train_steps_per_second": train_result.metrics.get("train_steps_per_second", 0),
        "emissions_kg_co2": emissions,
        "checkpoint_dir": str(checkpoints_dir),
        "results_dir": str(results_dir),
        "max_steps": 2000,
        "batch_size": 1,
        "gradient_accumulation_steps": 16,
        "learning_rate": 3e-4,
        "note": "Legislative bill summarization - GPT-2 QLoRA (HARDEST)"
    }
    
    result_file = results_dir / "E26_results.json"
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*80)
    print("✅ TRAINING COMPLETE!")
    print("="*80)
    print(f"Duration: {duration_minutes:.1f} minutes")
    print(f"Emissions: {emissions:.6f} kg CO2")
    print(f"Checkpoint: {checkpoints_dir}")
    print(f"Results: {result_file}")
    print("="*80)

except Exception as e:
    try:
        tracker.stop()
    except:
        pass
    
    end_time = time.time()
    duration_seconds = end_time - start_time
    
    results = {
        "experiment_id": "E26",
        "experiment_name": "E26_GPT2_QLoRA",
        "model": "gpt2-medium",
        "model_type": "gpt2",
        "method": "QLoRA",
        "dataset": "billsum",
        "status": "failed",
        "error": str(e),
        "timestamp": timestamp,
        "duration_seconds": duration_seconds
    }
    
    result_file = results_dir / "E26_results_FAILED.json"
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*80)
    print("❌ TRAINING FAILED!")
    print("="*80)
    print(f"Error: {e}")
    print(f"Failure info saved to: {result_file}")
    print("="*80)
    raise
