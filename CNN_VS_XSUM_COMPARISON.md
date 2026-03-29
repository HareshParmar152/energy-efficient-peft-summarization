# CNN/DailyMail vs XSum - Key Differences

## Your Completed Experiments

### CNN/DailyMail (Completed ✓)
- BART + LoRA ✓
- BART + QLoRA ✓
- BART + Adapters ✓

### XSum (Completed ✓)
- BART + LoRA ✓ (E1)
- BART + QLoRA ✓ (E2)
- BART + Adapters ✓ (E3)
- T5 + LoRA ✓ (E13)
- T5 + QLoRA ✓ (E14)
- T5 + Adapters ✓ (E15)

### OPT (In Progress)
- OPT + LoRA (E25)
- OPT + QLoRA (E26)
- OPT + Adapters (E27)

## Configuration Comparison

| Setting | CNN/DailyMail (Old) | XSum (Current) |
|---------|---------------------|----------------|
| **Model** | facebook/bart-base | facebook/bart-base |
| **Batch Size** | 2 | 16 |
| **Gradient Accumulation** | 8 | 1 |
| **Effective Batch** | 16 | 16 |
| **Learning Rate** | 2e-4 | 3e-4 |
| **Training** | 3 epochs | 2000 steps |
| **Max Source Length** | Not specified | 512 |
| **Max Target Length** | Not specified | 128 |
| **Warmup Steps** | 500 | 100 |
| **Evaluation** | During training | Separate |

## Performance Comparison

### CNN/DailyMail BART LoRA:
- Training time: 143.8 minutes (~2.4 hours)
- Emissions: 0.000618 kg CO2
- Eval loss: 2.074
- ROUGE-1: 0.560
- ROUGE-2: 0.276
- ROUGE-L: 0.523

### XSum BART LoRA (E1):
- Training time: 63.5 minutes (~1.1 hours)
- Emissions: 0.051 kg CO2
- Train loss: 2.464
- Speed: 0.528 steps/sec
- Samples/sec: 8.446

## Key Differences

### 1. Dataset Characteristics

| Feature | CNN/DailyMail | XSum |
|---------|---------------|------|
| **Article Length** | ~800 tokens | ~400 tokens |
| **Summary Length** | ~60 tokens | ~20 tokens |
| **Summary Style** | Extractive (copy from article) | Abstractive (rewrite) |
| **Difficulty** | Easier | Harder |
| **Dataset Size** | ~300K samples | ~200K samples |

### 2. Training Approach

**CNN/DailyMail (Old approach):**
- Small batch size (2) with high gradient accumulation (8)
- Epoch-based training (3 epochs)
- Evaluation during training
- Slower but more stable

**XSum (New approach):**
- Large batch size (16) with no gradient accumulation
- Step-based training (2000 steps)
- Separate evaluation
- Faster training

### 3. Why XSum is Faster

1. **Shorter sequences**: XSum articles are ~50% shorter
2. **Larger batches**: 16 vs 2 (8x larger)
3. **No gradient accumulation overhead**: 1 vs 8
4. **Optimized for GPU**: Better GPU utilization

## Why OPT/LLaMA is Different

### BART/T5 (Encoder-Decoder):
- ✓ Designed for summarization
- ✓ Efficient for seq2seq tasks
- ✓ Works well on 4GB GPU
- ✓ Fast training

### OPT/LLaMA (Decoder-Only):
- ⚠️ Designed for text generation
- ⚠️ Less efficient for summarization
- ⚠️ Requires more memory
- ⚠️ Slower training
- ⚠️ Different preprocessing (causal LM)

## The Real Issue with OPT/LLaMA

### It's NOT the dataset (XSum vs CNN/DailyMail)
The issue is the **model architecture**:

1. **Decoder-only models** (OPT/LLaMA) are fundamentally different from encoder-decoder models (BART/T5)
2. **Causal LM approach** requires different data preprocessing
3. **Memory usage** is higher for decoder-only models
4. **Training speed** is slower for decoder-only on summarization

### Why BART/T5 Work Better for Summarization

| Feature | BART/T5 | OPT/LLaMA |
|---------|---------|-----------|
| **Architecture** | Encoder-Decoder | Decoder-Only |
| **Designed For** | Summarization | Generation |
| **Memory Efficiency** | High | Lower |
| **Training Speed** | Fast | Slower |
| **XSum Performance** | Excellent | Good |
| **4GB GPU** | ✓ Works great | ⚠️ Challenging |

## Summary

### What Works:
- ✅ BART on CNN/DailyMail (completed)
- ✅ BART on XSum (completed - E1, E2, E3)
- ✅ T5 on XSum (completed - E13, E14, E15)

### What's Challenging:
- ⚠️ OPT on XSum (in progress - E25, E26, E27)
  - Decoder-only architecture
  - More memory intensive
  - Slower training
  - Windows multiprocessing issues

### The Bottom Line:
The issue is NOT XSum vs CNN/DailyMail. The issue is **decoder-only models (OPT/LLaMA) are harder to train for summarization** compared to encoder-decoder models (BART/T5).

Your BART and T5 experiments on XSum are working perfectly! The OPT experiments are just more challenging due to the architecture difference.
