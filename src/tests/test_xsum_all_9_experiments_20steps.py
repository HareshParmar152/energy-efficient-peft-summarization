#!/usr/bin/env python3
"""
Test All 9 XSum Experiments - 20 Steps Only
BART, T5, LLaMA × LoRA, QLoRA, Adapters
Quick test to verify all configurations work
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq,
)
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
import bitsandbytes as bnb

# Setup logging - Save to mandatory path
log_dir = Path("E:/Pending Experiment data/logs")
log_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = log_dir / f"test_xsum_all_9_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Experiment configurations - Following Rules file
EXPERIMENTS = [
    # E1-E3: BART experiments
    {"exp_id": "E1", "model": "facebook/bart-base", "model_type": "bart", "method": "LoRA", "name": "E1_BART_XSum_LoRA"},
    {"exp_id": "E2", "model": "facebook/bart-base", "model_type": "bart", "method": "QLoRA", "name": "E2_BART_XSum_QLoRA"},
    {"exp_id": "E3", "model": "facebook/bart-base", "model_type": "bart", "method": "Adapters", "name": "E3_BART_XSum_Adapters"},
    
    # E13-E15: T5 experiments
    {"exp_id": "E13", "model": "t5-base", "model_type": "t5", "method": "LoRA", "name": "E13_T5_XSum_LoRA"},
    {"exp_id": "E14", "model": "t5-base", "model_type": "t5", "method": "QLoRA", "name": "E14_T5_XSum_QLoRA"},
    {"exp_id": "E15", "model": "t5-base", "model_type": "t5", "method": "Adapters", "name": "E15_T5_XSum_Adapters"},
    
    # E25-E27: LLaMA experiments
    {"exp_id": "E25", "model": "meta-llama/Llama-2-7b-hf", "model_type": "llama", "method": "LoRA", "name": "E25_LLaMA_XSum_LoRA"},
    {"exp_id": "E26", "model": "meta-llama/Llama-2-7b-hf", "model_type": "llama", "method": "QLoRA", "name": "E26_LLaMA_XSum_QLoRA"},
    {"exp_id": "E27", "model": "meta-llama/Llama-2-7b-hf", "model_type": "llama", "method": "Adapters", "name": "E27_LLaMA_XSum_Adapters"},
]

# Test configuration
TEST_CONFIG = {
    "max_steps": 20,
    "batch_size": 4,
    "learning_rate": 3e-4,
    "max_source_length": 512,
    "max_target_length": 128,
    "save_steps": 10,
    "logging_steps": 5,
}

def load_and_prepare_dataset():
    """Load XSum dataset"""
    logger.info("Loading XSum dataset...")
    dataset = load_dataset("xsum")
    
    # Use small subset for testing
    train_dataset = dataset['train'].select(range(100))  # Only 100 samples for test
    val_dataset = dataset['validation'].select(range(20))
    
    logger.info(f"Test dataset: {len(train_dataset)} train, {len(val_dataset)} val")
    return train_dataset, val_dataset

def preprocess_function(examples, tokenizer, model_type):
    """Preprocess the dataset"""
    inputs = examples["document"]
    targets = examples["summary"]
    
    # T5 requires prefix
    if model_type == "t5":
        inputs = ["summarize: " + doc for doc in inputs]
    
    model_inputs = tokenizer(
        inputs,
        max_length=TEST_CONFIG["max_source_length"],
        truncation=True,
        padding="max_length"
    )
    
    labels = tokenizer(
        targets,
        max_length=TEST_CONFIG["max_target_length"],
        truncation=True,
        padding="max_length"
    )
    
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

def setup_lora_model(model, method, model_type):
    """Setup model with LoRA or QLoRA"""
    if method == "QLoRA":
        # Prepare model for QLoRA (4-bit)
        model = prepare_model_for_kbit_training(model)
    
    # LoRA configuration - different target modules for different models
    if model_type == "bart":
        target_modules = ["q_proj", "v_proj"]
    elif model_type == "t5":
        target_modules = ["q", "v"]  # T5 uses different naming
    elif model_type == "llama":
        target_modules = ["q_proj", "v_proj"]
    else:
        target_modules = ["q_proj", "v_proj"]
    
    if method in ["LoRA", "QLoRA"]:
        lora_config = LoraConfig(
            r=8,
            lora_alpha=16,
            target_modules=target_modules,
            lora_dropout=0.1,
            bias="none",
            task_type=TaskType.SEQ_2_SEQ_LM
        )
        model = get_peft_model(model, lora_config)
    elif method == "Adapters":
        # Use LoRA as adapters with more modules
        if model_type == "bart":
            target_modules = ["q_proj", "v_proj", "k_proj", "out_proj"]
        elif model_type == "t5":
            target_modules = ["q", "v", "k", "o"]
        elif model_type == "llama":
            target_modules = ["q_proj", "v_proj", "k_proj", "o_proj"]
        
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=target_modules,
            lora_dropout=0.1,
            bias="none",
            task_type=TaskType.SEQ_2_SEQ_LM
        )
        model = get_peft_model(model, lora_config)
    
    return model

def run_experiment(exp_config, train_dataset, val_dataset):
    """Run a single experiment"""
    exp_id = exp_config["exp_id"]
    exp_name = exp_config["name"]
    model_name = exp_config["model"]
    model_type = exp_config["model_type"]
    method = exp_config["method"]
    
    logger.info("=" * 80)
    logger.info(f"STARTING: {exp_id} - {exp_name}")
    logger.info("=" * 80)
    
    try:
        # Load tokenizer and model
        logger.info(f"Loading model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Handle models without pad token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Load model
        if method == "QLoRA":
            from transformers import BitsAndBytesConfig
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
            )
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name,
                quantization_config=bnb_config,
                device_map="auto"
            )
        else:
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        # Setup PEFT
        model = setup_lora_model(model, method, model_type)
        logger.info(f"Model configured with {method}")
        
        # Preprocess dataset
        logger.info("Preprocessing dataset...")
        
        train_processed = train_dataset.map(
            lambda x: preprocess_function(x, tokenizer, model_type),
            batched=True,
            remove_columns=train_dataset.column_names,
        )
        
        val_processed = val_dataset.map(
            lambda x: preprocess_function(x, tokenizer, model_type),
            batched=True,
            remove_columns=val_dataset.column_names,
        )
        
        # Data collator
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=tokenizer,
            model=model,
            padding=True
        )
        
        # Output directory - Save to mandatory path
        output_dir = Path(f"E:/Pending Experiment data/results/{exp_id}_{exp_name}_{timestamp}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Training arguments
        training_args = Seq2SeqTrainingArguments(
            output_dir=str(output_dir),
            max_steps=TEST_CONFIG["max_steps"],
            per_device_train_batch_size=TEST_CONFIG["batch_size"],
            per_device_eval_batch_size=TEST_CONFIG["batch_size"],
            learning_rate=TEST_CONFIG["learning_rate"],
            logging_steps=TEST_CONFIG["logging_steps"],
            save_steps=TEST_CONFIG["save_steps"],
            eval_steps=TEST_CONFIG["save_steps"],
            evaluation_strategy="steps",
            save_strategy="steps",
            fp16=torch.cuda.is_available(),
            report_to="none",
            save_total_limit=1,
            load_best_model_at_end=False,
        )
        
        # Trainer
        trainer = Seq2SeqTrainer(
            model=model,
            args=training_args,
            train_dataset=train_processed,
            eval_dataset=val_processed,
            tokenizer=tokenizer,
            data_collator=data_collator,
        )
        
        # Train
        logger.info(f"Starting training for {TEST_CONFIG['max_steps']} steps...")
        train_result = trainer.train()
        
        # Save results
        result = {
            "experiment_id": exp_id,
            "experiment": exp_name,
            "model": model_name,
            "model_type": model_type,
            "method": method,
            "status": "success",
            "steps": TEST_CONFIG["max_steps"],
            "train_loss": train_result.training_loss if hasattr(train_result, 'training_loss') else None,
            "timestamp": timestamp,
        }
        
        result_file = output_dir / f"{exp_id}_test_result.json"
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        logger.info(f"SUCCESS: {exp_id} - {exp_name}")
        logger.info(f"Results saved to: {result_file}")
        
        # Cleanup
        del model
        del trainer
        torch.cuda.empty_cache()
        
        return result
        
    except Exception as e:
        logger.error(f"FAILED: {exp_id} - {exp_name}")
        logger.error(f"Error: {str(e)}", exc_info=True)
        
        result = {
            "experiment_id": exp_id,
            "experiment": exp_name,
            "model": model_name,
            "model_type": model_type,
            "method": method,
            "status": "failed",
            "error": str(e),
            "timestamp": timestamp,
        }
        
        return result

def main():
    """Main test function"""
    logger.info("=" * 80)
    logger.info("TESTING ALL 9 XSUM EXPERIMENTS - 20 STEPS")
    logger.info("=" * 80)
    logger.info(f"Timestamp: {timestamp}")
    logger.info(f"Test configuration: {TEST_CONFIG}")
    logger.info("")
    
    # Load dataset once
    train_dataset, val_dataset = load_and_prepare_dataset()
    
    # Run all experiments
    results = []
    for i, exp_config in enumerate(EXPERIMENTS, 1):
        logger.info("")
        logger.info(f"Experiment {i}/9: {exp_config['name']}")
        result = run_experiment(exp_config, train_dataset, val_dataset)
        results.append(result)
        logger.info("")
    
    # Summary
    logger.info("=" * 80)
    logger.info("TEST SUMMARY")
    logger.info("=" * 80)
    
    success_count = sum(1 for r in results if r["status"] == "success")
    failed_count = len(results) - success_count
    
    logger.info(f"Total experiments: {len(results)}")
    logger.info(f"Successful: {success_count}")
    logger.info(f"Failed: {failed_count}")
    logger.info("")
    
    for result in results:
        status_icon = "[OK]" if result["status"] == "success" else "[FAIL]"
        logger.info(f"{status_icon} {result['experiment_id']}: {result['experiment']} - {result['status']}")
    
    # Save summary
    summary_file = log_dir / f"test_summary_{timestamp}.json"
    with open(summary_file, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "test_config": TEST_CONFIG,
            "total": len(results),
            "success": success_count,
            "failed": failed_count,
            "results": results
        }, f, indent=2)
    
    logger.info("")
    logger.info(f"Summary saved to: {summary_file}")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 80)
    
    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
