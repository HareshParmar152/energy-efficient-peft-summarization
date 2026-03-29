#!/usr/bin/env python3
"""
Reddit TIFU All 9 Experiments - 2000 Steps
BART, T5, GPT-2 with LoRA, QLoRA, Adapters
Dataset: Reddit TIFU (informal user narratives)
"""

import os
import sys
import json
import logging
import time
from datetime import datetime
from pathlib import Path

import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
    TrainerCallback,
)
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
from codecarbon import EmissionsTracker

# Base path
BASE_PATH = Path("E:/Pending Experiment data")
REDDIT_PATH = BASE_PATH / "Reddit_TIFU_Experiments"

# Setup logging
log_dir = REDDIT_PATH / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = log_dir / f"reddit_tifu_all_experiments_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8', mode='w'),
        logging.StreamHandler(sys.stdout)
    ],
    force=True
)
logger = logging.getLogger(__name__)

# Make logger flush after each message
class FlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

# Replace file handler with flushing version
for i, handler in enumerate(logging.root.handlers):
    if isinstance(handler, logging.FileHandler):
        new_handler = FlushFileHandler(log_file, encoding='utf-8', mode='w')
        new_handler.setFormatter(handler.formatter)
        new_handler.setLevel(handler.level)
        logging.root.handlers[i] = new_handler

# All 9 Experiment configurations
# QLoRA experiments at the end (Windows compatibility)
EXPERIMENTS = [
    # BART experiments (E1-E3)
    {"exp_id": "E1", "model": "facebook/bart-base", "model_type": "bart", "method": "LoRA", "folder": "BART"},
    {"exp_id": "E3", "model": "facebook/bart-base", "model_type": "bart", "method": "Adapters", "folder": "BART"},
    
    # T5 experiments (E13-E15)
    {"exp_id": "E13", "model": "t5-base", "model_type": "t5", "method": "LoRA", "folder": "T5"},
    {"exp_id": "E15", "model": "t5-base", "model_type": "t5", "method": "Adapters", "folder": "T5"},
    
    # GPT-2 experiments (E25-E27)
    {"exp_id": "E25", "model": "gpt2-medium", "model_type": "gpt2", "method": "LoRA", "folder": "GPT2"},
    {"exp_id": "E27", "model": "gpt2-medium", "model_type": "gpt2", "method": "Adapters", "folder": "GPT2"},
    
    # QLoRA experiments at the end
    {"exp_id": "E2", "model": "facebook/bart-base", "model_type": "bart", "method": "QLoRA", "folder": "BART"},
    {"exp_id": "E14", "model": "t5-base", "model_type": "t5", "method": "QLoRA", "folder": "T5"},
    {"exp_id": "E26", "model": "gpt2-medium", "model_type": "gpt2", "method": "QLoRA", "folder": "GPT2"},
]

# Configuration - Optimized for 4GB GPU with Reddit TIFU
CONFIG = {
    "dataset": "reddit_tifu",
    "max_steps": 2000,
    "batch_size": 8,  # Reddit TIFU has shorter texts than PubMed
    "gradient_accumulation_steps": 2,
    "learning_rate": 3e-4,
    "max_source_length": 512,  # Reddit posts
    "max_target_length": 128,  # TL;DR summaries
    "save_steps": 500,
    "logging_steps": 50,
    "warmup_steps": 100,
    "weight_decay": 0.01,
}

def log_system_info():
    """Log system information"""
    logger.info("="*80)
    logger.info("SYSTEM INFORMATION")
    logger.info("="*80)
    logger.info(f"Python: {sys.version}")
    logger.info(f"PyTorch: {torch.__version__}")
    logger.info(f"CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        logger.info(f"CUDA Version: {torch.version.cuda}")
        logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
        logger.info(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        logger.info("TF32 enabled for better performance")
    logger.info("="*80)

def load_and_prepare_dataset():
    """Load Reddit TIFU dataset"""
    logger.info("Loading Reddit TIFU dataset...")
    
    # Load dataset - using the long version for better summaries
    dataset = load_dataset("reddit_tifu", "long")
    
    # Calculate samples needed for 2000 steps
    samples_needed = CONFIG["max_steps"] * CONFIG["batch_size"] * CONFIG["gradient_accumulation_steps"]
    samples_needed = int(samples_needed * 1.1)  # Add 10% buffer
    
    train_dataset = dataset['train']
    if len(train_dataset) > samples_needed:
        logger.info(f"Limiting dataset from {len(train_dataset)} to {samples_needed} samples for efficiency")
        train_dataset = train_dataset.select(range(samples_needed))
    
    logger.info(f"Dataset loaded: Train: {len(train_dataset)} samples")
    return train_dataset

def preprocess_function_seq2seq(examples, tokenizer, model_type):
    """Preprocess for seq2seq models (BART, T5)"""
    # Reddit TIFU has 'documents' (post) and 'tldr' (summary) fields
    inputs = examples["documents"]
    targets = examples["tldr"]
    
    # Tokenize inputs
    model_inputs = tokenizer(
        inputs,
        max_length=CONFIG["max_source_length"],
        truncation=True,
        padding="max_length",
    )
    
    # Tokenize targets
    labels = tokenizer(
        text_target=targets,
        max_length=CONFIG["max_target_length"],
        truncation=True,
        padding="max_length",
    )
    
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

def preprocess_function_causal(examples, tokenizer):
    """Preprocess for causal LM (GPT-2)"""
    inputs = []
    for doc, tldr in zip(examples["documents"], examples["tldr"]):
        # Format as instruction-response
        text = f"Summarize: {doc}\n\nTL;DR: {tldr}"
        inputs.append(text)
    
    # Tokenize with padding
    model_inputs = tokenizer(
        inputs,
        max_length=CONFIG["max_source_length"] + CONFIG["max_target_length"],
        truncation=True,
        padding="max_length",
    )
    
    # For causal LM, labels are the same as input_ids
    model_inputs["labels"] = model_inputs["input_ids"].copy()
    
    return model_inputs

def setup_peft_model(model, method, model_type):
    """Setup model with PEFT method"""
    if method == "QLoRA":
        model = prepare_model_for_kbit_training(model)
        
        # CRITICAL FIX: Disable gradient checkpointing for QLoRA
        if hasattr(model, 'gradient_checkpointing_disable'):
            model.gradient_checkpointing_disable()
        
        # Enable input gradients
        model.enable_input_require_grads()
    
    # Target modules based on model type
    if model_type == "bart":
        target_modules_base = ["q_proj", "v_proj"]
        target_modules_full = ["q_proj", "v_proj", "k_proj", "out_proj"]
    elif model_type == "t5":
        target_modules_base = ["q", "v"]
        target_modules_full = ["q", "v", "k", "o"]
    elif model_type == "gpt2":
        target_modules_base = ["c_attn"]
        target_modules_full = ["c_attn", "c_proj", "c_fc"]
    else:
        target_modules_base = ["q_proj", "v_proj"]
        target_modules_full = ["q_proj", "v_proj", "k_proj", "out_proj"]
    
    # Task type
    task_type = TaskType.CAUSAL_LM if model_type == "gpt2" else TaskType.SEQ_2_SEQ_LM
    
    if method in ["LoRA", "QLoRA"]:
        lora_config = LoraConfig(
            r=8,
            lora_alpha=16,
            target_modules=target_modules_base,
            lora_dropout=0.1,
            bias="none",
            task_type=task_type
        )
    elif method == "Adapters":
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=target_modules_full,
            lora_dropout=0.1,
            bias="none",
            task_type=task_type
        )
    
    model = get_peft_model(model, lora_config)
    
    # Ensure all LoRA parameters require gradients
    if method == "QLoRA":
        for name, param in model.named_parameters():
            if 'lora_' in name:
                param.requires_grad = True
    
    return model

class ProgressLoggingCallback(TrainerCallback):
    """Custom callback to log training progress"""
    
    def __init__(self, logger, total_steps):
        self.logger = logger
        self.total_steps = total_steps
        self.start_time = None
        
    def on_train_begin(self, args, state, control, **kwargs):
        self.start_time = time.time()
        self.logger.info(f"Training started - Total steps: {self.total_steps}")
    
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs and 'loss' in logs:
            current_step = state.global_step
            progress = (current_step / self.total_steps) * 100
            elapsed = time.time() - self.start_time
            steps_per_sec = current_step / elapsed if elapsed > 0 else 0
            eta_seconds = (self.total_steps - current_step) / steps_per_sec if steps_per_sec > 0 else 0
            eta_minutes = eta_seconds / 60
            
            self.logger.info(
                f"Step {current_step}/{self.total_steps} ({progress:.1f}%) | "
                f"Loss: {logs['loss']:.4f} | "
                f"LR: {logs.get('learning_rate', 0):.2e} | "
                f"Speed: {steps_per_sec:.2f} steps/s | "
                f"ETA: {eta_minutes:.1f} min"
            )

def is_experiment_completed(exp_id, base_path):
    """Check if experiment already completed successfully"""
    for folder in ["BART", "T5", "GPT2"]:
        result_file = base_path / folder / "results" / f"{exp_id}_results.json"
        if result_file.exists():
            try:
                with open(result_file, 'r') as f:
                    results = json.load(f)
                    if results.get("status") == "success":
                        return True
            except:
                pass
    return False

def run_experiment(exp_config, train_dataset):
    """Run a single experiment"""
    exp_id = exp_config["exp_id"]
    model_name = exp_config["model"]
    model_type = exp_config["model_type"]
    method = exp_config["method"]
    folder = exp_config["folder"]
    
    exp_name = f"{exp_id}_{folder}_RedditTIFU_{method}"
    
    logger.info("")
    logger.info("="*80)
    logger.info(f"STARTING EXPERIMENT: {exp_id}")
    logger.info(f"Name: {exp_name}")
    logger.info(f"Model: {model_name}")
    logger.info(f"Type: {model_type}")
    logger.info(f"Method: {method}")
    logger.info("="*80)
    
    start_time = time.time()
    
    try:
        # Create output directories
        model_folder = REDDIT_PATH / folder
        results_dir = model_folder / "results"
        checkpoints_dir = model_folder / "checkpoints" / exp_name
        cache_dir = REDDIT_PATH / "cache" / model_type
        
        results_dir.mkdir(parents=True, exist_ok=True)
        checkpoints_dir.mkdir(parents=True, exist_ok=True)
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Start energy tracking
        tracker = EmissionsTracker(
            project_name=exp_name,
            output_dir=str(results_dir),
            log_level="error"
        )
        tracker.start()
        
        # Load tokenizer and model
        logger.info(f"Loading tokenizer and model...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Load model with quantization if QLoRA
        if method == "QLoRA":
            from transformers import BitsAndBytesConfig
            import gc
            
            # CRITICAL: Aggressive GPU cleanup before QLoRA loading
            if torch.cuda.is_available():
                try:
                    for _ in range(3):
                        gc.collect()
                        torch.cuda.empty_cache()
                        torch.cuda.synchronize()
                    logger.info("GPU memory aggressively cleared before QLoRA loading")
                except Exception as e:
                    logger.warning(f"GPU cleanup warning (non-fatal): {e}")
            
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
            )
            
            if model_type == "gpt2":
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    quantization_config=bnb_config,
                    device_map="auto",
                    torch_dtype=torch.float16,
                )
            else:
                model = AutoModelForSeq2SeqLM.from_pretrained(
                    model_name,
                    quantization_config=bnb_config,
                    device_map="auto",
                    torch_dtype=torch.float16,
                )
        else:
            # Regular loading
            if model_type == "gpt2":
                model = AutoModelForCausalLM.from_pretrained(model_name)
            else:
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            if torch.cuda.is_available():
                model = model.to("cuda")
                logger.info(f"Model moved to GPU: {torch.cuda.get_device_name(0)}")
        
        # Setup PEFT
        logger.info(f"PEFT configured: {method}")
        model = setup_peft_model(model, method, model_type)
        model.print_trainable_parameters()
        
        # Adjust batch size for memory constraints
        batch_size = CONFIG["batch_size"]
        gradient_accumulation = CONFIG["gradient_accumulation_steps"]
        
        if method == "QLoRA":
            batch_size = 4
            gradient_accumulation = 4
            logger.info("QLoRA: Using batch_size=4, gradient_accumulation=4")
        elif method == "Adapters":
            if model_type == "gpt2":
                batch_size = 2
                gradient_accumulation = 8
                logger.info("Adapters: Using batch_size=2, gradient_accumulation=8 (memory protection)")
            else:
                batch_size = 6
                gradient_accumulation = 3
                logger.info("Adapters: Using batch_size=6, gradient_accumulation=3")
        else:
            logger.info(f"LoRA: Using batch_size={batch_size}, gradient_accumulation={gradient_accumulation}")
        
        # Preprocess dataset
        logger.info("Preprocessing training dataset...")
        if model_type == "gpt2":
            train_processed = train_dataset.map(
                lambda x: preprocess_function_causal(x, tokenizer),
                batched=True,
                batch_size=1000,
                remove_columns=train_dataset.column_names,
                desc="Tokenizing train",
                load_from_cache_file=True,
                cache_file_name=str(cache_dir / f"train_gpt2_{len(train_dataset)}.cache"),
                num_proc=1,
            )
        else:
            train_processed = train_dataset.map(
                lambda x: preprocess_function_seq2seq(x, tokenizer, model_type),
                batched=True,
                batch_size=1000,
                remove_columns=train_dataset.column_names,
                desc="Tokenizing train",
                load_from_cache_file=True,
                cache_file_name=str(cache_dir / f"train_{model_type}_{len(train_dataset)}.cache"),
                num_proc=1,
            )
        
        # Data collator
        if model_type == "gpt2":
            data_collator = DataCollatorForSeq2Seq(
                tokenizer=tokenizer,
                model=model,
                label_pad_token_id=-100,
                padding=False,
            )
        else:
            data_collator = DataCollatorForSeq2Seq(
                tokenizer=tokenizer,
                model=model,
                padding=True
            )
        
        # Training arguments
        use_gradient_checkpointing = False
        if method == "Adapters":
            logger.info("Adapters: Gradient checkpointing disabled")
        
        if model_type == "gpt2":
            training_args = TrainingArguments(
                output_dir=str(checkpoints_dir),
                max_steps=CONFIG["max_steps"],
                per_device_train_batch_size=batch_size,
                gradient_accumulation_steps=gradient_accumulation,
                learning_rate=CONFIG["learning_rate"],
                weight_decay=CONFIG["weight_decay"],
                warmup_steps=CONFIG["warmup_steps"],
                logging_steps=CONFIG["logging_steps"],
                save_steps=CONFIG["save_steps"],
                save_strategy="steps",
                fp16=torch.cuda.is_available() and method != "QLoRA",
                save_total_limit=3,
                report_to="none",
                seed=42,
                dataloader_num_workers=0 if method == "QLoRA" else 4,
                dataloader_pin_memory=True,
                gradient_checkpointing=use_gradient_checkpointing,
            )
            
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=train_processed,
                data_collator=data_collator,
                callbacks=[ProgressLoggingCallback(logger, CONFIG["max_steps"])],
            )
        else:
            from transformers import Seq2SeqTrainingArguments, Seq2SeqTrainer
            
            training_args = Seq2SeqTrainingArguments(
                output_dir=str(checkpoints_dir),
                max_steps=CONFIG["max_steps"],
                per_device_train_batch_size=batch_size,
                gradient_accumulation_steps=gradient_accumulation,
                learning_rate=CONFIG["learning_rate"],
                weight_decay=CONFIG["weight_decay"],
                warmup_steps=CONFIG["warmup_steps"],
                logging_steps=CONFIG["logging_steps"],
                save_steps=CONFIG["save_steps"],
                save_strategy="steps",
                fp16=torch.cuda.is_available() and method != "QLoRA",
                save_total_limit=3,
                predict_with_generate=False,
                report_to="none",
                seed=42,
                dataloader_num_workers=0 if method == "QLoRA" else 4,
                dataloader_pin_memory=True,
                gradient_checkpointing=use_gradient_checkpointing,
            )
            
            trainer = Seq2SeqTrainer(
                model=model,
                args=training_args,
                train_dataset=train_processed,
                data_collator=data_collator,
                callbacks=[ProgressLoggingCallback(logger, CONFIG["max_steps"])],
            )
        
        # Train
        logger.info("Starting training for 2000 steps...")
        train_result = trainer.train()
        
        # Stop energy tracking
        emissions = tracker.stop()
        
        # Save model
        logger.info("Saving model...")
        trainer.save_model(checkpoints_dir)
        tokenizer.save_pretrained(checkpoints_dir)
        
        # Calculate metrics
        end_time = time.time()
        duration_seconds = end_time - start_time
        duration_minutes = duration_seconds / 60
        
        # Get trainable parameters
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in model.parameters())
        trainable_percentage = (trainable_params / total_params) * 100
        
        # Save results
        results = {
            "experiment_id": exp_id,
            "experiment_name": exp_name,
            "model": model_name,
            "model_type": model_type,
            "method": method,
            "dataset": "reddit_tifu",
            "status": "success",
            "timestamp": timestamp,
            "config": CONFIG,
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
            "note": "Causal LM approach for decoder-only model" if model_type == "gpt2" else "Seq2Seq model"
        }
        
        result_file = results_dir / f"{exp_id}_results.json"
        with open(result_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Experiment completed successfully in {duration_minutes:.1f} minutes")
        logger.info(f"Results saved to: {result_file}")
        
        # Cleanup
        del model
        del trainer
        del train_processed
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            logger.info("GPU memory cleared")
        
        return results
        
    except Exception as e:
        logger.error(f"[FAILED] {exp_id} - {exp_name}")
        logger.error(f"Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Save failure info
        end_time = time.time()
        duration_seconds = end_time - start_time
        
        results = {
            "experiment_id": exp_id,
            "experiment_name": exp_name,
            "model": model_name,
            "model_type": model_type,
            "method": method,
            "dataset": "reddit_tifu",
            "status": "failed",
            "error": str(e),
            "timestamp": timestamp,
            "duration_seconds": duration_seconds
        }
        
        result_file = results_dir / f"{exp_id}_results_FAILED.json"
        with open(result_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Cleanup on failure
        try:
            if 'model' in locals():
                del model
            if 'trainer' in locals():
                del trainer
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except:
            pass
        
        return results

def main():
    """Main execution function"""
    logger.info("="*80)
    logger.info("REDDIT TIFU ALL 9 EXPERIMENTS - 2000 STEPS")
    logger.info("="*80)
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Base path: {REDDIT_PATH}")
    logger.info(f"Configuration: {CONFIG}")
    logger.info("")
    
    # Log system info
    log_system_info()
    
    # Load dataset once
    train_dataset = load_and_prepare_dataset()
    
    # Run all experiments sequentially
    all_results = []
    
    for i, exp_config in enumerate(EXPERIMENTS, 1):
        logger.info("")
        logger.info("="*80)
        logger.info(f"EXPERIMENT {i}/{len(EXPERIMENTS)}: {exp_config['exp_id']}")
        logger.info("="*80)
        
        # Check if already completed
        if is_experiment_completed(exp_config['exp_id'], REDDIT_PATH):
            logger.info(f"Skipping {exp_config['exp_id']} - already completed")
            # Load existing results
            for folder in ["BART", "T5", "GPT2"]:
                result_file = REDDIT_PATH / folder / "results" / f"{exp_config['exp_id']}_results.json"
                if result_file.exists():
                    with open(result_file, 'r') as f:
                        all_results.append(json.load(f))
                    break
            continue
        
        result = run_experiment(exp_config, train_dataset)
        all_results.append(result)
        
        logger.info("")
        logger.info(f"Completed {i}/{len(EXPERIMENTS)} experiments")
        logger.info("")
        
        # CRITICAL: Aggressive GPU cleanup between experiments
        if torch.cuda.is_available():
            import gc
            gc.collect()
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            gc.collect()
            torch.cuda.empty_cache()
            logger.info("GPU memory aggressively cleared between experiments")
        
        # Small delay between experiments
        if i < len(EXPERIMENTS):
            logger.info("Waiting 10 seconds before next experiment...")
            time.sleep(10)
    
    # Final summary
    logger.info("")
    logger.info("="*80)
    logger.info("ALL EXPERIMENTS COMPLETED")
    logger.info("="*80)
    
    success_count = sum(1 for r in all_results if r["status"] == "success")
    failed_count = len(all_results) - success_count
    
    logger.info(f"Total experiments: {len(all_results)}")
    logger.info(f"Successful: {success_count}")
    logger.info(f"Failed: {failed_count}")
    logger.info("")
    
    # Summary by model
    for model_folder in ["BART", "T5", "GPT2"]:
        model_results = [r for r in all_results if model_folder.lower() in r.get("experiment_name", "").lower()]
        if model_results:
            logger.info(f"{model_folder}:")
            for r in model_results:
                status = "OK" if r["status"] == "success" else "FAIL"
                time_min = r.get("train_runtime_minutes", r.get("duration_seconds", 0) / 60)
                logger.info(f"  [{status}] {r['experiment_id']}: {r['method']} - Time: {time_min:.1f} min")
    
    # Save master summary
    summary_file = REDDIT_PATH / f"reddit_tifu_all_summary_{timestamp}.json"
    with open(summary_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    logger.info("")
    logger.info(f"Master summary saved to: {summary_file}")
    logger.info(f"Log file: {log_file}")
    logger.info("="*80)

if __name__ == "__main__":
    main()
