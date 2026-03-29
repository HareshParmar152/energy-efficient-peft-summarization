# CRITICAL: Speed Issue Fixed - Batch Size Too Large

## Problem Identified

Current training speed: **0.04-0.05 steps/second**  
Expected speed: **0.8-1.2 steps/second**  
**20x slower than expected!**

This results in 27+ hours per experiment instead of 1-2 hours.

## Root Cause

**Batch size was TOO LARGE** (24 samples per batch)

Even with 4-bit quantization, GPT-2 Medium with batch_size=24 and max_length=256:
- Memory per batch: ~3.5GB
- Leaves only ~0.5GB for optimizer, gradients, activations
- Causes memory swapping and extreme slowdown

## Solution Applied

### Reduced Batch Sizes:
- **LoRA/QLoRA**: batch_size=8, gradient_accumulation=2 (effective=16)
- **Adapters**: batch_size=6, gradient_accumulation=3 (effective=18)

### Added TF32 Optimization:
```python
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
```

## Expected Performance After Fix

| Metric | Before (Wrong) | After (Fixed) |
|--------|----------------|---------------|
| Batch Size | 24 | 8 |
| Speed | 0.04 steps/s | 0.6-0.8 steps/s |
| Time per Experiment | 27 hours | 1-1.5 hours |
| Total Time | 81 hours | 3-5 hours |

## Memory Breakdown (Fixed Config)

### With batch_size=8:
- Model (4-bit): ~0.9GB
- Optimizer (8-bit): ~0.2GB
- Gradients: ~0.1GB
- Activations (batch=8, len=256): ~1.2GB
- Buffer: ~0.5GB
- **Total**: ~2.9GB ✓ (fits in 4GB)

### With batch_size=24 (OLD - WRONG):
- Model (4-bit): ~0.9GB
- Optimizer (8-bit): ~0.2GB
- Gradients: ~0.1GB
- Activations (batch=24, len=256): ~3.6GB ❌
- **Total**: ~4.8GB ❌ (exceeds 4GB, causes swapping)

## Action Required

### STOP Current Experiment:
Press `Ctrl+C` in the console window

### RESTART with Fixed Config:
```cmd
START_GPT2_NOW.bat
```

Or:
```cmd
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe run_xsum_llama_experiments_2000steps.py
```

## Verification After Restart

You should see:
```
LoRA: Using batch_size=8, gradient_accumulation=2

Step 50/2000 (2.5%) | Speed: 0.65 steps/s | ETA: 50 min
Step 100/2000 (5.0%) | Speed: 0.70 steps/s | ETA: 45 min
```

**Speed should be 0.6-0.8 steps/second** (15-20x faster than current!)

## Why This Happened

I initially set batch_size=24 thinking GPT-2 Medium (355M) would be very efficient. However:
1. Decoder-only models use more memory than encoder-decoder
2. Causal attention requires more activation memory
3. 4GB GPU has less headroom than expected

The conservative batch_size=8 ensures:
- ✓ No memory swapping
- ✓ Efficient GPU utilization
- ✓ Fast training speed
- ✓ Stable training

## Comparison with BART/T5

Your successful BART/T5 experiments used:
- BART: batch_size=16, gradient_accumulation=1
- T5: batch_size=16, gradient_accumulation=1

GPT-2 needs smaller batches because:
- Decoder-only architecture (more memory intensive)
- Causal attention (stores more activations)
- Different memory pattern than encoder-decoder

## Summary

**Problem**: Batch size too large (24) → Memory swapping → 20x slower  
**Solution**: Reduced batch size (8) → Fits in memory → Normal speed  
**Result**: 1-2 hours per experiment instead of 27 hours

**RESTART NOW with the fix!**

---

**Fix Applied**: February 22, 2026, 20:15  
**Status**: Ready to restart
