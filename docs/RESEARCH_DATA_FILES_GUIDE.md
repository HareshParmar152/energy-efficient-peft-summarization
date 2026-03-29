# 📁 RESEARCH DATA FILES - COMPLETE GUIDE

**Date**: March 12, 2026  
**Purpose**: Guide to creating all required data files for research paper submission  
**Status**: Ready to generate

---

## 📋 REQUIRED FILES FOR RESEARCH PAPER

### 1. Research_Proposal.docx
**Purpose**: Original research proposal document  
**Status**: ✅ Available (see below for content)  
**Location**: To be created from existing markdown files

### 2. Experiment_Results.csv
**Purpose**: Complete experimental results in CSV format  
**Status**: ✅ Can be generated from existing data  
**Contains**: All 39 experiments with ROUGE scores

### 3. ROUGE_Scores.xlsx
**Purpose**: ROUGE scores in Excel format with charts  
**Status**: ✅ Can be generated from existing data  
**Contains**: ROUGE-1, ROUGE-2, ROUGE-L for all experiments

### 4. Training_Logs.csv
**Purpose**: Training metrics and logs  
**Status**: ✅ Available in experiment folders  
**Contains**: Loss, training time, steps, etc.

### 5. CodeCarbon_Logs.csv
**Purpose**: Energy consumption and carbon emissions  
**Status**: ⚠️ Need to check if CodeCarbon was enabled  
**Contains**: Energy usage, CO2 emissions, duration

### 6. Dataset_Descriptions.docx
**Purpose**: Detailed description of all 5 datasets  
**Status**: ✅ Can be created from existing documentation  
**Contains**: Dataset characteristics, statistics, examples

### 7. Literature_Papers.pdf
**Purpose**: Collection of related work papers  
**Status**: ⚠️ Need to compile references  
**Contains**: Key papers cited in research

---

## 📊 FILE 1: EXPERIMENT_RESULTS.CSV

This file will contain all 39 experiments with complete metrics.

### Columns:
- Experiment_ID
- Dataset
- Model
- Method
- ROUGE-1
- ROUGE-2
- ROUGE-L
- Training_Time_Hours
- Trainable_Parameters
- Total_Parameters
- Parameter_Efficiency_Percent
- Status

### Sample Data:
```csv
Experiment_ID,Dataset,Model,Method,ROUGE-1,ROUGE-2,ROUGE-L,Training_Time_Hours,Trainable_Parameters,Total_Parameters,Parameter_Efficiency_Percent,Status
CNN_E1,CNN/DailyMail,BART,LoRA,0.5599,0.3200,0.5231,12.5,0.38,100,99.62,Complete
CNN_E2,CNN/DailyMail,BART,QLoRA,0.5599,0.3200,0.5231,12.3,0.38,100,99.62,Complete
...
```

I'll create this file next.

---

## 📈 FILE 2: ROUGE_SCORES.XLSX

This Excel file will contain:

### Sheet 1: All Scores
- Complete ROUGE scores for all 39 experiments
- Formatted table with conditional formatting

### Sheet 2: By Dataset
- Pivot table showing scores by dataset
- Charts comparing datasets

### Sheet 3: By Model
- Pivot table showing scores by model
- Charts comparing models

### Sheet 4: By Method
- Pivot table showing scores by method
- Charts comparing methods

### Sheet 5: Top Performers
- Top 10 experiments ranked by ROUGE-1
- Visualization

---

## 📝 FILE 3: TRAINING_LOGS.CSV

This file will contain training metrics from all experiments.

### Columns:
- Experiment_ID
- Dataset
- Model
- Method
- Epoch
- Step
- Training_Loss
- Learning_Rate
- Gradient_Norm
- Timestamp

### Data Source:
Training logs are stored in:
- `E:\Pending Experiment data\{Dataset}_Experiments\logs\`
- `ALL_EXPERIMENTS_BACKUP_20260212_180205/01_COMPLETED_EXPERIMENTS/CNN_DailyMail/`

---

## 🌱 FILE 4: CODECARBON_LOGS.CSV

This file tracks energy consumption and carbon emissions.

### Columns:
- Experiment_ID
- Dataset
- Model
- Method
- Duration_Seconds
- Energy_Consumed_kWh
- CO2_Emissions_kg
- CPU_Energy_kWh
- GPU_Energy_kWh
- RAM_Energy_kWh

### Status:
Need to check if CodeCarbon tracking was enabled during experiments.

---

## 📚 FILE 5: DATASET_DESCRIPTIONS.DOCX

This document will contain detailed descriptions of all 5 datasets.

### Structure:

**1. CNN/DailyMail**
- Source: CNN and Daily Mail news articles
- Size: 287,113 training pairs
- Domain: News
- Avg Source Length: 600-800 tokens
- Avg Target Length: 100-150 tokens
- Characteristics: Well-structured news articles
- Citation: Hermann et al. (2015)

**2. PubMed**
- Source: Biomedical research abstracts
- Size: 119,924 training pairs
- Domain: Scientific/Medical
- Avg Source Length: 200-300 tokens
- Avg Target Length: 100-150 tokens
- Characteristics: Technical terminology, formal language
- Citation: Cohan et al. (2018)

**3. XSum**
- Source: BBC news articles
- Size: 204,045 training pairs
- Domain: News
- Avg Source Length: 300-400 tokens
- Avg Target Length: 20-30 tokens (extreme compression)
- Characteristics: Extreme summarization, single sentence
- Citation: Narayan et al. (2018)

**4. SAMSum**
- Source: Messenger-like conversations
- Size: 14,732 training pairs
- Domain: Conversational/Dialogue
- Avg Source Length: 400-600 tokens
- Avg Target Length: 50-100 tokens
- Characteristics: Informal language, dialogue structure
- Citation: Gliwa et al. (2019)

**5. BillSum**
- Source: US Congressional bills
- Size: 18,949 training pairs
- Domain: Legal/Legislative
- Avg Source Length: 1000-1500 tokens
- Avg Target Length: 100-200 tokens
- Characteristics: Long documents, formal legal language
- Citation: Kornilova & Eidelman (2019)

---

## 📖 FILE 6: LITERATURE_PAPERS.PDF

This PDF will compile key papers cited in the research.

### Papers to Include:

**PEFT Methods:**
1. LoRA: Hu et al. (2021) - "LoRA: Low-Rank Adaptation of Large Language Models"
2. QLoRA: Dettmers et al. (2023) - "QLoRA: Efficient Finetuning of Quantized LLMs"
3. Adapters: Houlsby et al. (2019) - "Parameter-Efficient Transfer Learning for NLP"

**Models:**
4. BART: Lewis et al. (2019) - "BART: Denoising Sequence-to-Sequence Pre-training"
5. T5: Raffel et al. (2019) - "Exploring the Limits of Transfer Learning with T5"
6. GPT-2: Radford et al. (2019) - "Language Models are Unsupervised Multitask Learners"

**Datasets:**
7. CNN/DailyMail: Hermann et al. (2015)
8. PubMed: Cohan et al. (2018)
9. XSum: Narayan et al. (2018)
10. SAMSum: Gliwa et al. (2019)
11. BillSum: Kornilova & Eidelman (2019)

**Related Work:**
12. Summarization surveys and benchmarks
13. Parameter-efficient fine-tuning surveys
14. Energy-efficient NLP papers

---

## 🚀 NEXT STEPS

I will now create each of these files for you:

1. ✅ Experiment_Results.csv
2. ✅ ROUGE_Scores_Data.csv (for Excel import)
3. ✅ Training_Logs_Summary.csv
4. ✅ Dataset_Descriptions.md (can convert to DOCX)
5. ⚠️ CodeCarbon_Logs.csv (need to check if data exists)
6. ✅ Literature_References.md (list of papers to compile)

---

**Status**: Guide Complete ✅  
**Next**: Creating individual data files

