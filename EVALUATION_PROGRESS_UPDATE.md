# Evaluation Progress Update

## Current Status: 16/30 Complete (53%)

**Last Updated**: March 8, 2026, 07:28 AM
**Script Running**: 11 hours 38 minutes
**Current Task**: Evaluating SAMSum experiments

## Completed Datasets ✅

### PubMed: 9/9 (100%) ✅
All experiments completed between 13:03 - 22:17 yesterday

| Exp | Method | ROUGE-1 | Status |
|-----|--------|---------|--------|
| E1  | LoRA   | 0.2962  | ✅ |
| E2  | QLoRA  | 0.3010  | ✅ |
| E3  | Adapters | 0.3035 | ✅ Best |
| E13 | LoRA   | 0.2737  | ✅ |
| E14 | QLoRA  | 0.2715  | ✅ |
| E15 | Adapters | 0.2739 | ✅ |
| E25 | LoRA   | 0.2204  | ✅ |
| E27 | Adapters | 0.2161 | ✅ |
| E29 | QLoRA  | 0.2023  | ✅ |

### XSum: 7/7 (100%) ✅
All experiments completed between 22:22 - 01:34 (last night/early morning)

| Exp | Method | ROUGE-1 | Status |
|-----|--------|---------|--------|
| E1  | LoRA   | 0.3379  | ✅ |
| E2  | QLoRA  | 0.3254  | ✅ |
| E3  | Adapters | 0.3444 | ✅ Best |
| E13 | LoRA   | 0.2872  | ✅ |
| E14 | QLoRA  | 0.2622  | ✅ |
| E15 | Adapters | 0.2550 | ✅ |
| E25 | LoRA   | 0.1261  | ✅ |
| E27 | Adapters | 0.1347 | ✅ |

**Note**: E26 (GPT-2 QLoRA) was not trained, so only 7/8 experiments

## Currently Running ⏳

### SAMSum: 0/9 (0%)
**Status**: In progress (started ~01:35 AM)
**Expected**: 9 experiments × 40-60 min = 6-9 hours
**ETA**: Complete by ~10:00 AM

| Exp | Method | Status |
|-----|--------|--------|
| E1  | LoRA   | ⏳ Running |
| E2  | QLoRA  | ⏳ Pending |
| E3  | Adapters | ⏳ Pending |
| E13 | LoRA   | ⏳ Pending |
| E14 | QLoRA  | ⏳ Pending |
| E15 | Adapters | ⏳ Pending |
| E25 | LoRA   | ⏳ Pending |
| E26 | QLoRA  | ⏳ Pending |
| E27 | Adapters | ⏳ Pending |

## Pending ⏳

### BillSum: 0/4 (0%)
**Status**: Not started yet
**Expected**: 4 experiments × 45-60 min = 3-4 hours
**ETA**: Start ~10:00 AM, complete by ~14:00 PM

| Exp | Method | Status |
|-----|--------|--------|
| E1  | LoRA   | ⏳ Pending |
| E3  | Adapters | ⏳ Pending |
| E13 | LoRA   | ⏳ Pending |
| E15 | Adapters | ⏳ Pending |

## Timeline

- **Started**: March 7, 2026, 19:50
- **PubMed Complete**: March 7, 22:17 (2.5 hours)
- **XSum Complete**: March 8, 01:34 (3 hours)
- **SAMSum In Progress**: Started 01:35, ETA 10:00 (6-9 hours)
- **BillSum Pending**: ETA 10:00-14:00 (3-4 hours)
- **Total Expected**: March 8, ~14:00 (18-19 hours total)

## Performance Summary

### Best Performing:
1. **XSum E3** (BART Adapters): ROUGE-1: 0.3444
2. **XSum E1** (BART LoRA): ROUGE-1: 0.3379
3. **XSum E2** (BART QLoRA): ROUGE-1: 0.3254
4. **PubMed E3** (BART Adapters): ROUGE-1: 0.3035
5. **PubMed E2** (BART QLoRA): ROUGE-1: 0.3010

### Key Findings:
- **BART** consistently outperforms T5 and GPT-2
- **Adapters** slightly better than LoRA/QLoRA
- **XSum** has highest scores (shorter summaries)
- **GPT-2** struggles on XSum but decent on PubMed

## What's Happening Now

The evaluation script is:
1. ✅ Skipping completed PubMed experiments (9)
2. ✅ Skipping completed XSum experiments (7)
3. ⏳ Currently evaluating SAMSum experiments (0/9 done)
4. ⏳ Will evaluate BillSum experiments next (0/4)

## How to Monitor

### Check Python process:
```powershell
Get-Process python
```

### Check latest results:
```powershell
Get-ChildItem "E:\Pending Experiment data" -Recurse -Filter "*_evaluation.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

### Check log file:
```powershell
Get-Content evaluation_resume_20260308_064303.log -Tail 50
```

## Expected Final Results

When complete (~14:00 today):
- ✅ PubMed: 9/9 (100%)
- ✅ XSum: 7/8 (88%) - E26 missing from training
- ✅ SAMSum: 9/9 (100%)
- ✅ BillSum: 4/4 (100%)
- ✅ **Total: 29/30 (97%)**

Only missing E26 (XSum GPT-2 QLoRA) which failed during training.

## Next Steps

1. ⏳ Wait for SAMSum to complete (~3-6 more hours)
2. ⏳ Wait for BillSum to complete (~3-4 hours after SAMSum)
3. ✅ Analyze all ROUGE scores
4. ✅ Create comparison tables
5. ✅ Write research paper!

---

**Status**: Evaluation running smoothly, 16/30 complete, ETA ~14:00 today
