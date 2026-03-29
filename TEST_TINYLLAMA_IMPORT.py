#!/usr/bin/env python3
"""
Quick test to verify TinyLlama can be loaded
"""

import sys
print(f"Python: {sys.executable}")
print(f"Python Version: {sys.version}")
print()

print("Testing imports...")
try:
    import torch
    print(f"✓ PyTorch: {torch.__version__}")
    print(f"✓ CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"✓ GPU: {torch.cuda.get_device_name(0)}")
        print(f"✓ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
except Exception as e:
    print(f"✗ PyTorch import failed: {e}")
    sys.exit(1)

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    print(f"✓ Transformers imported")
except Exception as e:
    print(f"✗ Transformers import failed: {e}")
    sys.exit(1)

try:
    from peft import LoraConfig, get_peft_model, TaskType
    print(f"✓ PEFT imported")
except Exception as e:
    print(f"✗ PEFT import failed: {e}")
    sys.exit(1)

try:
    from datasets import load_dataset
    print(f"✓ Datasets imported")
except Exception as e:
    print(f"✗ Datasets import failed: {e}")
    sys.exit(1)

print()
print("All imports successful! ✓")
print()
print("Testing TinyLlama model access...")
print("(This will download the model if not cached)")
print()

try:
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    print(f"Loading tokenizer for {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print(f"✓ Tokenizer loaded")
    
    print(f"Loading model {model_name}...")
    print("(This may take a few minutes on first run)")
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print(f"✓ Model loaded")
    
    # Get model size
    total_params = sum(p.numel() for p in model.parameters())
    print(f"✓ Model size: {total_params / 1e9:.2f}B parameters")
    
    # Move to GPU if available
    if torch.cuda.is_available():
        print("Moving model to GPU...")
        model = model.to("cuda")
        print(f"✓ Model on GPU")
        
        # Check memory usage
        allocated = torch.cuda.memory_allocated(0) / 1e9
        reserved = torch.cuda.memory_reserved(0) / 1e9
        print(f"✓ GPU Memory: Allocated={allocated:.2f}GB, Reserved={reserved:.2f}GB")
    
    print()
    print("="*60)
    print("SUCCESS! TinyLlama is ready to use!")
    print("="*60)
    print()
    print("You can now run: RUN_LLAMA_EXPERIMENTS.bat")
    
except Exception as e:
    print(f"✗ Model loading failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
