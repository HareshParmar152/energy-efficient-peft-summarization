#!/usr/bin/env python3
"""
Test script syntax for all training scripts
"""

import ast
import sys

scripts = [
    'train_billsum_e25.py',
    'train_billsum_e27.py', 
    'train_xsum_e26.py',
    'train_billsum_e2.py',
    'train_billsum_e14.py',
    'train_billsum_e26.py'
]

print("Testing script syntax...")
print("="*50)

for script in scripts:
    try:
        with open(script, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to check syntax
        ast.parse(content)
        print(f"✅ {script} - Syntax OK")
        
    except SyntaxError as e:
        print(f"❌ {script} - Syntax Error: {e}")
    except FileNotFoundError:
        print(f"❌ {script} - File not found")
    except Exception as e:
        print(f"⚠️  {script} - Other error: {e}")

print("="*50)
print("Syntax check complete!")