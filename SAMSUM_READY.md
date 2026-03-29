# SAMSum Experiments Ready to Run! 🚀

## Dataset 4: SAMSum (Replacement for Multi-News)

**Dataset:** SAMSum  
**Type:** Conversational dialogue summarization  
**Characteristics:** Short dialogues with concise summaries, messenger-style conversations

---

## Why SAMSum?

### Advantages:
✅ **Works perfectly** - No deprecated script issues  
✅ **Well-maintained** - Active Hugging Face dataset  
✅ **Good diversity** - Adds conversational text to your research  
✅ **Shorter texts** - Faster training than Multi-News  
✅ **Different domain** - Complements news/science datasets

### Dataset Characteristics:
- **Messenger conversations** - WhatsApp, Facebook Messenger style
- **Short dialogues** - 2-10 turns typically
- **Concise summaries** - 1-2 sentences
- **Informal language** - Casual, conversational style
- **14,732 samples** - Good size for training

---

## Script Created

**File:** `run_samsum_all_9_experiments_2000steps.py`

### Features:
✅ All optimizations from previous datasets applied  
✅ Aggressive GPU memory cleanup between experiments  
✅ QLoRA gradient fixes included  
✅ Caching enabled for fast preprocessing  
✅ Auto-skip completed experiments  
✅ Energy tracking with CodeCarbon  
✅ Windows-compatible (num_proc=1)

---

## Experiments to Run

### 9 Experiments Total:

#### BART (E1-E3):
- E1: BART + LoRA
- E2: BART + QLoRA
- E3: BART + Adapters

#### T5 (E13-E15):
- E13: T5 + LoRA
- E14: T5 + QLoRA
- E15: T5 + Adapters

#### GPT-2 (E25-E27):
- E25: GPT-2 + LoRA
- E26: GPT-2 + QLoRA
- E27: GPT-2 + Adapters

---

## Configuration

### Dataset Settings:
- **Source:** `samsum` from Hugging Face
- **Fields:** `dialogue` (conversation) → `summary`
- **Max source length:** 512 tokens
- **Max target length:** 128 tokens

### Training Settings:
- **Steps:** 2000
- **Base batch size:** 8 (SAMSum has short dialogues)
- **Gradient accumulation:** 2
- **Learning rate:** 3e-4

### Memory Protection:
- **QLoRA:** batch_size=4, gradient_accumulation=4
- **Adapters (GPT-2):** batch_size=2, gradient_accumulation=8
- **Adapters (BART/T5):** batch_size=6, gradient_accumulation=3

---

## How to Run

### Option 1: Use Batch File (Recommended)
```cmd
RUN_SAMSUM_EXPERIMENTS.bat
```

### Option 2: Manual Command
```cmd
deactivate
python run_samsum_all_9_experiments_2000steps.py
```

---

## Expected Timeline

### Estimated Time per Experiment:
SAMSum has shorter texts, so training is faster:

- **BART LoRA:** ~3-4 hours
- **BART QLoRA:** ~6-8 hours
- **BART Adapters:** ~4-5 hours
- **T5 LoRA:** ~8-10 hours
- **T5 QLoRA:** ~10-12 hours
- **T5 Adapters:** ~10-12 hours
- **GPT-2 LoRA:** ~6-8 hours
- **GPT-2 QLoRA:** ~8-10 hours
- **GPT-2 Adapters:** ~10-12 hours

### Total Time: ~50-70 hours (2-3 days)

---

## Output Locations

### Results:
- `E:\Pending Experiment data\SAMSum_Experiments\BART\results\`
- `E:\Pending Experiment data\SAMSum_Experiments\T5\results\`
- `E:\Pending Experiment data\SAMSum_Experiments\GPT2\results\`

### Checkpoints:
- `E:\Pending Experiment data\SAMSum_Experiments\{MODEL}\checkpoints\`

### Logs:
- `E:\Pending Experiment data\SAMSum_Experiments\logs\`

### Cache:
- `E:\Pending Experiment data\SAMSum_Experiments\cache\`

---

## After Completion

Once SAMSum is done, you'll have:
- **4/4 datasets complete** (CNN/DailyMail, PubMed, XSum, SAMSum)
- **35/36 experiments complete** (97%)
- **Excellent dataset diversity:**
  - Formal news (CNN/DailyMail)
  - Scientific text (PubMed)
  - Short news (XSum)
  - Conversations (SAMSum)
- **Ready for evaluation phase!**

---

## Why SAMSum is Better Than Multi-News

### SAMSum Advantages:
✅ Works without issues  
✅ Faster training (shorter texts)  
✅ Adds conversational domain  
✅ Well-maintained dataset  
✅ Good for testing generalization

### Research Coverage:
Your 4 datasets now cover:
- **Formal writing:** CNN/DailyMail
- **Scientific writing:** PubMed
- **News summaries:** XSum
- **Conversational:** SAMSum

This provides excellent diversity for evaluating PEFT methods!

---

## Monitoring Progress

### Check logs in real-time:
```cmd
type "E:\Pending Experiment data\SAMSum_Experiments\logs\samsum_all_experiments_*.log"
```

### Check completed experiments:
```cmd
dir "E:\Pending Experiment data\SAMSum_Experiments\*\results\*.json"
```

---

## Dataset Example

### Sample Dialogue:
```
Hannah: Hey, do you have Betty's number?
Amanda: Lemme check
Hannah: <file_gif>
Amanda: Sorry, can't find it.
Amanda: Ask Larry
Amanda: He called her last time we were at the park together
Hannah: I don't know him well
Hannah: <file_gif>
Amanda: Don't be shy, he's very nice
Hannah: If you say so..
Hannah: I'd rather you texted him
Amanda: Just text him 🙂
Hannah: Urgh.. Alright
Hannah: Bye
Amanda: Bye bye
```

### Summary:
```
Hannah needs Betty's number but Amanda doesn't have it. She needs to contact Larry.
```

---

Generated: 26-Feb-2026 22:50
Status: READY TO RUN - SAMSUM EXPERIMENTS
