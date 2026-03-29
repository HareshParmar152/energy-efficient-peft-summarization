# Fix PyTorch CUDA Installation

## Problem
Your PyTorch is installed as CPU-only version (2.10.0+cpu), which is why training takes 15 hours instead of 1-2 hours.

## Your System
- GPU: NVIDIA GeForce RTX 2050 (4GB VRAM)
- CUDA Driver: 13.0
- Python: 3.13.5
- Current PyTorch: 2.10.0+cpu (CPU-only)

## Solution

### Option 1: Automated Fix (Recommended)
Run the batch file:
```
FIX_PYTORCH_CUDA.bat
```

### Option 2: Manual Installation
Open Command Prompt and run:

```bash
# Uninstall CPU version
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -m pip uninstall -y torch torchvision torchaudio

# Install CUDA version (CUDA 12.4 - compatible with your CUDA 13.0 driver)
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Verify
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

## Verify Installation

After installation, you should see:
```
PyTorch Version: 2.10.0+cu124
CUDA Available: True
CUDA Version: 12.4
GPU Name: NVIDIA GeForce RTX 2050
```

## Expected Performance After Fix

### Before (CPU-only):
- Speed: ~28 seconds/iteration
- Total time: 15-16 hours for 2000 steps
- GPU utilization: 0%

### After (GPU with CUDA):
- Speed: ~2-4 seconds/iteration
- Total time: 1-2 hours for 2000 steps
- GPU utilization: 90-100%

**Speed improvement: 10-15x faster!**

## Important Notes

1. **RTX 2050 has 4GB VRAM** - This is limited, so:
   - Keep batch_size at 16 or lower
   - If you get OOM errors, reduce to batch_size=8 or 12
   - QLoRA experiments will use less memory (4-bit quantization)

2. **Close other GPU applications** before training:
   - Check with `nvidia-smi`
   - Currently using 810MB for display/other apps
   - You have ~3.2GB available for training

3. **Monitor GPU usage** during training:
   ```
   nvidia-smi dmon
   ```

## Troubleshooting

### If CUDA still shows False after installation:
1. Restart your terminal/command prompt
2. Make sure you're using the correct Python:
   ```
   C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe
   ```
3. Check NVIDIA driver is working: `nvidia-smi`

### If you get OOM (Out of Memory) errors:
Edit `run_xsum_all_9_experiments_2000steps.py`:
```python
CONFIG = {
    "batch_size": 8,  # Reduce from 16
    "gradient_accumulation_steps": 2,  # Increase to maintain effective batch size
}
```

## After Installation

Run your training again:
```
RUN_XSUM_ALL_9_PRODUCTION.bat
```

You should see in the logs:
```
CUDA Available: True
GPU: NVIDIA GeForce RTX 2050
Model moved to GPU: NVIDIA GeForce RTX 2050
```

And training speed should be:
```
~0.3-0.5 it/s (instead of 0.035 it/s)
```
