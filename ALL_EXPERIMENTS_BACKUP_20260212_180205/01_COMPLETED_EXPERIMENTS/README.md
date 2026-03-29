# COMPLETED EXPERIMENTS

## CNN/DailyMail Dataset - ALL COMPLETE ✅

All 9 experiments on CNN/DailyMail dataset are completed (100%).

### Structure

```
CNN_DailyMail/
├── BART/
│   ├── checkpoints/
│   │   ├── BART_cnn_dailymail_LoRA/
│   │   ├── BART_cnn_dailymail_QLoRA/
│   │   └── BART_cnn_dailymail_Adapters/
│   └── results/
│       ├── BART_cnn_dailymail_LoRA_results.json
│       ├── BART_cnn_dailymail_QLoRA_results.json
│       └── BART_cnn_dailymail_Adapters_results.json
├── T5/
│   ├── checkpoints/
│   └── results/
└── LLAMA/
    ├── checkpoints/
    └── results/
```

### Experiments Included

1. ✅ BART + LoRA
2. ✅ BART + QLoRA
3. ✅ BART + Adapters
4. ✅ T5 + LoRA
5. ✅ T5 + QLoRA
6. ✅ T5 + Adapters
7. ✅ LLAMA + LoRA
8. ✅ LLAMA + QLoRA
9. ✅ LLAMA + Adapters

### Results

Each experiment includes:
- Trained model checkpoints
- Results JSON with metrics (ROUGE scores, energy consumption, etc.)
- Training logs
- Configuration files

### How to Use

To load a trained model:

```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from peft import PeftModel

# Load base model
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

# Load PEFT adapter
model = PeftModel.from_pretrained(
    model, 
    "CNN_DailyMail/BART/checkpoints/BART_cnn_dailymail_LoRA/final_model"
)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")
```

---

Status: 9/9 completed (100%)
