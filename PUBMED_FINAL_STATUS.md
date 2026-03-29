# PubMed Experiments - Final Status Update

## ✅ E27 COMPLETED!

**E27: GPT-2 + Adapters**
- Status: ✅ SUCCESS
- Training time: 558.99 minutes (9.3 hours)
- Completed: Feb 26, 09:17 AM
- Checkpoints saved:
  - checkpoint-1500 (06:57 AM)
  - checkpoint-2000 (09:16 AM)
  - final_model (09:17 AM)

## 🔄 E26 CURRENTLY RUNNING

**E26: GPT-2 + QLoRA**
- Status: 🔄 IN PROGRESS
- Started: Feb 26, 09:17 AM (right after E27)
- Method: QLoRA (4-bit quantization)
- Expected time: ~8-10 hours
- Expected completion: **Feb 26, 5:00-7:00 PM**

## Current Progress Summary

**Completed: 8/9 experiments (89%)**

### BART Models (3/3) ✅
- E1: LoRA - 86.2 min
- E2: QLoRA - 131.9 min
- E3: Adapters - 89.3 min

### T5 Models (3/3) ✅
- E13: LoRA - 211.6 min
- E14: QLoRA - 242.8 min
- E15: Adapters - 231.3 min

### GPT-2 Models (2/3) 🔄
- E25: LoRA - 768.8 min ✅
- E27: Adapters - 559.0 min ✅
- E26: QLoRA - IN PROGRESS 🔄

## Total Training Time So Far

**Completed experiments:** 2,321 minutes = **38.7 hours**

**Remaining:** E26 (~8-10 hours)

**Total expected:** ~47-49 hours for all 9 PubMed experiments

## What Happens Next

1. **E26 completes** (~5-7 PM today)
2. **Script generates final summary** with all 9 experiments
3. **All PubMed experiments DONE!** 🎉
4. **Next:** Move to XSum dataset (0/9 experiments)

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
├── GPT2/results/
│   ├── E25_results.json ✅
│   ├── E27_results.json ✅ (NEW!)
│   └── E26_results.json 🔄 (will be created when done)
└── GPT2/checkpoints/
    └── E27_GPT2_PubMed_Adapters/
        ├── checkpoint-1500/ ✅
        ├── checkpoint-2000/ ✅
        └── final_model/ ✅
```

## Note

There was a brief network issue when saving E27 (couldn't reach huggingface.co), but the experiment completed successfully and results were saved locally.

---

**Status:** E26 is running smoothly. Just let it complete and all PubMed experiments will be done! 🎯
