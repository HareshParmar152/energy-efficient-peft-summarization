#!/usr/bin/env python3
"""
Evaluate All SAMSum Experiments
Evaluates all 9 SAMSum experiments (BART, T5, GPT-2 with LoRA, QLoRA, Adapters)
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
import torch
import gc
from datasets import load_from_disk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
from peft import PeftModel
from evaluate import load as load_metric
from tqdm import tqdm

# Setup logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"evaluation_samsum_all_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
BASE_PATH = Path("E:/Pending Experiment data")
DATASET_PATH = "E:/Pending Experiment data/local_datasets/samsum"

# All 9 SAMSum experiments
EXPERIMENTS = [
    {"id": "E1", "model": "facebook/bart-base", "type": "bart", "method": "LoRA", "folder": "BART"},
    {"id": "E2", "model": "facebook/bart-base", "type": "bart", "method": "QLoRA", "folder": "BART"},
    {"id": "E3", "model": "facebook/bart-base", "type": "bart", "method": "Adapters", "folder": "BART"},
    {"id": "E13", "model": "t5-base", "type": "t5", "method": "LoRA", "folder": "T5"},
    {"id": "E14", "model": "t5-base", "type": "t5", "method": "QLoRA", "folder": "T5"},
    {"id": "E15", "model": "t5-base", "type": "t5", "method": "Adapters", "folder": "T5"},
    {"id": "E25", "model": "gpt2-medium", "type": "gpt2", "method": "LoRA", "folder": "GPT2"},
    {"id": "E26", "model": "gpt2-medium", "type": "gpt2", "method": "QLoRA", "folder": "GPT2"},
    {"id": "E27", "model": "gpt2-medium", "type": "gpt2", "method": "Adapters", "folder": "GPT2"},
]


def aggressive_cleanup():
    """Aggressive GPU memory cleanup"""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
    import time
    time.sleep(2)


def load_model_and_tokenizer(base_model, model_type, checkpoint_path):
    """Load fine-tuned model and tokenizer"""
    logger.info(f"Loading model from: {checkpoint_path}")
    
    try:
        aggressive_cleanup()
        
        tokenizer = AutoTokenizer.from_pretrained(base_model)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        if model_type == "gpt2":
            base_model_obj = AutoModelForCausalLM.from_pretrained(base_model, torch_dtype=torch.float16)
        else:
            base_model_obj = AutoModelForSeq2SeqLM.from_pretrained(base_model, torch_dtype=torch.float16)
        
        model = PeftModel.from_pretrained(base_model_obj, str(checkpoint_path))
        model = model.merge_and_unload()
        
        if torch.cuda.is_available():
            model = model.to("cuda")
        
        model.eval()
        logger.info("Model loaded successfully")
        return model, tokenizer
    
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None, None


def generate_summaries(model, tokenizer, dataset, model_type, batch_size=4):
    """Generate summaries"""
    logger.info(f"Generating summaries for {len(dataset)} samples (batch_size={batch_size})...")
    
    summaries = []
    
    for i in tqdm(range(0, len(dataset), batch_size), desc="Generating"):
        batch = dataset[i:i+batch_size]
        texts = batch["dialogue"]
        
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
                        max_new_tokens=128,
                        num_beams=4,
                        early_stopping=True,
                        pad_token_id=tokenizer.pad_token_id,
                        eos_token_id=tokenizer.eos_token_id
                    )
                    generated = tokenizer.batch_decode(outputs[:, inputs['input_ids'].shape[1]:], skip_special_tokens=True)
                else:
                    outputs = model.generate(
                        **inputs,
                        max_length=128,
                        num_beams=4,
                        early_stopping=True
                    )
                    generated = tokenizer.batch_decode(outputs, skip_special_tokens=True)
            
            summaries.extend(generated)
            
            del inputs, outputs
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        
        except Exception as e:
            logger.error(f"Error generating batch {i}: {e}")
            summaries.extend([""] * len(texts))
            aggressive_cleanup()
    
    return summaries


def calculate_rouge(predictions, references):
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


def evaluate_experiment(exp_config, test_dataset):
    """Evaluate a single experiment"""
    logger.info("="*80)
    logger.info(f"Evaluating: SAMSum - {exp_config['id']} ({exp_config['method']})")
    logger.info("="*80)
    
    # Check checkpoint
    checkpoint_path = BASE_PATH / "SAMSum_Experiments" / exp_config["folder"] / "checkpoints" / f"{exp_config['id']}_{exp_config['folder']}_SAMSum_{exp_config['method']}"
    
    if not (checkpoint_path / "adapter_config.json").exists():
        logger.error(f"Checkpoint not found: {checkpoint_path}")
        return None
    
    try:
        # Load model
        model, tokenizer = load_model_and_tokenizer(
            exp_config["model"],
            exp_config["type"],
            str(checkpoint_path)
        )
        
        if model is None:
            return None
        
        # Generate summaries
        generated_summaries = generate_summaries(
            model,
            tokenizer,
            test_dataset,
            exp_config["type"],
            batch_size=4
        )
        
        # Get references
        reference_summaries = test_dataset["summary"]
        
        # Calculate ROUGE
        rouge_scores = calculate_rouge(generated_summaries, reference_summaries)
        
        if rouge_scores is None:
            return None
        
        # Save results
        results = {
            "experiment_id": exp_config["id"],
            "dataset": "SAMSum",
            "model": exp_config["model"],
            "model_type": exp_config["type"],
            "method": exp_config["method"],
            "num_samples": len(test_dataset),
            "rouge_scores": rouge_scores,
            "timestamp": timestamp
        }
        
        # Save to file
        results_dir = BASE_PATH / "SAMSum_Experiments" / "evaluation_results"
        results_dir.mkdir(exist_ok=True)
        
        results_file = results_dir / f"{exp_config['id']}_evaluation.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to: {results_file}")
        logger.info(f"ROUGE-1: {rouge_scores['rouge1']:.4f}")
        logger.info(f"ROUGE-2: {rouge_scores['rouge2']:.4f}")
        logger.info(f"ROUGE-L: {rouge_scores['rougeL']:.4f}")
        
        # Cleanup
        del model, tokenizer
        aggressive_cleanup()
        
        return results
    
    except Exception as e:
        logger.error(f"Error evaluating experiment: {e}")
        aggressive_cleanup()
        return None


def main():
    """Main evaluation function"""
    logger.info("="*80)
    logger.info("SAMSUM EVALUATION - ALL 9 EXPERIMENTS")
    logger.info("="*80)
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("")
    
    # Load test dataset
    logger.info("Loading SAMSum test dataset...")
    dataset = load_from_disk(DATASET_PATH)
    test_dataset = dataset["test"]
    logger.info(f"Loaded {len(test_dataset)} test samples")
    logger.info("")
    
    all_results = []
    
    for i, exp_config in enumerate(EXPERIMENTS, 1):
        logger.info(f"\n[{i}/9] Processing {exp_config['id']}...")
        
        result = evaluate_experiment(exp_config, test_dataset)
        
        if result:
            all_results.append(result)
        
        logger.info("")
    
    # Save master summary
    summary_file = f"evaluation_summary_samsum_{timestamp}.json"
    with open(summary_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    logger.info("="*80)
    logger.info("EVALUATION COMPLETE")
    logger.info("="*80)
    logger.info(f"Experiments evaluated: {len(all_results)}/9")
    logger.info(f"Summary saved to: {summary_file}")
    logger.info(f"Log file: {log_file}")
    logger.info("="*80)


if __name__ == "__main__":
    main()
