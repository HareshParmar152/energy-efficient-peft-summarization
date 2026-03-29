# CNN/DailyMail Dataset - All Experiments

## Overview

This folder contains all completed experiments on the CNN/DailyMail dataset.

**Total Experiments**: 9 (3 models × 3 PEFT methods)

## Folder Structure

```
CNN_Dataset_All_Experiments/
├── BART/
│   ├── checkpoints/
│   │   ├── BART_cnn_dailymail_LoRA/
│   │   ├── BART_cnn_dailymail_QLoRA/
│   │   └── BART_cnn_dailymail_Adapters/
│   ├── results/
│   │   ├── BART_cnn_dailymail_LoRA_results.json
│   │   ├── BART_cnn_dailymail_QLoRA_results.json
│   │   └── BART_cnn_dailymail_Adapters_results.json
│   └── README.md
├── T5/
│   ├── checkpoints/
│   ├── results/
│   └── README.md
├── LLAMA/
│   ├── checkpoints/
│   ├── results/
│   └── README.md
└── README.md (this file)
```

## Models Tested

### 1. BART (facebook/bart-base)
- ✅ LoRA
- ✅ QLoRA
- ✅ Adapters

### 2. T5 (t5-base)
- ✅ LoRA
- ✅ QLoRA
- ✅ Adapters

### 3. LLaMA (TinyLlama-1.1B-Chat-v1.0)
- ✅ LoRA
- ✅ QLoRA
- ✅ Adapters

## PEFT Methods

### LoRA (Low-Rank Adaptation)
- Rank: 16
- Alpha: 32
- Dropout: 0.1
- Target modules: Query, Key, Value, Output projections

### QLoRA (Quantized LoRA)
- 4-bit quantization
- Same LoRA parameters as above
- Reduced memory footprint

### Adapters
- Implemented using LoRA architecture
- Same configuration as LoRA

## Dataset

**CNN/DailyMail** (abisee/cnn_dailymail v3.0.0)
- Training samples: 10,000
- Validation samples: 1,000
- Test samples: 1,000
- Task: News article summarization

## Results

Each experiment includes:
- **ROUGE Scores**: rouge1, rouge2, rougeL
- **Energy Consumption**: kWh and CO2 emissions
- **Training Duration**: Minutes
- **Model Parameters**: Trainable vs total
- **System Info**: GPU, memory usage

Check individual model folders for detailed results.

## Usage

See individual model README files for:
- How to load trained models
- How to use for inference
- Result interpretation

## Status

✅ **All 9 experiments completed**
✅ **Models saved and ready for use**
✅ **Results documented**

## Next Steps

Continue with remaining datasets:
- pubmed
- multi_news
- newsroom
- reddit_tifu

Each dataset needs 9 experiments (3 models × 3 methods).
