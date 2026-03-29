# Option: Reduce Training Steps for Faster Completion

## Current Situation

SAMSum experiments are taking ~8 hours each (479.5 minutes for E15).
- 5 remaining experiments × 8 hours = 40 hours
- This is too long!

## Problem Analysis

**Why so slow?**
- 2000 steps with small batch sizes
- GPT-2 is slower than BART/T5
- 4GB GPU limits batch size

**Your completed datasets:**
- CNN/DailyMail: Used 2000 steps
- PubMed: Used 2000 steps
- XSum: Used 2000 steps

## Solution Options

### Option 1: Reduce Steps to 1000 (Recommended)
**Pros:**
- 50% faster (4 hours per experiment)
- Still sufficient for research
- Maintains consistency with other datasets
- 5 experiments × 4 hours = 20 hours total

**Cons:**
- Different step count than other datasets
- May need to mention in paper

### Option 2: Skip SAMSum and BillSum
**Pros:**
- No additional time needed
- You already have 3 datasets (26 experiments)

**Cons:**
- Only 3 datasets instead of 5
- Less diversity in research

### Option 3: Continue with 2000 Steps
**Pros:**
- Consistent with other datasets
- Maximum training

**Cons:**
- 40+ hours remaining
- Too long for your timeline

## Recommendation: Reduce to 1000 Steps

### Why 1000 Steps is Valid:

1. **Research Validity:**
   - You're comparing PEFT methods, not achieving SOTA
   - Relative performance matters, not absolute
   - 1000 steps is sufficient for comparison

2. **Consistency:**
   - All SAMSum experiments use 1000 steps
   - All BillSum experiments use 1000 steps
   - Fair comparison within each dataset

3. **Time Savings:**
   - SAMSum: 20 hours instead of 40 hours
   - BillSum: 25 hours instead of 50 hours
   - Total: 45 hours instead of 90 hours

4. **Paper Justification:**
   - "Due to computational constraints, SAMSum and BillSum were trained for 1000 steps while maintaining consistent methodology across all PEFT methods"

## What to Do

### I can create new scripts with 1000 steps:
- `run_samsum_all_9_experiments_1000steps.py`
- `run_billsum_all_9_experiments_1000steps.py`

### Or modify existing scripts:
- Change `max_steps` from 2000 to 1000
- Adjust `save_steps` from 500 to 250

## Your Choice

**Option A:** Create 1000-step scripts (faster, still valid)
**Option B:** Continue with 2000 steps (slower, consistent)
**Option C:** Skip SAMSum/BillSum (fastest, 3 datasets only)

Which would you prefer?

---

Generated: 28-Feb-2026 16:30
