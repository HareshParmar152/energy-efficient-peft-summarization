# Test All 9 XSum Experiments - 20 Steps

## Overview

This script tests all 9 XSum experiment configurations with only 20 training steps to quickly verify that everything works before running full training.

## Experiments Tested

### BART (3 experiments)
1. BART + LoRA
2. BART + QLoRA
3. BART + Adapters

### T5 (3 experiments)
4. T5 + LoRA
5. T5 + QLoRA
6. T5 + Adapters

### LLaMA (3 experiments)
7. LLaMA + LoRA
8. LLaMA + QLoRA
9. LLaMA + Adapters

## Test Configuration

```python
{
    "max_steps": 20,           # Only 20 steps for quick test
    "batch_size": 4,           # Small batch for speed
    "learning_rate": 3e-4,
    "max_source_length": 512,
    "max_target_length": 128,
    "save_steps": 10,          # Save at step 10 and 20
    "logging_steps": 5,        # Log every 5 steps
}
```

## Dataset

- **Dataset**: XSum
- **Train samples**: 100 (subset for testing)
- **Validation samples**: 20 (subset for testing)
- **Purpose**: Quick verification only

## Expected Time

- **Per experiment**: ~2-5 minutes
- **Total (all 9)**: ~20-45 minutes
- Much faster than full training (which takes hours)

## Running the Test

### Option 1: Windows Batch
```bash
RUN_TEST_XSUM_ALL_9.bat
```

### Option 2: PowerShell
```powershell
.\RUN_TEST_XSUM_ALL_9.ps1
```

### Option 3: Direct Python
```bash
python test_xsum_all_9_experiments_20steps.py
```

## Output Structure

```
test_outputs/
├── BART_XSum_LoRA_YYYYMMDD_HHMMSS/
│   ├── checkpoint-10/
│   ├── checkpoint-20/
│   └── test_result.json
├── BART_XSum_QLoRA_YYYYMMDD_HHMMSS/
│   └── test_result.json
├── ... (7 more experiments)

test_logs/
├── test_xsum_all_9_YYYYMMDD_HHMMSS.log
└── test_summary_YYYYMMDD_HHMMSS.json
```

## What Gets Tested

✅ **Model Loading**: Verifies all 3 models load correctly  
✅ **PEFT Configuration**: Tests LoRA, QLoRA, and Adapters setup  
✅ **Dataset Processing**: Checks XSum preprocessing  
✅ **Training Loop**: Runs 20 steps of training  
✅ **Checkpointing**: Saves checkpoints at step 10 and 20  
✅ **GPU/CPU Compatibility**: Tests on available hardware  

## Success Criteria

The test is successful if:
1. All 9 experiments complete without errors
2. Checkpoints are saved
3. Training loss decreases (even slightly)
4. No CUDA out of memory errors
5. No model loading errors

## Interpreting Results

### Test Summary (test_summary_*.json)
```json
{
  "timestamp": "20260216_120000",
  "total": 9,
  "success": 9,
  "failed": 0,
  "results": [...]
}
```

### Individual Results (test_result.json)
```json
{
  "experiment": "BART_XSum_LoRA",
  "model": "facebook/bart-base",
  "method": "LoRA",
  "status": "success",
  "steps": 20,
  "train_loss": 2.5,
  "timestamp": "20260216_120000"
}
```

## Troubleshooting

### Out of Memory
If you get CUDA OOM errors:
1. Reduce batch_size in the script (from 4 to 2 or 1)
2. Reduce max_source_length (from 512 to 256)

### Model Loading Errors
For LLaMA models, you may need:
1. Hugging Face authentication token
2. Access approval for Llama-2 models

### Import Errors
Install missing dependencies:
```bash
pip install transformers datasets peft bitsandbytes accelerate
```

## After Testing

### If All Tests Pass ✅
You can proceed with full training:
1. Increase max_steps to 800 or more
2. Use full dataset (not subset)
3. Run experiments individually or in sequence

### If Some Tests Fail ❌
1. Check the error logs in test_logs/
2. Fix configuration issues
3. Re-run the test
4. Don't proceed to full training until all pass

## Next Steps

### For Full Training

After successful testing, modify the script for full training:

```python
TEST_CONFIG = {
    "max_steps": 800,          # Full training
    "batch_size": 8,           # Larger batch
    "learning_rate": 3e-4,
    "max_source_length": 512,
    "max_target_length": 128,
    "save_steps": 200,         # Save every 200 steps
    "logging_steps": 50,
}

# Use full dataset
train_dataset = dataset['train']  # All ~204K samples
val_dataset = dataset['validation']  # All ~11K samples
```

## Comparison with CNN Experiments

| Aspect | CNN (Completed) | XSum (Testing) |
|--------|----------------|----------------|
| **Dataset** | CNN/DailyMail | XSum |
| **Train Samples** | 10,000 | 100 (test) / ~204K (full) |
| **Steps** | 1,875 (3 epochs) | 20 (test) / 800+ (full) |
| **Time per Exp** | 2-4 hours | 2-5 min (test) / 30-60 min (full) |
| **Purpose** | Production | Testing → Production |

## Important Notes

1. **This is a TEST only** - Results are not meaningful for research
2. **Purpose**: Verify configurations work before full training
3. **Don't use test results** in your paper
4. **After testing**: Run full training with proper parameters

## Files Created

1. `test_xsum_all_9_experiments_20steps.py` - Main test script
2. `RUN_TEST_XSUM_ALL_9.bat` - Windows batch launcher
3. `RUN_TEST_XSUM_ALL_9.ps1` - PowerShell launcher
4. `README_TEST_XSUM_ALL_9.md` - This file

## Support

If you encounter issues:
1. Check test_logs/ for detailed error messages
2. Verify GPU memory availability
3. Ensure all dependencies are installed
4. Try running one experiment at a time

---

**Created:** February 16, 2026  
**Purpose:** Quick verification before full XSum training  
**Status:** Ready to run
