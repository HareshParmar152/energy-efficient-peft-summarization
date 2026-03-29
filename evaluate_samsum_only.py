#!/usr/bin/env python3
"""
Evaluate SAMSum only - for testing
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
import torch
import gc
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel
from evaluate import load as load_metric
from tqdm import tqdm

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Test with SAMSum E1 only
BASE_PATH = Path("E:/Pending Experiment data")
checkpoint_base = BASE_PATH / "SAMSum_Experiments" / "BART" / "checkpoints" / "E1_BART_SAMSum_LoRA"
checkpoint_path = checkpoint_base / "final_model"

logger.info("="*80)
logger.info("TEST: SAMSum E1 (BART LoRA)")
logger.info("="*80)

# Check checkpoint
if not checkpoint_path.exists():
    if (checkpoint_base / "adapter_config.json").exists():
        checkpoint_path = checkpoint_base
        logger.info(f"Using checkpoint from base folder: {checkpoint_path}")
    else:
        logger.error(f"Checkpoint not found")
        exit(1)

# Load dataset
logger.info("Loading SAMSum test dataset...")
from datasets import load_from_disk
dataset = load_from_disk("E:/Pending Experiment data/local_datasets/samsum")["test"]
logger.info(f"Loaded {len(dataset)} samples")

# Use only 10 samples for quick test
test_samples = dataset.select(range(10))
logger.info(f"Testing with {len(test_samples)} samples")

# Load model
logger.info("Loading model...")
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")
base_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base", torch_dtype=torch.float16)
model = PeftModel.from_pretrained(base_model, str(checkpoint_path))
model = model.merge_and_unload()

if torch.cuda.is_available():
    model = model.to("cuda")
    logger.info("Using GPU")
else:
    logger.info("Using CPU")

model.eval()

# Generate summaries
logger.info("Generating summaries...")
generated_summaries = []

for sample in tqdm(test_samples):
    text = sample["dialogue"]
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    
    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=128, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        generated_summaries.append(summary)
        print(f"Generated: {summary[:100]}...")

# Get references
reference_summaries = test_samples["summary"]

# Calculate ROUGE
logger.info("Calculating ROUGE scores...")
rouge = load_metric("rouge")
results = rouge.compute(predictions=generated_summaries, references=reference_summaries)

logger.info("="*80)
logger.info("RESULTS")
logger.info("="*80)
logger.info(f"ROUGE-1: {results['rouge1']:.4f}")
logger.info(f"ROUGE-2: {results['rouge2']:.4f}")
logger.info(f"ROUGE-L: {results['rougeL']:.4f}")
logger.info(f"ROUGE-Lsum: {results['rougeLsum']:.4f}")
logger.info("="*80)
logger.info("TEST SUCCESSFUL!")
logger.info("="*80)
