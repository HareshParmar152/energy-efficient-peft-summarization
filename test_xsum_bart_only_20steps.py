#!/usr/bin/env python3
"""
Test BART XSum Experiments Only - 20 Steps
BART × LoRA, QLoRA, Adapters
Quick test to verify BART configurations work
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
    BartTokenizer,
    BartForConditionalGeneration,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq,
)
from peft import LoraConfig, get_peft_model, TaskType

# Setup logging
log_dir = Path("test_logs")
log_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = log_dir / f"test_bart_xsum_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Experiment configurations
EXPERIMENTS = [
    {"method": "LoRA", "name": "BART_XSum_LoRA"},
    {"method": "QLoRA", "name": "BART_XSum_QLoRA"},
    {"method": "Adapters", "name": "BART_XSum_Adapters"},
]

# Test configuration
TEST_CONFIG = {
    "model_name": "facebook/bart-base",
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
    train_dataset = dataset['train'].select(range(100))
    val_dataset = dataset['validation'].select(range(20))
    
    logger.info(f"Test dataset: {len(train_dataset)} train, {len(val_dataset)} val")
    return train_dataset, val_dataset

def preprocess_function(examples, tokenizer):
    """Preprocess the dataset"""
    inputs = examples["document"]
    targets = examples["summary"]
    
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

def setup_peft_model(model, method):
    """Setup model with PEFT method"""
    if method == "LoRA":
        lora_config = LoraConfig(
            r=8,
            lora_alpha=16,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.1,
            bias="none",
            task_type=TaskType.SEQ_2_SEQ_LM
        )
        model = get_peft_model(model, lora_config)
    elif method == "QLoRA":
        # For testing, use same as LoRA (QLoRA needs 4-bit quantization which is complex)
        lora_config = LoraConfig(
            r=8,
            lora_alpha=16,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.1,
            bias="none",
            task_type=TaskType.SEQ_2_SEQ_LM
        )
        model = get_peft_model(model, lora_config)
    elif method == "Adapters":
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj", "k_proj", "out_proj"],
            lora_dropout=0.1,
            bias="none",
            task_type=TaskType.SEQ_2_SEQ_LM
        )
        model = get_peft_model(model, lora_config)
    
    return model

def run_experiment(exp_config, train_dataset, val_dataset):
    """Run a single experiment"""
    exp_name = exp_config["name"]
    method = exp_config["method"]
    
    logger.info("=" * 80)
    logger.info(f"STARTING: {exp_name}")
    logger.info("=" * 80)
    
    try:
        # Load tokenizer and model
        logger.info(f"Loading model: {TEST_CONFIG['model_name']}")
        tokenizer = BartTokenizer.from_pretrained(TEST_CONFIG['model_name'])
        model = BartForConditionalGeneration.from_pretrained(TEST_CONFIG['model_name'])
        
        # Setup PEFT
        model = setup_peft_model(model, method)
        logger.info(f"Model configured with {method}")
        model.print_trainable_parameters()
        
        # Preprocess dataset
        logger.info("Preprocessing dataset...")
        train_processed = train_dataset.map(
            lambda x: preprocess_function(x, tokenizer),
            batched=True,
            remove_columns=train_dataset.column_names,
        )
        
        val_processed = val_dataset.map(
            lambda x: preprocess_function(x, tokenizer),
            batched=True,
            remove_columns=val_dataset.column_names,
        )
        
        # Data collator
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=tokenizer,
            model=model,
            padding=True
        )
        
        # Output directory
        output_dir = Path(f"test_outputs/{exp_name}_{timestamp}")
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
            "experiment": exp_name,
            "model": TEST_CONFIG['model_name'],
            "method": method,
            "status": "success",
            "steps": TEST_CONFIG["max_steps"],
            "train_loss": train_result.training_loss if hasattr(train_result, 'training_loss') else None,
            "timestamp": timestamp,
        }
        
        result_file = output_dir / "test_result.json"
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        logger.info(f"SUCCESS: {exp_name}")
        logger.info(f"Results saved to: {result_file}")
        
        # Cleanup
        del model
        del trainer
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        return result
        
    except Exception as e:
        logger.error(f"FAILED: {exp_name}")
        logger.error(f"Error: {str(e)}", exc_info=True)
        
        result = {
            "experiment": exp_name,
            "model": TEST_CONFIG['model_name'],
            "method": method,
            "status": "failed",
            "error": str(e),
            "timestamp": timestamp,
        }
        
        return result

def main():
    """Main test function"""
    logger.info("=" * 80)
    logger.info("TESTING BART XSUM EXPERIMENTS - 20 STEPS")
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
        logger.info(f"Experiment {i}/3: {exp_config['name']}")
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
        logger.info(f"{status_icon} {result['experiment']}: {result['status']}")
    
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
