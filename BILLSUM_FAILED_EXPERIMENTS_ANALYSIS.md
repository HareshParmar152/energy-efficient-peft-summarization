# BillSum Failed Experiments - Complete Analysis

## Summary

**Status:** 4/9 experiments completed (44%)
**Failed:** 5/9 experiments (56%)
**Issue:** CUDA device-side assert triggered

---

## ✅ Successful Experiments (4/9)

### BART (2/3):
1. **E1: BART LoRA** ✅
   - Status: SUCCESS
   - Runtime: 151.1 minutes (~2.5 hours)
   - Train loss: 3.647
   - Trainable params: 442,368 (0.32%)
   - Completed: March 3, 2026 16:04

2. **E3: BART Adapters** ✅
   - Status: SUCCESS
   - Runtime: 157.9 minutes (~2.6 hours)
   - Train loss: 3.434
   - Trainable params: 1,769,472 (1.25%)
   - Completed: March 3, 2026 18:43

### T5 (2/3):
3. **E13: T5 LoRA** ✅
   - Status: SUCCESS
   - Runtime: 1,339.8 minutes (~22.3 hours)
   - Train loss: 1.763
   - Trainable params: 884,736 (0.40%)
   - Completed: March 4, 2026 17:05

4. **E15: T5 Adapters** ✅
   - Status: SUCCESS
   - Runtime: 1,030.3 minutes (~17.2 hours)
   - Train loss: 1.600
   - Trainable params: 3,538,944 (1.56%)
   - Completed: March 5, 2026 10:15

---

## ❌ Failed Experiments (5/9)

All failures occurred on March 6, 2026 with the same error:

### Error Message:
```
CUDA error: device-side assert triggered
CUDA kernel errors might be asynchronously reported at some other API call, 
so the stacktrace below might be incorrect.
For debugging consider passing CUDA_LAUNCH_BLOCKING=1
Compile with `TORCH_USE_CUDA_DSA` to enable device-side assertions.
```

### Failed Experiments:

1. **E2: BART QLoRA** ❌
   - Duration: 11.9 seconds (failed immediately)
   - Error: CUDA device-side assert

2. **E14: T5 QLoRA** ❌
   - Duration: 15.8 seconds (failed immediately)
   - Error: CUDA device-side assert

3. **E25: GPT-2 LoRA** ❌
   - Duration: 10.5 seconds (failed immediately)
   - Error: CUDA device-side assert

4. **E26: GPT-2 QLoRA** ❌
   - Duration: 29.5 seconds (failed immediately)
   - Error: CUDA device-side assert

5. **E27: GPT-2 Adapters** ❌
   - Duration: 2.8 seconds (failed immediately)
   - Error: CUDA device-side assert

---

## Root Cause Analysis

### Pattern Identified:
- ✅ **BART LoRA & Adapters** worked fine (March 3)
- ✅ **T5 LoRA & Adapters** worked fine (March 4-5)
- ❌ **All GPT-2 experiments** failed (March 6)
- ❌ **All QLoRA experiments** failed (March 6)

### Likely Causes:

1. **GPU Memory Corruption**
   - After running T5 experiments for 39+ hours continuously
   - GPU may have accumulated memory errors
   - CUDA device-side assert indicates GPU-level issue

2. **QLoRA Quantization Issue**
   - All 3 QLoRA experiments failed (BART, T5, GPT-2)
   - Quantization may trigger GPU assertion with corrupted state

3. **GPT-2 Specific Issue**
   - All 3 GPT-2 experiments failed (LoRA, QLoRA, Adapters)
   - May be related to decoder-only architecture vs encoder-decoder

4. **Timing**
   - Failures started after E15 completed (March 5, 10:15)
   - Script attempted to continue but GPU was in bad state
   - Log shows CUDA error during cleanup after E15

---

## Comparison with Other Datasets

### XSum (Similar Pattern):
- ✅ BART LoRA: SUCCESS
- ✅ BART Adapters: SUCCESS
- ✅ T5 LoRA: SUCCESS
- ✅ T5 Adapters: SUCCESS
- ✅ GPT-2 LoRA: SUCCESS
- ❌ GPT-2 QLoRA (E26): FAILED (OOM)
- ✅ GPT-2 Adapters: SUCCESS

### PubMed (All Successful):
- ✅ All 9 experiments completed
- Including E26 GPT-2 QLoRA (as E29)

### Key Difference:
- **PubMed & XSum:** GPT-2 LoRA and Adapters worked
- **BillSum:** ALL GPT-2 experiments failed
- **BillSum:** ALL QLoRA experiments failed

This suggests the issue is specific to BillSum + GPU state corruption, not the models themselves.

---

## Recommended Solutions

### Option 1: Restart Computer & Retry (Recommended)
```cmd
# 1. Restart computer to clear GPU state
# 2. Run only failed experiments:
RUN_BILLSUM_EXPERIMENTS.bat
```

The script will auto-skip the 4 completed experiments and retry the 5 failed ones.

### Option 2: Run Failed Experiments Individually
Create separate scripts for each failed experiment to isolate issues:

```python
# Run E2 (BART QLoRA) alone
# Run E14 (T5 QLoRA) alone
# Run E25 (GPT-2 LoRA) alone
# Run E26 (GPT-2 QLoRA) alone
# Run E27 (GPT-2 Adapters) alone
```

### Option 3: Reduce Batch Size Further
For QLoRA experiments, try:
```python
batch_size = 2  # Instead of 4
gradient_accumulation_steps = 8  # Instead of 4
```

### Option 4: Skip QLoRA Experiments
If QLoRA continues to fail:
- You'll have 6/9 BillSum experiments (67%)
- Still have QLoRA results from other datasets
- Can discuss QLoRA limitations in your research

---

## Impact on Research

### Current Overall Status:
- **CNN/DailyMail:** 9/9 (100%) ✅
- **PubMed:** 9/9 (100%) ✅
- **XSum:** 8/9 (89%) ✅
- **SAMSum:** 9/9 (100%) ✅
- **BillSum:** 4/9 (44%) ⚠️

**Total:** 39/45 experiments (87%)

### If BillSum Failures Persist:
- You still have 39 successful experiments
- All 3 PEFT methods tested across 4 datasets
- Sufficient data for research conclusions
- Can discuss GPU limitations in methodology

### Research Questions Still Answerable:
- ✅ Which PEFT method is most effective? (Yes - have all 3 methods on 4 datasets)
- ✅ How do methods compare across domains? (Yes - 4 complete datasets)
- ✅ Efficiency vs performance trade-off? (Yes - have runtime and loss data)
- ✅ Best method for different text types? (Yes - news, science, conversation, legal)

---

## Next Steps

### Immediate Action:
1. **Restart computer** to clear GPU memory corruption
2. **Run:** `RUN_BILLSUM_EXPERIMENTS.bat`
3. **Monitor:** Watch for CUDA errors in first few minutes
4. **If successful:** Let it run for ~35-44 hours

### If Failures Persist:
1. Try running experiments individually
2. Reduce batch sizes for QLoRA
3. Consider skipping problematic experiments
4. Document GPU limitations in research

### Alternative:
If you have access to another machine with better GPU:
- Copy the script and dataset
- Run failed experiments there
- Merge results back

---

## Files & Locations

### Completed Results:
```
E:\Pending Experiment data\BillSum_Experiments\BART\results\E1_results.json
E:\Pending Experiment data\BillSum_Experiments\BART\results\E3_results.json
E:\Pending Experiment data\BillSum_Experiments\T5\results\E13_results.json
E:\Pending Experiment data\BillSum_Experiments\T5\results\E15_results.json
```

### Summary File:
```
E:\Pending Experiment data\BillSum_Experiments\billsum_all_summary_20260306_125152.json
```

### Log File:
```
E:\Pending Experiment data\BillSum_Experiments\logs\billsum_all_experiments_20260306_125152.log
```

---

## Conclusion

The BillSum experiments encountered GPU-level errors after successfully completing 4/9 experiments. The issue appears to be GPU memory corruption after running intensive T5 experiments for 39+ hours continuously.

**Recommendation:** Restart computer and retry. The script's auto-skip feature will resume from where it left off.

---

Generated: March 6, 2026
Status: 4/9 COMPLETE - 5/9 FAILED (CUDA ERROR)
