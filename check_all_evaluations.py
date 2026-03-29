#!/usr/bin/env python3
"""Check all evaluation results across all datasets"""

import json
from pathlib import Path

BASE_PATH = Path("E:/Pending Experiment data")

datasets = {
    "PubMed": {
        "path": BASE_PATH / "PubMed_Experiments" / "evaluation_results",
        "expected": ["E1", "E2", "E3", "E13", "E14", "E15", "E25", "E27", "E29"]
    },
    "XSum": {
        "path": BASE_PATH / "XSum_Experiments" / "evaluation_results",
        "expected": ["E1", "E2", "E3", "E13", "E14", "E15", "E25", "E27"]  # E26 failed training
    },
    "SAMSum": {
        "path": BASE_PATH / "SAMSum_Experiments" / "evaluation_results",
        "expected": ["E1", "E2", "E3", "E13", "E14", "E15", "E25", "E26", "E27"]
    },
    "BillSum": {
        "path": BASE_PATH / "BillSum_Experiments" / "evaluation_results",
        "expected": ["E1", "E3", "E13", "E15"]  # Only 4 trained
    }
}

print("="*80)
print("COMPLETE EVALUATION STATUS CHECK")
print("="*80)

total_evaluated = 0
total_expected = 0

for dataset_name, dataset_info in datasets.items():
    print(f"\n{'='*80}")
    print(f"{dataset_name} Dataset")
    print(f"{'='*80}")
    
    results_path = dataset_info["path"]
    expected_exps = dataset_info["expected"]
    
    if not results_path.exists():
        print(f"❌ Results folder not found: {results_path}")
        print(f"Expected: {len(expected_exps)} experiments")
        print(f"Found: 0 experiments")
        print(f"Status: NOT EVALUATED")
        total_expected += len(expected_exps)
        continue
    
    # Find all evaluation JSON files
    result_files = list(results_path.glob("*_evaluation.json"))
    evaluated_exps = [f.stem.split("_")[0] for f in result_files]
    
    print(f"Expected: {len(expected_exps)} experiments")
    print(f"Found: {len(evaluated_exps)} experiments")
    print()
    
    # Check each expected experiment
    for exp_id in expected_exps:
        if exp_id in evaluated_exps:
            # Load and show results
            result_file = results_path / f"{exp_id}_evaluation.json"
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)
                    rouge1 = data.get("rouge_scores", {}).get("rouge1", 0)
                    rouge2 = data.get("rouge_scores", {}).get("rouge2", 0)
                    rougeL = data.get("rouge_scores", {}).get("rougeL", 0)
                    method = data.get("method", "Unknown")
                    model = data.get("model_type", "Unknown")
                    
                    print(f"✅ {exp_id} ({model.upper()} {method})")
                    print(f"   ROUGE-1: {rouge1:.4f} | ROUGE-2: {rouge2:.4f} | ROUGE-L: {rougeL:.4f}")
                    total_evaluated += 1
            except Exception as e:
                print(f"✅ {exp_id} (file exists but error reading: {e})")
                total_evaluated += 1
        else:
            print(f"❌ {exp_id} - NOT EVALUATED")
    
    total_expected += len(expected_exps)
    
    # Status
    if len(evaluated_exps) == len(expected_exps):
        print(f"\n✅ Status: COMPLETE ({len(evaluated_exps)}/{len(expected_exps)})")
    else:
        print(f"\n⏳ Status: INCOMPLETE ({len(evaluated_exps)}/{len(expected_exps)})")

print("\n" + "="*80)
print("OVERALL SUMMARY")
print("="*80)
print(f"Total Evaluated: {total_evaluated}/{total_expected} ({total_evaluated/total_expected*100:.1f}%)")
print()
print("Dataset Breakdown:")
for dataset_name, dataset_info in datasets.items():
    results_path = dataset_info["path"]
    expected = len(dataset_info["expected"])
    if results_path.exists():
        found = len(list(results_path.glob("*_evaluation.json")))
    else:
        found = 0
    status = "✅" if found == expected else "⏳"
    print(f"  {status} {dataset_name}: {found}/{expected}")

print("="*80)
