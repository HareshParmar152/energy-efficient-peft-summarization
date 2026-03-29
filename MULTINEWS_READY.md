# Multi-News Experiments Ready to Run! 🚀

## Dataset 4: Multi-News

**Dataset:** Multi-News  
**Type:** Multi-document summarization  
**Characteristics:** Summaries created from multiple news articles, requires cross-document reasoning

---

## Script Created

**File:** `run_multinews_all_9_experiments_2000steps.py`

### Features:
✅ All optimizations from previous datasets applied  
✅ Aggressive GPU memory cleanup between experiments  
✅ QLoRA gradient fixes included  
✅ Caching enabled for fast preprocessing  
✅ Auto-skip completed experiments  
✅ Energy tracking with CodeCarbon  
✅ Windows-compatible (num_proc=1)  
✅ **Optimized for long documents** (1024 source tokens, 256 target tokens)

---

## Experiments to Run

### 9 Experiments Total:

#### BART (E1-E3):
- E1: BART + LoRA
- E2: BART + QLoRA
- E3: BART + Adapters

#### T5 (E13-E15):
- E13: T5 + LoRA
- E14: T5 + QLoRA
- E15: T5 + Adapters

#### GPT-2 (E25-E27):
- E25: GPT-2 + LoRA
- E26: GPT-2 + QLoRA
- E27: GPT-2 + Adapters

---

## Configuration

### Dataset Settings:
- **Source:** `multi_news` from Hugging Face
- **Fields:** `document` (multiple articles) → `summary`
- **Max source length:** 1024 tokens (longer for multi-document)
- **Max target length:** 256 tokens (longer summaries)

### Training Settings:
- **Steps:** 2000
- **Base batch size:** 4 (Multi-News has very long documents)
- **Gradient accumulation:** 4
- **Learning rate:** 3e-4

### Memory Protection (Extra Conservative):
- **QLoRA:** batch_size=2, gradient_accumulation=8
- **Adapters (GPT-2):** batch_size=1, gradient_accumulation=16 (minimal!)
- **Adapters (BART/T5):** batch_size=3, gradient_accumulation=5
- **LoRA:** batch_size=4, gradient_accumulation=4

---

## How to Run

### Option 1: Use Batch File (Recommended)
```cmd
RUN_MULTINEWS_EXPERIMENTS.bat
```

### Option 2: Manual Command
```cmd
deactivate
python run_multinews_all_9_experiments_2000steps.py
```

---

## Expected Timeline

### Estimated Time per Experiment:
Multi-News has longer documents, so training will be slower:

- **BART LoRA:** ~6-8 hours
- **BART QLoRA:** ~10-12 hours
- **BART Adapters:** ~7-9 hours
- **T5 LoRA:** ~12-15 hours
- **T5 QLoRA:** ~15-18 hours
- **T5 Adapters:** ~15-18 hours
- **GPT-2 LoRA:** ~10-12 hours
- **GPT-2 QLoRA:** ~12-15 hours
- **GPT-2 Adapters:** ~15-20 hours

### Total Time: ~70-90 hours (3-4 days)

---

## Output Locations

### Results:
- `E:\Pending Experiment data\MultiNews_Experiments\BART\results\`
- `E:\Pending Experiment data\MultiNews_Experiments\T5\results\`
- `E:\Pending Experiment data\MultiNews_Experiments\GPT2\results\`

### Checkpoints:
- `E:\Pending Experiment data\MultiNews_Experiments\{MODEL}\checkpoints\`

### Logs:
- `E:\Pending Experiment data\MultiNews_Experiments\logs\`

### Cache:
- `E:\Pending Experiment data\MultiNews_Experiments\cache\`

---

## What Makes Multi-News Special

### Multi-Document Summarization:
- **Input:** Multiple news articles about the same event
- **Output:** Single coherent summary
- **Challenge:** Cross-document reasoning and information fusion

### Why This Dataset Matters:
- Tests model's ability to synthesize information from multiple sources
- Requires understanding relationships between documents
- More complex than single-document summarization
- Important for real-world applications (news aggregation, research synthesis)

---

## After Completion

Once Multi-News is done, you'll have:
- **4/4 datasets complete** (CNN/DailyMail, PubMed, XSum, Multi-News)
- **35/36 experiments complete** (97%)
- **Ready for evaluation phase!**

Note: Newsroom is optional 5th dataset if you want 100% completion.

---

## Monitoring Progress

### Check logs in real-time:
```cmd
type "E:\Pending Experiment data\MultiNews_Experiments\logs\multinews_all_experiments_*.log"
```

### Check completed experiments:
```cmd
dir "E:\Pending Experiment data\MultiNews_Experiments\*\results\*.json"
```

---

## Memory Considerations

Multi-News has the longest documents of all datasets:
- **1024 source tokens** (vs 512 for others)
- **256 target tokens** (vs 128 for others)
- **Batch sizes are extra conservative** to prevent OOM
- **GPT-2 Adapters uses batch_size=1** (absolute minimum)

If you encounter OOM errors, the script is already at minimum settings. You may need to:
1. Restart computer before running
2. Close all other applications
3. Run experiments individually

---

## Troubleshooting

### If dataset download fails:
```python
# Manually download first:
from datasets import load_dataset
dataset = load_dataset("multi_news")
```

### If OOM persists:
The script already uses minimal batch sizes. If issues continue:
- Reduce max_source_length from 1024 to 768
- Skip GPT-2 Adapters (E27) which is most memory-intensive

---

Generated: 26-Feb-2026 22:30
Status: READY TO RUN - MULTI-NEWS EXPERIMENTS
