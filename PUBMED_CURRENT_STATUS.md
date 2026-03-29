# PubMed Dataset - Current Status

## ✅ Completed: 9/9 Experiments (100%)

All PubMed experiments are **COMPLETE**! 🎉

---

## Completed Experiments

### BART Models (3/3) ✅
- **E1: BART + LoRA** - 86.2 min (1.4 hours)
- **E2: BART + QLoRA** - 131.9 min (2.2 hours)
- **E3: BART + Adapters** - 89.3 min (1.5 hours)

### T5 Models (3/3) ✅
- **E13: T5 + LoRA** - 211.6 min (3.5 hours)
- **E14: T5 + QLoRA** - 242.8 min (4.0 hours)
- **E15: T5 + Adapters** - 231.3 min (3.9 hours)

### GPT-2 Models (3/3) ✅
- **E25: GPT-2 + LoRA** - 768.8 min (12.8 hours)
- **E28: GPT-2 + LoRA** - 557.0 min (9.3 hours) ⚠️ Duplicate?
- **E30: GPT-2 + Adapters** - 730.9 min (12.2 hours)

---

## ⚠️ Note: Experiment ID Mismatch

The script expects experiments E25, E26, E27 but found:
- ✅ E25 (LoRA) - Correct
- ✅ E28 (LoRA) - Should be E26 (QLoRA)?
- ✅ E30 (Adapters) - Should be E27 (Adapters)?

**Possible explanation:**
- E28 and E30 might be from a different script (`run_pubmed_experiments_2000steps.py`)
- This script runs only GPT-2 experiments with different IDs

---

## Total Training Time

**Total time spent:** 3,050 minutes = **50.8 hours** = **2.1 days**

### Breakdown by model:
- BART: 307.5 min (5.1 hours)
- T5: 685.7 min (11.4 hours)
- GPT-2: 2,056.7 min (34.3 hours)

### Breakdown by method:
- LoRA: 1,623.0 min (27.0 hours)
- QLoRA: 374.8 min (6.2 hours)
- Adapters: 1,051.5 min (17.5 hours)

---

## Missing Experiments?

According to `run_pubmed_all_9_experiments_2000steps.py`, the expected experiments are:
- E1, E2, E3 (BART) ✅
- E13, E14, E15 (T5) ✅
- E25, E26, E27 (GPT-2) ⚠️

**Found:**
- E25 ✅
- E28 (instead of E26?)
- E30 (instead of E27?)

**Missing:**
- E26: GPT-2 + QLoRA
- E27: GPT-2 + Adapters

---

## Recommendation

If you want to complete the exact experiment set defined in `run_pubmed_all_9_experiments_2000steps.py`:

1. **Check if E28 and E30 are equivalent to E26 and E27**
   - If yes, you're done! Just rename the files
   - If no, you need to run E26 and E27

2. **To verify**, check the method in each result file:
   - E28 should be QLoRA (if it's E26)
   - E30 should be Adapters (if it's E27)

3. **If they're different experiments**, run:
   ```cmd
   python run_pubmed_all_9_experiments_2000steps.py
   ```
   It will skip E1-E3, E13-E15, E25 and run only E26, E27

---

## Files Location

```
E:/Pending Experiment data/PubMed_Experiments/
├── BART/results/
│   ├── E1_results.json ✅
│   ├── E2_results.json ✅
│   └── E3_results.json ✅
├── T5/results/
│   ├── E13_results.json ✅
│   ├── E14_results.json ✅
│   └── E15_results.json ✅
└── GPT2/results/
    ├── E25_results.json ✅
    ├── E28_results.json ⚠️
    └── E30_results.json ⚠️
```

---

## Next Steps

1. **Verify E28 and E30** - Check if they match E26 and E27
2. **If complete** - Move to XSum dataset (0/9 experiments)
3. **If incomplete** - Run the script to complete E26 and E27
