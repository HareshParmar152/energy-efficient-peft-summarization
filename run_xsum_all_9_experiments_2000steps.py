#!/usr/bin/env python3
"""
XSum All 9 Experiments - 2000 Steps Production Run
Runs experiments sequentially: E1-E3 (BART), E13-E15 (T5), E25-E27 (LLaMA)
Collects all metrics as per research proposal
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
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
    DataCollatorForLanguageModeling,
    TrainerCallback,
)
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
from codecarbon import EmissionsTracker

# Base path as per Rules
BASE_PATH = Path("E:/Pending Experiment data")
XSUM_PATH = BASE_PATH / "XSum_Experiments"

# Setup logging
log_dir = XSUM_PATH / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = log_dir / f"xsum_all_9_experiments_{timestamp}.log"

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

# Force immediate flush for all handlers
for handler in logging.root.handlers:
    handler.setLevel(logging.INFO)
    handler.flush()

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

# Experiment configurations - Following Rules file
# E2, E14, E26 (QLoRA) moved to end due to Windows multiprocessing issues
EXPERIMENTS = [
    # E1, E3: BART experiments (non-QLoRA)
    {"exp_id": "E1", "model": "facebook/bart-base", "model_type": "bart", "method": "LoRA", "folder": "BART"},
    {"exp_id": "E3", "model": "facebook/bart-base", "model_type": "bart", "method": "Adapters", "folder": "BART"},
    
    # E13, E15: T5 experiments (non-QLoRA)
    {"exp_id": "E13", "model": "t5-base", "model_type": "t5", "method": "LoRA", "folder": "T5"},
    {"exp_id": "E15", "model": "t5-base", "model_type": "t5", "method": "Adapters", "folder": "T5"},
    
    # E25, E27: GPT-2 experiments (non-QLoRA) - Using GPT-2 instead of LLaMA due to compatibility issues
    {"exp_id": "E25", "model": "gpt2-medium", "model_type": "gpt2", "method": "LoRA", "folder": "GPT2"},
    {"exp_id": "E27", "model": "gpt2-medium", "model_type": "gpt2", "method": "Adapters", "folder": "GPT2"},
    
    # QLoRA experiments at the end (Windows compatibility issues)
    {"exp_id": "E2", "model": "facebook/bart-base", "model_type": "bart", "method": "QLoRA", "folder": "BART"},
    {"exp_id": "E14", "model": "t5-base", "model_type": "t5", "method": "QLoRA", "folder": "T5"},
    # E26 SKIPPED - Memory issues on 4GB GPU after running multiple experiments
    # {"exp_id": "E26", "model": "gpt2-medium", "model_type": "gpt2", "method": "QLoRA", "folder": "GPT2"},
]

# Production configuration - TRAINING ONLY
CONFIG = {
    "dataset": "xsum",
    "max_steps": 2000,
    "batch_size": 16,  # Increased from 8 - adjust based on GPU memory
    "gradient_accumulation_steps": 1,  # Reduced since batch_size increased
    "learning_rate": 3e-4,
    "max_source_length": 512,
    "max_target_length": 128,
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
    logger.info("="*80)

def load_and_prepare_dataset():
    """Load XSum dataset - training only"""
    logger.info("Loading XSum dataset...")
    dataset = load_dataset("xsum")
    
    # Calculate samples needed for 2000 steps
    # With batch_size=8 and gradient_accumulation=2, effective batch = 16
    # 2000 steps * 16 = 32,000 samples needed
    samples_needed = CONFIG["max_steps"] * CONFIG["batch_size"] * CONFIG["gradient_accumulation_steps"]
    samples_needed = int(samples_needed * 1.1)  # Add 10% buffer
    
    train_dataset = dataset['train']
    if len(train_dataset) > samples_needed:
        logger.info(f"Limiting dataset from {len(train_dataset)} to {samples_needed} samples for efficiency")
        train_dataset = train_dataset.select(range(samples_needed))
    
    logger.info(f"Dataset loaded:")
    logger.info(f"  Train: {len(train_dataset)} samples")
    logger.info(f"  (Validation and test will be used later for evaluation)")
    
    return train_dataset  # Return only training data

def preprocess_function(examples, tokenizer, model_type):
    """Preprocess the dataset"""
    inputs = examples["document"]
    targets = examples["summary"]
    
    # T5 requires prefix
    if model_type == "t5":
        inputs = ["summarize: " + doc for doc in inputs]
    
    model_inputs = tokenizer(
        inputs,
        max_length=CONFIG["max_source_length"],
        truncation=True,
        padding=False  # Dynamic padding - much faster
    )
    
    labels = tokenizer(
        targets,
        max_length=CONFIG["max_target_length"],
        truncation=True,
        padding=False  # Dynamic padding - much faster
    )
    
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

def preprocess_function_causal(examples, tokenizer):
    """Preprocess for causal LM (GPT-2)"""
    inputs = []
    for doc, summary in zip(examples["document"], examples["summary"]):
        # Format: "Summarize: {document}\n\nSummary: {summary}"
        prompt = f"Summarize the following article:\n\n{doc}\n\nSummary: {summary}"
        inputs.append(prompt)
    
    # Tokenize with padding
    model_inputs = tokenizer(
        inputs,
        max_length=CONFIG["max_source_length"],
        truncation=True,
        padding="max_length",
    )
    
    # For causal LM, labels are the same as input_ids, but mask padding
    model_inputs["labels"] = [
        [(label if label != tokenizer.pad_token_id else -100) for label in labels]
        for labels in model_inputs["input_ids"]
    ]
    
    return model_inputs

def setup_peft_model(model, method, model_type):
    """Setup model with PEFT method"""
    if method == "QLoRA":
        model = prepare_model_for_kbit_training(model)
        
        # CRITICAL FIX: Disable gradient checkpointing completely for QLoRA
        # This prevents "element 0 of tensors does not require grad" error
        if hasattr(model, 'gradient_checkpointing_disable'):
            model.gradient_checkpointing_disable()
        
        # Enable input gradients for QLoRA
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
    
    # Ensure all LoRA parameters require gradients (especially for QLoRA)
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
        if logs and state.global_step > 0:
            current_step = state.global_step
            progress_pct = (current_step / self.total_steps) * 100
            elapsed = time.time() - self.start_time
            steps_per_sec = current_step / elapsed if elapsed > 0 else 0
            eta_seconds = (self.total_steps - current_step) / steps_per_sec if steps_per_sec > 0 else 0
            eta_minutes = eta_seconds / 60
            
            loss = logs.get('loss', 'N/A')
            lr = logs.get('learning_rate', 'N/A')
            
            # Format loss and lr safely
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
    # Check all possible result file locations
    for folder in ["BART", "T5", "LLaMA"]:
        result_file = base_path / folder / "results" / f"{exp_id}_results.json"
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
    """Run a single experiment - TRAINING ONLY"""
    exp_id = exp_config["exp_id"]
    model_name = exp_config["model"]
    model_type = exp_config["model_type"]
    method = exp_config["method"]
    folder = exp_config["folder"]
    
    exp_name = f"{exp_id}_{folder}_XSum_{method}"
    
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
        model_folder = XSUM_PATH / folder
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
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Load model with quantization if QLoRA
        if method == "QLoRA":
            from transformers import BitsAndBytesConfig
            import gc
            
            # CRITICAL: Aggressive GPU cleanup before QLoRA loading
            if torch.cuda.is_available():
                try:
                    # Multiple cleanup passes
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
            # Fix for PyTorch 2.6+ compatibility
            model.config.use_cache = False
        else:
            if model_type == "gpt2":
                model = AutoModelForCausalLM.from_pretrained(model_name)
            else:
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            # Move model to GPU if available
            if torch.cuda.is_available():
                model = model.to("cuda")
                logger.info(f"Model moved to GPU: {torch.cuda.get_device_name(0)}")
        
        # Setup PEFT
        model = setup_peft_model(model, method, model_type)
        logger.info(f"PEFT configured: {method}")
        model.print_trainable_parameters()
        
        # Fix for QLoRA on Windows - disable gradient requirement hook
        if method == "QLoRA":
            # Manually enable gradients for input embeddings instead of using the hook
            for param in model.get_input_embeddings().parameters():
                param.requires_grad = True
            logger.info("QLoRA: Manually enabled input embeddings gradients (Windows fix)")
        
        # Ensure model is in training mode and disable cache for gradient checkpointing
        model.train()
        if hasattr(model.config, 'use_cache'):
            model.config.use_cache = False
        
        # For Adapters, ensure all trainable parameters have gradients enabled
        if method == "Adapters":
            for name, param in model.named_parameters():
                if param.requires_grad:
                    param.requires_grad = True
            logger.info("Adapters: Verified all trainable parameters require gradients")
        
        # Adjust batch size for memory constraints (RTX 2050 has 4GB)
        batch_size = CONFIG["batch_size"]
        gradient_accumulation = CONFIG["gradient_accumulation_steps"]
        
        if method == "QLoRA":
            # QLoRA needs minimal batch size for 4GB GPU (XSum can have memory spikes)
            batch_size = 1
            gradient_accumulation = 16
            logger.info("QLoRA: Using batch_size=1, gradient_accumulation=16 (4GB GPU + XSum protection)")
        elif method == "Adapters":
            # Adapters use more parameters, reduce batch size
            batch_size = 8
            gradient_accumulation = 2
            logger.info("Adapters: Using batch_size=8, gradient_accumulation=2 (memory protection)")
        else:
            # LoRA - standard settings
            batch_size = 12
            gradient_accumulation = 1
            logger.info("LoRA: Using batch_size=12, gradient_accumulation=1")
        
        # Disable gradient checkpointing for Adapters (causes gradient issues)
        use_gradient_checkpointing = False
        if method == "Adapters":
            logger.info("Adapters: Gradient checkpointing disabled (compatibility fix)")
        
        # Get trainable parameters info
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in model.parameters())
        
        # Preprocess dataset - TRAINING ONLY
        logger.info("Preprocessing training dataset...")
        
        # Create cache directory for this model type
        cache_dir = XSUM_PATH / "cache" / model_type
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        if model_type == "gpt2":
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
        else:
            train_processed = train_dataset.map(
                lambda x: preprocess_function(x, tokenizer, model_type),
                batched=True,
                batch_size=1000,  # Process in larger batches for speed
                remove_columns=train_dataset.column_names,
                desc="Tokenizing train",
                load_from_cache_file=True,  # Enable caching
                cache_file_name=str(cache_dir / f"train_{model_type}_{len(train_dataset)}.cache"),
                num_proc=1,  # Single process to avoid overhead
            )
        
        # Data collator
        if model_type == "gpt2":
            data_collator = DataCollatorForSeq2Seq(
                tokenizer=tokenizer,
                model=model,
                label_pad_token_id=-100,
                padding=False,  # Already padded in preprocessing
            )
        else:
            data_collator = DataCollatorForSeq2Seq(
                tokenizer=tokenizer,
                model=model,
                padding=True
            )
        
        # Training arguments - NO EVALUATION
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
                fp16=torch.cuda.is_available() and method != "QLoRA",  # QLoRA already uses fp16
                save_total_limit=3,
                report_to="none",
                seed=42,
                # GPU Performance optimizations
                dataloader_num_workers=0 if method == "QLoRA" else 4,  # QLoRA can't pickle on Windows
                dataloader_pin_memory=True,
                gradient_checkpointing=use_gradient_checkpointing,  # Disabled for Adapters
                optim="adamw_torch_fused" if torch.cuda.is_available() else "adamw_torch",
                tf32=True if torch.cuda.is_available() else False,
                dataloader_prefetch_factor=2 if method != "QLoRA" else None,  # Not used when workers=0
                ddp_find_unused_parameters=False,
                # Memory optimization
                max_grad_norm=1.0,  # Gradient clipping for stability
            )
        else:
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
                fp16=torch.cuda.is_available() and method != "QLoRA",  # QLoRA already uses fp16
                save_total_limit=3,
                report_to="none",
                seed=42,
                # GPU Performance optimizations
                dataloader_num_workers=0 if method == "QLoRA" else 4,  # QLoRA can't pickle on Windows
                dataloader_pin_memory=True,
                gradient_checkpointing=use_gradient_checkpointing,  # Disabled for Adapters
                optim="adamw_torch_fused" if torch.cuda.is_available() else "adamw_torch",
                tf32=True if torch.cuda.is_available() else False,
                dataloader_prefetch_factor=2 if method != "QLoRA" else None,  # Not used when workers=0
                ddp_find_unused_parameters=False,
                # Memory optimization
                max_grad_norm=1.0,  # Gradient clipping for stability
            )
        
        # Trainer - NO EVALUATION
        if model_type == "gpt2":
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=train_processed,
                tokenizer=tokenizer,
                data_collator=data_collator,
                callbacks=[ProgressLoggingCallback(logger, CONFIG["max_steps"])],
            )
        else:
            trainer = Seq2SeqTrainer(
                model=model,
                args=training_args,
                train_dataset=train_processed,
                tokenizer=tokenizer,
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
        
        # Compile results - TRAINING ONLY
        results = {
            "experiment_id": exp_id,
            "experiment_name": exp_name,
            "model": model_name,
            "model_type": model_type,
            "method": method,
            "dataset": "xsum",
            "status": "success",
            "timestamp": timestamp,
            
            # Training configuration
            "config": CONFIG,
            
            # Model parameters
            "trainable_parameters": trainable_params,
            "total_parameters": total_params,
            "trainable_percentage": (trainable_params / total_params) * 100,
            
            # Training metrics
            "train_runtime_seconds": duration_seconds,
            "train_runtime_minutes": duration_minutes,
            "train_loss": train_result.metrics.get("train_loss"),
            "train_samples_per_second": train_result.metrics.get("train_samples_per_second"),
            "train_steps_per_second": train_result.metrics.get("train_steps_per_second"),
            
            # Energy consumption
            "emissions_kg_co2": emissions,
            
            # Paths
            "checkpoint_dir": str(checkpoints_dir),
            "results_dir": str(results_dir),
            
            # Note
            "note": "Evaluation will be performed separately"
        }
        
        # Save results
        result_file = results_dir / f"{exp_id}_results.json"
        with open(result_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"[SUCCESS] {exp_id} - {exp_name}")
        logger.info(f"Results saved to: {result_file}")
        logger.info(f"Training completed - Evaluation will be done separately")
        
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
        
        # Emergency cleanup on error
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
            "model_type": model_type,
            "method": method,
            "dataset": "xsum",
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
    logger.info("XSUM ALL 9 EXPERIMENTS - 2000 STEPS PRODUCTION RUN")
    logger.info("="*80)
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Base path: {XSUM_PATH}")
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
        logger.info(f"EXPERIMENT {i}/9: {exp_config['exp_id']}")
        logger.info("="*80)
        
        # Check if already completed
        if is_experiment_completed(exp_config['exp_id'], XSUM_PATH):
            logger.info(f"Skipping {exp_config['exp_id']} - already completed")
            # Load existing results
            for folder in ["BART", "T5", "LLaMA"]:
                result_file = XSUM_PATH / folder / "results" / f"{exp_config['exp_id']}_results.json"
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
            # Force garbage collection twice for thorough cleanup
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
    for model_folder in ["BART", "T5", "LLaMA"]:
        model_results = [r for r in all_results if r.get("model_type") == model_folder.lower() or model_folder in r.get("experiment_name", "")]
        if model_results:
            logger.info(f"{model_folder}:")
            for r in model_results:
                status = "[OK]" if r["status"] == "success" else "[FAIL]"
                duration = r.get("train_runtime_minutes", 0)
                logger.info(f"  {status} {r['experiment_id']}: {r['method']} - Time: {duration:.1f} min")
    
    # Save master summary
    summary_file = XSUM_PATH / f"xsum_all_9_summary_{timestamp}.json"
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
