# T5 - CNN/DailyMail Experiments

## Completed Experiments

All 3 PEFT methods tested on CNN/DailyMail dataset:

1. **LoRA** (Low-Rank Adaptation)
   - Checkpoint: `checkpoints/T5_cnn_dailymail_LoRA/`
   - Results: `results/T5_cnn_dailymail_LoRA_results.json`

2. **QLoRA** (Quantized LoRA)
   - Checkpoint: `checkpoints/T5_cnn_dailymail_QLoRA/`
   - Results: `results/T5_cnn_dailymail_QLoRA_results.json`

3. **Adapters**
   - Checkpoint: `checkpoints/T5_cnn_dailymail_Adapters/`
   - Results: `results/T5_cnn_dailymail_Adapters_results.json`

## Folder Structure

```
T5/
├── checkpoints/          # Trained model checkpoints
│   ├── T5_cnn_dailymail_LoRA/
│   ├── T5_cnn_dailymail_QLoRA/
│   └── T5_cnn_dailymail_Adapters/
└── results/              # Experiment results (JSON)
    ├── T5_cnn_dailymail_LoRA_results.json
    ├── T5_cnn_dailymail_QLoRA_results.json
    └── T5_cnn_dailymail_Adapters_results.json
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
model = PeftModel.from_pretrained(model, "checkpoints/T5_cnn_dailymail_LoRA/final_model")

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
