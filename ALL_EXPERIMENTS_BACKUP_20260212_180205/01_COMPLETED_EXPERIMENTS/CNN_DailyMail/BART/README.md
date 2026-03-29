# BART - CNN/DailyMail Experiments

## Completed Experiments

All 3 PEFT methods tested on CNN/DailyMail dataset:

1. **LoRA** (Low-Rank Adaptation)
   - Checkpoint: `checkpoints/BART_cnn_dailymail_LoRA/`
   - Results: `results/BART_cnn_dailymail_LoRA_results.json`

2. **QLoRA** (Quantized LoRA)
   - Checkpoint: `checkpoints/BART_cnn_dailymail_QLoRA/`
   - Results: `results/BART_cnn_dailymail_QLoRA_results.json`

3. **Adapters**
   - Checkpoint: `checkpoints/BART_cnn_dailymail_Adapters/`
   - Results: `results/BART_cnn_dailymail_Adapters_results.json`

## Folder Structure

```
BART/
├── checkpoints/          # Trained model checkpoints
│   ├── BART_cnn_dailymail_LoRA/
│   ├── BART_cnn_dailymail_QLoRA/
│   └── BART_cnn_dailymail_Adapters/
└── results/              # Experiment results (JSON)
    ├── BART_cnn_dailymail_LoRA_results.json
    ├── BART_cnn_dailymail_QLoRA_results.json
    └── BART_cnn_dailymail_Adapters_results.json
```

## Results Summary

Check the JSON files in `results/` folder for:
- ROUGE scores (rouge1, rouge2, rougeL)
- Energy consumption
- Training duration
- Model parameters
- System information

## Usage

To load a trained model:

```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from peft import PeftModel

# Load base model
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")  # or t5-base, TinyLlama

# Load PEFT adapter
model = PeftModel.from_pretrained(model, "checkpoints/BART_cnn_dailymail_LoRA/final_model")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")

# Use for inference
text = "Your article text here..."
inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
outputs = model.generate(**inputs, max_length=128)
summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

## Status

✅ All experiments completed
✅ Models saved
✅ Results recorded
