# XSum All 9 Experiments - Production Run

## Overview

This script runs all 9 XSum experiments sequentially with 2000 steps each, collecting comprehensive metrics as per research proposal.

## Experiments

### BART (E1-E3)
- **E1**: BART | XSum | LoRA
- **E2**: BART | XSum | QLoRA
- **E3**: BART | XSum | Adapters

### T5 (E13-E15)
- **E13**: T5 | XSum | LoRA
- **E14**: T5 | XSum | QLoRA
- **E15**: T5 | XSum | Adapters

### LLaMA (E25-E27)
- **E25**: LLaMA | XSum | LoRA
- **E26**: LLaMA | XSum | QLoRA
- **E27**: LLaMA | XSum | Adapters

## Configuration

```python
{
    "dataset": "xsum",
    "max_steps": 2000,
    "batch_size": 8,
    "gradient_accumulation_steps": 2,
    "learning_rate": 3e-4,
    "max_source_length": 512,
    "max_target_length": 128,
    "save_steps": 500,
    "eval_steps": 500,
    "logging_steps": 50,
    "warmup_steps": 100,
    "weight_decay": 0.01,
}
```

## Output Structure

```
E:\Pending Experiment data\XSum_Experiments\
├── BART\
│   ├── results\
│   │   ├── E1_results.json
│   │   ├── E2_results.json
│   │   └── E3_results.json
│   └── checkpoints\
│       ├── E1_BART_XSum_LoRA\
│       ├── E2_BART_XSum_QLoRA\
│       └── E3_BART_XSum_Adapters\
├── T5\
│   ├── results\
│   │   ├── E13_results.json
│   │   ├── E14_results.json
│   │   └── E15_results.json
│   └── checkpoints\
│       ├── E13_T5_XSum_LoRA\
│       ├── E14_T5_XSum_QLoRA\
│       └── E15_T5_XSum_Adapters\
├── LLaMA\
│   ├── results\
│   │   ├── E25_results.json
│   │   ├── E26_results.json
│   │   └── E27_results.json
│   └── checkpoints\
│       ├── E25_LLaMA_XSum_LoRA\
│       ├── E26_LLaMA_XSum_QLoRA\
│       └── E27_LLaMA_XSum_Adapters\
└── logs\
    └── xsum_all_9_experiments_YYYYMMDD_HHMMSS.log
```

## Data Collected (Per Research Proposal)

### Model Information
- Experiment ID (E1-E27)
- Model name and type
- PEFT method
- Trainable parameters
- Total parameters
- Trainable percentage

### Training Metrics
- Training loss
- Training runtime (seconds and minutes)
- Samples per second
- Steps per second
- Total steps completed

### Evaluation Metrics
- ROUGE-1
- ROUGE-2
- ROUGE-L
- ROUGE-Lsum
- Evaluation loss
- Evaluation runtime
- Evaluation samples per second

### Energy Consumption
- CO2 emissions (kg)
- Tracked using CodeCarbon

### Checkpoints
- Saved every 500 steps
- Final model saved
- Best model based on ROUGE-L

## Running the Experiments

### Start Production Run
```bash
RUN_XSUM_ALL_9_PRODUCTION.bat
```

### What Happens
1. Activates virtual environment
2. Loads XSum dataset once
3. Runs experiments sequentially (one at a time)
4. Saves results after each experiment
5. Creates master summary at the end

### Execution Order
1. E1: BART + LoRA
2. E2: BART + QLoRA
3. E3: BART + Adapters
4. E13: T5 + LoRA
5. E14: T5 + QLoRA
6. E15: T5 + Adapters
7. E25: LLaMA + LoRA
8. E26: LLaMA + QLoRA
9. E27: LLaMA + Adapters

## Expected Time

| Experiment | Model | Method | Est. Time |
|------------|-------|--------|-----------|
| E1 | BART | LoRA | ~1-1.5 hours |
| E2 | BART | QLoRA | ~1-1.5 hours |
| E3 | BART | Adapters | ~1-1.5 hours |
| E13 | T5 | LoRA | ~1-1.5 hours |
| E14 | T5 | QLoRA | ~1-1.5 hours |
| E15 | T5 | Adapters | ~1-1.5 hours |
| E25 | LLaMA | LoRA | ~1.5-2 hours |
| E26 | LLaMA | QLoRA | ~1.5-2 hours |
| E27 | LLaMA | Adapters | ~1.5-2 hours |

**Total: 10-15 hours**

## Monitoring Progress

### Check Logs
```bash
# View latest log
type "E:\Pending Experiment data\XSum_Experiments\logs\xsum_all_9_experiments_*.log"
```

### Check Results
Each experiment saves results immediately after completion:
```bash
# Check BART results
type "E:\Pending Experiment data\XSum_Experiments\BART\results\E1_results.json"
```

### Monitor GPU
```bash
nvidia-smi
```

## Result Files

### Individual Results (E1_results.json)
```json
{
  "experiment_id": "E1",
  "experiment_name": "E1_BART_XSum_LoRA",
  "model": "facebook/bart-base",
  "method": "LoRA",
  "status": "success",
  "trainable_parameters": 2359296,
  "total_parameters": 139420416,
  "trainable_percentage": 1.69,
  "train_runtime_minutes": 75.5,
  "eval_rouge1": 0.3845,
  "eval_rouge2": 0.1623,
  "eval_rougeL": 0.3124,
  "emissions_kg_co2": 0.0012,
  ...
}
```

### Master Summary
```json
{
  "timestamp": "20260219_120000",
  "total_experiments": 9,
  "successful": 9,
  "failed": 0,
  "results": [...]
}
```

## Features

### Sequential Execution
- Runs one experiment at a time
- Prevents GPU memory issues
- Allows monitoring individual progress

### Comprehensive Logging
- System information
- Training progress
- Evaluation results
- Error tracking

### Energy Tracking
- CodeCarbon integration
- CO2 emissions per experiment
- Saved in results

### Automatic Cleanup
- Clears GPU memory after each experiment
- Prevents memory leaks

### Error Handling
- Continues to next experiment if one fails
- Saves error information
- Creates summary even with failures

## Troubleshooting

### Out of Memory
If you get CUDA OOM errors:
1. Reduce batch_size (from 8 to 4)
2. Increase gradient_accumulation_steps (from 2 to 4)

### LLaMA Access Issues
LLaMA models require Hugging Face authentication:
```bash
huggingface-cli login
```

### Slow Training
- Check GPU utilization with `nvidia-smi`
- Ensure FP16 is enabled
- Verify batch size is appropriate

## After Completion

### Verify Results
```bash
python verify_xsum_results.py
```

### Extract for Paper
All metrics are ready for research paper:
- ROUGE scores
- Training time
- Energy consumption
- Parameter efficiency

### Compare with CNN
Use the same metrics format as CNN experiments for easy comparison.

## Important Notes

1. **Do not interrupt** - Let all 9 experiments complete
2. **Monitor disk space** - Checkpoints require ~5GB per experiment
3. **Check logs regularly** - Identify issues early
4. **GPU availability** - Ensure GPU is free for 10-15 hours

## Next Steps

After successful completion:
1. Verify all 9 result files exist
2. Check ROUGE scores are reasonable
3. Compare with CNN/DailyMail results
4. Use data for research paper

---

**Created:** February 19, 2026  
**Purpose:** Production run for XSum experiments  
**Status:** Ready to execute
