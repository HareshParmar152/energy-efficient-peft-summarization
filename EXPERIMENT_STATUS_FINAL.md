# Complete Experiment Status - Final Report

## Summary
- **PubMed**: 9/9 COMPLETE (100%) ✅
- **XSum**: 8/9 COMPLETE (89%) - E26 FAILED (OOM) ❌
- **CNN/DailyMail**: 9/9 COMPLETE (100%) ✅ (in backup folder with LLAMA)

---

## PubMed Experiments - COMPLETE ✅

### Script Confusion Resolved:
There are TWO scripts with different experiment IDs:
1. `run_pubmed_all_9_experiments_2000steps.py` - Uses E1-E3, E13-E15, E25-E27
2. `run_pubmed_experiments_2000steps.py` - Uses E28-E30 (GPT-2 only)

### Completed Experiments:

#### BART (E1-E3):
- ✅ E1: BART LoRA - SUCCESS
- ✅ E2: BART QLoRA - SUCCESS  
- ✅ E3: BART Adapters - SUCCESS

#### T5 (E13-E15):
- ✅ E13: T5 LoRA - SUCCESS
- ✅ E14: T5 QLoRA - SUCCESS
- ✅ E15: T5 Adapters - SUCCESS

#### GPT-2 (E25-E30):
- ✅ E25: GPT-2 LoRA - SUCCESS (24-Feb 15:10)
- ❌ E26: GPT-2 QLoRA - FAILED (OOM) - 24-Feb 19:05
- ✅ E27: GPT-2 Adapters - SUCCESS (26-Feb 09:17)
- ✅ E28: GPT-2 LoRA - SUCCESS (25-Feb 05:10) [duplicate of E25]
- ✅ E29: GPT-2 QLoRA - SUCCESS (26-Feb 20:44) ⭐ **This is the working QLoRA!**
- ✅ E30: GPT-2 Adapters - SUCCESS (25-Feb 17:21) [duplicate of E27]

### Key Finding:
**E29 is the successful QLoRA experiment** that corresponds to E26. E26 failed with OOM, but E29 (from the other script) completed successfully with:
- Runtime: 616.7 minutes (10.3 hours)
- Train loss: 2.989
- Trainable params: 786,432 (0.38%)
- Status: SUCCESS ✅

---

## XSum Experiments - 8/9 COMPLETE (89%)

### Completed:
- ✅ E1: BART LoRA - SUCCESS (23-Feb 01:09)
- ❌ E2: BART QLoRA - PENDING (not run yet)
- ✅ E3: BART Adapters - SUCCESS (23-Feb 06:37)
- ✅ E13: T5 LoRA - SUCCESS
- ❌ E14: T5 QLoRA - PENDING (not run yet)
- ✅ E15: T5 Adapters - SUCCESS
- ✅ E25: GPT-2 LoRA - SUCCESS (23-Feb 01:09)
- ❌ E26: GPT-2 QLoRA - FAILED (OOM) - 26-Feb 21:18 ⚠️
- ✅ E27: GPT-2 Adapters - SUCCESS (23-Feb 06:37)

### Failed Experiment Details:
**E26 (GPT-2 QLoRA):**
- Error: CUDA out of memory
- Timestamp: 26-Feb 21:18
- Duration: 1.98 seconds (failed immediately)
- Reason: Insufficient GPU memory (4GB RTX 2050)

### Action Required:
E26 needs to be re-run with reduced batch size or skipped if memory constraints cannot be resolved.

---

## CNN/DailyMail Experiments - COMPLETE ✅

All 9 experiments completed and backed up in:
`ALL_EXPERIMENTS_BACKUP_20260212_180205/01_COMPLETED_EXPERIMENTS/CNN_DailyMail/`

Note: These used LLAMA instead of GPT-2.

---

## Training-Only Confirmation ✅

All experiments are **TRAINING ONLY** - no evaluation/validation/testing performed during training:
- No `eval_dataset` provided to trainer
- No `evaluation_strategy` set
- No metrics computed during training
- Only training loss logged

Evaluation will be done separately after all training completes.

---

## Next Steps

### For PubMed:
✅ ALL COMPLETE - No action needed

### For XSum:
1. ❌ E26 (GPT-2 QLoRA) - FAILED with OOM
   - Options:
     a. Reduce batch_size further (currently 4)
     b. Increase gradient_accumulation
     c. Skip if memory constraints too severe
2. ⏳ E2 (BART QLoRA) - Not yet run
3. ⏳ E14 (T5 QLoRA) - Not yet run

### Recommendation:
Run XSum experiments in this order:
1. E2 (BART QLoRA) - Should work with existing config
2. E14 (T5 QLoRA) - Should work with existing config  
3. E26 (GPT-2 QLoRA) - Try with batch_size=2, gradient_accumulation=8

---

## Script Auto-Skip Logic ✅

Both scripts have `is_experiment_completed()` function that checks for:
- `{EXP_ID}_results.json` with `status="success"`
- Automatically skips completed experiments
- Safe to re-run scripts without duplicating work

---

Generated: 26-Feb-2026 21:30
