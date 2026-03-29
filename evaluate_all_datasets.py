#!/usr/bin/env python3
"""
Evaluation Script for All Datasets (Excluding CNN/DailyMail)
Generates summaries and calculates ROUGE scores for:
- PubMed (9 experiments)
- XSum (8 experiments)
- SAMSum (9 experiments)
- BillSum (4 experiments)
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
from peft import PeftModel
from evaluate import load as load_metric
from tqdm import tqdm

# Setup logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"evaluation_all_{timestamp}.log"

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

# Datasets to evaluate (excluding CNN/DailyMail)
DATASETS = {
    "PubMed": {
        "path": BASE_PATH / "PubMed_Experiments",
        "dataset_name": "ccdv/pubmed-summarization",
        "text_column": "article",
        "summary_column": "abstract",
        "split": "test",
        "max_samples": 1000,
        "experiments": ["E1", "E2", "E3", "E13", "E14", "E15", "E25", "E27", "E29"]  # E29 is working QLoRA
    },
    "XSum": {
        "path": BASE_PATH / "XSum_Experiments",
        "dataset_name": "EdinburghNLP/xsum",
        "text_column": "document",
        "summary_column": "summary",
        "split": "test",
        "max_samples": 1000,
        "experiments": ["E1", "E2", "E3", "E13", "E14", "E15", "E25", "E27"]  # E26 failed
    },
    "SAMSum": {
        "path": BASE_PATH / "SAMSum_Experiments",
        "dataset_name": "samsum",  # Fixed: was Samsung/samsum
        "text_column": "dialogue",
        "summary_column": "summary",
        "split": "test",
        "max_samples": 818,  # Full test set
        "experiments": ["E1", "E2", "E3", "E13", "E14", "E15", "E25", "E26", "E27"]
    },
    "BillSum": {
        "path": BASE_PATH / "BillSum_Experiments",
        "dataset_name": "billsum",
        "text_column": "text",
        "summary_column": "summary",
        "split": "test",
        "max_samples": 1000,
        "experiments": ["E1", "E3", "E13", "E15"]  # Only completed experiments
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
    "E29": {"model": "gpt2-medium", "model_type": "gpt2", "method": "QLoRA", "folder": "GPT2"},  # PubMed QLoRA
}


def load_test_dataset(dataset_name, text_column, summary_column, split, max_samples):
    """Load test dataset"""
    logger.info(f"Loading dataset: {dataset_name}")
    
    try:
        if dataset_name == "ccdv/pubmed-summarization":
            dataset = load_dataset(dataset_name, "document", split=split)
        else:
            dataset = load_dataset(dataset_name, split=split)
        
        # Limit samples
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
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(base_model)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Load base model
        if model_type == "gpt2":
            base_model_obj = AutoModelForCausalLM.from_pretrained(base_model)
        else:
            base_model_obj = AutoModelForSeq2SeqLM.from_pretrained(base_model)
        
        # Load PEFT adapter
        model = PeftModel.from_pretrained(base_model_obj, checkpoint_path)
        model = model.merge_and_unload()  # Merge adapter weights
        
        if torch.cuda.is_available():
            model = model.to("cuda")
        
        model.eval()
        logger.info("Model loaded successfully")
        return model, tokenizer
    
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None, None


def generate_summaries(model, tokenizer, dataset, text_column, model_type, max_length=128, batch_size=8):
    """Generate summaries for test dataset"""
    logger.info(f"Generating summaries for {len(dataset)} samples...")
    
    summaries = []
    
    for i in tqdm(range(0, len(dataset), batch_size), desc="Generating"):
        batch = dataset[i:i+batch_size]
        texts = batch[text_column]
        
        try:
            if model_type == "gpt2":
                # For GPT-2, use prompt format
                prompts = [f"Summarize: {text}\n\nSummary:" for text in texts]
                inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=512)
            else:
                # For BART/T5
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
                    # Decode only the generated part (after prompt)
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
        
        except Exception as e:
            logger.error(f"Error generating batch {i}: {e}")
            summaries.extend([""] * len(texts))
    
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
    
    # Check if checkpoint exists - look in final_model subdirectory
    checkpoint_base = dataset_config["path"] / exp_config["folder"] / "checkpoints" / f"{exp_id}_{exp_config['folder']}_{dataset_name}_{exp_config['method']}"
    checkpoint_path = checkpoint_base / "final_model"
    
    if not checkpoint_path.exists():
        logger.warning(f"Checkpoint not found: {checkpoint_path}")
        return None
    
    # Load test dataset
    test_dataset = load_test_dataset(
        dataset_config["dataset_name"],
        dataset_config["text_column"],
        dataset_config["summary_column"],
        dataset_config["split"],
        dataset_config["max_samples"]
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
        exp_config["model_type"]
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
    del model
    del tokenizer
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    return results


def main():
    """Main evaluation function"""
    logger.info("="*80)
    logger.info("EVALUATION - ALL DATASETS (Excluding CNN/DailyMail)")
    logger.info("="*80)
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("")
    
    all_results = []
    
    for dataset_name, dataset_config in DATASETS.items():
        logger.info("")
        logger.info(f"Processing dataset: {dataset_name}")
        logger.info(f"Experiments to evaluate: {len(dataset_config['experiments'])}")
        logger.info("")
        
        for exp_id in dataset_config["experiments"]:
            if exp_id not in EXPERIMENT_CONFIGS:
                logger.warning(f"Unknown experiment ID: {exp_id}")
                continue
            
            exp_config = EXPERIMENT_CONFIGS[exp_id]
            
            result = evaluate_experiment(dataset_name, dataset_config, exp_id, exp_config)
            
            if result:
                all_results.append(result)
            
            logger.info("")
    
    # Save master summary
    summary_file = f"evaluation_summary_all_{timestamp}.json"
    with open(summary_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    logger.info("="*80)
    logger.info("EVALUATION COMPLETE")
    logger.info("="*80)
    logger.info(f"Total experiments evaluated: {len(all_results)}")
    logger.info(f"Summary saved to: {summary_file}")
    logger.info(f"Log file: {log_file}")
    logger.info("="*80)


if __name__ == "__main__":
    main()
