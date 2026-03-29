@echo off
echo ============================================
echo TRAIN PENDING EXPERIMENTS - BATCH RUNNER
echo ============================================
echo.
echo This will train all 6 pending experiments
echo one by one.
echo.
echo Experiments to train:
echo 1. BillSum E25 (GPT-2 LoRA)
echo 2. BillSum E27 (GPT-2 Adapters)
echo 3. XSum E26 (GPT-2 QLoRA)
echo 4. BillSum E2 (BART QLoRA)
echo 5. BillSum E14 (T5 QLoRA)
echo 6. BillSum E26 (GPT-2 QLoRA)
echo.
echo Total estimated time: 12-18 hours
echo.
pause

call .venv\Scripts\activate.bat

echo.
echo ============================================
echo EXPERIMENT 1: BillSum E25 (GPT-2 LoRA)
echo ============================================
python train_billsum_e25.py
if errorlevel 1 (
    echo ❌ E25 FAILED
) else (
    echo ✅ E25 COMPLETED
)
echo.
pause

echo.
echo ============================================
echo EXPERIMENT 2: BillSum E27 (GPT-2 Adapters)
echo ============================================
python train_billsum_e27.py
if errorlevel 1 (
    echo ❌ E27 FAILED
) else (
    echo ✅ E27 COMPLETED
)
echo.
pause

echo.
echo ============================================
echo EXPERIMENT 3: XSum E26 (GPT-2 QLoRA)
echo ============================================
python train_xsum_e26.py
if errorlevel 1 (
    echo ❌ E26 FAILED
) else (
    echo ✅ E26 COMPLETED
)
echo.
pause

echo.
echo ============================================
echo EXPERIMENT 4: BillSum E2 (BART QLoRA)
echo ============================================
python train_billsum_e2.py
if errorlevel 1 (
    echo ❌ E2 FAILED
) else (
    echo ✅ E2 COMPLETED
)
echo.
pause

echo.
echo ============================================
echo EXPERIMENT 5: BillSum E14 (T5 QLoRA)
echo ============================================
python train_billsum_e14.py
if errorlevel 1 (
    echo ❌ E14 FAILED
) else (
    echo ✅ E14 COMPLETED
)
echo.
pause

echo.
echo ============================================
echo EXPERIMENT 6: BillSum E26 (GPT-2 QLoRA)
echo ============================================
python train_billsum_e26.py
if errorlevel 1 (
    echo ❌ E26 FAILED
) else (
    echo ✅ E26 COMPLETED
)
echo.

echo.
echo ============================================
echo ALL EXPERIMENTS COMPLETED
echo ============================================
echo Check the checkpoints folder for results
echo.
pause
