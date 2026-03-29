# E25 Memory Fix Applied ✅

## Issue

E25 (GPT-2 LoRA on SAMSum) failed with OOM error:
```
RuntimeError: CUDA error: out of memory
```

## Root Cause

GPT-2 with causal LM uses more memory than seq2seq models (BART/T5), even with LoRA. The script was using batch_size=8 for GPT-2 LoRA, which is too large for 4GB GPU.

## Fix Applied

### SAMSum Script:
- **Before:** GPT-2 LoRA used batch_size=8, gradient_accumulation=2
- **After:** GPT-2 LoRA uses batch_size=4, gradient_accumulation=4

### BillSum Script:
- **Before:** GPT-2 LoRA used batch_size=4, gradient_accumulation=4
- **After:** GPT-2 LoRA uses batch_size=2, gradient_accumulation=8

## Updated Configuration

### SAMSum (Short Texts):
```python
if model_type == "gpt2":
    if method == "LoRA":
        batch_size = 4
        gradient_accumulation = 4
    elif method == "Adapters":
        batch_size = 2
        gradient_accumulation = 8
    elif method == "QLoRA":
        batch_size = 4
        gradient_accumulation = 4
```

### BillSum (Long Texts):
```python
if model_type == "gpt2":
    if method == "LoRA":
        batch_size = 2
        gradient_accumulation = 8
    elif method == "Adapters":
        batch_size = 2
        gradient_accumulation = 8
    elif method == "QLoRA":
        batch_size = 2
        gradient_accumulation = 8
```

## Effective Batch Size

Both configurations maintain effective batch size of 16:
- SAMSum: 4 × 4 = 16
- BillSum: 2 × 8 = 16

## Current Status

### SAMSum Completed (4/9):
- ✅ E1 - BART LoRA
- ✅ E3 - BART Adapters
- ✅ E13 - T5 LoRA
- ✅ E15 - T5 Adapters
- ❌ E25 - GPT-2 LoRA (FAILED - now fixed)

### SAMSum Remaining (5/9):
- E25 - GPT-2 LoRA (needs retry)
- E27 - GPT-2 Adapters
- E2 - BART QLoRA
- E14 - T5 QLoRA
- E26 - GPT-2 QLoRA

## How to Continue

### Option 1: Restart Script (Recommended)
The script will auto-skip completed experiments and retry E25 with new settings:

```cmd
RUN_SAMSUM_EXPERIMENTS.bat
```

### Option 2: Manual Restart
```cmd
deactivate
python run_samsum_all_9_experiments_2000steps.py
```

## What Will Happen

1. Script checks for completed experiments
2. Skips E1, E3, E13, E15 (already done)
3. Retries E25 with batch_size=4 (fixed)
4. Continues with E27, E2, E14, E26

## Expected Timeline

Remaining experiments (~30-40 hours):
- E25: ~6-8 hours (retry)
- E27: ~8-10 hours
- E2: ~6-8 hours
- E14: ~6-8 hours
- E26: ~6-8 hours (may fail like XSum E26)

## Notes

- GPT-2 requires more memory than BART/T5
- Causal LM is more memory-intensive than seq2seq
- 4GB GPU is at the limit for GPT-2 Medium
- E26 (GPT-2 QLoRA) may still fail (known issue)

---

Generated: 28-Feb-2026 16:20
Status: FIX APPLIED - RESTART SCRIPT
