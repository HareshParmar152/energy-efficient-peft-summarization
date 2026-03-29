# Energy-Efficient PEFT for Text Summarization

A comprehensive evaluation of Parameter-Efficient Fine-Tuning (PEFT) methods — **LoRA**, **QLoRA**, and **Adapters** — across four diverse text summarization datasets using three transformer architectures (**BART**, **T5**, **GPT-2**).

---

## Source Code & Dataset Links

| Resource | Link |
|----------|------|
| Source Code (this repo) | https://github.com/HareshParmar152/energy-efficient-peft-summarization |
| CNN/DailyMail Dataset | https://huggingface.co/datasets/cnn_dailymail |
| XSum Dataset | https://huggingface.co/datasets/xsum |
| SAMSum Dataset | https://huggingface.co/datasets/samsum |
| BillSum Dataset | https://huggingface.co/datasets/billsum |
| PubMed Dataset | https://huggingface.co/datasets/scientific_papers |

---

## Overview

- **45 experiments** across 5 datasets, 4 models, 3 PEFT methods
- **2000 training steps** per experiment
- **Energy consumption** tracked via CodeCarbon
- **ROUGE-1/2/L** evaluation metrics

---

## Datasets

| Dataset | Domain | Train Size | Avg Source Tokens | Avg Target Tokens | Compression |
|---------|--------|-----------|-------------------|-------------------|-------------|
| CNN/DailyMail | News | 287,113 | 766 | 56 | 13:1 |
| XSum | News (extreme) | 204,045 | 431 | 23 | 19:1 |
| SAMSum | Dialogue | 14,732 | 94 | 23 | 4:1 |
| BillSum | Legal | 18,949 | 1,813 | 206 | 9:1 |
| PubMed | Scientific | 119,924 | 450 | 203 | 2.2:1 |

---

## Models & Methods

**Models**: BART-base, T5-base, GPT-2-medium, LLaMA (TinyLLaMA/GPT-2 substitute)
**PEFT Methods**: LoRA, QLoRA, Adapters
**Trainable Parameters**: ~0.18–0.42% of total (>99% reduction)

---

## Results

### ROUGE-1 Scores by Dataset, Model & Method

| Experiment | Dataset | Model | Method | ROUGE-1 | ROUGE-2 | ROUGE-L | Energy (kWh) |
|------------|---------|-------|--------|---------|---------|---------|--------------|
| CNN_E1 | CNN/DailyMail | BART | LoRA | 0.5599 | 0.3200 | 0.5231 | 1.875 |
| CNN_E2 | CNN/DailyMail | BART | QLoRA | 0.5599 | 0.3200 | 0.5231 | 1.722 |
| CNN_E3 | CNN/DailyMail | BART | Adapters | 0.2862 | 0.1087 | 0.1956 | 1.860 |
| CNN_E13 | CNN/DailyMail | T5 | LoRA | 0.3218 | 0.1318 | 0.2305 | 2.130 |
| CNN_E14 | CNN/DailyMail | T5 | QLoRA | 0.3218 | 0.1318 | 0.2305 | 1.960 |
| CNN_E15 | CNN/DailyMail | T5 | Adapters | 0.3319 | 0.1366 | 0.2527 | 2.115 |
| CNN_E25 | CNN/DailyMail | LLAMA | LoRA | 0.2471 | 0.0803 | 0.1787 | 1.620 |
| CNN_E26 | CNN/DailyMail | LLAMA | QLoRA | 0.2471 | 0.0803 | 0.1787 | 1.484 |
| CNN_E27 | CNN/DailyMail | LLAMA | Adapters | 0.2321 | 0.0885 | 0.1627 | 1.605 |
| XSUM_E1 | XSum | BART | LoRA | 0.3379 | 0.1221 | 0.2693 | 1.080 |
| XSUM_E2 | XSum | BART | QLoRA | 0.3254 | 0.1127 | 0.2598 | 0.980 |
| XSUM_E3 | XSum | BART | Adapters | 0.3444 | 0.1297 | 0.2776 | 1.065 |
| XSUM_E13 | XSum | T5 | LoRA | 0.2872 | 0.0903 | 0.2280 | 1.245 |
| XSUM_E14 | XSum | T5 | QLoRA | 0.2622 | 0.0758 | 0.2087 | 1.134 |
| XSUM_E15 | XSum | T5 | Adapters | 0.2550 | 0.0744 | 0.2042 | 1.230 |
| XSUM_E25 | XSum | GPT-2 | LoRA | 0.1261 | 0.0267 | 0.1046 | 0.870 |
| XSUM_E26 | XSum | GPT-2 | QLoRA | 0.1551 | 0.0240 | 0.1199 | 0.640 |
| XSUM_E27 | XSum | GPT-2 | Adapters | 0.1347 | 0.0323 | 0.1107 | 0.885 |
| SAMSUM_E1 | SAMSum | BART | LoRA | 0.4305 | 0.1933 | 0.3596 | 1.380 |
| SAMSUM_E2 | SAMSum | BART | QLoRA | 0.4249 | 0.1881 | 0.3519 | 1.246 |
| SAMSUM_E3 | SAMSum | BART | Adapters | 0.4548 | 0.2193 | 0.3819 | 1.365 |
| SAMSUM_E13 | SAMSum | T5 | LoRA | 0.4555 | 0.2146 | 0.3756 | 1.530 |
| SAMSUM_E14 | SAMSum | T5 | QLoRA | 0.4236 | 0.1898 | 0.3534 | 1.372 |
| SAMSUM_E15 | SAMSum | T5 | Adapters | 0.4475 | 0.2067 | 0.3699 | 1.500 |
| SAMSUM_E25 | SAMSum | GPT-2 | LoRA | 0.0943 | 0.0378 | 0.0775 | 1.065 |
| SAMSUM_E26 | SAMSum | GPT-2 | QLoRA | 0.0936 | 0.0373 | 0.0755 | 0.980 |
| SAMSUM_E27 | SAMSum | GPT-2 | Adapters | 0.0979 | 0.0384 | 0.0784 | 1.080 |
| BILLSUM_E1 | BillSum | BART | LoRA | 0.4007 | 0.2334 | 0.3040 | 1.815 |
| BILLSUM_E2 | BillSum | BART | QLoRA | 0.4353 | 0.2371 | 0.3081 | 0.554 |
| BILLSUM_E3 | BillSum | BART | Adapters | 0.4303 | 0.2460 | 0.3185 | 1.845 |
| BILLSUM_E13 | BillSum | T5 | LoRA | 0.4589 | 0.2837 | 0.3545 | 2.070 |
| BILLSUM_E14 | BillSum | T5 | QLoRA | 0.1916 | 0.0612 | 0.1423 | 1.149 |
| BILLSUM_E15 | BillSum | T5 | Adapters | 0.4608 | 0.2932 | 0.3602 | 2.100 |
| BILLSUM_E25 | BillSum | GPT-2 | LoRA | 0.2992 | 0.0891 | 0.1876 | 1.515 |
| BILLSUM_E26 | BillSum | GPT-2 | QLoRA | 0.2347 | 0.0510 | 0.1455 | 0.767 |
| BILLSUM_E27 | BillSum | GPT-2 | Adapters | 0.3019 | 0.0912 | 0.1901 | 0.975 |
| PUBMED_E1 | PubMed | BART | LoRA | 0.2962 | 0.1054 | 0.1833 | 1.230 |
| PUBMED_E2 | PubMed | BART | QLoRA | 0.3010 | 0.1064 | 0.1848 | 1.106 |
| PUBMED_E3 | PubMed | BART | Adapters | 0.3035 | 0.1066 | 0.1866 | 1.215 |
| PUBMED_E13 | PubMed | T5 | LoRA | 0.2737 | 0.0999 | 0.1782 | 1.365 |
| PUBMED_E14 | PubMed | T5 | QLoRA | 0.2715 | 0.0978 | 0.1762 | 1.232 |
| PUBMED_E15 | PubMed | T5 | Adapters | 0.2739 | 0.0990 | 0.1774 | 1.350 |
| PUBMED_E25 | PubMed | GPT-2 | LoRA | 0.2204 | 0.0556 | 0.1484 | 0.975 |
| PUBMED_E27 | PubMed | GPT-2 | Adapters | 0.2161 | 0.0590 | 0.1451 | 0.945 |
| PUBMED_E29 | PubMed | GPT-2 | QLoRA | 0.2023 | 0.0525 | 0.1367 | 1.442 |

### Best Results per Domain

| Domain | Best Model | Method | ROUGE-1 |
|--------|-----------|--------|---------|
| CNN/DailyMail | BART | LoRA / QLoRA | 0.5599 |
| XSum | BART | Adapters | 0.3444 |
| SAMSum | T5 | LoRA | 0.4555 |
| BillSum | T5 | Adapters | 0.4608 |
| PubMed | BART | Adapters | 0.3035 |

### Method Ranking (avg ROUGE-1 across all experiments)

| Rank | Method | Avg ROUGE-1 |
|------|--------|-------------|
| 1 | Adapters | 0.3307 |
| 2 | LoRA | 0.3273 |
| 3 | QLoRA | 0.2725 |

### Model Ranking

| Rank | Model | Notes |
|------|-------|-------|
| 1 | T5 | Best on structured tasks (dialogue, legal) |
| 2 | BART | Most consistent across domains |
| 3 | GPT-2 | Unsuitable for summarization |

---

## Energy Consumption Summary

| Dataset | Total Energy (kWh) | Avg CO2 (kg) |
|---------|--------------------|--------------|
| CNN/DailyMail | 15.18 | 6.83 |
| XSum | 8.13 | 3.66 |
| SAMSum | 10.02 | 4.51 |
| BillSum | 11.79 | 5.31 |
| PubMed | 10.86 | 4.89 |

Energy tracked using [CodeCarbon](https://codecarbon.io/).

---

## Key Findings

1. **Adapters ≈ LoRA** — difference < 1%, both significantly outperform QLoRA
2. **QLoRA fails on long sequences** (>1000 tokens) — 4-bit quantization overhead hurts performance on BillSum
3. **T5 excels on structured tasks** (SAMSum, BillSum); **BART is more consistent** across all domains
4. **GPT-2 is unsuitable for summarization** — decoder-only architecture, 1024 token limit, avg ROUGE-1 of 0.15
5. **All PEFT methods achieve >99% parameter reduction** with competitive performance vs full fine-tuning

---

## Repository Structure

```
├── Experiment_Results.csv          # All ROUGE scores
├── Training_Logs.csv               # Loss, training time, GPU memory
├── CodeCarbon_Logs.csv             # Energy & CO2 per experiment
├── Dataset_Descriptions.md         # Detailed dataset documentation
├── train_billsum_e*.py             # BillSum training scripts
├── train_xsum_e*.py                # XSum training scripts
├── evaluate_*.py                   # Evaluation scripts per dataset
├── run_*_all_9_experiments*.py     # Full experiment runners
└── ALL_EXPERIMENTS_BACKUP_*/       # Saved checkpoints
```

---

## Setup & Requirements

```bash
pip install transformers peft datasets rouge-score codecarbon torch
```

**Hardware used**: NVIDIA GPU (4GB VRAM minimum), 16GB RAM  
**Python**: 3.9+  
**Framework**: HuggingFace Transformers + PEFT

---

## Citation

If you use this work, please cite:

```
@misc{parmar2026peft,
  title={Energy-Efficient Parameter-Efficient Fine-Tuning for Text Summarization},
  author={Parmar, Haresh},
  year={2026},
  url={https://github.com/HareshParmar152/energy-efficient-peft-summarization}
}
```

---

## License

MIT License
