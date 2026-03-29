# Restart SAMSum Experiments

## What Happened

E25 (GPT-2 LoRA) failed with out of memory error. This has been fixed.

## What's Been Fixed

- ✅ Reduced GPT-2 LoRA batch size from 8 to 4
- ✅ Increased gradient accumulation from 2 to 4
- ✅ Same fix applied to BillSum script

## Current Progress

**Completed (4/9):**
- ✅ E1 - BART LoRA (479.5 min)
- ✅ E3 - BART Adapters
- ✅ E13 - T5 LoRA
- ✅ E15 - T5 Adapters (479.5 min)

**Remaining (5/9):**
- E25 - GPT-2 LoRA (will retry with fix)
- E27 - GPT-2 Adapters
- E2 - BART QLoRA
- E14 - T5 QLoRA
- E26 - GPT-2 QLoRA

## How to Restart

### Just run the batch file again:
```cmd
RUN_SAMSUM_EXPERIMENTS.bat
```

The script will:
1. ✅ Auto-skip E1, E3, E13, E15 (already completed)
2. 🔄 Retry E25 with new batch size (fixed)
3. ▶️ Continue with remaining experiments

## No Data Loss

All completed experiments are saved:
- E1 results: `E:\Pending Experiment data\SAMSum_Experiments\BART\results\E1_results.json`
- E3 results: `E:\Pending Experiment data\SAMSum_Experiments\BART\results\E3_results.json`
- E13 results: `E:\Pending Experiment data\SAMSum_Experiments\T5\results\E13_results.json`
- E15 results: `E:\Pending Experiment data\SAMSum_Experiments\T5\results\E15_results.json`

## Expected Timeline

Remaining time: ~30-40 hours
- E25: ~6-8 hours
- E27: ~8-10 hours
- E2: ~6-8 hours
- E14: ~6-8 hours
- E26: ~6-8 hours (may fail)

## Note on E26

E26 (GPT-2 QLoRA) may still fail like it did on XSum. This is a known issue with GPT-2 QLoRA on 4GB GPU. If it fails, you'll have 8/9 SAMSum experiments complete, which is still excellent.

---

## Quick Command

```cmd
RUN_SAMSUM_EXPERIMENTS.bat
```

---

Generated: 28-Feb-2026 16:22
Status: READY TO RESTART
