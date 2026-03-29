# PubMed Experiments - Retry E26 & E27

## Current Status (7/9 Complete)

✅ **Completed Successfully:**
- E1: BART + LoRA (86.2 min)
- E3: BART + Adapters (89.3 min)
- E2: BART + QLoRA (131.9 min)
- E13: T5 + LoRA (211.6 min)
- E15: T5 + Adapters (231.3 min)
- E14: T5 + QLoRA (242.8 min)
- E25: GPT-2 + LoRA (768.8 min = 12.8 hours)

❌ **Failed (Need Retry):**
- E27: GPT-2 + Adapters (OOM - batch size too large)
- E26: GPT-2 + QLoRA (OOM - GPU still full from E27)

## What Went Wrong

**E27 (Adapters):**
- Batch size 6 was too large for 4GB GPU
- GPT-2 Medium (355M) + Adapters (6.3M trainable) + batch 6 + seq 512 = OOM

**E26 (QLoRA):**
- GPU memory wasn't fully cleared after E27 failure
- Couldn't even load the model

## Fixes Applied

1. **Reduced batch size for GPT-2 Adapters:**
   - Changed from batch_size=6 to batch_size=2
   - Increased gradient_accumulation from 3 to 8
   - Maintains same effective batch size (16) but uses less memory

2. **Improved GPU memory cleanup:**
   - Added dataset deletion
   - Added garbage collection
   - Double cache clearing

## Expected Performance After Fix

**E27 (GPT-2 Adapters):**
- Batch size: 2 (very conservative)
- Gradient accumulation: 8
- Expected time: ~18-20 hours (slow but won't OOM)
- Speed: ~30-35 seconds per step

**E26 (GPT-2 QLoRA):**
- Batch size: 4 (standard)
- Gradient accumulation: 4
- Expected time: ~8-10 hours
- Speed: ~15-18 seconds per step

## How to Retry

Simply run the script again:
```cmd
python run_pubmed_all_9_experiments_2000steps.py
```

The script will:
1. Skip all 7 completed experiments (E1, E2, E3, E13, E14, E15, E25)
2. Run only E27 and E26
3. Use the new conservative batch sizes
4. Complete all 9 experiments

## Why E27 Takes So Long

GPT-2 Adapters is the slowest combination because:
- **Largest model**: GPT-2 Medium (355M params)
- **Most trainable params**: Adapters (6.3M = 1.74%)
- **Longest sequences**: PubMed (512 tokens)
- **Smallest batch**: 2 (memory constraint)
- **4GB GPU limitation**

This is unavoidable with your hardware. The alternative would be to reduce training steps from 2000 to 1000, but that would affect research quality.

## Total Time Estimate

- E27: ~18-20 hours
- E26: ~8-10 hours
- **Total remaining: ~26-30 hours**

After this, all 9 PubMed experiments will be complete!
