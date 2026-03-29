#!/usr/bin/env python3
"""
Download datasets locally to avoid Hugging Face loading issues
"""

import os
from pathlib import Path
from datasets import load_dataset

# Base path for local datasets
LOCAL_DATASETS_PATH = Path("E:/Pending Experiment data/local_datasets")
LOCAL_DATASETS_PATH.mkdir(parents=True, exist_ok=True)

print("="*80)
print("DOWNLOADING DATASETS LOCALLY")
print("="*80)
print(f"Save location: {LOCAL_DATASETS_PATH}")
print()

# List of datasets to try downloading
datasets_to_download = [
    {
        "name": "SAMSum",
        "paths": ["Samsung/samsum", "samsum", "knkarthick/samsum"],
        "save_name": "samsum"
    },
    {
        "name": "Multi-News",
        "paths": ["alexfabbri/multi_news", "multi_news"],
        "save_name": "multinews"
    },
    {
        "name": "BillSum",
        "paths": ["billsum"],
        "save_name": "billsum"
    },
    {
        "name": "ArXiv",
        "paths": ["scientific_papers"],
        "config": "arxiv",
        "save_name": "arxiv"
    }
]

def download_dataset(name, paths, save_name, config=None):
    """Try to download dataset from multiple paths"""
    print(f"\n{'='*80}")
    print(f"Attempting to download: {name}")
    print(f"{'='*80}")
    
    save_path = LOCAL_DATASETS_PATH / save_name
    
    for path in paths:
        try:
            print(f"\nTrying: {path}")
            if config:
                print(f"Config: {config}")
                dataset = load_dataset(path, config)
            else:
                dataset = load_dataset(path)
            
            print(f"✅ SUCCESS! Downloaded from: {path}")
            print(f"Train samples: {len(dataset['train'])}")
            if 'validation' in dataset:
                print(f"Validation samples: {len(dataset['validation'])}")
            if 'test' in dataset:
                print(f"Test samples: {len(dataset['test'])}")
            
            # Save to disk
            print(f"\nSaving to: {save_path}")
            dataset.save_to_disk(str(save_path))
            print(f"✅ Saved successfully!")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            continue
    
    print(f"\n❌ Could not download {name} from any source")
    return False

# Download each dataset
results = {}
for ds_info in datasets_to_download:
    success = download_dataset(
        ds_info["name"],
        ds_info["paths"],
        ds_info["save_name"],
        ds_info.get("config")
    )
    results[ds_info["name"]] = success

# Summary
print("\n" + "="*80)
print("DOWNLOAD SUMMARY")
print("="*80)
for name, success in results.items():
    status = "✅ SUCCESS" if success else "❌ FAILED"
    print(f"{name}: {status}")

print("\n" + "="*80)
print("NEXT STEPS")
print("="*80)
print("Successfully downloaded datasets can be loaded using:")
print("dataset = load_from_disk('E:/Pending Experiment data/local_datasets/<dataset_name>')")
print("="*80)
