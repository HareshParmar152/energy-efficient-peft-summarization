# Start Local Dataset Experiments ✅

## Status: Ready to Run!

Both SAMSum and BillSum datasets have been downloaded locally and experiment scripts are ready.

---

## Quick Start

### Option 1: Run SAMSum (Recommended First)
```cmd
RUN_SAMSUM_EXPERIMENTS.bat
```

### Option 2: Run BillSum
```cmd
RUN_BILLSUM_EXPERIMENTS.bat
```

---

## What's Ready

### ✅ SAMSum Experiments
- **Script:** `run_samsum_all_9_experiments_2000steps.py`
- **Dataset:** Loaded from `E:/Pending Experiment data/local_datasets/samsum`
- **Experiments:** 9 (E1, E2, E3, E13, E14, E15, E25, E26, E27)
- **Time:** ~50-70 hours (2-3 days)
- **Batch file:** `RUN_SAMSUM_EXPERIMENTS.bat`

### ✅ BillSum Experiments
- **Script:** `run_billsum_all_9_experiments_2000steps.py`
- **Dataset:** Loaded from `E:/Pending Experiment data/local_datasets/billsum`
- **Experiments:** 9 (E1, E2, E3, E13, E14, E15, E25, E26, E27)
- **Time:** ~60-80 hours (2.5-3.5 days)
- **Batch file:** `RUN_BILLSUM_EXPERIMENTS.bat`

---

## Dataset Characteristics

### SAMSum (Conversational Dialogues)
- **Source:** Messenger conversations
- **Input length:** 512 tokens (short dialogues)
- **Output length:** 128 tokens (short summaries)
- **Batch size:** 8 (smaller due to short texts)
- **Style:** Informal, casual
- **Advantage:** Fast training, adds conversational domain

### BillSum (Legislative Bills)
- **Source:** US Congress bills
- **Input length:** 1024 tokens (long documents)
- **Output length:** 256 tokens (longer summaries)
- **Batch size:** 4 (smaller due to long texts)
- **Style:** Formal, legal
- **Advantage:** Adds formal/legal domain

---

## Configuration Details

### SAMSum Config:
```python
CONFIG = {
    "dataset": "samsum",
    "max_steps": 2000,
    "batch_size": 8,
    "gradient_accumulation_steps": 2,
    "max_source_length": 512,
    "max_target_length": 128,
}
```

### BillSum Config:
```python
CONFIG = {
    "dataset": "billsum",
    "max_steps": 2000,
    "batch_size": 4,
    "gradient_accumulation_steps": 4,
    "max_source_length": 1024,
    "max_target_length": 256,
}
```

---

## Experiment Order (Both Scripts)

1. **E1** - BART LoRA
2. **E3** - BART Adapters
3. **E13** - T5 LoRA
4. **E15** - T5 Adapters
5. **E25** - GPT-2 LoRA
6. **E27** - GPT-2 Adapters
7. **E2** - BART QLoRA
8. **E14** - T5 QLoRA
9. **E26** - GPT-2 QLoRA

QLoRA experiments run last for better Windows compatibility.

---

## Key Features

### Both Scripts Include:
- ✅ Local dataset loading (no Hugging Face issues)
- ✅ Auto-skip completed experiments
- ✅ Aggressive GPU memory management
- ✅ Progress logging with ETA
- ✅ Energy tracking (CodeCarbon)
- ✅ Dataset caching for speed
- ✅ Conservative batch sizes for 4GB GPU
- ✅ Comprehensive error handling

### Memory Optimizations:
- QLoRA: batch_size=2-4, gradient_accumulation=4-8
- Adapters: batch_size=2-6, gradient_accumulation=3-8
- LoRA: batch_size=4-8, gradient_accumulation=2-4
- Triple-pass GPU cleanup between experiments

---

## Running the Experiments

### Step 1: Choose Dataset
Decide whether to run SAMSum or BillSum first.

**Recommendation:** Start with SAMSum (faster, shorter texts)

### Step 2: Run Batch File
```cmd
RUN_SAMSUM_EXPERIMENTS.bat
```
or
```cmd
RUN_BILLSUM_EXPERIMENTS.bat
```

### Step 3: Monitor Progress
- Watch console output for real-time progress
- Check logs in respective experiment folders
- Each experiment saves results immediately

### Step 4: Wait for Completion
- SAMSum: ~50-70 hours
- BillSum: ~60-80 hours
- Scripts auto-skip completed experiments if interrupted

---

## Output Locations

### SAMSum:
```
E:/Pending Experiment data/SAMSum_Experiments/
├── BART/
│   ├── checkpoints/
│   └── results/
├── T5/
│   ├── checkpoints/
│   └── results/
├── GPT2/
│   ├── checkpoints/
│   └── results/
├── logs/
└── cache/
```

### BillSum:
```
E:/Pending Experiment data/BillSum_Experiments/
├── BART/
│   ├── checkpoints/
│   └── results/
├── T5/
│   ├── checkpoints/
│   └── results/
├── GPT2/
│   ├── checkpoints/
│   └── results/
├── logs/
└── cache/
```

---

## Progress Tracking

### Check Experiment Status:
Look for `{EXP_ID}_results.json` files in results folders:
- `E1_results.json` - BART LoRA
- `E2_results.json` - BART QLoRA
- `E3_results.json` - BART Adapters
- etc.

### Check Logs:
- Real-time: Console output
- Detailed: `logs/samsum_all_experiments_*.log`
- Detailed: `logs/billsum_all_experiments_*.log`

---

## If Interrupted

Both scripts auto-skip completed experiments. Just re-run the batch file:
```cmd
RUN_SAMSUM_EXPERIMENTS.bat
```

The script will:
1. Check for existing `{EXP_ID}_results.json` files
2. Skip experiments with `status="success"`
3. Continue from where it left off

---

## After Completion

### Your Final Status:
- **CNN/DailyMail:** 9/9 ✅
- **PubMed:** 9/9 ✅
- **XSum:** 8/9 ✅
- **SAMSum:** 9/9 ✅ (after running)
- **BillSum:** 9/9 ✅ (after running)

**Total:** 44/45 experiments (98% complete)

### Research Validity:
- ✅ 5 diverse datasets
- ✅ Multiple domains (news, science, conversation, legal)
- ✅ Multiple text lengths (short, medium, long)
- ✅ Multiple styles (formal, informal, technical, casual)
- ✅ All research questions answerable

---

## Troubleshooting

### If OOM Error:
- Script will save failure info
- Check logs for specific experiment
- May need to skip problematic experiment (like E26)

### If Dataset Loading Fails:
- Script will attempt Hugging Face download as fallback
- Check internet connection
- Verify local dataset path exists

### If Script Hangs:
- Check GPU memory usage
- May need to restart and let auto-skip handle it

---

## Recommendations

### Best Approach:
1. **Start with SAMSum** (faster, 2-3 days)
2. **Monitor first few experiments** to ensure stability
3. **Let it run unattended** once stable
4. **Then run BillSum** (2.5-3.5 days)

### Total Time:
- SAMSum: ~50-70 hours
- BillSum: ~60-80 hours
- **Combined:** ~110-150 hours (4.5-6 days)

### Alternative:
If time is limited, running just SAMSum gives you 4 datasets (35 experiments), which is still excellent for your research.

---

## Commands Summary

### Run SAMSum:
```cmd
RUN_SAMSUM_EXPERIMENTS.bat
```

### Run BillSum:
```cmd
RUN_BILLSUM_EXPERIMENTS.bat
```

### Manual Run (if needed):
```cmd
deactivate
python run_samsum_all_9_experiments_2000steps.py
```

---

Generated: 27-Feb-2026
Status: READY TO START LOCAL EXPERIMENTS ✅
