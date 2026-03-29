# PyTorch Installation Required

## Issue
Your virtual environment (.venv) doesn't have PyTorch and required packages installed.

## Solution

### Option 1: Simple Installation (Recommended)
```cmd
.\INSTALL_SIMPLE.bat
```

This installs everything you need in one go.

### Option 2: Detailed Installation
```cmd
.\INSTALL_PYTORCH_VENV.bat
```

This shows more details during installation.

### Option 3: Manual Installation
```cmd
# Activate virtual environment
.venv\Scripts\activate.bat

# Install PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other packages
pip install transformers peft adapters datasets evaluate rouge-score accelerate bitsandbytes codecarbon tqdm
```

## What Gets Installed

1. **PyTorch** (with CUDA 11.8 support) - Deep learning framework
2. **Transformers** - Hugging Face models (BART, T5, GPT-2)
3. **PEFT** - Parameter-Efficient Fine-Tuning (LoRA, QLoRA, Adapters)
4. **Datasets** - Hugging Face datasets library
5. **Evaluate** - Evaluation metrics (ROUGE)
6. **Accelerate** - Training acceleration
7. **BitsAndBytes** - Quantization for QLoRA
8. **CodeCarbon** - Energy monitoring
9. **Other utilities** - tqdm, sentencepiece, etc.

## Installation Time
- **Download**: 2-5 minutes (depends on internet speed)
- **Installation**: 3-5 minutes
- **Total**: 5-10 minutes

## After Installation

### Test the installation:
```cmd
.\TEST_EVALUATION.bat
```

This runs a quick test (1-2 minutes) to verify everything works.

### Run full evaluation:
```cmd
.\RUN_EVALUATION_ALL.bat
```

This evaluates all 30 experiments (3-5 hours).

## Why This Happened

The virtual environment (.venv) is isolated from your system Python. Even if PyTorch is installed system-wide, it needs to be installed separately in the virtual environment.

This is actually a good thing - it keeps your project dependencies isolated and reproducible.

## Troubleshooting

### If installation fails:
1. Check your internet connection
2. Make sure you have enough disk space (need ~5GB)
3. Try running PowerShell as Administrator
4. Check if antivirus is blocking downloads

### If CUDA not available after installation:
- This is OK for evaluation (will use CPU)
- Evaluation will be slower but will work
- Your GPU drivers might need updating

### If specific package fails:
- Try installing packages one by one
- Check error messages for specific issues
- Some packages (like bitsandbytes) are optional for evaluation

## Quick Reference

```cmd
# Install everything
.\INSTALL_SIMPLE.bat

# Test (1-2 min)
.\TEST_EVALUATION.bat

# Full evaluation (3-5 hours)
.\RUN_EVALUATION_ALL.bat
```

## Files Created

- `INSTALL_SIMPLE.bat` - Easy installation script
- `INSTALL_PYTORCH_VENV.bat` - Detailed installation script
- `requirements.txt` - List of all packages
- `RUN_THIS_FIRST.txt` - Quick instructions

## Next Steps

1. ✅ Run `.\INSTALL_SIMPLE.bat`
2. ✅ Wait for installation to complete
3. ✅ Run `.\TEST_EVALUATION.bat`
4. ✅ If test passes, run `.\RUN_EVALUATION_ALL.bat`
5. ✅ Wait 3-5 hours for evaluation to complete
6. ✅ Analyze results and write your paper!

---

**Start here**: `.\INSTALL_SIMPLE.bat`
