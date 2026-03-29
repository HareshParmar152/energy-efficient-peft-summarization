#!/usr/bin/env python3
"""
Resume Evaluation - Continue from where it left off
Skips already completed experiments
Reduces batch size to avoid OOM errors
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
import torch
import gc
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
from peft import PeftModel
from evaluate import load as load_metric
from tqdm import tqdm

# Setup logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"evaluation_resume_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Base paths
BASE_PATH = Path("E:/Pending Experiment data")

# Datasets to evaluate
DATASETS = {
    "PubMed": {
        "path": BASE_PATH / "PubMed_Experiments",
        "dataset_name": "ccdv/pubmed-summarization",
        "text_column": "article",
        "summary_column": "abstract",
        "split": "test",
        "max_samples": 1000,
        "experiments": ["E1", "E2", "E3", "E13", "E14", "E15", "E25", "E27", "E29"]
    },
    "XSum": {
        "path": BASE_PATH / "XSum_Experiments",
        "dataset_name": "EdinburghNLP/xsum",
        "text_column": "document",
        "summary_column": "summary",
        "split": "test",
        "max_samples": 1000,
        "experiments": ["E1", "E2", "E3", "E13", "E14", "E15", "E25", "E27"]
    },
    "SAMSum": {
        "path": BASE_PATH / "SAMSum_Experiments",
        "dataset_name": "local",  # Use local dataset
        "dataset_path": "E:/Pending Experiment data/local_datasets/samsum",
        "text_column": "dialogue",
        "summary_column": "summary",
        "split": "test",
        "max_samples": 818,
        "experiments": ["E1", "E2", "E3", "E13", "E14", "E15", "E25", "E26", "E27"]
    },
    "BillSum": {
        "path": BASE_PATH / "BillSum_Experiments",
        "dataset_name": "local",  # Use local dataset
        "dataset_path": "E:/Pending Experiment data/local_datasets/billsum",
        "text_column": "text",
        "summary_column": "summary",
        "split": "test",
        "max_samples": 1000,
        "experiments": ["E1", "E3", "E13", "E15"]
    }
}

# Experiment configurations
EXPERIMENT_CONFIGS = {
    "E1": {"model": "facebook/bart-base", "model_type": "bart", "method": "LoRA", "folder": "BART"},
    "E2": {"model": "facebook/bart-base", "model_type": "bart", "method": "QLoRA", "folder": "BART"},
    "E3": {"model": "facebook/bart-base", "model_type": "bart", "method": "Adapters", "folder": "BART"},
    "E13": {"model": "t5-base", "model_type": "t5", "method": "LoRA", "folder": "T5"},
    "E14": {"model": "t5-base", "model_type": "t5", "method": "QLoRA", "folder": "T5"},
    "E15": {"model": "t5-base", "model_type": "t5", "method": "Adapters", "folder": "T5"},
    "E25": {"model": "gpt2-medium", "model_type": "gpt2", "method": "LoRA", "folder": "GPT2"},
    "E26": {"model": "gpt2-medium", "model_type": "gpt2", "method": "QLoRA", "folder": "GPT2"},
    "E27": {"model": "gpt2-medium", "model_type": "gpt2", "method": "Adapters", "folder": "GPT2"},
    "E29": {"model": "gpt2-medium", "model_type": "gpt2", "method": "QLoRA", "folder": "GPT2"},
}


def is_already_evaluated(dataset_path, exp_id):
    """Check if experiment already has results"""
    results_file = dataset_path / "evaluation_results" / f"{exp_id}_evaluation.json"
    if results_file.exists():
        try:
            with open(results_file, 'r') as f:
                data = json.load(f)
                # Check if ROUGE scores are valid (not 0.0)
                if data.get("rouge_scores", {}).get("rouge1", 0) > 0.01:
                    return True
        except:
            pass
    return False


def aggressive_memory_cleanup():
    """Aggressive GPU memory cleanup"""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
    import time
    time.sleep(2)


def load_test_dataset(dataset_name, text_column, summary_column, split, max_samples, dataset_path=None):
    """Load test dataset"""
    logger.info(f"Loading dataset: {dataset_name}")
    
    try:
        if dataset_name == "local":
            # Load from local disk
            from datasets import load_from_disk
            dataset = load_from_disk(dataset_path)[split]
        elif dataset_name == "ccdv/pubmed-summarization":
            dataset = load_dataset(dataset_name, "document", split=split)
        else:
            dataset = load_dataset(dataset_name, split=split)
        
        if len(dataset) > max_samples:
            dataset = dataset.select(range(max_samples))
        
        logger.info(f"Loaded {len(dataset)} samples")
        return dataset
    
    except Exception as e:
        logger.error(f"Error loading dataset {dataset_name}: {e}")
        return None


def load_model_and_tokenizer(base_model, model_type, checkpoint_path):
    """Load fine-tuned model and tokenizer"""
    logger.info(f"Loading model from: {checkpoint_path}")
    
    try:
        aggressive_memory_cleanup()
        
        tokenizer = AutoTokenizer.from_pretrained(base_model)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        if model_type == "gpt2":
            base_model_obj = AutoModelForCausalLM.from_pretrained(base_model, torch_dtype=torch.float16)
        else:
            base_model_obj = AutoModelForSeq2SeqLM.from_pretrained(base_model, torch_dtype=torch.float16)
        
        model = PeftModel.from_pretrained(base_model_obj, checkpoint_path)
        model = model.merge_and_unload()
        
        if torch.cuda.is_available():
            model = model.to("cuda")
        
        model.eval()
        logger.info("Model loaded successfully")
        return model, tokenizer
    
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None, None


def generate_summaries(model, tokenizer, dataset, text_column, model_type, max_length=128, batch_size=4):
    """Generate summaries - REDUCED batch size to 4"""
    logger.info(f"Generating summaries for {len(dataset)} samples (batch_size={batch_size})...")
    
    summaries = []
    
    for i in tqdm(range(0, len(dataset), batch_size), desc="Generating"):
        batch = dataset[i:i+batch_size]
        texts = batch[text_column]
        
        try:
            if model_type == "gpt2":
                prompts = [f"Summarize: {text[:512]}\n\nSummary:" for text in texts]
                inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=512)
            else:
                inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
            
            if torch.cuda.is_available():
                inputs = {k: v.to("cuda") for k, v in inputs.items()}
            
            with torch.no_grad():
                if model_type == "gpt2":
                    outputs = model.generate(
                        **inputs,
                        max_new_tokens=max_length,
                        num_beams=4,
                        early_stopping=True,
                        pad_token_id=tokenizer.pad_token_id,
                        eos_token_id=tokenizer.eos_token_id
                    )
                    generated = tokenizer.batch_decode(outputs[:, inputs['input_ids'].shape[1]:], skip_special_tokens=True)
                else:
                    outputs = model.generate(
                        **inputs,
                        max_length=max_length,
                        num_beams=4,
                        early_stopping=True
                    )
                    generated = tokenizer.batch_decode(outputs, skip_special_tokens=True)
            
            summaries.extend(generated)
            
            # Cleanup after each batch
            del inputs, outputs
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        
        except Exception as e:
            logger.error(f"Error generating batch {i}: {e}")
            summaries.extend([""] * len(texts))
            aggressive_memory_cleanup()
    
    return summaries


def calculate_rouge_scores(predictions, references):
    """Calculate ROUGE scores"""
    logger.info("Calculating ROUGE scores...")
    
    try:
        rouge = load_metric("rouge")
        results = rouge.compute(predictions=predictions, references=references)
        
        return {
            "rouge1": results["rouge1"],
            "rouge2": results["rouge2"],
            "rougeL": results["rougeL"],
            "rougeLsum": results["rougeLsum"]
        }
    
    except Exception as e:
        logger.error(f"Error calculating ROUGE: {e}")
        return None


def evaluate_experiment(dataset_name, dataset_config, exp_id, exp_config):
    """Evaluate a single experiment"""
    logger.info("="*80)
    logger.info(f"Evaluating: {dataset_name} - {exp_id} ({exp_config['method']})")
    logger.info("="*80)
    
    # Check if already evaluated
    if is_already_evaluated(dataset_config["path"], exp_id):
        logger.info(f"✓ Already evaluated - skipping")
        return "skipped"
    
    # Check if checkpoint exists - try final_model subdirectory first, then base folder
    checkpoint_base = dataset_config["path"] / exp_config["folder"] / "checkpoints" / f"{exp_id}_{exp_config['folder']}_{dataset_name}_{exp_config['method']}"
    checkpoint_path = checkpoint_base / "final_model"
    
    # If final_model doesn't exist, try the base folder (SAMSum/BillSum structure)
    if not checkpoint_path.exists():
        if (checkpoint_base / "adapter_config.json").exists():
            checkpoint_path = checkpoint_base
            logger.info(f"Using checkpoint from base folder: {checkpoint_path}")
        else:
            logger.warning(f"Checkpoint not found in either location: {checkpoint_path}")
            return None
    
    try:
        # Load test dataset
        test_dataset = load_test_dataset(
            dataset_config["dataset_name"],
            dataset_config["text_column"],
            dataset_config["summary_column"],
            dataset_config["split"],
            dataset_config["max_samples"],
            dataset_config.get("dataset_path")
        )
        
        if test_dataset is None:
            return None
        
        # Load model
        model, tokenizer = load_model_and_tokenizer(
            exp_config["model"],
            exp_config["model_type"],
            str(checkpoint_path)
        )
        
        if model is None:
            return None
        
        # Generate summaries
        generated_summaries = generate_summaries(
            model,
            tokenizer,
            test_dataset,
            dataset_config["text_column"],
            exp_config["model_type"],
            batch_size=4  # Reduced from 8
        )
        
        # Get reference summaries
        reference_summaries = test_dataset[dataset_config["summary_column"]]
        
        # Calculate ROUGE scores
        rouge_scores = calculate_rouge_scores(generated_summaries, reference_summaries)
        
        if rouge_scores is None:
            return None
        
        # Save results
        results = {
            "experiment_id": exp_id,
            "dataset": dataset_name,
            "model": exp_config["model"],
            "model_type": exp_config["model_type"],
            "method": exp_config["method"],
            "num_samples": len(test_dataset),
            "rouge_scores": rouge_scores,
            "timestamp": timestamp
        }
        
        # Save to file
        results_dir = dataset_config["path"] / "evaluation_results"
        results_dir.mkdir(exist_ok=True)
        
        results_file = results_dir / f"{exp_id}_evaluation.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to: {results_file}")
        logger.info(f"ROUGE-1: {rouge_scores['rouge1']:.4f}")
        logger.info(f"ROUGE-2: {rouge_scores['rouge2']:.4f}")
        logger.info(f"ROUGE-L: {rouge_scores['rougeL']:.4f}")
        
        # Cleanup
        del model, tokenizer
        aggressive_memory_cleanup()
        
        return results
    
    except Exception as e:
        logger.error(f"Error evaluating experiment: {e}")
        aggressive_memory_cleanup()
        return None


def main():
    """Main evaluation function"""
    logger.info("="*80)
    logger.info("RESUME EVALUATION - Continue from where it left off")
    logger.info("="*80)
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("")
    
    all_results = []
    skipped_count = 0
    
    for dataset_name, dataset_config in DATASETS.items():
        logger.info("")
        logger.info(f"Processing dataset: {dataset_name}")
        logger.info(f"Experiments to check: {len(dataset_config['experiments'])}")
        logger.info("")
        
        for exp_id in dataset_config["experiments"]:
            if exp_id not in EXPERIMENT_CONFIGS:
                logger.warning(f"Unknown experiment ID: {exp_id}")
                continue
            
            exp_config = EXPERIMENT_CONFIGS[exp_id]
            
            result = evaluate_experiment(dataset_name, dataset_config, exp_id, exp_config)
            
            if result == "skipped":
                skipped_count += 1
            elif result:
                all_results.append(result)
            
            logger.info("")
    
    # Save master summary
    summary_file = f"evaluation_summary_resume_{timestamp}.json"
    with open(summary_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    logger.info("="*80)
    logger.info("EVALUATION COMPLETE")
    logger.info("="*80)
    logger.info(f"Experiments evaluated: {len(all_results)}")
    logger.info(f"Experiments skipped (already done): {skipped_count}")
    logger.info(f"Summary saved to: {summary_file}")
    logger.info(f"Log file: {log_file}")
    logger.info("="*80)


if __name__ == "__main__":
    main()
