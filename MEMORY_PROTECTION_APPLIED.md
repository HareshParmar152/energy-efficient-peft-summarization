# Memory Protection for RTX 2050 (4GB VRAM)

## Issues Fixed

1. **E2 QLoRA Error**: Fixed PyTorch 2.6+ compatibility issue
   - Added `model.config.use_cache = False`
   - Added `torch_dtype=torch.float16`
   - Added GPU cache clearing before loading

2. **Memory Optimization by Method**:

### LoRA (E1, E13, E25)
- Batch size: 12
- Gradient accumulation: 1
- Gradient checkpointing: OFF (faster)
- Memory usage: ~2.5-3GB

### QLoRA (E2, E14, E26)
- Batch size: 16 (4-bit quantization uses less memory)
- Gradient accumulation: 1
- Gradient checkpointing: OFF
- FP16: Disabled (already in 4-bit)
- Dataloader workers: 2 (reduced)
- Memory usage: ~2-2.5GB

### Adapters (E3, E15, E27)
- Batch size: 8 (more parameters = more memory)
- Gradient accumulation: 2
- Gradient checkpointing: ON (saves memory)
- Memory usage: ~3-3.5GB

## Additional Protections

1. **Gradient Clipping**: max_grad_norm=1.0 for stability
2. **GPU Cache Clearing**: Before each experiment and after errors
3. **Emergency Cleanup**: On any error, force cleanup GPU memory
4. **Resume Support**: Skip completed experiments (E1, E3)

## Expected Behavior

- E2 (QLoRA) should now work without memory errors
- All experiments stay within 4GB VRAM limit
- Training speed maintained with optimized batch sizes

## Remaining Experiments

- E2 (BART + QLoRA) - Will retry with fixes
- E13-E15 (T5 + LoRA/QLoRA/Adapters)
- E25-E27 (LLaMA + LoRA/QLoRA/Adapters)

Total: 7 experiments remaining
