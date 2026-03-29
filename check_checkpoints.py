#!/usr/bin/env python3
"""
Checkpoint Verification Script
Checks if all required checkpoints exist before evaluation
"""

from pathlib import Path

BASE_PATH = Path("E:/Pending Experiment data")

# Define all experiments to check
CHECKPOINTS = {
    "PubMed": [
        ("E1", "BART", "E1_BART_PubMed_LoRA"),
        ("E2", "BART", "E2_BART_PubMed_QLoRA"),
        ("E3", "BART", "E3_BART_PubMed_Adapters"),
        ("E13", "T5", "E13_T5_PubMed_LoRA"),
        ("E14", "T5", "E14_T5_PubMed_QLoRA"),
        ("E15", "T5", "E15_T5_PubMed_Adapters"),
        ("E25", "GPT2", "E25_GPT2_PubMed_LoRA"),
        ("E27", "GPT2", "E27_GPT2_PubMed_Adapters"),
        ("E29", "GPT2", "E29_GPT2_PubMed_QLoRA"),
    ],
    "XSum": [
        ("E1", "BART", "E1_BART_XSum_LoRA"),
        ("E2", "BART", "E2_BART_XSum_QLoRA"),
        ("E3", "BART", "E3_BART_XSum_Adapters"),
        ("E13", "T5", "E13_T5_XSum_LoRA"),
        ("E14", "T5", "E14_T5_XSum_QLoRA"),
        ("E15", "T5", "E15_T5_XSum_Adapters"),
        ("E25", "GPT2", "E25_GPT2_XSum_LoRA"),
        ("E27", "GPT2", "E27_GPT2_XSum_Adapters"),
    ],
    "SAMSum": [
        ("E1", "BART", "E1_BART_SAMSum_LoRA"),
        ("E2", "BART", "E2_BART_SAMSum_QLoRA"),
        ("E3", "BART", "E3_BART_SAMSum_Adapters"),
        ("E13", "T5", "E13_T5_SAMSum_LoRA"),
        ("E14", "T5", "E14_T5_SAMSum_QLoRA"),
        ("E15", "T5", "E15_T5_SAMSum_Adapters"),
        ("E25", "GPT2", "E25_GPT2_SAMSum_LoRA"),
        ("E26", "GPT2", "E26_GPT2_SAMSum_QLoRA"),
        ("E27", "GPT2", "E27_GPT2_SAMSum_Adapters"),
    ],
    "BillSum": [
        ("E1", "BART", "E1_BART_BillSum_LoRA"),
        ("E3", "BART", "E3_BART_BillSum_Adapters"),
        ("E13", "T5", "E13_T5_BillSum_LoRA"),
        ("E15", "T5", "E15_T5_BillSum_Adapters"),
    ]
}

print("="*80)
print("CHECKPOINT VERIFICATION")
print("="*80)
print()

total_checkpoints = 0
found_checkpoints = 0
missing_checkpoints = []

for dataset, experiments in CHECKPOINTS.items():
    print(f"\n{dataset}:")
    print("-" * 40)
    
    for exp_id, model_folder, checkpoint_name in experiments:
        total_checkpoints += 1
        checkpoint_path = BASE_PATH / f"{dataset}_Experiments" / model_folder / "checkpoints" / checkpoint_name
        
        if checkpoint_path.exists():
            print(f"  ✓ {exp_id} ({checkpoint_name})")
            found_checkpoints += 1
        else:
            print(f"  ✗ {exp_id} ({checkpoint_name}) - MISSING")
            missing_checkpoints.append(f"{dataset}/{exp_id}")

print()
print("="*80)
print("SUMMARY")
print("="*80)
print(f"Total checkpoints: {total_checkpoints}")
print(f"Found: {found_checkpoints}")
print(f"Missing: {len(missing_checkpoints)}")
print()

if missing_checkpoints:
    print("Missing checkpoints:")
    for checkpoint in missing_checkpoints:
        print(f"  - {checkpoint}")
    print()
    print("⚠️  Some checkpoints are missing. Evaluation will skip these experiments.")
else:
    print("✅ All checkpoints found! Ready to run evaluation.")

print("="*80)
