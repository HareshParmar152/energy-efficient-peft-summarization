# Performance Optimizations Applied

## Changes Made to Speed Up Training

### 1. Dynamic Padding (BIGGEST IMPACT)
**Before:** `padding="max_length"` - Every sample padded to 512 tokens
**After:** `padding=False` - Dynamic padding per batch
**Impact:** 3-5x faster training, less wasted computation

### 2. GPU Optimizations
- `dataloader_pin_memory=True` - Faster CPU->GPU memory transfer
- `dataloader_num_workers=4` - Parallel data loading
- `dataloader_prefetch_factor=2` - Prefetch next batches
- `optim="adamw_torch_fused"` - Fused GPU optimizer (faster than standard)
- `tf32=True` - Use TensorFloat32 on Ampere GPUs (RTX 30xx/40xx)
- Model explicitly moved to GPU for LoRA/Adapters

### 3. Batch Size Optimization
**Before:** batch_size=8, gradient_accumulation=2 (effective batch=16)
**After:** batch_size=16, gradient_accumulation=1 (effective batch=16)
**Impact:** Fewer gradient accumulation steps = faster

### 4. Removed Gradient Checkpointing
- Disabled for speed (was trading memory for time)
- Enable only if you get OOM errors

## Expected Performance

**Before:** ~28.5 seconds/iteration → 15.8 hours for 2000 steps
**After:** ~3-5 seconds/iteration → 1.5-3 hours for 2000 steps

**Speed improvement: 5-10x faster**

## If You Still Get OOM (Out of Memory)

Adjust these settings in order:

1. Reduce batch_size: 16 → 12 → 8
2. Increase gradient_accumulation_steps: 1 → 2 → 4
3. Enable gradient_checkpointing: False → True
4. Reduce max_source_length: 512 → 384 → 256

## Monitor Training

Watch for:
- GPU utilization: Should be 90-100% (check with `nvidia-smi`)
- Samples/second: Should be 15-30+ samples/sec
- Steps/second: Should be 0.2-0.5 steps/sec

## Additional Tips

- Close other GPU applications
- Use `nvidia-smi dmon` to monitor GPU usage in real-time
- First experiment will be slower (model download + compilation)
- Subsequent experiments will be faster (cached)
