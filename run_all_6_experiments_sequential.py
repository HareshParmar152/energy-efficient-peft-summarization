#!/usr/bin/env python3
"""
Run All 6 Pending Experiments Sequentially
Automatically starts next experiment when previous completes
"""

import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Experiment order (easiest to hardest)
EXPERIMENTS = [
    {"script": "train_billsum_e25.py", "name": "E25 - BillSum GPT-2 LoRA", "difficulty": "EASIEST"},
    {"script": "train_billsum_e27.py", "name": "E27 - BillSum GPT-2 Adapters", "difficulty": "EASY"},
    {"script": "train_xsum_e26.py", "name": "E26 - XSum GPT-2 QLoRA", "difficulty": "MEDIUM"},
    {"script": "train_billsum_e2.py", "name": "E2 - BillSum BART QLoRA", "difficulty": "HARD"},
    {"script": "train_billsum_e14.py", "name": "E14 - BillSum T5 QLoRA", "difficulty": "HARD"},
    {"script": "train_billsum_e26.py", "name": "E26 - BillSum GPT-2 QLoRA", "difficulty": "HARDEST"},
]

def print_banner(text):
    print("\n" + "="*80)
    print(text.center(80))
    print("="*80 + "\n")

def run_experiment(exp_num, exp_info):
    """Run a single experiment"""
    script = exp_info["script"]
    name = exp_info["name"]
    difficulty = exp_info["difficulty"]
    
    print_banner(f"EXPERIMENT {exp_num}/6: {name} ({difficulty})")
    
    start_time = time.time()
    
    try:
        # Run the training script
        result = subprocess.run(
            [sys.executable, script],
            check=True,
            capture_output=False,
            text=True
        )
        
        end_time = time.time()
        duration_minutes = (end_time - start_time) / 60
        
        print_banner(f"✅ EXPERIMENT {exp_num}/6 COMPLETED - {name}")
        print(f"Duration: {duration_minutes:.1f} minutes")
        print(f"Status: SUCCESS")
        
        return True, duration_minutes
        
    except subprocess.CalledProcessError as e:
        end_time = time.time()
        duration_minutes = (end_time - start_time) / 60
        
        print_banner(f"❌ EXPERIMENT {exp_num}/6 FAILED - {name}")
        print(f"Duration: {duration_minutes:.1f} minutes")
        print(f"Status: FAILED")
        print(f"Error: Training failed (likely GPU OOM)")
        
        return False, duration_minutes
    
    except Exception as e:
        end_time = time.time()
        duration_minutes = (end_time - start_time) / 60
        
        print_banner(f"❌ EXPERIMENT {exp_num}/6 ERROR - {name}")
        print(f"Duration: {duration_minutes:.1f} minutes")
        print(f"Status: ERROR")
        print(f"Error: {e}")
        
        return False, duration_minutes

def main():
    print_banner("SEQUENTIAL TRAINING OF 6 PENDING EXPERIMENTS")
    print("This will run all 6 experiments one after another")
    print("Each experiment will start automatically when the previous completes")
    print("\nOrder: Easiest → Hardest")
    print("Expected total time: 10-15 hours")
    print("\nPress Ctrl+C to stop at any time")
    
    input("\nPress ENTER to start...")
    
    overall_start = time.time()
    results = []
    
    for i, exp_info in enumerate(EXPERIMENTS, 1):
        success, duration = run_experiment(i, exp_info)
        
        results.append({
            "experiment": exp_info["name"],
            "script": exp_info["script"],
            "success": success,
            "duration_minutes": duration
        })
        
        # Wait a bit between experiments for GPU cleanup
        if i < len(EXPERIMENTS):
            print("\nWaiting 30 seconds for GPU cleanup...")
            time.sleep(30)
    
    # Final summary
    overall_end = time.time()
    total_duration = (overall_end - overall_start) / 60
    
    print_banner("ALL EXPERIMENTS COMPLETED")
    
    print("RESULTS SUMMARY:")
    print("-" * 80)
    
    successful = 0
    failed = 0
    
    for i, result in enumerate(results, 1):
        status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
        print(f"{i}. {result['experiment']}")
        print(f"   Status: {status}")
        print(f"   Duration: {result['duration_minutes']:.1f} minutes")
        print()
        
        if result["success"]:
            successful += 1
        else:
            failed += 1
    
    print("-" * 80)
    print(f"Total experiments: {len(EXPERIMENTS)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success rate: {(successful/len(EXPERIMENTS)*100):.1f}%")
    print(f"Total duration: {total_duration:.1f} minutes ({total_duration/60:.1f} hours)")
    print("-" * 80)
    
    print("\nNEXT STEPS:")
    print("1. Check the results JSON files for each successful experiment")
    print("2. Run evaluation scripts for successful experiments")
    print("3. Update your research summary documents")
    
    if successful > 0:
        print(f"\n✅ {successful} experiments completed successfully!")
        print(f"   New total: {39 + successful}/45 experiments ({(39+successful)/45*100:.1f}%)")
    
    if failed > 0:
        print(f"\n⚠️  {failed} experiments failed (likely GPU memory limitations)")
        print("   This is expected and documented in your research")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + "="*80)
        print("TRAINING INTERRUPTED BY USER")
        print("="*80)
        print("\nYou can resume by running individual scripts:")
        print("python train_billsum_e25.py")
        print("python train_billsum_e27.py")
        print("etc.")
        sys.exit(1)
