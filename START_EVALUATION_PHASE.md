# Start Evaluation Phase

## Training Complete! Now Evaluate Models 📊

All 26 experiments are trained. Now you need to evaluate them to get ROUGE scores.

## What You Need to Do

### 1. Create Evaluation Script

Create a script that:
- Loads each trained checkpoint
- Generates summaries on test set
- Calculates ROUGE scores
- Saves results

### 2. Evaluation Script Template

```python
# evaluate_all_experiments.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
from datasets import load_dataset
from peft import PeftModel
import torch
from rouge_score import rouge_scorer
import json
from pathlib import Path

def evaluate_experiment(checkpoint_dir, dataset_name, model_type):
    """Evaluate a single experiment"""
    
    # Load tokenizer and base model
    if model_type == "gpt2":
        base_model = AutoModelForCausalLM.from_pretrained("gpt2-medium")
    elif model_type == "bart":
        base_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")
    elif model_type == "t5":
        base_model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
    
    # Load PEFT adapter
    model = PeftModel.from_pretrained(base_model, checkpoint_dir)
    model.eval()
    
    tokenizer = AutoTokenizer.from_pretrained(checkpoint_dir)
    
    # Load test dataset
    if dataset_name == "cnn_dailymail":
        dataset = load_dataset("cnn_dailymail", "3.0.0", split="test[:1000]")
    elif dataset_name == "pubmed":
        dataset = load_dataset("scientific_papers", "pubmed", split="test[:1000]")
    elif dataset_name == "xsum":
        dataset = load_dataset("xsum", split="test[:1000]")
    
    # Generate summaries
    predictions = []
    references = []
    
    for example in dataset:
        # Tokenize input
        inputs = tokenizer(example["article"], max_length=512, truncation=True, return_tensors="pt")
        
        # Generate summary
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=128)
        
        # Decode
        pred = tokenizer.decode(outputs[0], skip_special_tokens=True)
        predictions.append(pred)
        references.append(example["highlights"])
    
    # Calculate ROUGE scores
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
    rouge1_scores = []
    rouge2_scores = []
    rougeL_scores = []
    
    for pred, ref in zip(predictions, references):
        scores = scorer.score(ref, pred)
        rouge1_scores.append(scores['rouge1'].fmeasure)
        rouge2_scores.append(scores['rouge2'].fmeasure)
        rougeL_scores.append(scores['rougeL'].fmeasure)
    
    # Average scores
    results = {
        "rouge1": sum(rouge1_scores) / len(rouge1_scores),
        "rouge2": sum(rouge2_scores) / len(rouge2_scores),
        "rougeL": sum(rougeL_scores) / len(rougeL_scores),
    }
    
    return results

# Evaluate all experiments
experiments = [
    # PubMed
    {"checkpoint": "E:/Pending Experiment data/PubMed_Experiments/BART/checkpoints/E1_BART_PubMed_LoRA", "dataset": "pubmed", "model": "bart"},
    # ... add all 26 experiments
]

for exp in experiments:
    results = evaluate_experiment(exp["checkpoint"], exp["dataset"], exp["model"])
    print(f"{exp['checkpoint']}: {results}")
```

### 3. Required Packages

Install if needed:
```cmd
pip install rouge-score
pip install nltk
```

### 4. Evaluation Strategy

#### Quick Evaluation (Recommended First):
- Use test[:1000] (1000 samples)
- Faster, good for initial comparison
- Takes ~2-3 hours per experiment

#### Full Evaluation:
- Use entire test set
- More accurate
- Takes ~8-10 hours per experiment

### 5. What to Evaluate

For each of 26 experiments, calculate:
- ROUGE-1 (unigram overlap)
- ROUGE-2 (bigram overlap)
- ROUGE-L (longest common subsequence)
- Optional: BLEU, METEOR

### 6. Expected Output

Create a comparison table:

```
| Dataset | Model | Method | ROUGE-1 | ROUGE-2 | ROUGE-L | Training Time | CO2 |
|---------|-------|--------|---------|---------|---------|---------------|-----|
| PubMed  | BART  | LoRA   | 0.45    | 0.23    | 0.41    | 86.2 min      | ... |
| PubMed  | BART  | QLoRA  | 0.44    | 0.22    | 0.40    | 131.9 min     | ... |
| ...     | ...   | ...    | ...     | ...     | ...     | ...           | ... |
```

---

## Alternative: Do You Have Evaluation Scripts?

If you already have evaluation scripts from your research setup, you can:
1. Point them to the checkpoint directories
2. Run evaluation on all 26 experiments
3. Collect ROUGE scores

---

## Questions to Answer

1. Do you have existing evaluation scripts?
2. Do you want me to create a complete evaluation script?
3. Should we start with quick evaluation (1000 samples) or full evaluation?
4. What metrics do you need? (ROUGE, BLEU, METEOR, etc.)

---

## Next Action

Let me know:
- "Create evaluation script" - I'll build a complete evaluation pipeline
- "I have scripts" - Tell me where they are and I'll help adapt them
- "Skip evaluation" - If you want to do something else first

---

Generated: 26-Feb-2026 21:55
