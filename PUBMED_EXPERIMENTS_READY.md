# PubMed Experiments Ready - Next Dataset

## ✅ Rules File Updated

Changed all LLaMA references to GPT-2:
- E25-E27: GPT-2 + XSum ✓
- E28-E30: GPT-2 + PubMed (Ready)
- E31-E33: GPT-2 + Multi-News (Future)
- E34-E36: GPT-2 + Newsroom (Future)

## 📋 Dataset Order

According to your research:
1. ✅ **CNN/DailyMail** - Already completed (BART, T5, LLaMA)
2. ✅ **XSum** - Almost done (E26 finishing in ~2 hours)
3. ⏳ **PubMed** - Ready to start (E28, E29, E30)
4. ⏳ **Multi-News** - Future
5. ⏳ **Newsroom** - Future

**Note**: Reddit TIFU was skipped due to dataset issues (as you mentioned)

## 🔬 PubMed Experiments Configuration

### Experiments:
- **E28**: GPT-2 Medium + LoRA
- **E29**: GPT-2 Medium + QLoRA
- **E30**: GPT-2 Medium + Adapters

### Dataset:
- **Name**: PubMed Summarization
- **Source**: `ccdv/pubmed-summarization`
- **Type**: Biomedical literature abstracts
- **Characteristics**: 
  - Scientific/medical terminology
  - Longer abstracts than XSum
  - More formal language

### Configuration:
```python
{
    "dataset": "pubmed",
    "max_steps": 2000,
    "batch_size": 6,  # Smaller for longer abstracts
    "gradient_accumulation_steps": 3,
    "learning_rate": 2e-4,
    "max_length": 512,  # PubMed abstracts are longer
    "save_steps": 500,
    "logging_steps": 50
}
```

### Why Different from XSum:
- **Batch size**: 6 (vs 8 for XSum) - PubMed abstracts are longer
- **Max length**: 512 (vs 256 for XSum) - Need more tokens for biomedical text
- **Gradient accumulation**: 3 (vs 2) - Maintain effective batch size of 18

## 📁 Output Location

```
E:\Pending Experiment data\PubMed_Experiments\
├── GPT2\
│   ├── checkpoints\
│   │   ├── E28_GPT2_PubMed_LoRA\
│   │   ├── E29_GPT2_PubMed_QLoRA\
│   │   └── E30_GPT2_PubMed_Adapters\
│   └── results\
│       ├── E28_results.json
│       ├── E29_results.json
│       └── E30_results.json
└── logs\
    └── pubmed_gpt2_experiments_*.log
```

## ⏱️ Expected Timeline

### Per Experiment:
- **E28 (LoRA)**: ~1.5-2 hours
- **E29 (QLoRA)**: ~2-2.5 hours
- **E30 (Adapters)**: ~2-2.5 hours

### Total: ~6-7 hours

**Note**: Slightly longer than XSum due to:
- Longer sequences (512 vs 256 tokens)
- Smaller batch size (6 vs 8)
- More complex biomedical vocabulary

## 🚀 How to Start

### After XSum E26 Completes:

**Option 1: Batch File**
```cmd
RUN_PUBMED_EXPERIMENTS.bat
```

**Option 2: Direct Command**
```cmd
C:\Users\hares\AppData\Local\Programs\Python\Python313\python.exe run_pubmed_experiments_2000steps.py
```

## 📊 Progress Tracking

### Completed:
- ✅ CNN/DailyMail: BART (3), T5 (3), LLaMA (3) = 9 experiments
- ✅ XSum: BART (3), T5 (3), GPT-2 (2/3) = 8 experiments

### Running:
- ⏳ XSum: GPT-2 E26 (QLoRA) - ~2 hours remaining

### Next:
- ⏳ PubMed: GPT-2 (3) - Ready to start

### Total Progress:
- **Completed**: 17/36 experiments (47%)
- **Running**: 1/36 (3%)
- **Remaining**: 18/36 (50%)

## 🔍 What's Different in PubMed Script

### 1. Dataset Loading:
```python
dataset = load_dataset("ccdv/pubmed-summarization", "document")
```

### 2. Preprocessing:
```python
for article, abstract in zip(examples["article"], examples["abstract"]):
    prompt = f"Summarize the following biomedical article:\n\n{article}\n\nAbstract: {abstract}"
```

### 3. Batch Configuration:
- Smaller batches (6 vs 8) for longer sequences
- Higher gradient accumulation (3 vs 2)
- Longer max_length (512 vs 256)

## ✅ Ready to Start

Everything is configured and ready:
- ✅ Script created: `run_pubmed_experiments_2000steps.py`
- ✅ Batch file created: `RUN_PUBMED_EXPERIMENTS.bat`
- ✅ Rules file updated: LLaMA → GPT-2
- ✅ Paths configured: `E:\Pending Experiment data\PubMed_Experiments\`

**Wait for XSum E26 to complete (~2 hours), then start PubMed experiments!**

---

**Created**: February 23, 2026  
**Status**: Ready to run after XSum completes
