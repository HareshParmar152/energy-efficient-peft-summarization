# Evaluation Phase - Complete Guide

## Overview
You have completed 39/45 experiments (87%). Now it's time to evaluate them and generate ROUGE scores for your research paper.

## What Will Be Evaluated

### Datasets (Excluding CNN/DailyMail - Already Done)
1. **PubMed**: 9 experiments (E1, E2, E3, E13, E14, E15, E25, E27, E29)
2. **XSum**: 8 experiments (E1, E2, E3, E13, E14, E15, E25, E27)
3. **SAMSum**: 9 experiments (E1, E2, E3, E13, E14, E15, E25, E26, E27)
4. **BillSum**: 4 experiments (E1, E3, E13, E15)

**Total**: 30 experiments to evaluate

## Step-by-Step Instructions

### Step 1: Test Evaluation (RECOMMENDED)
Test with a single experiment first to ensure everything works:

```cmd
.\TEST_EVALUATION.bat
```

This will:
- Test SAMSum E1 (BART LoRA) with 10 samples
- Take 1-2 minutes
- Verify model loading and ROUGE calculation work

### Step 2: Run Full Evaluation
Once test passes, run the full evaluation:

```cmd
.\RUN_EVALUATION_ALL.bat
```

This will:
- Evaluate all 30 experiments
- Generate summaries on test sets
- Calculate ROUGE scores (ROUGE-1, ROUGE-2, ROUGE-L, ROUGE-Lsum)
- Save results to JSON files
- Take approximately 3-5 hours

## What the Script Does

For each experiment:
1. Loads the trained model from checkpoint
2. Loads the test dataset
3. Generates summaries for test samples
4. Calculates ROUGE scores
5. Saves results to JSON file
6. Cleans up GPU memory

## Output Files

### Individual Results
Each experiment gets a JSON file:
```
E:/Pending Experiment data/[Dataset]_Experiments/evaluation_results/[ExpID]_evaluation.json
```

Example:
```json
{
  "experiment_id": "E1",
  "dataset": "SAMSum",
  "model": "facebook/bart-base",
  "method": "LoRA",
  "num_samples": 818,
  "rouge_scores": {
    "rouge1": 0.4523,
    "rouge2": 0.2145,
    "rougeL": 0.3876,
    "rougeLsum": 0.3891
  }
}
```

### Master Summary
All results combined:
```
evaluation_summary_all_[timestamp].json
```

### Log File
Detailed execution log:
```
evaluation_all_[timestamp].log
```

## Evaluation Settings

- **Test samples**: 1000 per dataset (818 for SAMSum - full test set)
- **Max summary length**: 128 tokens
- **Batch size**: 8
- **Beam search**: 4 beams
- **GPU**: Automatically used if available

## Expected Time

- **Per experiment**: 5-10 minutes
- **Total (30 experiments)**: 3-5 hours
- **Depends on**: GPU speed, dataset size

## Troubleshooting

### If evaluation fails:
1. Check the log file for error details
2. Verify checkpoint paths exist
3. Ensure enough GPU memory (4GB should be fine)
4. Try reducing batch_size in the script if OOM errors

### If a specific experiment fails:
- The script will continue with other experiments
- Failed experiments will be logged
- You can re-run just that experiment later

## After Evaluation

Once complete, you'll have:
1. ROUGE scores for all 30 experiments
2. Individual result files for each experiment
3. Master summary file with all results
4. Ready for paper writing and analysis

## Next Steps After Evaluation

1. Analyze ROUGE scores across methods (LoRA, QLoRA, Adapters)
2. Compare performance across models (BART, T5, GPT-2)
3. Create tables and figures for your paper
4. Write results section with statistical analysis

## Important Notes

- CNN/DailyMail is NOT included (already evaluated)
- BillSum only has 4/9 experiments (hardware limitations - justified)
- All other datasets are complete
- 87% completion rate is excellent for publication

## Questions?

If you encounter issues:
1. Check the log file first
2. Verify virtual environment is activated
3. Ensure PyTorch and dependencies are installed
4. Check GPU availability with `nvidia-smi`
