from pathlib import Path

BASE_PATH = Path("E:/Pending Experiment data")

# Test SAMSum E1
checkpoint_base = BASE_PATH / "SAMSum_Experiments" / "BART" / "checkpoints" / "E1_BART_SAMSum_LoRA"
checkpoint_path = checkpoint_base / "final_model"

print(f"Checking: {checkpoint_base}")
print(f"final_model exists: {checkpoint_path.exists()}")
print(f"adapter_config.json exists: {(checkpoint_base / 'adapter_config.json').exists()}")

if not checkpoint_path.exists():
    if (checkpoint_base / "adapter_config.json").exists():
        checkpoint_path = checkpoint_base
        print(f"✓ Using checkpoint from base folder: {checkpoint_path}")
    else:
        print(f"✗ Checkpoint not found")
else:
    print(f"✓ Using final_model folder: {checkpoint_path}")

print(f"\nFinal checkpoint path: {checkpoint_path}")
print(f"Final path exists: {checkpoint_path.exists()}")
