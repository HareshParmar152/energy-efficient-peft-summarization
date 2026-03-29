# Reddit TIFU Experiments Ready to Run! 🚀

## Dataset 4: Reddit TIFU

**Dataset:** Reddit TIFU ("Today I F***ed Up")  
**Type:** Informal user narratives with TL;DR summaries  
**Characteristics:** Conversational language, slang, noisy structure

---

## Script Created

**File:** `run_reddit_tifu_all_9_experiments_2000steps.py`

### Features:
✅ All optimizations from PubMed/XSum applied  
✅ Aggressive GPU memory cleanup between experiments  
✅ QLoRA gradient fixes included  
✅ Caching enabled for fast preprocessing  
✅ Auto-skip completed experiments  
✅ Energy tracking with CodeCarbon  
✅ Windows-compatible (num_proc=1)

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
- **Source:** `reddit_tifu` (long version)
- **Fields:** `documents` (post) → `tldr` (summary)
- **Max source length:** 512 tokens
- **Max target length:** 128 tokens

### Training Settings:
- **Steps:** 2000
- **Base batch size:** 8 (Reddit posts are shorter than PubMed)
- **Gradient accumulation:** 2
- **Learning rate:** 3e-4

### Memory Protection:
- **QLoRA:** batch_size=4, gradient_accumulation=4
- **Adapters (GPT-2):** batch_size=2, gradient_accumulation=8
- **Adapters (BART/T5):** batch_size=6, gradient_accumulation=3

---

## How to Run

### Option 1: Use Batch File (Recommended)
```cmd
RUN_REDDIT_TIFU_EXPERIMENTS.bat
```

### Option 2: Manual Command
```cmd
deactivate
python run_reddit_tifu_all_9_experiments_2000steps.py
```

---

## Expected Timeline

### Estimated Time per Experiment:
- **BART LoRA:** ~4-5 hours
- **BART QLoRA:** ~8-10 hours
- **BART Adapters:** ~5-6 hours
- **T5 LoRA:** ~10-12 hours
- **T5 QLoRA:** ~12-15 hours
- **T5 Adapters:** ~12-15 hours
- **GPT-2 LoRA:** ~8-10 hours
- **GPT-2 QLoRA:** ~10-12 hours
- **GPT-2 Adapters:** ~12-15 hours

### Total Time: ~65-85 hours (2.7-3.5 days)

---

## Output Locations

### Results:
- `E:\Pending Experiment data\Reddit_TIFU_Experiments\BART\results\`
- `E:\Pending Experiment data\Reddit_TIFU_Experiments\T5\results\`
- `E:\Pending Experiment data\Reddit_TIFU_Experiments\GPT2\results\`

### Checkpoints:
- `E:\Pending Experiment data\Reddit_TIFU_Experiments\{MODEL}\checkpoints\`

### Logs:
- `E:\Pending Experiment data\Reddit_TIFU_Experiments\logs\`

### Cache:
- `E:\Pending Experiment data\Reddit_TIFU_Experiments\cache\`

---

## What Happens During Execution

1. **System check** - Logs GPU, CUDA, PyTorch info
2. **Dataset loading** - Downloads Reddit TIFU from Hugging Face
3. **Dataset limiting** - Uses only samples needed for 2000 steps
4. **Sequential execution** - Runs 9 experiments one by one
5. **Auto-skip** - Skips any already completed experiments
6. **GPU cleanup** - Aggressive memory clearing between experiments
7. **Results saving** - JSON files with metrics, energy, CO2
8. **Master summary** - Combined results file at the end

---

## Monitoring Progress

### Check logs in real-time:
```cmd
type "E:\Pending Experiment data\Reddit_TIFU_Experiments\logs\reddit_tifu_all_experiments_*.log"
```

### Check completed experiments:
```cmd
dir "E:\Pending Experiment data\Reddit_TIFU_Experiments\*\results\*.json"
```

---

## After Completion

Once Reddit TIFU is done, you'll have:
- **4/5 datasets complete** (CNN/DailyMail, PubMed, XSum, Reddit TIFU)
- **35/45 experiments complete** (78%)
- **1 dataset remaining:** Multi-News (9 experiments)

---

## Notes

### Dataset Characteristics:
- **Informal language** - Tests model robustness
- **Noisy structure** - Variable quality posts
- **Conversational style** - Different from news/scientific text
- **User-generated** - Spelling errors, slang, abbreviations

### Why This Dataset Matters:
- Provides contrast to formal datasets (CNN, PubMed)
- Tests generalization to casual text
- Important for real-world applications (social media, forums)

---

## Troubleshooting

### If OOM errors occur:
The script has aggressive memory cleanup, but if issues persist:
1. Restart computer to clear GPU memory
2. Run experiments individually by commenting out others
3. Reduce batch sizes further in the script

### If dataset download fails:
```python
# Manually download first:
from datasets import load_dataset
dataset = load_dataset("reddit_tifu", "long")
```

---

Generated: 26-Feb-2026 22:10
Status: READY TO RUN - REDDIT TIFU EXPERIMENTS
