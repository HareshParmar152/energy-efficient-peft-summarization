#!/usr/bin/env python3
"""
PubMed GPT-2 Experiments - 2000 Steps
Uses Causal LM approach for decoder-only models (E28-E30)
Model: GPT-2 Medium (355M parameters - decoder-only architecture)
Dataset: PubMed (biomedical literature summarization)
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
PUBMED_PATH = BASE_PATH / "PubMed_Experiments"

# Setup logging
log_dir = PUBMED_PATH / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = log_dir / f"pubmed_gpt2_experiments_{timestamp}.log"

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

# GPT-2 Experiment configurations - Using GPT-2 Medium for 4GB GPU
EXPERIMENTS = [
    {"exp_id": "E28", "model": "gpt2-medium", "method": "LoRA", "folder": "GPT2"},
    {"exp_id": "E30", "model": "gpt2-medium", "method": "Adapters", "folder": "GPT2"},
    {"exp_id": "E29", "model": "gpt2-medium", "method": "QLoRA", "folder": "GPT2"},
]

# Configuration - Optimized for GPT-2 Medium on 4GB GPU
CONFIG = {
    "dataset": "pubmed",
    "max_steps": 2000,
    "batch_size": 6,  # Smaller for longer PubMed abstracts
    "gradient_accumulation_steps": 3,  # Maintain effective batch size
    "learning_rate": 2e-4,
    "max_length": 512,  # PubMed abstracts can be long
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
        # Enable TF32 for better performance on Ampere GPUs
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        logger.info("TF32 enabled for better performance")
    logger.info("="*80)

def load_and_prepare_dataset():
    """Load PubMed dataset"""
    logger.info("Loading PubMed dataset...")
    dataset = load_dataset("ccdv/pubmed-summarization", "document")
    
    # Calculate samples needed for 2000 steps
    # With batch_size=6 and gradient_accumulation=3, effective batch = 18
    # 2000 steps * 18 = 36,000 samples needed
    samples_needed = CONFIG["max_steps"] * CONFIG["batch_size"] * CONFIG["gradient_accumulation_steps"]
    samples_needed = int(samples_needed * 1.1)  # Add 10% buffer
    
    train_dataset = dataset['train']
    if len(train_dataset) > samples_needed:
        logger.info(f"Limiting dataset from {len(train_dataset)} to {samples_needed} samples for efficiency")
        train_dataset = train_dataset.select(range(samples_needed))
    
    logger.info(f"Dataset loaded: Train: {len(train_dataset)} samples")
    return train_dataset

def preprocess_function_causal(examples, tokenizer):
    """Preprocess for causal LM with prompt format - PubMed"""
    inputs = []
    for article, abstract in zip(examples["article"], examples["abstract"]):
        # Format for biomedical summarization
        prompt = f"Summarize the following biomedical article:\n\n{article}\n\nAbstract: {abstract}"
        inputs.append(prompt)
    
    # Tokenize with padding
    model_inputs = tokenizer(
        inputs,
        max_length=CONFIG["max_length"],
        truncation=True,
        padding="max_length",
    )
    
    # For causal LM, labels are the same as input_ids
    model_inputs["labels"] = [
        [(label if label != tokenizer.pad_token_id else -100) for label in labels]
        for labels in model_inputs["input_ids"]
    ]
    
    return model_inputs

def setup_peft_model(model, method):
    """Setup model with PEFT method - all methods use 4-bit quantization"""
    # Always prepare for quantization since we're using 4-bit for all methods
    model = prepare_model_for_kbit_training(model)
    
    # Target modules for GPT-2
    target_modules_base = ["c_attn"]  # GPT-2 uses c_attn for Q,K,V
    target_modules_full = ["c_attn", "c_proj", "c_fc"]
    
    if method in ["LoRA", "QLoRA"]:
        lora_config = LoraConfig(
            r=8,
            lora_alpha=16,
            target_modules=target_modules_base,
            lora_dropout=0.1,
            bias="none",
            task_type=TaskType.CAUSAL_LM  # Changed to CAUSAL_LM
        )
    elif method == "Adapters":
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=target_modules_full,
            lora_dropout=0.1,
            bias="none",
            task_type=TaskType.CAUSAL_LM  # Changed to CAUSAL_LM
        )
    
    model = get_peft_model(model, lora_config)
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
        if logs and state.global_step > 0:
            current_step = state.global_step
            progress_pct = (current_step / self.total_steps) * 100
            elapsed = time.time() - self.start_time
            steps_per_sec = current_step / elapsed if elapsed > 0 else 0
            eta_seconds = (self.total_steps - current_step) / steps_per_sec if steps_per_sec > 0 else 0
            eta_minutes = eta_seconds / 60
            
            loss = logs.get('loss', 'N/A')
            lr = logs.get('learning_rate', 'N/A')
            
            loss_str = f"{loss:.4f}" if isinstance(loss, (int, float)) else str(loss)
            lr_str = f"{lr:.2e}" if isinstance(lr, (int, float)) else str(lr)
            
            self.logger.info(
                f"Step {current_step}/{self.total_steps} ({progress_pct:.1f}%) | "
                f"Loss: {loss_str} | "
                f"LR: {lr_str} | "
                f"Speed: {steps_per_sec:.2f} steps/s | "
                f"ETA: {eta_minutes:.1f} min"
            )
            
    def on_train_end(self, args, state, control, **kwargs):
        elapsed = time.time() - self.start_time
        self.logger.info(f"Training completed in {elapsed/60:.2f} minutes")

def is_experiment_completed(exp_id, base_path):
    """Check if an experiment is already completed"""
    result_file = base_path / "GPT2" / "results" / f"{exp_id}_results.json"
    if result_file.exists():
        try:
            with open(result_file, 'r') as f:
                result = json.load(f)
                if result.get("status") == "success":
                    logger.info(f"[SKIP] {exp_id} already completed successfully")
                    return True
        except:
            pass
    return False

def run_experiment(exp_config, train_dataset):
    """Run a single GPT-2 experiment on PubMed"""
    exp_id = exp_config["exp_id"]
    model_name = exp_config["model"]
    method = exp_config["method"]
    folder = exp_config["folder"]
    
    exp_name = f"{exp_id}_GPT2_PubMed_{method}"
    
    logger.info("")
    logger.info("="*80)
    logger.info(f"STARTING EXPERIMENT: {exp_id}")
    logger.info(f"Name: {exp_name}")
    logger.info(f"Model: {model_name}")
    logger.info(f"Method: {method}")
    logger.info("="*80)
    
    start_time = time.time()
    
    try:
        # Create output directories
        model_folder = PUBMED_PATH / folder
        results_dir = model_folder / "results"
        checkpoints_dir = model_folder / "checkpoints" / exp_name
        
        results_dir.mkdir(parents=True, exist_ok=True)
        checkpoints_dir.mkdir(parents=True, exist_ok=True)
        
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
        
        # Set pad token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            tokenizer.pad_token_id = tokenizer.eos_token_id
        
        # Load model with 4-bit quantization for ALL methods (4GB GPU limitation)
        from transformers import BitsAndBytesConfig
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        logger.info(f"Loading model with 4-bit quantization (required for 4GB GPU)...")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto",
            low_cpu_mem_usage=True,
        )
        model.config.use_cache = False
        
        # Enable gradient checkpointing for memory efficiency
        model.gradient_checkpointing_enable()
        
        logger.info(f"Model loaded with 4-bit quantization")
        
        # Setup PEFT
        model = setup_peft_model(model, method)
        logger.info(f"PEFT configured: {method}")
        model.print_trainable_parameters()
        
        model.train()
        if hasattr(model.config, 'use_cache'):
            model.config.use_cache = False
        
        # Adjust batch size for GPT-2 Medium with 4-bit quantization
        batch_size = CONFIG["batch_size"]
        gradient_accumulation = CONFIG["gradient_accumulation_steps"]
        
        # Conservative batch sizes to ensure GPU efficiency
        if method == "Adapters":
            batch_size = 6
            gradient_accumulation = 3
            logger.info("Adapters: Using batch_size=6, gradient_accumulation=3")
        else:
            batch_size = 8
            gradient_accumulation = 2
            logger.info(f"{method}: Using batch_size=8, gradient_accumulation=2")
        
        # Get trainable parameters info
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in model.parameters())
        
        # Preprocess dataset
        logger.info("Preprocessing training dataset...")
        
        # Create cache directory
        cache_dir = PUBMED_PATH / "cache" / "gpt2"
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        train_processed = train_dataset.map(
            lambda x: preprocess_function_causal(x, tokenizer),
            batched=True,
            batch_size=1000,  # Process in larger batches for speed
            remove_columns=train_dataset.column_names,
            desc="Tokenizing train",
            load_from_cache_file=True,  # Enable caching
            cache_file_name=str(cache_dir / f"train_gpt2_{len(train_dataset)}.cache"),
            num_proc=1,  # Single process to avoid overhead
        )
        
        # Data collator for causal LM - no additional padding needed
        from transformers import DataCollatorForSeq2Seq
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=tokenizer,
            model=model,
            label_pad_token_id=-100,
            padding=False,  # Already padded in preprocessing
        )
        
        # Training arguments - all methods use 4-bit quantization
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
            fp16=False,  # Using 4-bit quantization instead
            save_total_limit=2,
            report_to="none",
            seed=42,
            dataloader_num_workers=0,  # MUST be 0 on Windows to avoid multiprocessing errors
            dataloader_pin_memory=True,
            dataloader_prefetch_factor=None,  # Disabled for num_workers=0
            gradient_checkpointing=False,  # Disabled to avoid Windows multiprocessing issues
            optim="paged_adamw_8bit",  # 8-bit optimizer for better memory efficiency
            max_grad_norm=1.0,
            ddp_find_unused_parameters=False,
        )
        
        # Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_processed,
            data_collator=data_collator,
            callbacks=[ProgressLoggingCallback(logger, CONFIG["max_steps"])],
        )
        
        # Train
        logger.info(f"Starting training for {CONFIG['max_steps']} steps...")
        train_result = trainer.train()
        
        # Stop energy tracking
        emissions = tracker.stop()
        
        # Calculate duration
        duration_seconds = time.time() - start_time
        duration_minutes = duration_seconds / 60
        
        logger.info("Training completed!")
        logger.info(f"Duration: {duration_minutes:.2f} minutes")
        logger.info(f"Emissions: {emissions:.6f} kg CO2")
        
        # Save model
        logger.info("Saving final model...")
        trainer.save_model(str(checkpoints_dir / "final_model"))
        tokenizer.save_pretrained(str(checkpoints_dir / "final_model"))
        
        # Compile results
        results = {
            "experiment_id": exp_id,
            "experiment_name": exp_name,
            "model": model_name,
            "model_type": "gpt2",
            "method": method,
            "dataset": "pubmed",
            "status": "success",
            "timestamp": timestamp,
            "config": CONFIG,
            "trainable_parameters": trainable_params,
            "total_parameters": total_params,
            "trainable_percentage": (trainable_params / total_params) * 100,
            "train_runtime_seconds": duration_seconds,
            "train_runtime_minutes": duration_minutes,
            "train_loss": train_result.metrics.get("train_loss"),
            "train_samples_per_second": train_result.metrics.get("train_samples_per_second"),
            "train_steps_per_second": train_result.metrics.get("train_steps_per_second"),
            "emissions_kg_co2": emissions,
            "checkpoint_dir": str(checkpoints_dir),
            "results_dir": str(results_dir),
            "note": "Causal LM approach for decoder-only model"
        }
        
        # Save results
        result_file = results_dir / f"{exp_id}_results.json"
        with open(result_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"[SUCCESS] {exp_id} - {exp_name}")
        logger.info(f"Results saved to: {result_file}")
        
        # Cleanup
        del model
        del trainer
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            logger.info("GPU memory cleared")
        
        return results
        
    except Exception as e:
        logger.error(f"[FAILED] {exp_id} - {exp_name}")
        logger.error(f"Error: {str(e)}", exc_info=True)
        
        # Emergency cleanup
        try:
            if 'model' in locals():
                del model
            if 'trainer' in locals():
                del trainer
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except:
            pass
        
        duration_seconds = time.time() - start_time
        
        results = {
            "experiment_id": exp_id,
            "experiment_name": exp_name,
            "model": model_name,
            "model_type": "gpt2",
            "method": method,
            "dataset": "pubmed",
            "status": "failed",
            "error": str(e),
            "timestamp": timestamp,
            "duration_seconds": duration_seconds,
        }
        
        # Save error results
        result_file = results_dir / f"{exp_id}_results_FAILED.json"
        with open(result_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results

def main():
    """Main execution function"""
    logger.info("="*80)
    logger.info("PUBMED GPT-2 EXPERIMENTS - 2000 STEPS (Causal LM Approach)")
    logger.info("="*80)
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Base path: {PUBMED_PATH}")
    logger.info(f"Model: GPT-2 Medium (355M - decoder-only architecture)")
    logger.info(f"Dataset: PubMed (biomedical literature)")
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
        logger.info(f"EXPERIMENT {i}/3: {exp_config['exp_id']}")
        logger.info("="*80)
        
        # Check if already completed
        if is_experiment_completed(exp_config['exp_id'], PUBMED_PATH):
            logger.info(f"Skipping {exp_config['exp_id']} - already completed")
            result_file = PUBMED_PATH / "GPT2" / "results" / f"{exp_config['exp_id']}_results.json"
            with open(result_file, 'r') as f:
                all_results.append(json.load(f))
            continue
        
        result = run_experiment(exp_config, train_dataset)
        all_results.append(result)
        
        logger.info("")
        logger.info(f"Completed {i}/3 experiments")
        logger.info("")
        
        # Small delay between experiments
        if i < len(EXPERIMENTS):
            logger.info("Waiting 10 seconds before next experiment...")
            time.sleep(10)
    
    # Final summary
    logger.info("")
    logger.info("="*80)
    logger.info("ALL GPT-2 EXPERIMENTS COMPLETED")
    logger.info("="*80)
    
    success_count = sum(1 for r in all_results if r["status"] == "success")
    failed_count = len(all_results) - success_count
    
    logger.info(f"Total experiments: {len(all_results)}")
    logger.info(f"Successful: {success_count}")
    logger.info(f"Failed: {failed_count}")
    logger.info("")
    
    for r in all_results:
        status = "[OK]" if r["status"] == "success" else "[FAIL]"
        duration = r.get("train_runtime_minutes", 0)
        logger.info(f"  {status} {r['experiment_id']}: {r['method']} - Time: {duration:.1f} min")
    
    # Save master summary
    summary_file = PUBMED_PATH / f"pubmed_gpt2_summary_{timestamp}.json"
    with open(summary_file, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "config": CONFIG,
            "total_experiments": len(all_results),
            "successful": success_count,
            "failed": failed_count,
            "results": all_results
        }, f, indent=2)
    
    logger.info("")
    logger.info(f"Master summary saved to: {summary_file}")
    logger.info(f"Log file: {log_file}")
    logger.info("="*80)
    
    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
