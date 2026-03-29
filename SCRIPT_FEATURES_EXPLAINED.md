# Script Features - run_pubmed_all_9_experiments_2000steps.py

## ✅ Feature 1: Auto-Skip Completed Experiments

**How it works:**
1. Before running each experiment, checks for result file:
   - `E:/Pending Experiment data/PubMed_Experiments/{MODEL}/results/{EXP_ID}_results.json`
2. If file exists AND status="success" → **SKIP**
3. If file doesn't exist OR status="failed" → **RUN**

**Example:**
```
Checking E1... Found E1_results.json with status="success" → SKIP ✅
Checking E2... Found E2_results.json with status="success" → SKIP ✅
Checking E27... Not found → RUN 🔄
```

---

## ✅ Feature 2: Complete Training Information Collection

### Per Experiment Information Saved:

**File:** `{EXP_ID}_results.json`

**Contains:**
```json
{
  "experiment_id": "E1",
  "experiment_name": "E1_BART_PubMed_LoRA",
  "model": "facebook/bart-base",
  "model_type": "bart",
  "method": "LoRA",
  "dataset": "pubmed",
  "status": "success",
  "timestamp": "20260224_165306",
  "config": {
    "max_steps": 2000,
    "batch_size": 4,
    "learning_rate": 0.0003,
    ...
  },
  "trainable_parameters": 442368,
  "total_parameters": 139862784,
  "trainable_percentage": 0.316,
  "train_runtime_seconds": 5172,
  "train_runtime_minutes": 86.2,
  "train_loss": 2.1234,
  "train_samples_per_second": 12.5,
  "train_steps_per_second": 0.387,
  "emissions_kg_co2": 0.045,
  "checkpoint_dir": "path/to/checkpoints",
  "results_dir": "path/to/results"
}
```

---

## ✅ Feature 3: Master Summary at End

**File:** `pubmed_all_summary_{timestamp}.json`

**Contains:**
```json
{
  "timestamp": "20260224_165306",
  "config": {...},
  "total_experiments": 9,
  "successful": 7,
  "failed": 2,
  "results": [
    {...all E1 data...},
    {...all E2 data...},
    {...all E3 data...},
    ...
  ]
}
```

**Console Output:**
```
================================================================================
ALL PUBMED EXPERIMENTS COMPLETED
================================================================================
Total experiments: 9
Successful: 7
Failed: 2

  [OK] E1: LoRA - Time: 86.2 min
  [OK] E3: Adapters - Time: 89.3 min
  [OK] E2: QLoRA - Time: 131.9 min
  [OK] E13: LoRA - Time: 211.6 min
  [OK] E15: Adapters - Time: 231.3 min
  [OK] E14: QLoRA - Time: 242.8 min
  [OK] E25: LoRA - Time: 768.8 min
  [FAIL] E27: Adapters - Time: 0.0 min
  [FAIL] E26: QLoRA - Time: 0.0 min

Master summary saved to: E:\Pending Experiment data\PubMed_Experiments\pubmed_all_summary_20260224_165306.json
Log file: E:\Pending Experiment data\PubMed_Experiments\logs\pubmed_all_experiments_20260224_165306.log
================================================================================
```

---

## Information Collected for Each Experiment

### Training Metrics:
- ✅ Training loss
- ✅ Training runtime (seconds & minutes)
- ✅ Samples per second
- ✅ Steps per second
- ✅ Learning rate schedule

### Model Information:
- ✅ Model name and type
- ✅ Total parameters
- ✅ Trainable parameters
- ✅ Trainable percentage
- ✅ PEFT method used

### Energy Metrics:
- ✅ CO2 emissions (kg)
- ✅ Energy consumption

### Configuration:
- ✅ All hyperparameters
- ✅ Batch size
- ✅ Gradient accumulation
- ✅ Learning rate
- ✅ Max steps
- ✅ Dataset info

### Paths:
- ✅ Checkpoint directory
- ✅ Results directory
- ✅ Log file location

---

## How to Use

**Run the script:**
```cmd
python run_pubmed_all_9_experiments_2000steps.py
```

**What happens:**
1. Checks each experiment (E1, E3, E2, E13, E15, E14, E25, E27, E26)
2. Skips completed ones automatically
3. Runs pending ones sequentially
4. Saves detailed results for each
5. Creates master summary at end

**No manual intervention needed!** Just start it and let it run.

---

## Summary Files Location

```
E:/Pending Experiment data/PubMed_Experiments/
├── BART/results/
│   ├── E1_results.json
│   ├── E2_results.json
│   └── E3_results.json
├── T5/results/
│   ├── E13_results.json
│   ├── E14_results.json
│   └── E15_results.json
├── GPT2/results/
│   ├── E25_results.json
│   ├── E26_results.json
│   └── E27_results.json
├── pubmed_all_summary_20260224_165306.json  ← Master summary
└── logs/
    └── pubmed_all_experiments_20260224_165306.log  ← Full log
```

All information is automatically collected and saved! 🎉
