# All Fixes Applied to Experiments

## Issues Found and Fixed:

### 1. Invalid Format Specifier (E2, E13, E14)
**Error**: `Invalid format specifier '.4f if isinstance(loss, float) else loss'`
**Fix**: Changed to proper conditional formatting:
```python
loss_str = f"{loss:.4f}" if isinstance(loss, (int, float)) else str(loss)
```

### 2. LLaMA Gated Repo Access (E25, E26, E27)
**Error**: `You are trying to access a gated repo`
**Fix**: Removed LLaMA experiments from the queue (requires HuggingFace authentication)

### 3. QLoRA Windows Multiprocessing (E2, E14, E26)
**Error**: `Can't get local object 'PreTrainedModel.enable_input_require_grads'`
**Fix**: 
- Set `dataloader_num_workers=0` for QLoRA (no multiprocessing)
- Manually enable input embeddings gradients
- Moved QLoRA experiments to end of queue

### 4. E15 Gradient Issue
**Error**: `element 0 of tensors does not require grad and does not have a grad_fn`
**Fix**: Added explicit gradient verification for Adapters method

## Current Experiment Queue (6 total):

1. E1 (BART + LoRA) ✓ Already completed
2. E3 (BART + Adapters) ✓ Already completed  
3. E13 (T5 + LoRA) - Pending
4. E15 (T5 + Adapters) - Pending
5. E2 (BART + QLoRA) - Pending (at end)
6. E14 (T5 + QLoRA) - Pending (at end)

## Excluded:
- E25, E26, E27 (LLaMA) - Require HuggingFace authentication

## Status:
All fixes applied. Ready to run 4 remaining experiments (E13, E15, E2, E14).
