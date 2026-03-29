# XSum Experiments Status Report

**Generated**: February 23, 2026, 08:15 AM

## Overall Progress: 8/9 Complete (89%)

---

## ✅ Completed Experiments (8/9)

### BART (3/3) ✓
| Exp ID | Method | Status | Time | Date Completed |
|--------|--------|--------|------|----------------|
| E1 | LoRA | ✅ Success | 63.5 min | Feb 20, 12:31 |
| E2 | QLoRA | ✅ Success | 140.8 min | Feb 21, 17:50 |
| E3 | Adapters | ✅ Success | 92.6 min | Feb 20, 14:05 |

### T5 (3/3) ✓
| Exp ID | Method | Status | Time | Date Completed |
|--------|--------|--------|------|----------------|
| E13 | LoRA | ✅ Success | 262.4 min | Feb 21, 15:27 |
| E14 | QLoRA | ✅ Success | 209.4 min | Feb 21, 21:20 |
| E15 | Adapters | ✅ Success | 385.6 min | Feb 22, 03:49 |

### GPT-2 (2/3) ✓
| Exp ID | Method | Status | Time | Date Completed |
|--------|--------|--------|------|----------------|
| E25 | LoRA | ✅ Success | 252.6 min | Feb 23, 01:09 |
| E27 | Adapters | ✅ Success | 328.1 min | Feb 23, 06:37 |

---

## ⏳ Running Now (1/9)

### GPT-2 E26 (QLoRA)
- **Status**: Running (Step 750/2000 - 37.5%)
- **Started**: Feb 23, 06:40
- **Current Speed**: 0.13 steps/second
- **ETA**: ~155 minutes remaining (~2.6 hours)
- **Expected Completion**: ~11:00 AM today

**Progress**:
```
Step 750/2000 (37.5%) | Loss: 2.7032 | Speed: 0.13 steps/s | ETA: 155.7 min
```

---

## Summary Statistics

### Completion Rate:
- **Total Experiments**: 9
- **Completed**: 8 (89%)
- **Running**: 1 (11%)
- **Failed**: 0

### By Model:
- **BART**: 3/3 (100%) ✓
- **T5**: 3/3 (100%) ✓
- **GPT-2**: 2/3 (67%) - E26 running

### By PEFT Method:
- **LoRA**: 3/3 (100%) ✓
- **QLoRA**: 2/3 (67%) - E26 running
- **Adapters**: 3/3 (100%) ✓

---

## Training Time Analysis

### BART (Encoder-Decoder):
- Average: 98.9 minutes
- Range: 63.5 - 140.8 minutes
- Fastest: E1 (LoRA)

### T5 (Encoder-Decoder):
- Average: 285.8 minutes
- Range: 209.4 - 385.6 minutes
- Fastest: E14 (QLoRA)

### GPT-2 (Decoder-Only):
- Average (completed): 290.4 minutes
- Range: 252.6 - 328.1 minutes
- E26 (running): ~240 minutes estimated

---

## Performance Metrics

### Completed GPT-2 Experiments:

#### E25 (LoRA):
- Trainable params: 786,432 (0.38%)
- Training loss: 2.711
- Speed: 0.133 steps/sec
- CO2 emissions: 0.210 kg

#### E27 (Adapters):
- Trainable params: 6,291,456 (2.99%)
- Training loss: 2.677
- Speed: 0.102 steps/sec
- CO2 emissions: 0.273 kg

---

## Expected Completion

### E26 (QLoRA) - Running:
- **Current Progress**: 750/2000 steps (37.5%)
- **Remaining Steps**: 1,250 steps
- **Current Speed**: 0.13 steps/sec
- **Time Remaining**: ~155 minutes (~2.6 hours)
- **Expected Completion**: ~11:00 AM, Feb 23, 2026

---

## Research Complete After E26!

Once E26 completes, you will have:

✅ **3 Models**: BART, T5, GPT-2  
✅ **3 PEFT Methods**: LoRA, QLoRA, Adapters  
✅ **9 Total Experiments**: All complete  
✅ **Energy Data**: CodeCarbon tracking for all  
✅ **ROUGE Scores**: Ready for evaluation  

---

## Next Steps After Completion

1. **Evaluate Models**: Run ROUGE evaluation on test set
2. **Analyze Results**: Compare PEFT methods across models
3. **Energy Analysis**: Compare CO2 emissions
4. **Write Report**: Use MODEL_SUBSTITUTION_JUSTIFICATION.md for GPT-2 rationale

---

## Files Location

### Results:
```
E:\Pending Experiment data\XSum_Experiments\
├── BART\results\
│   ├── E1_results.json ✓
│   ├── E2_results.json ✓
│   └── E3_results.json ✓
├── T5\results\
│   ├── E13_results.json ✓
│   ├── E14_results.json ✓
│   └── E15_results.json ✓
└── GPT2\results\
    ├── E25_results.json ✓
    ├── E27_results.json ✓
    └── E26_results.json (in progress)
```

### Checkpoints:
All models saved with checkpoints every 500 steps.

### Logs:
```
E:\Pending Experiment data\XSum_Experiments\logs\
└── xsum_gpt2_experiments_20260222_205642.log
```

---

## Status: ALMOST COMPLETE! 🎉

**8/9 experiments done - Only E26 (QLoRA) remaining!**

Expected completion: ~2.6 hours from now (11:00 AM)

---

**Report Generated**: February 23, 2026, 08:15 AM  
**Last Updated**: Step 750/2000 of E26
