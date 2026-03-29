#!/usr/bin/env python3
"""
Evaluate BillSum E25 (GPT-2 LoRA) and E27 (GPT-2 Adapters)
Generates ROUGE scores for both experiments
"""

import os
import json
from pathlib import Path
from datetime import datetime

import torch
from datasets import load_from_disk
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import evaluate

print("="*80)
print("EVALUATION: BillSum E25 & E27")
print("="*80)

# Load ROUGE metric
rouge = evaluate.load('rouge')

# Base paths
BASE_PATH = Path("E:/Pending Experiment data/BillSum_Experiments")
results_dir = BASE_PATH / "GPT2" / "results"

# Load dataset
print("\n1. Loading BillSum test dataset...")
dataset = load_from_disk("E:/Pending Experiment data/local_datasets/billsum")
test_dataset = dataset["test"].select(range(100))  # Use 100 samples for evaluation
print(f"   Test samples: {len(test_dataset)}")

# Experiments to evaluate
experiments = [
    {
        "id": "E25",
        "name": "E25_LoRA",
        "checkpoint": BASE_PATH / "GPT2" / "checkpoints" / "E25_LoRA",
        "method": "LoRA"
    },
    {
        "id": "E27",
        "name": "E27_Adapters",
        "checkpoint": BASE_PATH / "GPT2" / "checkpoints" / "E27_Adapters",
        "method": "Adapters"
    }
]

for exp in experiments:
    print("\n" + "="*80)
    print(f"EVALUATING: {exp['id']} ({exp['method']})")
    print("="*80)
    
    try:
        # Load tokenizer
        print(f"\n2. Loading tokenizer from {exp['checkpoint']}...")
        tokenizer = AutoTokenizer.from_pretrained(exp['checkpoint'])
        tokenizer.pad_token = tokenizer.eos_token
        
        # Load base model
        print(f"\n3. Loading base model...")
        base_model = AutoModelForCausalLM.from_pretrained(
            "gpt2-medium",
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        # Load PEFT model
        print(f"\n4. Loading PEFT adapter...")
        model = PeftModel.from_pretrained(base_model, exp['checkpoint'])
        model.eval()
        
        # Generate summaries
        print(f"\n5. Generating summaries for {len(test_dataset)} samples...")
        predictions = []
        references = []
        
        for i, example in enumerate(test_dataset):
            if i % 10 == 0:
                print(f"   Progress: {i}/{len(test_dataset)}")
            
            # Prepare input
            input_text = f"Summarize: {example['text'][:512]}\n\nSummary:"
            inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)
            inputs = {k: v.to(model.device) for k, v in inputs.items()}
            
            # Generate
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=128,
                    num_beams=4,
                    early_stopping=True,
                    no_repeat_ngram_size=3
                )
            
            # Decode
            generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract only the summary part (after "Summary:")
            if "Summary:" in generated:
                generated = generated.split("Summary:")[-1].strip()
            
            predictions.append(generated)
            references.append(example['summary'])
        
        # Calculate ROUGE scores
        print(f"\n6. Calculating ROUGE scores...")
        results = rouge.compute(
            predictions=predictions,
            references=references,
            use_stemmer=True
        )
        
        # Print results
        print(f"\n7. Results for {exp['id']}:")
        print(f"   ROUGE-1: {results['rouge1']:.4f}")
        print(f"   ROUGE-2: {results['rouge2']:.4f}")
        print(f"   ROUGE-L: {results['rougeL']:.4f}")
        
        # Save evaluation results
        eval_results = {
            "experiment_id": exp['id'],
            "experiment_name": exp['name'],
            "method": exp['method'],
            "dataset": "billsum",
            "test_samples": len(test_dataset),
            "rouge1": float(results['rouge1']),
            "rouge2": float(results['rouge2']),
            "rougeL": float(results['rougeL']),
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        
        eval_file = results_dir / f"{exp['id']}_evaluation.json"
        with open(eval_file, 'w') as f:
            json.dump(eval_results, f, indent=2)
        
        print(f"\n   Evaluation saved to: {eval_file}")
        
        # Cleanup
        del model
        del base_model
        torch.cuda.empty_cache()
        
        print(f"\n✅ {exp['id']} EVALUATION COMPLETE!")
        
    except Exception as e:
        print(f"\n❌ {exp['id']} EVALUATION FAILED!")
        print(f"   Error: {e}")
        continue

print("\n" + "="*80)
print("ALL EVALUATIONS COMPLETE!")
print("="*80)
print("\nResults saved to:")
print(f"  - {results_dir}/E25_evaluation.json")
print(f"  - {results_dir}/E27_evaluation.json")
print("="*80)
