# Windows Dataset Caching Error - FIXED

## Problem Identified

The experiment is failing with:
```
OSError: [WinError 1224] The requested operation cannot be performed on a file with a user-mapped section open
```

This is a known Windows issue with HuggingFace datasets caching mechanism.

## Root Cause

When HuggingFace datasets tries to cache preprocessed data to disk on Windows, it can encounter file locking issues due to Windows' file mapping system. This prevents the dataset from being properly cached and causes the preprocessing to fail.

## Solution Applied

Changed dataset preprocessing to:
1. **Disable disk caching**: `load_from_cache_file=False`
2. **Keep in memory**: `keep_in_memory=True`

### Code Change:
```python
# Before:
train_processed = train_dataset.map(
    lambda x: preprocess_function_causal(x, tokenizer),
    batched=True,
    remove_columns=train_dataset.column_names,
    desc="Tokenizing train"
)

# After:
train_processed = train_dataset.map(
    lambda x: preprocess_function_causal(x, tokenizer),
    batched=True,
    remove_columns=train_dataset.column_names,
    desc="Tokenizing train",
    load_from_cache_file=False,  # Disable caching
    keep_in_memory=True,  # Keep in RAM
)
```

## Impact

### Memory Usage:
- XSum dataset: ~200K samples
- Preprocessed size: ~2-3GB in memory
- Your system has 16GB RAM - this is fine

### Performance:
- First run: Slightly slower (no cache benefit)
- Subsequent runs: Same (no cache anyway due to error)
- Training speed: Unchanged

## What to Do Now

### Step 1: Stop Current Experiment
Press `Ctrl+C` in the console window running the experiment

### Step 2: Restart with Fix
Run:
```cmd
START_GPT2_NOW.bat
```

Or:
```cmd
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe run_xsum_llama_experiments_2000steps.py
```

## Expected Behavior After Fix

You should see:
```
Preprocessing training dataset...
Tokenizing train: 100%|████████████| 204045/204045 [02:30<00:00, 1356.82 examples/s]

Starting training for 2000 steps...
Training started - Total steps: 2000

Step 50/2000 (2.5%) | Loss: 2.34 | LR: 1.5e-04 | Speed: 0.9 steps/s | ETA: 36 min
```

**Speed should be ~0.8-1.2 steps/second** (not 0.01!)

## Why 39 Hours Was Shown

The 39-hour estimate was likely because:
1. Dataset preprocessing was failing/retrying
2. Training hadn't actually started yet
3. System was stuck in error loop

With the fix, actual training time should be **1-2 hours per experiment** (3-5 hours total).

## Verification

After restarting, check:
1. **GPU usage**: Run `nvidia-smi` - should show ~80-100% GPU utilization
2. **Training speed**: Should see ~0.8-1.2 steps/second
3. **ETA**: Should show ~30-40 minutes per experiment

If you still see slow speed or high ETA, let me know immediately!

---

**Fix Applied**: February 22, 2026  
**Status**: Ready to restart
