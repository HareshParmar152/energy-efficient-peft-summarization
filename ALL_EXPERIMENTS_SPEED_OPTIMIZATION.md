# Speed Optimization Applied to ALL Experiment Scripts

## Problem
All experiment scripts were taking too long during dataset preprocessing:
- Processing entire datasets (119,924 samples for PubMed, 204,045 for XSum)
- Re-tokenizing from scratch for each experiment
- Slow tokenization speed (~106 examples/s)
- No caching enabled

## Files Optimized
✅ `run_pubmed_all_9_experiments_2000steps.py` (BART, T5, GPT-2 on PubMed)
✅ `run_xsum_all_9_experiments_2000steps.py` (BART, T5, GPT-2 on XSum) - **GPT-2 replaces LLaMA**
✅ `run_xsum_llama_experiments_2000steps.py` (GPT-2 on XSum)
✅ `run_pubmed_experiments_2000steps.py` (GPT-2 on PubMed)

**Note:** All scripts now use GPT-2 Medium instead of LLaMA due to authentication and compatibility issues on Windows.

## Solutions Applied to ALL Scripts

### 1. Dataset Size Limitation
Each script now calculates exact samples needed based on its configuration:
- **PubMed (BART/T5/GPT-2)**: 2000 steps × 4 batch × 4 accumulation = 32,000 samples + 10% = 35,200
- **PubMed (GPT-2 only)**: 2000 steps × 6 batch × 3 accumulation = 36,000 samples + 10% = 39,600
- **XSum (BART/T5/LLaMA)**: 2000 steps × 8 batch × 2 accumulation = 32,000 samples + 10% = 35,200
- **XSum (GPT-2 only)**: 2000 steps × 8 batch × 2 accumulation = 32,000 samples + 10% = 35,200

Reduces preprocessing by 70-80% depending on dataset

### 2. Enable Caching
- Changed `load_from_cache_file=False` → `True` in all scripts
- Added cache directories:
  - PubMed: `E:/Pending Experiment data/PubMed_Experiments/cache/{model_type}/`
  - XSum: `E:/Pending Experiment data/XSum_Experiments/cache/{model_type}/`
- Cache files named by model and dataset size
- After first run, subsequent experiments reuse cached data (instant loading)

### 3. Batch Processing Optimization
- Increased batch_size from default to 1000 for tokenization in all scripts
- Reduces overhead from processing small batches
- Speeds up tokenization significantly

### 4. Single Process
- Set `num_proc=1` in all scripts to avoid multiprocessing overhead on Windows
- Prevents cache conflicts and file locking issues

## Expected Results

### First Run (No Cache)
- Each model type's first experiment: ~10 min preprocessing
- Subsequent experiments of same model type: Instant (cache hit)

### Subsequent Runs (With Cache)
All experiments load instantly from cache

## Time Savings Per Full Run

### PubMed All 9 Experiments
- Before: ~3.6 hours preprocessing (9 × 24 min)
- After: ~30 minutes first run, instant for reruns
- **Savings: ~3 hours**

### XSum All 9 Experiments  
- Before: ~4.5 hours preprocessing (9 × 30 min)
- After: ~30 minutes first run, instant for reruns
- **Savings: ~4 hours**

### Total Savings Across All Scripts
- **~7 hours saved per complete experiment cycle**

## Cache Locations

### PubMed Experiments
```
E:/Pending Experiment data/PubMed_Experiments/cache/
├── bart/train_bart_35200.cache
├── t5/train_t5_35200.cache
└── gpt2/train_gpt2_39600.cache
```

### XSum Experiments
```
E:/Pending Experiment data/XSum_Experiments/cache/
├── bart/train_bart_35200.cache
├── t5/train_t5_35200.cache
└── gpt2/train_gpt2_35200.cache
```

**Note:** GPT-2 is used for experiments E25, E26, E27 instead of LLaMA.

## Cache Management
To clear cache if needed: Delete the respective cache directory
Cache is automatically reused when dataset size matches
